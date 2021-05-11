from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response 
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
#from flask_mail import Mail
from cryptography.fernet import Fernet as frt
import json
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from flask_cors import CORS, cross_origin
import os
import uuid
import random
import string
import re

import weexConstants
import correoweex
from werkzeug.security import generate_password_hash, check_password_hash

import schedule
import time
import webscraping
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

## Mail
#mail = Mail(app)

## MySQL Connection
app.config['MYSQL_HOST'] = weexConstants.MYSQL_HOST
app.config['MYSQL_USER'] = weexConstants.MYSQL_USER
app.config['MYSQL_PASSWORD'] = weexConstants.MYSQL_PASSWORD
app.config['MYSQL_DB'] = weexConstants.MYSQL_DB
mysql = MySQL(app)

#settings secret key
app.secret_key = 'my$ecre7key'
app.permanent_session_lifetime = timedelta(minutes=8)

varPath1 = str(app.root_path)
varPath2 = app.instance_path
varPath3 = os.path.dirname(app.instance_path)

## Config values for upload image
# app.config["IMAGE_UPLOADS"] = "D:\\FREDDY\\Escritorio\\Trabajos\\We-Exchange\\flask\\we_ex_app\\static\\img\\uploads"

vardirf1 = str(r"" + varPath1   +  "") 

#os.path.dirname(r"static\img\uploads") 

vardirf2 = os.path.dirname(r"\static\img\uploads")
vardirf3 =  vardirf1 + vardirf2



app.config["IMAGE_UPLOADS"] =  vardirf3 

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 500000 # 500 000 bytes

