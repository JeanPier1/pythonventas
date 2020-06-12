import json
from flask import Flask,jsonify,request;
from flask import json
import sys
import requests
from flask_restful import Resource,Api;
import mysql.connector
import time

app = Flask(__name__)

api = Api(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route('/nu/<dni>', methods=['GET'])
def listarPerson(dni):

    conexion={
        'host'     : 'localhost',
        'user'     : 'root',
        'password' : '',
        'database' : 'ventasbd'
    }
    conexion=mysql.connector.connect(**conexion)
    cursor=conexion.cursor()
    cursor.execute("select * from persona where dni= %s"%dni)
    data=cursor.fetchall()
    print(data)
    return jsonify(data[0]),200

@app.route('/pro/<codigo>', methods=['GET'])
def listarProduc(codigo):

    conexion={
        'host'     : 'localhost',
        'user'     : 'root',
        'password' : '',
        'database' : 'ventasbd'
    }
    conexion=mysql.connector.connect(**conexion)
    cursor=conexion.cursor()
    cursor.execute("select * from producto where codigo= %s"%codigo)
    data=cursor.fetchall()
    print(data)
    return jsonify(data[0]),200


class listarProductos(Resource):
    def get(self):
        print(sys.version)
        conexion={
            'host'     : 'localhost',
            'user'     : 'root',
            'password' : '',
            'database' : 'ventasbd'
        }
        conexion=mysql.connector.connect(**conexion)
        cursor=conexion.cursor()
        cursor.execute("select * from producto")
        data=cursor.fetchall()

        return {'data':data},200

class listarClientes(Resource):
    def get(self):
        conexion={
            'host'     : 'localhost',
            'user'     : 'root',
            'password' : '',
            'database' : 'ventasbd'
        }
        conexion=mysql.connector.connect(**conexion)
        cursor=conexion.cursor()
        cursor.execute("select * from persona")
        data=cursor.fetchall()

        response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
        )
        return response
@app.route('/venta/', methods=['POST'])
def GuardarVentas():
    fecha=time.strftime("2019-%m-%d")
    some_json=request.get_json()
    idp=some_json['idpersona']
    idc=some_json['idcliente']
    conexion={
        'host'     : 'localhost',
        'user'     : 'root',
        'password' : '',
        'database' : 'ventasbd'
    }
    conexion=mysql.connector.connect(**conexion)
    cursor=conexion.cursor()
    cursor.execute("insert into ventas (idventas,fecha,idpersona,idcliente) values (null,%s,%s,%s)",(fecha,idp,idc))
    conexion.commit()
    cursor.execute("select idventas from ventas order by idventas desc limit 1")
    data=cursor.fetchall()
    idv=data[0][0]
    return jsonify(idv)

@app.route('/venta/detalle', methods=['POST'])
def GuardarDetalle():
    some_json=request.get_json()
    cant=some_json['cantidad']
    prec=some_json['precio']
    idpro=some_json['idproducto']
    idv=some_json['idventas']
    conexion={
        'host'     : 'localhost',
        'user'     : 'root',
        'password' : '',
        'database' : 'ventasbd'
    }
    conexion=mysql.connector.connect(**conexion)
    cursor=conexion.cursor()
    cursor.execute("insert into detalle_venta(iddetalle_venta,idventas,idproducto,precio,cantidad) values (null,%s,%s,%s,%s)",(idv,idpro,prec,cant))
    conexion.commit()

    return "Creado detalle"

api.add_resource(listarProductos,'/producto/listar')
api.add_resource(listarClientes,'/persona/listar')


if __name__ == '__main__':
    app.run(debug=True)