import os, csv
from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['directory'] = '/Tanisha_PV_dir/'

@app.route('/SummationProcess', methods=['POST'])
def SummationProcess():
    data = request.get_json()
    productToSearch = data.get('product_ToBe_Search')
    filenameToRead = data.get('file')
    file_path = os.path.join(app.config['directory'], filenameToRead)

    try:
        with open(file_path, 'r') as OpenfileToRead:
            try:
                """   
                The below code lines (line number 22 - 24 has been referred from the source provided and is modified to include multiple characters as headers .
                Source: https://docs.python.org/3/library/csv.html#csv.Sniffer
                """
                InputCSVdialect = csv.Sniffer().sniff(OpenfileToRead.read(4096))
                OpenfileToRead.seek(0)
                if InputCSVdialect.delimiter != ',':
                    error_message = {'file': filenameToRead, 'error': 'Input file not in CSV format.'}
                    error_response = jsonify(error_message)
                    error_response.error_code = 200
                    return error_response

                
                else:
                    send_value=Check_csv_format(filenameToRead,productToSearch,file_path)
                    if send_value is not None:
                        return send_value


                    """   
                    The below code lines (line number 41 - 45) has been referred from the source provided and is modified to calculate total sum  of the product amount in the file.
                    Source: https://realpython.com/lessons/reading-csvs-pythons-csv-module/ 
                    """
                    CSVDataReader = csv.DictReader(OpenfileToRead)
                    summation_amount = 0
                    for eachrowinFile in CSVDataReader:
                        if eachrowinFile['product'] == productToSearch:
                            summation_amount = summation_amount + int(eachrowinFile['amount'])
                    return jsonify({'file': filenameToRead, 'sum': summation_amount}), 200

            except csv.Error as e:
                return jsonify({'file': filenameToRead, 'error': 'Input file not in CSV format.'}), 200

    except FileNotFoundError:
        return jsonify({'file': filenameToRead, 'error': 'File not found.'}), 404

def Check_csv_format(file_name,product_search,path):
    with open(path, 'r') as OpenfileToRead:
        csv_check_read = csv.reader(OpenfileToRead)
        row_one = next(csv_check_read)
        if row_one is None or all(text =='' for text in row_one):
            return jsonify({'file': file_name, 'error': 'Input file not in CSV format.'}), 200

        else:
            for value in row_one:
                if value.isdigit():
                    return jsonify({'file': file_name, 'error': 'Input file not in CSV format.'}), 200


if __name__ == '__main__':
    os.makedirs(app.config['directory'], exist_ok=True)
    app.run(host='0.0.0.0', port=7000)
