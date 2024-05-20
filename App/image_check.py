# this example uses requests
import requests
import json
import os

API_KEY = os.getenv('API_KEY')
API_USER = os.getenv('API_USER')

def check_image_api(image):
    params = {
      'models': 'genai',
      'api_user': API_USER,
      'api_secret': API_KEY
    }

    print(params)

    files = {'media': image}
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    output = json.loads(r.text)
    print(output)

    if output['status'] == 'success':
        return output['type']
    else:
        return {'ai_generated' : 0}