def allowed_image(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else :
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def ExisteCliente(correo):
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM m_cliente WHERE CORREO_ELECTRONICO = '" + correo + "'")
    data = cur.fetchall()
    cur.close()
    if(len(data) == 1):
        return True
    else:
        return False

def ExisteOrden(codorden):
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM m_orden WHERE CODORDEN = '" + codorden + "'")
    data = cur.fetchall()
    cur.close()
    if(len(data) == 1):
        return True
    else:
        return False

""" @app.route('/prueba') """
def TraerTipoCambioDolarSimulacion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COMPRA, VENTA FROM tasa_cambio WHERE IDMONEDA_1 = 2 ORDER BY FECHAHORAACTUALIZACION DESC LIMIT 1")
    data = cur.fetchall()
    dataTC = data[0]
    cur.close()
    return dataTC

@app.route('/weex/tasa-cambio/v1', methods=['GET'])
def apiTipoCambioMonedas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COMPRA, VENTA FROM tasa_cambio WHERE IDMONEDA_1 = 2 ORDER BY FECHAHORAACTUALIZACION DESC LIMIT 1")
    data = cur.fetchall()
    print(data[0][0])
    print(data[0][1])
    #dataTC = data[0]
    #print("data = " + data[0])
    cur.close()
    result = {
        'ratesBD': {
                'compra': data[0][0],
                'venta': data[0][1]
            }
        }

    ##
    return jsonify(result)

@app.route('/weex/tasa-cambio/v1/<moneda>', methods=['GET'])
@cross_origin()
def apiTipoCambioMonedashome(moneda):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COMPRA, VENTA FROM tasa_cambio WHERE IDMONEDA_1 = 2 ORDER BY FECHAHORAACTUALIZACION DESC LIMIT 1")
    data = cur.fetchall()
    equivalenteUSD = 1 / data[0][0]
    equivalentePEN = data[0][1]
    cur.close()
    
    if (moneda == 'PEN'):
        result = {
            'rates': {
                'USD': equivalenteUSD,
                'PEN': 1
                }
            }

    if (moneda == 'USD'):
        result = {
            'rates': {
                'USD': 1,
                'PEN': equivalentePEN
                }
            }

    return jsonify(result)

@app.route('/weex/actualizar/tasa-cambio/v1', methods=['POST'])
def updateTipoCambioInvesting():
    requestBody = request.get_json(force=True)
    #print(requestBody['compra'])
    # type(requestBody)
    # print(type(requestBody))
    params = {
        "id": requestBody['id'],
        "compra": requestBody['compra'],
        "venta": requestBody['venta']
    }
    #print(params)
    query = "UPDATE tasa_cambio SET COMPRA = {data[compra]}, VENTA = {data[venta]} WHERE ID = {data[id]}"
    query = query.format(data=params)
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    result = {
        'response': {
            'code': '000',
            'message': 'Se actualizó el tipo de cambio correctamente'
        }
    }
    return jsonify(result)

def TraerDataBancoDeDondeEnvias():
    cur = mysql.connection.cursor()
    cur.execute("SELECT IDBANCO, NOMBRE, DESCRIPCION FROM de_banco WHERE NOMBRE IN ('BCP','INTERBANK')")
    data = cur.fetchall()
    dataBanco = data
    cur.close()
    return dataBanco

def TraerDataTipDoc():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID, DESCRIPCION FROM de_tipo_documento")
    data = cur.fetchall()
    dataTipDoc = data
    cur.close()
    return dataTipDoc

def TraerDataBanco():
    cur = mysql.connection.cursor()
    cur.execute("SELECT IDBANCO, NOMBRE, DESCRIPCION FROM de_banco")
    data = cur.fetchall()
    dataBanco = data
    cur.close()
    return dataBanco

def ObtenerIdMoneda(codigoMoneda):
    cur = mysql.connection.cursor()
    cur.execute("SELECT IDMONEDA from de_moneda WHERE CODIGO = '" + codigoMoneda + "'")
    data = cur.fetchall()
    dataIdMoneda = data
    cur.close()
    return dataIdMoneda

def TraerDataCuentas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT IDCUENTA, IDBANCO , NUMERO_CUENTA, NOMBRE_TITULAR, IDMONEDA from m_cuenta WHERE IDCLIENTE = '" + id + "'")
    data = cur.fetchall()
    dataCuentasCliente = data
    cur.close()
    return dataCuentasCliente

def ExisteUsuarioResetPass(id, token):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM m_cliente WHERE ID = '" + id + "' AND TOKEN = '" + token + "'")
    data = cur.fetchall()
    cur.close()
    if(len(data) == 1):
        return True
    else:
        return False

def ResetPasswordUser(id, token, newPassword):
    newPasswordHash = generate_password_hash(newPassword)
    newToken = str(uuid.uuid4())
    cur = mysql.connection.cursor()
    cur.execute("UPDATE m_cliente SET PASSWORD_HASH = '" + newPasswordHash +"' , TOKEN = '" + newToken + "' WHERE ID = '" + id + "' AND TOKEN = '" + token + "'")
    mysql.connection.commit()
    return redirect(url_for('Index'))


def write_fernet_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def EsCorrectoPasswordHash(correo, password):
    cur = mysql.connection.cursor() 
    #cur.execute("SELECT * FROM m_cliente WHERE CORREO_ELECTRONICO = '" + correo + "' AND PASSWORD_HASH = '" + passwordHash + "'" )
    cur.execute("SELECT PASSWORD_HASH FROM m_cliente WHERE CORREO_ELECTRONICO = '" + correo + "' " )
    data = cur.fetchall()
    data2 = data[0]
    passwordHash = data2[0]
    cur.close()
    if check_password_hash(passwordHash, password):
        return True
    else:
        return False

def EsCorrectoPasswordHash2():
    if check_password_hash('pbkdf2:sha256:50000$8p5FhkoZ$6474e973bdd18688237dd5afcd277bfc3cc1bb1b6fe5e42a5a0c09e91f7b8728', 'lolopo'):
        print('Validacion correcta')
    else:
        print('Validacion incorrecta')
    return redirect(url_for('login')) 

@app.route('/restart-password-f/<id>/<token>')
def get_data_user(id,token):
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID, CORREO_ELECTRONICO, TOKEN FROM m_cliente WHERE ID = %s AND TOKEN = %s", [id,token], )   ###The reasoning is that execute's second parameter represents a list of the objects to be converted
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0]) 


