import json
import boto3
import os

def get_users():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['DYNAMOTABLE'])

    user = dict(
            id='1',
            firstName='Davi',
            lastName='Holanda',
            email='davirolim94@gmail.com'
    )

    users = [user]
    try:
    # is not a good practice to use scan but is just for testing purposes
        users = table.scan()
    except Exception as e:
        print(e)
    return users


def handler(event, context):
    print(event)
    users = get_users()
    headers = {
      'Access-Control-Allow-Origin': '*', # Required for CORS support to work
      'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
    }
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(users)
    }
