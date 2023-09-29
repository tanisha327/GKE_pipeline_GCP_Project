import json
import hashlib
import requests

def lambda_handler(event, context):
    
    #Below code from line 8 - 11 has been referred from https://docs.python.org/3/library/hashlib.html and has been modified to encode the string.
    passed_value = event['input']
    utf_value = passed_value.encode('utf-8')
    output_string = hashlib.sha256(utf_value)
    output_string = output_string.hexdigest()
    send_back_headers, send_back_json, send_back_url = send_back_defination(output_string, passed_value)
    print(send_back_headers)

    try:
        # Below code in line 17 has been referred from https://docs.python.org/3/library/json.html.
        send_back = requests.post(send_back_url, data=send_back_json, headers=send_back_headers)
    except Exception as e:
        print("Error:", str(e))

    return {
        'statusCode': 200,
        'body': send_back_json
    }
def send_back_defination(output_string, passed_value):
    send_back = {
        "banner": "B00946400",
        "result": output_string,
        "arn": "arn:aws:lambda:us-east-1:541064286200:function:SHA_256_hashing",
        "action": "sha256",
        "value": passed_value
    }
    # Below code from line 34 - 36 has been referred from https://docs.python.org/3/library/json.html.
    send_back_json = json.dumps(send_back)
    send_back_url = "https://v7qaxwoyrb.execute-api.us-east-1.amazonaws.com/default/end"
    send_back_headers = {'Content-Type': 'application/json'}
    return send_back_headers, send_back_json, send_back_url

