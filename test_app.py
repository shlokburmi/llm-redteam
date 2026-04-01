import requests
try:
    r = requests.post("http://localhost:5000/chat", json={"prompt": "hello"})
    print(r.status_code)
    try:
        print(r.json())
    except:
        print(r.text)
except Exception as e:
    print("Connection failed:", e)
