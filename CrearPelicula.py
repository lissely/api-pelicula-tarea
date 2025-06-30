import json
import boto3
import uuid
import os
import traceback

def lambda_handler(event, context):
    try:
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "event": event
            }
        }))

        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        pelicula = {
            "tenant_id": tenant_id,
            "uuid": str(uuid.uuid4()),
            "pelicula_datos": pelicula_datos
        }

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película guardada exitosamente",
                "pelicula": pelicula,
                "dynamodb_response": response.get("ResponseMetadata", {})
            }
        }))

        return {
            "statusCode": 200,
            "body": json.dumps({
                "pelicula": pelicula
            })
        }

    except Exception as e:
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al procesar la solicitud",
                "error": str(e),
                "stack_trace": traceback.format_exc(),
                "event": event
            }
        }))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "mensaje": "Error interno al procesar la solicitud",
                "error": str(e)
            })
        }