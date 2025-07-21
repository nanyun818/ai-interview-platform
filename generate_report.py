import requests

try:
    response = requests.post('http://127.0.0.1:5001/generate_report')
    print(f'Status code: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')