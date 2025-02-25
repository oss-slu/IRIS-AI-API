import requests 

url="127.0.0.1:5000/search"
files={"image": open(r"C:\Users\Julian\Downloads\lucy.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())