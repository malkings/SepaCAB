from importaciones_instru import *

from B_Conexion import *

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
#LOGIN ------------------------ inicio de app
# Genera una clave para Fernet
clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

@app.route('/')
def login():
    return render_template ("loginsepa.html")

#INGRESO LOGIN -----------------------------------------------------
@app.route('/ingresa_usuario',methods = ['POST'])
def ingresa_usuario():
    cedulaingreso = request.form['cedulaingreso']
    claveingreso = request.form['claveingreso']
    
    patron_clave = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$')
    
    if (cedulaingreso)and(claveingreso):
        
        # Cifrar contraseña
        clavecifrada = hashlib.pbkdf2_hmac('sha256', claveingreso.encode('utf-8'), b'saltsupersegura', 100000).hex()
        
        if (patron_clave.match(claveingreso)):
            
            sql = f"SELECT  doc_indentidad, estado, clave FROM usuario_instructor WHERE doc_indentidad = '{cedulaingreso}' AND clave = '{clavecifrada}'"
            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            
            cur = conexion.cursor()
            cur.execute(sql)
            datosingreso = cur.fetchall()
            cur.close()
            conexion.close()
            
            if datosingreso:
                if(datosingreso[0][1]=="activo"):
                #es intructor
                    if(clavecifrada == datosingreso[0][2])and(cedulaingreso == datosingreso[0][0]):
                        #Se hace la comparacion donde la contraseña sea igual a la del input
                        
                        ##SE DECLARAN LAS VARIABLES SESSION DEL INSTRUCTOR   
                            
                        session["logueado"]=True
                        session["instru_cedula"]=datosingreso[0][0]
                        app.config['PERMANENT_SESSION_LIFETIME'] = 1800 ###INICIALIZA EL TIEMPO DE SESION A 30 MIN
                                
                        return redirect('/home_instru')
                else:
                            mensaje_error_inactivo="El usuario esta inactivo"         
                            return render_template('loginsepa.html', mensaje_error_inactivo=mensaje_error_inactivo) 
            else:
                        mensaje_error_ingreso="El usuario no existe"         
                        return render_template('loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)      
        else:
            mensaje_error_ingreso="Contraseña no valida"
            return render_template('loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
    else:
        mensaje_error_ingreso="Contraseña o correo no ingresado"
        return render_template('loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
    
#################################################HOME INSTU----------------------------------------------------------------

@app.route('/home_instru')
def home_instru():
    
    if (session.get("logueado"))and(session['logueado']==True):
        
            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            cur = conexion.cursor()
            sql=f"SELECT * FROM aprendices"
            cur.execute(sql)
            dataprendiz = cur.fetchall()
            cur.close()
            conexion.close()
            
            if dataprendiz:
                
                return render_template('instru.html', dataprendiz = dataprendiz)

            else:
                
                return render_template('instru.html', errordatos = "Datos no incontrados")
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')
        
########################BUSCADOR PRINCIPAL (HOME)--------------------------------------------------------------
        
@app.route('/buscador_instru_prin', methods=['POST'])
def buscador_instru_prin():
    
    if (session.get("logueado"))and(session['logueado']==True):
        
        busca_palabra = request.form['busca_instru_prin']
        
        if (busca_palabra):
            
            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            cur = conexion.cursor()
            sql=f"SELECT * FROM aprendices WHERE apellidos LIKE '%{busca_palabra}%' OR municipio LIKE '%{busca_palabra}%' OR nombres LIKE '%{busca_palabra}%' OR doc_identificacion LIKE '%{busca_palabra}%' OR telefono LIKE '%{busca_palabra}%'"
            cur.execute(sql)
            dataprendiz = cur.fetchall()
            cur.close()
            conexion.close()
            
            return render_template("/instru.html", dataprendiz = dataprendiz)
        
        else:  
            resultado = "Digite palabra a buscar"
            return render_template('instru.html', dataprendiz = dataprendiz)
        
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')
        
########################BUSCADOR PRINCIPAL (aprendices)--------------------------------------------------------------
        
@app.route('/buscador_instru_apre', methods=['POST'])
def buscador_instru_apre():
    
    if (session.get("logueado"))and(session['logueado']==True):
        
        busca_palabra = request.form['busca_instru_prin']
        
        if (busca_palabra):
            
            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            cur = conexion.cursor()
            sql=f"SELECT * FROM aprendices WHERE apellidos LIKE '%{busca_palabra}%' OR municipio LIKE '%{busca_palabra}%' OR nombres LIKE '%{busca_palabra}%' OR doc_identificacion LIKE '%{busca_palabra}%' OR telefono LIKE '%{busca_palabra}%'"
            cur.execute(sql)
            dataprendiz = cur.fetchall()
            cur.close()
            conexion.close()
            
            return render_template("/instru.html", dataprendiz = dataprendiz)
        
        else:  
            resultado = "Digite palabra a buscar"
            return render_template('instru.html', dataprendiz = dataprendiz)
        
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')
        
#################################encripta id de detalles------------------------------------------------
# Función para encriptar el ID
@app.route('/encriptar_id_detalles/<id>')
def encriptar_id_detalles(id):
    id_encriptado = cipher_suite.encrypt(str(id).encode()).decode('utf-8')
    return redirect(url_for('ver_aprendiz_instru', id=id_encriptado))

#################################ENCRIPTA id de BITACORAS------------------------------------------------
# Función para encriptar el ID
@app.route('/encriptar_id_bitacoras/<id>')
def encriptar_id_bitacoras(id):
    id_encriptado = cipher_suite.encrypt(str(id).encode()).decode('utf-8')
    return redirect(url_for('ver_bitacoras_instru', id=id_encriptado))

#################################ENCRIPTA id de OBSERVACIONES------------------------------------------------
# Función para encriptar el ID
@app.route('/encriptar_id_observaciones/<id>')
def encriptar_id_observaciones(id):
    id_encriptado = cipher_suite.encrypt(str(id).encode()).decode('utf-8')
    return redirect(url_for('ver_observaciones_instru', id=id_encriptado))

#################################VER MAS APRENDIZ------------------------------------------------
@app.route('/ver_aprendiz_instru/<id>')
def ver_aprendiz_instru(id):
    
    if (session.get("logueado"))and(session['logueado']==True):
        id = cipher_suite.decrypt(id.encode()).decode('utf-8')
        
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        cur.execute("SELECT doc_identificacion, nombres, apellidos, telefono, correo FROM aprendices WHERE doc_identificacion=%s",(id,))
        datos_aprendiz = cur.fetchall()
        
        cur.execute("SELECT id_contrato, ficha, curso, jefe_area, tipo_contrato  FROM contratos WHERE id_aprendiz=%s",(id,))
        datos_contrato = cur.fetchall()
        
        idcontrato = datos_contrato[0][0]
        
        sql = f"SELECT *  FROM empresa WHERE id_contrato='{idcontrato}'"
        cur.execute(sql)
        datos_empresa= cur.fetchall()
        
        cur.close()
        conexion.close()
        
        return render_template('ver_detalles_instru.html',datos_aprendiz=datos_aprendiz, datos_contrato=datos_contrato)
    
    else:
        ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
        return render_template ('loginsepa.html')
    
################################## VER BITACORAS DEL APRENDIZ
@app.route('/ver_bitacoras_instru/<id>')
def ver_bitacoras_instru(id):
    
    if (session.get("logueado"))and(session['logueado']==True):
        id = cipher_suite.decrypt(id.encode()).decode('utf-8')
        
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        cur.execute("SELECT * FROM bitacoras WHERE id_aprendiz=%s",(id,))
        datos_bitacoras = cur.fetchall()
        
        cur.close()
        conexion.close()
        
        return render_template('ver_bitacoras_instru.html', datos_bitacoras=datos_bitacoras)
    
    else:
        ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
        return render_template ('loginsepa.html')
    
################################## VER OBSERVACIONES DEL APRENDIZ
@app.route('/ver_observaciones_instru/<id>')
def ver_observaciones_instru(id):
    
    if (session.get("logueado"))and(session['logueado']==True):
        id = cipher_suite.decrypt(id.encode()).decode('utf-8')
        
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        cur.execute("SELECT observacion ,fecha FROM observaciones WHERE id_aprendiz=%s",(id,))
        datos_observaciones = cur.fetchall()
        
        cur.close()
        conexion.close()
        
        return render_template('ver_observaciones_instru.html', datos_observaciones=datos_observaciones, id=id)
    
    else:
        ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
        return render_template ('loginsepa.html')
    
################################## CREAR OBSERVACION
@app.route('/crea_observacion', methods=['POST'])
def crea_observacion():
    
        id_aprendiz = request.form['ingreso_id']
        observacion = request.form['text_observacion']
        id_instru = session.get("instru_cedula")
        fecha_actual = datetime.now().date()
        
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        sql=f"INSERT INTO observaciones(id_aprendiz, id_instructor, observacion, fecha) VALUES ('{id_aprendiz}','{id_instru}','{observacion}','{fecha_actual}')"
        cur.execute(sql)
        conexion.commit()
        cur.close()
        conexion.close()
        
        
        return render_template('ver_observaciones_instru.html')
    
#####################################MODULO DE OBSERVACION-------------------------------------------------

@app.route('/obser_instru')
def obser_instru():
    
    if (session.get("logueado"))and(session['logueado']==True):
        
        cedula =session.get("instru_cedula")
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        sql=f"SELECT id_aprendiz, observacion, fecha  FROM observaciones WHERE id_instructor ='{cedula}'"
        cur.execute(sql) 
        datos_obser = cur.fetchall()
        
        id_aprendiz=datos_obser[0][0]
        
        sql=f"SELECT doc_identificacion, nombres, apellidos  FROM aprendices WHERE doc_identificacion='{id_aprendiz}'"
        cur.execute(sql) 
        datos_apre = cur.fetchall()
        
        cur.close()
        conexion.close()
        
        return  render_template ('obser_instru.html',datos_obser=datos_obser, datos_apre=datos_apre)
    
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')

###################################MODULO DE PERFIL ----------------------------

@app.route('/perfil_instru')
def perfil():
    if (session.get("logueado"))and(session['logueado']==True):
        
        cedula =session.get("instru_cedula")
        
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        sql=f"SELECT telefono, nombres FROM datos_instructor WHERE id_instructor ='{cedula}'"
        cur.execute(sql) 
        telefono = cur.fetchall()
        
        cur = conexion.cursor()
        sql=f"SELECT correo,estado FROM usuario_instructor WHERE doc_indentidad ='{cedula}'"
        cur.execute(sql)
        correo = cur.fetchall()
        cur.close()
        conexion.close()
        
        correo= correo[0][0]
        telefono = telefono[0][0]
        
        return  render_template ('perfil_instru.html',telefono=telefono,correo=correo)
    
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')
        
###################################MODULO DE PERFIL(edita sus propios datos) ----------------------------

@app.route('/editar_datos_instru', methods=['POST'])
def editar_datos_instru():

        cedula =session.get("instru_cedula")
        nuevocorreo = request.form['nuevocorreo']
        nuevotelefono = request.form['nuevotelefono']
        nuevaclave = request.form['nuevaclave']
        nuevaclave_confirma = request.form['nuevaclave_confirma']
        
        #ACTUALIZA CONTRASEÑA SI FUERON INGRESADAS
        if (len(nuevaclave) > 1) and (len(nuevaclave_confirma) > 1) and (nuevaclave==nuevaclave_confirma):
            
            
            if(nuevaclave==nuevaclave_confirma):
                
                patron_clave = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$')
            
                # Cifrar contraseña
                clavecifrada = hashlib.pbkdf2_hmac('sha256', nuevaclave.encode('utf-8'), b'saltsupersegura', 100000).hex()
            
                if (patron_clave.match(nuevaclave)):
                
                    conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                    cur = conexion.cursor()
                    sql=f"UPDATE usuario_instructor SET clave ='{clavecifrada}' WHERE doc_indentidad = '{cedula}'"
                    cur.execute(sql)
                    conexion.commit()
                    cur.close()
                    conexion.close()
                    
                    #OSINO GUARDA RESTO DE DATOS
                    # Definir el patrón del telefono y correo
            
                    patron_telefono = re.compile(r'^\d{10}$')
                    patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            
                    if patron_correo.match(nuevocorreo):
                        if patron_telefono.match(nuevotelefono):
                    
                            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                            cur = conexion.cursor()
                            sql=f"UPDATE usuario_instructor SET correo ='{nuevocorreo}' WHERE doc_indentidad = '{cedula}'"
                            cur.execute(sql)
                            conexion.commit()
                        
                            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                            cur = conexion.cursor()
                            sql=f"UPDATE datos_instructor SET telefono ='{nuevotelefono}' WHERE id_instructor = '{cedula}'"
                            cur.execute(sql)
                            conexion.commit()
                            cur.close()
                            conexion.close()
                        
                            return render_template('perfil_instru.html', var_modal_bueno="true")
                    
                        else:
                            mensaje="Telefono incorrecto!"
                            return render_template('perfil_instru.html', var_modal_malo="true", mensaje=mensaje)
                    else:
                        mensaje="El correo no cumple con la estructura"
                        return render_template('perfil_instru.html', var_modal_malo="true", mensaje=mensaje)
                else:
                    mensaje="La contraseña no cumple con los requisitos"
                    return render_template('perfil_instru.html', var_modal_malo="true", mensaje=mensaje)
            else:
                mensaje="Las contraseñas no coinciden"
                return render_template('perfil_instru.html', var_modal_malo="true", mensaje=mensaje)
        else:
        #OSINO GUARDA RESTO DE DATOS
            # Definir el patrón del telefono y correo
            
            patron_telefono = re.compile(r'^\d{10}$')
            patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            
            if patron_correo.match(nuevocorreo):
                if patron_telefono.match(nuevotelefono):
                    
                        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                        cur = conexion.cursor()
                        sql=f"UPDATE usuario_instructor SET correo ='{nuevocorreo}' WHERE doc_indentidad = '{cedula}'"
                        cur.execute(sql)
                        conexion.commit()
                        
                        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                        cur = conexion.cursor()
                        sql=f"UPDATE datos_instructor SET telefono ='{nuevotelefono}' WHERE id_instructor = '{cedula}'"
                        cur.execute(sql)
                        conexion.commit()
                        cur.close()
                        conexion.close()
                        
                        return render_template('perfil_instru.html', var_modal_bueno="true")
                    
                else:
                    
                    mensaje="Telefono incorrecto!"
                    return  render_template ('/perfil_instru.html',mensaje=mensaje)   
            else:
                
                mensaje="El correo no cumple con la estructura"
                return  render_template ('/perfil_instru.html',mensaje=mensaje)      
            
            

##############################MODULO BITACORAS------------------------------------------------------------

@app.route('/bitacoras_instru')
def bitacoras_instru():
    
    if (session.get("logueado"))and(session['logueado']==True):
        
        return  render_template ('bitacoras_instru.html')
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')

##################################MODULO DE APRENDICES----------------------------------------------------

@app.route('/aprendices_instru')
def aprendices_instru():
    if (session.get("logueado"))and(session['logueado']==True):
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        cur = conexion.cursor()
        sql=f"SELECT * FROM aprendices"
        cur.execute(sql)
        dataprendiz = cur.fetchall()
        cur.close()
        conexion.close()
        
        if dataprendiz:
            
            return render_template('aprendices_instru.html', dataprendiz = dataprendiz)

        else:
            
            return render_template('aprendices_instru.html', errordatos = "Datos no incontrados")
        
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')
    
################################CERRAR SESION------------------------------------------------
    
@app.route('/cerrar_sesion_instru')
def cerrar_sesion_instru():
    if (session.get("logueado"))and(session['logueado']==True):
        session.pop('usuario_nombre', None)
        session.pop('logueado', None)
        session.pop('instru_nombre', None)
        session.pop('instru_cedula', None)
        session.pop('instru_telefono', None)
        session.pop('instru_area', None)
        session.pop('instru_centro', None)
        session.clear()
        return redirect('/')
    else:
            ##DEVUELVE AL LOGIN SI NO HAY SESSION INICIADA
            return render_template ('loginsepa.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    