@app.route('/mail/<id>/<token>', methods=['GET','POST'])
def MailClass():
    #apikey = "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"
    
    url = "http://localhost:3000/reset-password/"

    """ 
    params = {
        "receiver_email_address": "royerleandroroblesvega@gmail.com",
    }
    correoweex.enviarCorreo(params) 
    """

    message = Mail(
        from_email='alonsog@we-ex.pe',
        to_emails='freddychpo@gmail.com',
        subject='Recuperacion de contraseña',
        html_content='Para crear su nueva contraseña por favor ingresa al siguiente link en el navegador: ')
    try:
        #sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #sg = SendGridAPIClient(os.environ.get(apikey))
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print("try")
    except Exception as e:
        print(e)
        print(e.body)
        print("exception")
    return "envio de mail"

@app.route('/home')
def Home():
    #print(str(uuid.uuid4()))
    dataTipoCambio = TraerTipoCambioDolarSimulacion()
    #print(dataTipoCambio)
    return render_template('home.html', dataTC = dataTipoCambio)

@app.route('/inicio')
def Inicio():
    
    session.permanent == True
    idCliente = obtenerIdClienteUsuLogueado(session['user'])
    session['idCli']=idCliente
    
    return render_template('inicio.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/cuenta')
def Cuenta():

    key = open("key.key", "rb").read()
    f = Fernet(key)
    idCLiente= session['idCli']
    print(idCLiente)
    dataCuentasUsuario = TraerDataCuentas(str(idCLiente))
    listCuentasUsuario = list(dataCuentasUsuario)

    print(dataCuentasUsuario)
    print(listCuentasUsuario)

    numeroRegistros = len(listCuentasUsuario)

    items = []
    for i in range(0, numeroRegistros):
        #i = str(i)
        tupleAux = tuple(listCuentasUsuario[i])
        # dict == {}
        # you just don't have to quote the keys
        #an_item = dict(banco=tupleAux[0], cuenta=tupleAux[1], titular=tupleAux[2], moneda=tupleAux[3])
        an_item = dict(banco= tupleAux[1], cuenta= f.decrypt(tupleAux[2]).decode('utf-8') , titular=f.decrypt(tupleAux[3]).decode('utf-8'), moneda=tupleAux[4])
        items.append(an_item)
   
    
    session["items"] = items

    print(items)


    return render_template('cuenta.html')


@app.route('/datos-personales')
def DatosPersonales():
    return render_template('datos-personales.html')

def listarOrdenesByIdCliente(idCliente):
    id= str(idCliente)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM m_orden WHERE IDCLIENTE = '" +id  + "'")
															
    data = cur.fetchall()
    cur.close()
    return data

def obtenerNombreUserLogueado(correo):
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT NOMBRE FROM m_cliente WHERE CORREO_ELECTRONICO = '" + correo + "'")
    data = cur.fetchall()
    nombreUsuarioLogueado = data
    print("Obteniendo Id de cliente logueado")
    prin(nombreUsuarioLogueado)
    cur.close()
    return nombreUsuarioLogueado

def obtenerIdClienteUsuLogueado(correo):
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT ID FROM m_cliente WHERE CORREO_ELECTRONICO = '" + correo + "'")
    data = cur.fetchmany(1)
    idCliente = data[0][0]
    print("Obteniendo Id de cliente logueado")
    print (idCliente)
    cur.close()
    return idCliente
@app.route('/ordenes')
def Ordenes():
    session.permanent == True
    print("Listar orden")
    print(session['user'])		   
    listOrdenes = listarOrdenesByIdCliente(session['idCli'])
    return render_template('ordenes.html', data = listOrdenes)

@app.route('/')
def Redirect():
    dataTipoCambio = TraerTipoCambioDolarSimulacion()
    #print(dataTipoCambio)
    print(vardirf3)
    print(app.config["SERVER_NAME"])
    return render_template('home.html', dataTC = dataTipoCambio)

