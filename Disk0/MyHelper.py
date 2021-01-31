import requests

__api_url = 'http://localhost:8000'

def api_get_task(self, guid) :
    url = F"{self.__api_url}/api/helper/get_task"
    payload={'guid': guid}
    files=[]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None

# app = MyHelper()
# app.api_get_task('9bf156676cec41e38e6e95f987dd50e1')