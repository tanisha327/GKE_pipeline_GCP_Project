from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def RDS_tbl():
    try:
        # Below code from line 9-21 has been referred from the source: "https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html" and has been modified with aws credential values.
        RDS_hst = 'a3-database-1-instance-1.cmd5ij9yw5sk.us-east-1.rds.amazonaws.com'
        prt = 3306
        usr_nm = 'admin'
        psswrd = 'admin123'
        dtbse = 'a3_database'

        MySQL_cnncton = mysql.connector.connect(
            host=RDS_hst,
            port=prt,
            user=usr_nm,
            password=psswrd,
            database=dtbse
        )
        #Below code from lines 23 to 29 has been referred from the source https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html and has been modified for running the query.
        MySQL_crsr = MySQL_cnncton.cursor()

        MySQL_crsr.execute("CREATE TABLE IF NOT EXISTS products (name VARCHAR(256), price VARCHAR(256), availability BOOLEAN);")

        MySQL_cnncton.close()

        return True
    except Exception as e:
        print(str(e))
        return False


def sngl_values(sngl_vl):
    sngl_vl_nm = sngl_vl.get('name', '')
    sngl_prc = sngl_vl.get('price', '')
    sngl_ava = sngl_vl.get('availability', False)
    return sngl_ava, sngl_prc, sngl_vl_nm


def sngl_prod_val(sngl_vl):
    sngl_prd = {
        'name': sngl_vl[0],
        'price': sngl_vl[1],
        'availability': sngl_vl[2]
    }
    return sngl_prd

@app.route('/store-products', methods=['POST'])
def store_products():
    try:
        JSN_bdy = request.get_json()
        JSON_prdct = JSN_bdy.get('products', [])

        RDS_tbl()

        # Below code from line 60-73 has been referred from the source: "https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html" and has been modified with aws values.

        RDS_hst = 'a3-database-1-instance-1.cmd5ij9yw5sk.us-east-1.rds.amazonaws.com'
        prt = 3306
        usr_nm = 'admin'
        psswrd = 'admin123'
        dtbse = 'a3_database'


        MySQL_cnncton = mysql.connector.connect(
            host=RDS_hst,
            port=prt,
            user=usr_nm,
            password=psswrd,
            database=dtbse
        )
        #Below code from lines 75 to 88 has been referred from the source https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html and has been modified for running the query and extracting values.
        MySQL_crsr = MySQL_cnncton.cursor()

        for sngl_vl in JSON_prdct:

            sngl_ava, sngl_prc, sngl_vl_nm = sngl_values(sngl_vl)

            MySQL_crsr.execute("INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)", (sngl_vl_nm, sngl_prc, sngl_ava))

        MySQL_cnncton.commit()
        MySQL_cnncton.close()
        mssg = 'Success.'
        return jsonify({'message': mssg }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list-products', methods=['GET'])
def list_products():
    try:
        RDS_tbl()

        # Below code from line 96-108 has been referred from the source: "https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html" and has been modified with aws credential values.
        RDS_hst = 'a3-database-1-instance-1.cmd5ij9yw5sk.us-east-1.rds.amazonaws.com'
        prt = 3306
        usr_nm = 'admin'
        psswrd = 'admin123'
        dtbse = 'a3_database'

        MySQL_cnncton = mysql.connector.connect(
            host=RDS_hst,
            port=prt,
            user=usr_nm,
            password=psswrd,
            database= dtbse
        )
        #Below code from lines 110 to 122 has been referred from the source https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html and has been modified for running the query and appending values.
        MySQL_crsr = MySQL_cnncton.cursor()

        MySQL_crsr.execute("SELECT * FROM products;")

        MySQL_rws = MySQL_crsr.fetchall()

        dict_prdct = []
        for sngl_vl in MySQL_rws:
            append_prd = sngl_prod_val(sngl_vl)
            dict_prdct.append(append_prd)

        MySQL_cnncton.close()
        return jsonify({'products':dict_prdct}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