@app.route('/register')
def Index(): ## funcion para manejar la peticion
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM de_tipo_documento')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM de_tipo_persona')
    data2 = cur2.fetchall()
    #filas  = cur2.rowcount
    cur.close()
    cur2.close()
    return render_template('add-client.html', tipo_documentos = data, tipo_persona = data2) #flask ya tiene configurado el nombre de la carpeta templates

    #return render_template('index.html', contacts = data) #flask ya tiene configurado el nombre de la carpeta templates
    #return 'Hello World'


@app.route('/add_test_2', methods=['GET','POST'])
def add_test_2():
    cur = mysql.connection.cursor() 
    cur.execute('SELECT NOMBRE_TITULAR, NUMERO_CUENTA, NUMDOC FROM m_cuenta_prueba')
    data = cur.fetchall()

    key = open("key.key", "rb").read()
    f = Fernet(key)

    for x in data:
        for y in x:
            decrypted_encrypted = f.decrypt(y)
            decrypted_encrypted_decoded = decrypted_encrypted.decode('utf-8') 
            print(decrypted_encrypted_decoded)

    return redirect(url_for('Index'))



@app.route('/test_01', methods=['GET', 'POST'])
def test_01():
    
    #key=frt.generate_key()
    key = open("key.key", "rb").read()

    cur = mysql.connection.cursor() 
    cur.execute('SELECT NOMBRE_TITULAR, NUMERO_CUENTA, NUMDOC FROM m_cuenta_prueba')
    data = cur.fetchall()


    for x in data:
        #s = "message"
        #s = data[x]
        """ s = x
        print('input string: {0}'.format(s))
        #key=base64.b64encode(key) #no need to do this
        print('key: {0}, type: {1}'.format(key, type(key)))
        f=frt(key)
        token = f.encrypt(s.encode('utf-8')) #need to convert the string to bytes
        print ('encrypted: {0}'.format(token))
        output = f.decrypt(token)
        output_decoded = output.decode('utf-8')
        print ('decrypted: {0}'.format(output_decoded)) """
        print(x)

    for x in data:
        for y in x:
            print(y)   
            """ s = y
            print('input string: {0}'.format(s))
            #key=base64.b64encode(key) #no need to do this
            print('key: {0}, type: {1}'.format(key, type(key)))
            f=frt(key)
            token = f.encrypt(s.encode('utf-8')) #need to convert the string to bytes
            print ('encrypted: {0}'.format(token)) """
            f=frt(key)
            token = y
            output = f.decrypt(token)
            output_decoded = output.decode('utf-8')
            print ('decrypted: {0}'.format(output_decoded))


    thistuple = ("apple", "banana", "cherry")
    for x in thistuple:
        print(x)        

    return redirect(url_for('Index'))

