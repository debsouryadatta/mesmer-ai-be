import requests

url = "http://localhost:8000/get_response"

with requests.post(url,
                   json={
                          "user_id": 1,
                          "user_input": "Tell me a story"
                   }
                   , stream=True) as r:
    for chunk in r.iter_content(1024):  # or, for line in r.iter_lines():
        print(chunk)