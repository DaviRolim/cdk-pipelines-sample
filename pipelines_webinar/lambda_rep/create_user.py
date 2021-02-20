import json
import uuid
import boto3
import os
def create_user(user):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['DYNAMOTABLE'])
    user_id = str(uuid.uuid4())

    response = table.put_item(
        Item={
            "id": user_id,
            "firstName": user['firstName'],
            "lastName": user['lastName'],
            "email": user['email']
        }
    )
    return response
    
def handler(event, context):
    print(event)
    user = event['body']
    res = create_user(user)
    print(res)
    headers = {
      'Access-Control-Allow-Origin': '*', # Required for CORS support to work
      'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
    }
    return {
        'statusCode': 201,
        'headers': headers,
        'body': 'User added successfully'
    }