@app.route('/add_test', methods=['GET','POST'])
def add_test():
    if request.method == 'GET':
        return render_template('pruebaEncriptar.html')
    if request.method == 'POST':
        NumeroCuenta = request.form['NumeroCuenta']
        NombreTitular = request.form['NombreTitular']
        NumeroDocumento = request.form['NumeroDocumento']
        

        key = open("key.key", "rb").read()
        """ key = load_key() """

        print(NumeroCuenta)
        print(NombreTitular)
        print(NumeroDocumento)

        """    
        NumeroCuentaEncoded = NumeroCuenta.encode('utf-8')
        NombreTitularEncoded = NombreTitular.encode('utf-8')
        NumeroDocumentoEncoded = NumeroDocumento.encode('utf-8')
        """
        f = Fernet(key)

        """  
        NumeroCuentaEncrypted = f.encrypt(NumeroCuentaEncoded)
        NombreTitularEncrypted = f.encrypt(NombreTitularEncoded)
        NumeroDocumentoEncrypted = f.encrypt(NumeroDocumentoEncoded) 
        """

        NumeroCuentaEncrypted = f.encrypt(NumeroCuenta.encode('utf-8'))
        NombreTitularEncrypted = f.encrypt(NombreTitular.encode('utf-8'))
        NumeroDocumentoEncrypted = f.encrypt(NumeroDocumento.encode('utf-8'))

        print(NumeroCuentaEncrypted)
        print(NombreTitularEncrypted)
        print(NumeroDocumentoEncrypted)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO m_cuenta_prueba
            VALUES('', %s, %s, %s)
            """, 
        (NombreTitularEncrypted, NumeroCuentaEncrypted, NumeroDocumentoEncrypted))
        mysql.connection.commit()    
        return redirect(url_for('Index'))




@app.route('/add_client', methods=['GET','POST'])
def add_client():
    print('print inicio add cliente')
    if request.method == 'POST':
        ## Validación de la carga de imagenes ############################
        ## Validación de la foto del cliente ############################
        """
        if request.files:   
            if not allowed_image_filesize(request.cookies.get("filesizeFoto")) or not allowed_image_filesize(request.cookies.get("filesizeFotoDoc")):
                print('El archivo excedio el tamano maximo')
                return redirect(url_for('Index'))
                #return redirect(request.url)

            #print(request.cookies)
            imagenFoto = request.files["imagenFoto"] ## name property
            imagenFotoDocFrontal = request.file["imagenFotoDocFrontal"]
            imagenFotoDocPosterior = request.file["imagenFotoDocPosterior"]

            if imagenFoto.filename == "" or imagenFotoDocFrontal == "" or imagenFotoDocPosterior == "":
                print('Foto de usuario debe tener un nombre')
                return redirect(url_for('Index'))
                #return redirect(request.url)

            if not allowed_image(imagenFoto.filename) or not allowed_image(imagenFotoDocFrontal.filename) or not allowed_image(imagenFotoDocPosterior.filename):
                print('La extensión de la foto del cliente no esta permitida')
                return redirect(url_for('Index'))
                #return redirect(request.url)

            else:
                filenameFoto = secure_filename(imagenFoto.filename)
                filenameFotoDocFrontal = secure_filename(imagenFotoDocFrontal.filename)
                filenameFotoDocPosterior = secure_filename(imagenFotoDocPosterior.filename)

            
            imagenFoto.save(os.path.join(app.config["IMAGE_UPLOADS"], filenameFoto))
            imagenFotoDocFrontal.save(os.path.join(app.config["IMAGE_UPLOADS"], filenameFotoDocFrontal))
            imagenFotoDocPosterior.save(os.path.join(app.config["IMAGE_UPLOADS"], filenameFotoDocPosterior))
        """
        
    #################################################################################################

        filenameFoto = ''
        filenameFotoDoc = ''
        filenameFotoDocPosterior = ''

        nombre = request.form['Nombre']
        apellidoPaterno = request.form['ApellidoPaterno']
        apellidoMaterno = request.form['ApellidoMaterno']
        correoElectronico = request.form['CorreoElectronico']
        celular = request.form['Celular']
        password = request.form['Password']
        token = str(uuid.uuid4())
        tipoDocumento = request.form.get('TipoDocumento', None)
        numeroDocumento = request.form['NumeroDocumento']
        fechaEmisionDocumento = request.form['FechaEmisionDocumento']
        personaPolitica = request.form.get('PersonaPolitica', None)
        tipoPersona = request.form.get('TipoPersona', None)
        ocupacion = request.form['Ocupacion']
        #fotoCliente = request.form['FotoCliente']
        fotoCliente = '' #app.config["IMAGE_UPLOADS"] + "\\" + filenameFoto
        fotoDocumento = '' #app.config["IMAGE_UPLOADS"] + "\\" + filenameFotoDoc
        fotoDocumentoB = '' #app.config["IMAGE_UPLOADS"] + "\\" + filenameFotoDocPosterior
        #fotoDocumento = request.form['FotoDocumento']

        now = datetime.now()

        cur = mysql.connection.cursor()
        
        cur.execute("""
            INSERT INTO m_cliente
            VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
        (nombre, apellidoPaterno, apellidoMaterno, correoElectronico,celular, generate_password_hash(password), 
        token, tipoDocumento, numeroDocumento, fechaEmisionDocumento, personaPolitica, tipoPersona, ocupacion,
        fotoCliente, fotoDocumento, fotoDocumentoB, now))#uso de tupla
        mysql.connection.commit()    

        flash('Usuario registrado correctamente')
        return redirect(url_for('Index'))
        #return 'received'
