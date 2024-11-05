from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import openai
import boto3
import os
import uuid
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests

# Cargar variables de entorno
load_dotenv()

# BLoque de configuración de la API de OpenAI y S3
openai.api_key = os.getenv("OPENAI_API_KEY")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "generacion-imagenes-ia-dastyb"

# Llamado de cliente de S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name="us-east-2"
)

# Crear la aplicación de FastAPI
app = FastAPI()

# Función encargada de generar una URL firmada (temporal), para el caso actual es de 1 semana
def generate_presigned_url(file_name, expiration=604800):
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"Error al generar la URL firmada: {e}")
        raise HTTPException(status_code=500, detail="Error al generar la URL firmada")

# Función encargada de subir imágenes a S3
def upload_image_to_s3(image_data, file_name):
    print("Iniciando carga de imagen en S3...")
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=image_data,
            ContentType="image/png"
        )
        print("Imagen cargada exitosamente en S3.")
        return generate_presigned_url(file_name)
    except Exception as e:
        print(f"Error al cargar la imagen en S3: {e}")
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {str(e)}")

# Función encargada de crear una variación de la imagen usando OpenAI
def generate_image_variation(image_file):
    response = openai.Image.create_variation(
        image=image_file, 
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# Endpoint para generar o transformar imagen
@app.post("/generate-image/")
async def generate_image(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    if text:
        # Generar imagen con OpenAI desde texto
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # Descargar la imagen generada desde la URL de OpenAI
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            img_byte_arr = image_response.content
            
            # Generar un nombre único para la imagen
            file_name = f"{uuid.uuid4()}.png"
            signed_url = upload_image_to_s3(img_byte_arr, file_name)

            # Retornar la URL firmada de la imagen en S3
            return {"presigned_url": signed_url}
        else:
            raise HTTPException(status_code=500, detail="Error al descargar la imagen generada.")

    elif file:
        # Procesar la imagen subida
        try:
            image = Image.open(file.file)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()

            # Crear una variación de la imagen cargada
            variation_url = generate_image_variation(BytesIO(img_byte_arr))

            # Descargar la imagen de la variación
            variation_response = requests.get(variation_url)
            if variation_response.status_code == 200:
                img_byte_arr = variation_response.content

                # Generar un nombre único para la imagen
                file_name = f"{uuid.uuid4()}.png"
                s3_url = upload_image_to_s3(img_byte_arr, file_name)

                # Generar la URL firmada
                presigned_url = generate_presigned_url(file_name)
                return {"presigned_url": presigned_url}
            else:
                raise HTTPException(status_code=500, detail="Error al descargar la variación de la imagen.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Debes proporcionar un texto o un archivo de imagen.")