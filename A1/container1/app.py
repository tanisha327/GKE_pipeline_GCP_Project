from flask import Flask, request,jsonify
import os,requests

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])



def calculate():

    if not (request.is_json):
        return jsonify({'error': 'Invalid JSON input.'}), 200

    input_JSON_data = request.get_json()
    request_input_filename = input_JSON_data['file']

    if not  request_input_filename or 'file' not in input_JSON_data :
        data_return = {
        'file': None, 
        'error': 'Invalid JSON input.'
        }
        return jsonify(data_return), 200


    mounted_volume_path = '/app/data/' + request_input_filename

    if not os.path.exists(mounted_volume_path):
        return jsonify({'file': request_input_filename, 'error': 'File not found.'}), 404

    product_ToBe_Search = input_JSON_data.get('product')
    
    request_send_Cont2 = make_request_to_container2(request_input_filename,product_ToBe_Search)    

    return jsonify(request_send_Cont2.json()), request_send_Cont2.status_code

def make_request_to_container2(filename,productName):
    
    docker_container2_data = {
        'file': filename,
        'product_ToBe_Search': productName
    }
    docker_container2_url = 'http://container2:7000/SummationProcess'
    response_from_container2 = requests.post(docker_container2_url, json=docker_container2_data)
    return response_from_container2



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 6000)))