""" 
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CONTACTS WHERE ID = %s", [id])   ###The reasoning is that execute's second parameter represents a list of the objects to be converted
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])   
 """

"""  @app.route("/user")
 def user():
    if "user" in session:
         user = session["user"]
         return f"<h1>{user}</h1>"
    else: """

@app.route("/operacion-cambio-post" , methods=['GET','POST'])
def operacionCambioPost():
    if request.method == 'POST':
        """ dataTipoCambio = TraerTipoCambioDolarSimulacion()
        session["dataTC"] = dataTipoCambio    """

        montoEnviar = request.form['montoEnviar']
        session["montoEnviar"] = montoEnviar    

        montoRecibir = request.form['montoRecibir']
        session["montoRecibir"] = montoRecibir

        monedaCambio = request.form['monedaCambio']
        session["monedaCambio"] = monedaCambio

        tipoCambio = session["dataTC"]

        if (monedaCambio == "Moneda: Dólares a Soles"):
            session["tipoCambio"] = tipoCambio[0];

        if (monedaCambio == "Moneda: Soles a Dólares"):
            session["tipoCambio"] = tipoCambio[1];

        return redirect(url_for('operacionCambioCuentas')) 



@app.route("/operacion-cambio" , methods=['GET','POST'])
def operacionCambio():
    dataTipoCambio = TraerTipoCambioDolarSimulacion()
    session["dataTC"] = dataTipoCambio   

    if request.method == 'POST':   
        """ dataTipoCambio = TraerTipoCambioDolarSimulacion()
        session["dataTC"] = dataTipoCambio    """

        print("POST")
        """ return redirect(url_for('operacionCambioCuentas', dataTC = dataTipoCambio  )) """
        return redirect(url_for('operacionCambioCuentas')) 
    else:
        print("GET")
        return render_template("operacion-cambio.html", dataTC = dataTipoCambio,  )


@app.route("/operacion/validar/<codinterno>", methods=['GET','POST'])
def operacionValidarOrden(codinterno):
    return render_template("orden.html")

@app.route("/procesar-orden", methods=['GET','POST'])
def operacionProcesarOrden():
    if request.method == 'POST' and request.form['procesar_orden'] == 'Procesar':
        montoEnviar = session["montoEnviar"]
        montoRecibir = session["montoRecibir"]
        monedaCambio = session["monedaCambio"]
        tipoCambio = session["dataTC"]
    
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print(key, " : ", value)

        cad=""

        for item,value in request.form.items():
            cad+="{}:{}<br/>".format(item,value)

        return cad

        #return montoEnviar + ' ' + montoRecibir + ' ' +  monedaCambio + ' ' + str(tipoCambio) + ' ' + str(request.form)
    else:
        return "no entro al post"





