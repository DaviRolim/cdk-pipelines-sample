import json

def handler(event, context):
    user = dict(
            id='1',
            firstName='Davi',
            lastName='Holanda',
            email='davirolim94@gmail.com'
        )
    users = [user]
    headers = {
      'Access-Control-Allow-Origin': '*', # Required for CORS support to work
      'Access-Control-Allow-Credentials': True, # Required for cookies, authorization headers with HTTPS
    }
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(users)
    }
