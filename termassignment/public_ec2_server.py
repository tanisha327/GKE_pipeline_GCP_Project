from flask import Flask, request, jsonify
import paramiko
import os
import requests
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

PRIVATE_EC2_IP = '10.0.130.141'
PRIVATE_EC2_USERNAME = 'ec2-user'
PRIVATE_EC2_KEY_PATH = './tanisha.pem'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/app.js')
def app_js():
    return app.send_static_file('app.js')

def transfer_file_to_private_ec2(hostname, username, key_filename, inputFileName, s3_folder_path):
    try:
        conn = paramiko.SSHClient()

        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        file_transfer = conn.open_sftp()

        file_transfer.put(inputFileName, inputFileName)

        conn.connect(hostname, username=username, pkey=param_key)

        file_transfer.close()

        s3_command = "aws s3 cp {} {}".format(inputFileName, s3_folder_path)

        stdin, stdout, stderr = conn.exec_command(s3_command)
        print(stdout.read().decode())

        conn.close()

    except paramiko.AuthenticationException as e:
        print("Failed to authenticate :", str(e))
    except paramiko.SSHException as e:
        print("Failed SSH:", str(e))
    except Exception as e:
        print("Error:", str(e))


    return 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    s3_folder_path = "s3://client-data-step/upload_file/"
    file.save('/tmp/' + file.filename)
    response = transfer_file_to_private_ec2(PRIVATE_EC2_IP, PRIVATE_EC2_USERNAME, PRIVATE_EC2_KEY_PATH, '/tmp/' + file.filename, s3_folder_path)
    os.remove('/tmp/' + file.filename)

    sleep(40)
    if response == 200:
        return jsonify({'message': 'File uploaded successfully', 'url': 'https://client-data-step.s3.amazonaws.com/final_file/download.csv'}), 200
    else:
        return jsonify({'message': 'Failed to upload the file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)