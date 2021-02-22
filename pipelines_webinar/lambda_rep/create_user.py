import json
import uuid
import boto3
import os
def create_user(user):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['DYNAMOTABLE'])
    user_id = str(uuid.uuid4())
    response = ''
    try:
        response = table.put_item(
            Item={
                "id": user_id,
                "firstName": user['firstName'],
                "lastName": user['lastName'],
                "email": user['email']
            }
        )
    except Exception as e:
        print(e)
    return response
    
def handler(event, context):
    print(event)
    body = event['body']
    if isinstance(body, str):
        user = json.loads(body['user'])
    else:
        user = body['user']
    print(user)
    res = create_user(user)
    print(res)
    headers = {
      'Access-Control-Allow-Origin': '*', # Required for CORS support to workx
      'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
    }
    return {
        'statusCode': 201,
        'headers': headers,
        'body': 'User added successfully'
    }
