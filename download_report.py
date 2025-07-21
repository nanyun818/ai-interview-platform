import requests

try:
    response = requests.get('http://127.0.0.1:5001/download_report', stream=True)
    if response.status_code == 200:
        with open('downloaded_report.pdf', 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print('Report downloaded successfully as downloaded_report.pdf')
    else:
        print(f'Error: {response.status_code} - {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')