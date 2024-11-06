# API para Generación y Modificación de Imágenes usando IA con OpenAI y Almacenamiento en AWS S3
# Desarrollado por: Dayan Styben Auzaque Lancheros

## Descripción General
El desarrollo de esta API se encuentra enfocada en permitir a los usuarios generar imágenes basadas en descripciones textuales o cargar imágenes para aplicarles variaciones usando IA de acuerdo a los requerimientos solicitados. Esta solución presentada utiliza los servicios propios de IA de OpenAI para la generación y transformación de imágenes y seguido a ello almacena los resultados generados por OpenAI de manera segura en AWS S3. 

## Características
- **Generación de imágenes a partir de texto**: Esta funcionalidad crea imágenes usando el motor de OpenAI a partir de un prompt textual suministrado por el usuario.
- **Modificación de imágenes cargadas**: Esta funcionalidad permite subir una imagen por parte del usuario y aplicar una transformación IA para generar una variación de la imagen cargada.
- **Almacenamiento seguro**: Estas imágenes que son generadas se almacenan en un bucket de Amazon S3, donde el acceso a cada una de dichas imagenes será controlado mediante URLs firmadas.

## Requisitos Previos
Para ejecutar esta API que ha sido contruida debe garantizarse que en el entorno local se cuente con:
- **Python 3.8+** instalado.
- **Cuenta de OpenAI** En esta cuenta se debe tener acceso a la API de generación de imágenes en OpenAI y generar una clave para conectar con la misma.
- **Cuenta de AWS** Se debe contar con una cuenta de AWS con permisos de acceso y escritura en S3 para almacenar las imágenes generadas y a su vez habee creado un bucket en especifico para dicho almacenamiento.

## Configuración del Proyecto
1. **Clonar el repositorio**:

   git clone https://github.com/Dastyb/GeneracionImagenesAPI

2. **Cambiar al directorio del proyecto**: 

   cd GeneracionImagenesAPI

4. **Instalar dependencias**: Se debe ejecutar el siguiente comando en la ubicación raíz del proyecto para poder instalar las bibliotecas necesarias, para la correcta funcionalidad de la API:

    pip install -r requirements.txt

5. **Configurar variables de entorno**: Se debe crear un archivo .env en la carpeta raíz del proyecto, donde se deberán agregar las siguientes credenciales:

    - OPENAI_API_KEY=api_key_Obtenida_de_OpenAI,
    - AWS_ACCESS_KEY_ID=acces_key_Obtenida_de_AWS,
    - AWS_SECRET_ACCESS_KEY=secret_key_Obtenida_de_AWS

    - **OPENAI_API_KEY**: Almacena la ApiKey que fue generada desde OpenAI, para acceder al servicio de generación de imagenes.
    - **AWS_ACCESS_KEY_ID** y **AWS_SECRET_ACCESS_KEY**: Son las claves generadas, para poder acceder a AWS S3.
    - **RENOMBRAR BUCKETNAME EN main.py**: Es importante ingresar a main.py y modificar la variable llamada "BUCKET_NAME", donde se debe ingresar el respectivo nombre del bucket que se haya creado de manera independiente en el servicio de S3.
    - **Seleccion de región en S3**: Se debe ingresar a main.py y registrar en la variable denominada "region_name" el nombre de la respectiva región en la cual se encuentra el servicio S3 propio en AWS.

## Ejecución de la API
Una vez configurados los requerimientos mencionados del proyecto, se puede iniciar el servidor FastAPI de manera local, mediante el siguiente comando:

    uvicorn main:app --reload

Esto iniciará el servidor en el localhost: http://127.0.0.1:8000 y a su vez se podrá acceder a la documentación interactiva de Swagger generada autoamticamente en la ruta: http://127.0.0.1:8000/docs.

## Endpoint disponible

    POST /generate-image/

Este endpoint creado permite tanto generar imágenes desde texto como cargar una imagen para aplicar una variación mediante los servicios de IA de OpenAI

