import requests
import os
from pipelines_webinar.lambda_rep import create_user

def test_200_response():
  url = os.environ['SERVICE_URL'] + '/users'
  print(url)
  with requests.get(url) as response:
    print(response)
    assert response.status_code == 200

def test_cretea_user():
  url = os.environ['SERVICE_URL'] + '/users'
  payload = {'{"user":{"firstName":"Davi","lastName":"Holanda","email":"davirolim94@gmail.com"}}'}
  with requests.post(url, payload) as response:
    print(response)
    assert response.status_code == 200