@app.route("/operacion-cambio/cuentas", methods=['GET','POST'])
def operacionCambioCuentas():
    session.permanent == True
    idCliente = session['idCli']

    if request.method == 'POST':
        if "GuardarCuenta" in request.form:
            key = open("key.key", "rb").read()
            f = Fernet(key)

            Banco = request.form['Banco']
            NumeroCuenta = request.form['NumeroCuenta']
            NombreTitular = request.form['NombreTitular']
            tipoDocumento = request.form.get('TipoDocumento', None)
            NumeroDocumento = request.form['NumeroDocumento']

            NumeroCuentaEncrypted = f.encrypt(NumeroCuenta.encode('utf-8'))
            NombreTitularEncrypted = f.encrypt(NombreTitular.encode('utf-8'))
            NumeroDocumentoEncrypted = f.encrypt(NumeroDocumento.encode('utf-8'))

            print(tipoDocumento)
            print(NumeroDocumento)

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO m_cuenta
                VALUES('', %s, %s, %s, %s, %s, %s, %s, %s)
                """, 
            ( idCliente, Banco, '0', '1', NumeroCuentaEncrypted, NombreTitularEncrypted, tipoDocumento, NumeroDocumentoEncrypted )) 
            mysql.connection.commit()     

            return redirect(url_for('operacionCambioCuentas'))
            
        if "ProcesarOrden" in request.form:
            print("Procesar Orden")
            codinterno = random.randint(10000, 99999)
            session["codinterno"] = codinterno

            montoEnviar = session["montoEnviar"]
            montoRecibir = session["montoRecibir"]
            monedaCambio = session["monedaCambio"]
            tipoCambio = session["dataTC"]
            print("Tipo de Cambio = " , monedaCambio)
            if(monedaCambio == "Moneda: Dólares a Soles"):
                    monedaEnvio = ObtenerIdMoneda('USD')[0][0]
                    monedaRecibo = ObtenerIdMoneda('PEN')[0][0]
                    mtoTipoCambio = tipoCambio[0]
                    session["strMonedaEnvio"] = 'Dólares' 
                    session["strMonedaRecibo"] = 'Soles'
            elif(monedaCambio == "Moneda: Soles a Dólares"):
                    monedaEnvio = ObtenerIdMoneda('PEN')[0][0]
                    monedaRecibo = ObtenerIdMoneda('USD')[0][0]
                    mtoTipoCambio = tipoCambio[1]
                    session["strMonedaEnvio"] = 'Soles' 
                    session["strMonedaRecibo"] = 'Dólares'

            BancoEnvio = request.form.get('BancoEnvio', None)
            CuentaRecibo = request.form.get('CuentaRecibo', None)

            stringLength = 7
            lettersAndDigits  = string.ascii_uppercase + string.digits
            nro_orden = ''.join(random.sample(lettersAndDigits, stringLength))

            while ExisteOrden(nro_orden) == True:
                stringLength = 7
                lettersAndDigits  = string.ascii_uppercase + string.digits
                nro_orden = ''.join(random.sample(lettersAndDigits, stringLength))

                if ExisteOrden(nro_orden) == False:
                    break

            session["nro_orden"] = nro_orden

            now = datetime.now()
            session["strHoraraInicio"] = str(now)
            print("antes de insertar orden")
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO m_orden
                VALUES(0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, 
            ( codinterno, nro_orden, idCliente, now, montoEnviar, monedaEnvio, BancoEnvio, montoRecibir, monedaRecibo, CuentaRecibo, mtoTipoCambio, '1' )) 
            mysql.connection.commit()   
             

            return redirect(url_for('operacionValidarOrden', codinterno = codinterno))

    elif request.method == 'GET':

        key = open("key.key", "rb").read()
        f = Fernet(key)

        dataBancoDeDondeEnvias = TraerDataBancoDeDondeEnvias()
        session["dataBanco1"] = dataBancoDeDondeEnvias  

        dataBanco = TraerDataBanco()
        session["dataBanco2"] = dataBanco  


        dataTipDoc = TraerDataTipDoc()
        session["dataTipDoc"] = dataTipDoc 

        dataCuentasUsuario = TraerDataCuentas(str(idCliente))
        session["dataCuentasUsuario"] = dataCuentasUsuario

        """     print(len(dataBancoDeDondeEnvias))
        print(dataBancoDeDondeEnvias)

        print(len(dataCuentasUsuario))
        print(dataCuentasUsuario) """

        dataCuentasUsuario = TraerDataCuentas(str(idCliente))
        listCuentasUsuario = list(dataCuentasUsuario)

        """ print(dataCuentasUsuario)
        print(listCuentasUsuario) """

        numeroRegistros = len(listCuentasUsuario)

        items = []
        for i in range(0, numeroRegistros):
            #i = str(i)
            tupleAux = tuple(listCuentasUsuario[i])
            # dict == {}
            # you just don't have to quote the keys
            #an_item = dict(banco=tupleAux[0], cuenta=tupleAux[1], titular=tupleAux[2], moneda=tupleAux[3])
            an_item = dict( id = tupleAux[0] ,banco= tupleAux[1], cuenta= f.decrypt(tupleAux[2]).decode('utf-8') , titular=f.decrypt(tupleAux[3]).decode('utf-8'), moneda=tupleAux[4])
            items.append(an_item)
    
        
        session["items"] = items

        return render_template("cuentas.html")


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")


@app.route('/recover_account', methods=['GET','POST'])
def recoverAccount():
    url = "http://demo.weex.pe/reset_password/"
    if request.method == 'POST':
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID, CORREO_ELECTRONICO, TOKEN FROM m_cliente WHERE CORREO_ELECTRONICO = %s", [correo])   ###The reasoning is that execute's second parameter represents a list of the objects to be converted
        data = cur.fetchall()
        data2 = data[0]
        id = data2[0]
        token = data2[2]

        #print("ingeso aqui")

        html_content='Para crear su nueva contraseña por favor ingresa al siguiente link en el navegador: ' + url + str(id) +'/' + token 

        params = {
            "receiver_email_address": "royerleandroroblesvega@gmail.com",
            "html_content": html_content
        }

        print("params")
        print(params)

        responseCorreo = correoweex.enviarCorreo(params, correo, html_content)
        print("respuesta correo")
        print(responseCorreo['status_code'])

        """ message = Mail(
            from_email='alonsog@we-ex.pe',
            #to_emails='freddychpo@gmail.com',
            to_emails= correo,
            subject='Recuperacion de contraseña',
            #html_content='Para crear su nueva contraseña por favor ingresa al siguiente link en el navegador: ' + url + 'id/' + 'token' )
            html_content='Para crear su nueva contraseña por favor ingresa al siguiente link en el navegador: ' + url + str(id) +'/' + token )
        try:
            #sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            #sg = SendGridAPIClient(os.environ.get(apikey))
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print("try")
        except Exception as e:
            print(e)
            print(e.body)
            print("exception") """


        #return render_template('edit-contact.html', user = data[0]) 
        return 'envio de email'

        #return render_template("reset-password.html")

    
@app.route('/reset-password', methods=['GET','POST'])
def resetPassword():    
    return render_template("reset-password.html")

@app.route('/reset_password/<id>/<token>', methods=['GET','POST'])
def reset_password(id, token):
    if request.method == 'POST':
        print('post_reset_password')
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        
        if(password == passwordConfirm):
            if(ExisteUsuarioResetPass(id, token)):
                #actualizar a una nueva contrasena en base a paramtros: id y token
                ResetPasswordUser(id, token, passwordConfirm)
                print('se actualizo correctamente la contrasena del usuario')
                return redirect(url_for('Redirect'))
        else:
            print('los valores de la nueva contrasena y la confirmacion de la nueva contrasena no coinciden')
    else:
        print('get_reset_password', id, token)
        return render_template("reset-password.html", id = id, token = token)

@app.route('/loginValidate', methods=['GET','POST'])
def loginValidate():
    if request.method == 'POST':
        session.permanent == True
        user = request.form['username']
        password = request.form['password']

        passwordHashConvert = generate_password_hash(password)

        if(ExisteCliente(user)):
            #if(EsCorrectoPasswordHash(user, password)):
                #print('Inicio sesion correcto')

            if(EsCorrectoPasswordHash(user, password)):
                print('Inicio sesion correcto')
                #EsCorrectoPasswordHash(user,password)   
                #return render_template("index.html")
                session['user'] = user
                print(user)	   
                return redirect(url_for('Inicio'))
            else:
                print('password incorrecto')
                return render_template("login.html")
        else:
            print('no existe usuario')
            return render_template("login.html")

    

@app.route('/recover-account', methods=['GET'])
def recover_account():
    return render_template("recover-account.html")

@app.route('/update/<id>', methods = ['POST']) #methods es igual a un arreglo POST
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE CONTACTS
                SET fullname = %s,
                    email = %s,
                    phone =%s
                WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CONTACTS WHERE ID = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
   app.run(debug=True)