1. **Parámetros**: Para poder realizar el llamado a la API mediante servicio POST, es necesario tener en cuenta los siguietnes parametros, los cuales serán independientes, así que por ende unicamente se gestionará un parametro por cada solicitud que se realicé:

    - text (opcional): Una cadena de texto prompt que describra a detalle la solicitud de imagen que se desea crear.
    - file (opcional): Carga de un archivo de imagen (PNG o JPG) al cual se le aplicará una transformación mediante IA, que modificará la imagen original.

2. **Ejemplo de Solicitud**: A continuación se mostrará 2 ejemplos, que demosrtarán las funcionalidades construidas, a su vez servirá como  ejemplo para realizar la solicitud POST directamente desde consola para la verificación de la API:

    * Generación desde texto:

    curl -X POST "http://127.0.0.1:8000/generate-image/" -F "text=un dia soleado en un campo colombiano"

    * Modificación de una imagen cargada:

    curl -X POST "http://127.0.0.1:8000/generate-image/" -F "file=@C:\Imagenes_Prueba\Imagen_Prueba_Carga_Gato_Animado.png"

    La ruta a agregar será la caracteristica donde se encuentre la imagen que se desea modificar.

3. **Respuesta**: Para los ejemplos presentados anteriormente se ha generado las siguientes repuestas que se adjuntarán, dichas imagenes pueden ser consultadas directamente dando click en cada ruta compartida:

    * Respuesta de imagen generada mediante texto:

    https://generacion-imagenes-ia-dastyb.s3.amazonaws.com/f71dc5ae-96d5-4e89-b4d9-3fc417e685dd.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4SZHOBCMX7U72KXE%2F20241105%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20241105T082637Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=91d3c96125bbab4f99948f05edaf7f2d757b820473e695752d4599b98e1dfda2

    * Respuesta de imagen modificada:

    https://generacion-imagenes-ia-dastyb.s3.amazonaws.com/b35ad417-49f5-4111-97d8-5abc16bb32f7.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4SZHOBCMX7U72KXE%2F20241105%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20241105T083332Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=5e856719258068beea7eb542ff2ba05ac5157967557c92b890096d1b19dac77b
    
## Descripción de seguridad
A continuacuón se presentan los conceptos claves que se tuvieron en cuenta en cuenta respecto a seguridad al momento de la creación de la API:

   * **Control de acceso**: Las imagenes que son cargadas en S3, solamente son accesibles al publico atraves de URLs firmadas qeu expiran automaticamente despues de un determinado periodo de tiempo que fe definido (actualmente 1 semana).
   * **Almacenamiento de credenciales**: Las credenciales empleadas (Claves de OpenAI y AWS) son almacenadas en un archivo .env, lo cual grantiza que dichas claves sean privadas para cada usuario.
   * **Manejo de errores**: La API construida cuneta con un manejo de errores comunes, como la carga de imagenes o problemas de conexión con el servicio, retornando mensajes de error descriptivos para el usuario.
## Estructura del código, patrones y modularización
Toda la lógica construida de la API se encuentra en el archivo main.py, donde se incluyen tanto los endpoint contruidos como las funciones auxiliares.
Por ende, para esta API los patrones de diseño empleados son los siguientes:

   - **Factory method**: Ha sido usado para crear variaciones de imagenes con OpenAI, donde se instancia un nuevo proceso para la transformación segun el tipo de solicitud.
   - **Gestión de dependencias**: Utiliza dotenv para cargar las variables de entorno que se encuentran en .env y botos3 como cliente para gestionar la conexión con S3.
   - **Modularización**: La logica que se ha construido en esta API ha sido dividida en funciones claras que permiten facilitar la escalabilidad y el mantenimiento de la misma, dichasa funciones principales pueden observarse a continuación: 
   - **upload_image_to_s3**: Realiza el proceso de carga de la imagen que se ha gestionado en openAI al servicio S3 de AWS y a su vez retorna la URL firmada
   - **generate_presigned_url**: Retorna una URL firmada para el acceso seguro a la respectiva imagen.
   - **generate_image_variation**: Realiza el proceso encargado de realizar las variaciones o modificaciones a las imaganes que son cargadas por el usuario, haciendo uso de OpenAI.
