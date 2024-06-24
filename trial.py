import requests

url = 'http://localhost:5000/api/business'
data = {
    'name': 'Example Pharmaceuticals',
    'address': '123 Main St, Cityville',
    'gst_no': 'GST1234567890',
    'phone_number': '+1234567890',
    'dl_no': 'DL1234567890',
    'email_id': 'info@example.com'
}
files = {
    'file': open('/Users/sakthi/Downloads/a.jpg', 'rb')  # Replace with your actual file path
}

response = requests.post(url, data=data, files=files)
print(response.json())
