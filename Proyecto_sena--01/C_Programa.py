from B_Conexion import *
from routes.datAprend import mostrarDatos_aprendiz

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

@programa.route('/upload/<nombre>')
def upload(nombre):
    return send_from_directory(programa.config['CARPETA_IMG'],nombre)

#Inicio del programa
@programa.route('/')
def index():
    return render_template('/loginsepa/loginsepa.html')
    #Ruta en la que inicia el html
#------------------------------------------------------------------------------------------------------------------------------------------------------------

#INGRESO LOGIN -----------------------------------------------------
@programa.route('/ingresa_usuario', methods = ['POST'])
def ingresa_usuario():
    cedulaingreso = request.form['cedulaingreso']
    claveingreso = request.form['claveingreso']
    
    patron_clave = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$')
    patron_cedula = re.compile(r'^\d{8,}$')
    
    if (cedulaingreso)and(claveingreso):
        
        # Cifrar contraseña
        clavecifrada = hashlib.pbkdf2_hmac('sha256', claveingreso.encode('utf-8'), b'saltsupersegura', 100000).hex()
        
        if (patron_clave.match(claveingreso)):
            
            if (patron_cedula.match(cedulaingreso)):
                
                ##Pregunta por los 3 roles para ver si existen
                ##instru
                sql = f"SELECT  doc_indentidad, estado, clave FROM usuario_instructor WHERE doc_indentidad = '{cedulaingreso}' AND clave = '{clavecifrada}'"
                conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                
                cur = conexion.cursor()
                cur.execute(sql)
                datosingreso_i = cur.fetchall()
                
                ###aprendiz
                sql = f"SELECT doc_indentidad, clave, estado FROM usuario_aprendiz WHERE doc_indentidad = '{cedulaingreso}' AND clave = '{clavecifrada}'"
                conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                    
                cur = conexion.cursor()
                cur.execute(sql)
                datosingreso_a = cur.fetchall()
                
                ##coordi
                sql = f"SELECT  * FROM usuario_coordi WHERE doc_indentidad = '{cedulaingreso}' AND clave = '{clavecifrada}'"
                conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                    
                cur = conexion.cursor()
                cur.execute(sql)
                datosingreso_c = cur.fetchall()
                cur.close()
                conexion.close()
                     
                if datosingreso_i:
                    
                    if(datosingreso_i[0][1]=="activo"):
                    #es intructor
                        if(clavecifrada == datosingreso_i[0][2])and(cedulaingreso == datosingreso_i[0][0]):
                            #Se hace la comparacion donde la contraseña sea igual a la del input
                            
                            ##SE DECLARAN LAS VARIABLES SESSION DEL INSTRUCTOR   
                                
                            session["logueado"]=True
                            session["instru_cedula"]=datosingreso_i[0][0]
                            programa.config['PERMANENT_SESSION_LIFETIME'] = 7200 ###INICIALIZA EL TIEMPO DE SESION A 2 horas
                                    
                            return redirect('/home_instru')
                    else:
                                mensaje_error_inactivo="El usuario esta inactivo"         
                                return render_template('/loginsepa/loginsepa.html', mensaje_error_inactivo=mensaje_error_inactivo) 
                
                elif datosingreso_a:
                        
                        #es aprendiz
                        
                        if(datosingreso_a[0][2]=="activo"):
                        
                            if(clavecifrada == datosingreso_a[0][1])and(cedulaingreso == datosingreso_a[0][0]):
                                #Se hace la comparacion donde la contraseña sea igual a la del input
                                ##poner variables q usan en aprendiz
                                session["logueado"]=True
                                session["aprendiz_cedula"]=datosingreso_a[0][0]
                                    
                                programa.config['PERMANENT_SESSION_LIFETIME'] = 1800 ###INICIALIZA EL TIEMPO DE SESION A 30 MIN
                                    
                                return redirect('/mostrarDatos_aprendiz')
                            
                            ##CREAR RUTA DEL HOME APRENDIZ
                        else:
                                mensaje_error_inactivo="El usuario esta inactivo"         
                                return render_template('/loginsepa/loginsepa.html', mensaje_error_inactivo=mensaje_error_inactivo),print("Error encontrado en el apartado del aprendiz")
                                
                elif datosingreso_c:
                        
                            #es coordinador
                            if(datosingreso_c[0][5]=="activo"):
                            
                                if(clavecifrada == datosingreso_c[0][1])and(cedulaingreso == datosingreso_c[0][0]):
                                #Se hace la comparacion donde la contraseña sea igual a la del input 
                                ##poner variables q usan en COORDINADOR
                                    session["logueado"]=True
                                    session["aprendiz_nombre"]=datosingreso_c[0][4]
                                    session["aprendiz_cedula"]=datosingreso_c[0][7]
                                    
                                    programa.config['PERMANENT_SESSION_LIFETIME'] = 28800 ###INICIALIZA EL TIEMPO DE SESION A 8 horas
                                    
                                    return redirect('/home_aprendiz')
                                    ##CREAR RUTA DEL HOME COORDINADOR
                                    
                            else:
                                mensaje_error_inactivo="El usuario esta inactivo"         
                                return render_template('/loginsepa/loginsepa.html', mensaje_error_inactivo=mensaje_error_inactivo)
                else:
                    mensaje_error_ingreso="El usuario no existe o la contraseña no es correcta!"         
                    return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)  
            else:
                mensaje_error_ingreso="Cedula no valida!"
                return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso),print("Error encontrado en la cedula")
        else:
            mensaje_error_ingreso="Contraseña no valida!"
            return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
    else:
        mensaje_error_ingreso="Contraseña o correo no ingresado!"
        return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
    
###########################RECUPERA CONTRASEÑA--------------------------------------------------------

@programa.route('/recupera')
def recupera():
    return render_template ("/loginsepa/envia_correo.html")

################ENVIA CORREO-------------------------------------------------------------------------

@programa.route('/envia_correo', methods=['POST'])
def enviar_correo():
    
    destinatario = request.form['correoingreso']
    
    patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if patron_correo.match(destinatario):
        
        ##REVISAR SI CORREO EXISTE EN BASE DE DATOS:
        ## INSTRU
        sql = f"SELECT doc_indentidad,correo FROM usuario_instructor WHERE correo = '{destinatario}' AND estado='activo'"
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        
        cur = conexion.cursor()
        cur.execute(sql)
        datexiten_instru = cur.fetchall()
        cur.close()
        conexion.close()
        
        ######Aprendiz
        
        sql = f"SELECT doc_indentidad,correo FROM usuario_aprendiz WHERE correo = '{destinatario}' AND estado='activo'"
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        
        cur = conexion.cursor()
        cur.execute(sql)
        datexiten_aprendiz = cur.fetchall()
        cur.close()
        conexion.close()
        
        #########COORDI
        
        sql = f"SELECT doc_indentidad,correo FROM usuario_coordi WHERE correo = '{destinatario}' AND estado='activo'"
        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
        
        cur = conexion.cursor()
        cur.execute(sql)
        datexiten_coordi = cur.fetchall()
        cur.close()
        conexion.close()
        
        if len(datexiten_instru) > 0:
            ##ES INSTRU
            # Obtener la fecha de la base de datos
            sql = f"SELECT fecha_ultimo_cambio, doc_indentidad FROM usuario_instructor WHERE correo = '{destinatario}'"
            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            cur = conexion.cursor()
            cur.execute(sql)
            fecha_base_datos = cur.fetchall()
            
            fechabd_str = fecha_base_datos[0][0]
            fechabd = datetime.strptime(fechabd_str, '%Y-%m-%d')

            # Obtener la fecha actual
            fecha_actual = datetime.now()

            # Sumar exactamente 30 días a la fecha de la base de datos simulada
            fecha_30_dias_despues = fechabd + timedelta(days=30)
            
            # Verificar si la fecha actual es igual o mayor a la fecha guardada bd
            if fecha_actual >= fecha_30_dias_despues:
                ##dejara al usuario cambiar su contraseña automaticamente, enviandolo al correo
                
                cedula = datexiten_instru[0][0]
                asunto = "Recuperacion de contraseña SEPA/CAB"
                servidor_smtp = "smtp.gmail.com"
                puerto_smtp = 587
                usuario_smtp = "Sepacap2024@gmail.com"
                contraseña_smtp = "kdcg jmxs kduz tgtn"
                mensaje = MIMEMultipart()
                mensaje['From'] = usuario_smtp
                mensaje['To'] = destinatario
                mensaje['Subject'] = asunto
                
                ##GENERA CLAVE ALEATORIAS
                longitud = random.randint(8, 10)  # Longitud aleatoria entre 8 y 10 caracteres
                caracteres = string.ascii_letters + string.digits + string.punctuation
                clave_generada = ''
                while True:
                    clave_generada = ''.join(random.choice(caracteres) for i in range(longitud))
                    if (any(c.islower() for c in clave_generada)
                        and any(c.isupper() for c in clave_generada)
                        and any(c.isdigit() for c in clave_generada)
                        and any(c in string.punctuation for c in clave_generada)):
                        break
                
                ##TRAER DATOS PERSONALES
                sql = f"SELECT nombres, apellidos FROM datos_instructor WHERE id_instructor = '{cedula}'"
                conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                cur = conexion.cursor()
                cur.execute(sql)
                datos_instru = cur.fetchall()
                nombre = datos_instru[0][0]
                apellido = datos_instru[0][1]
                
                # Cifrar contraseña
                clave_envia_cifrada = hashlib.pbkdf2_hmac('sha256', clave_generada.encode('utf-8'), b'saltsupersegura', 100000).hex()
                # Crear el cuerpo del mensaje en formato HTML
                cuerpo_html = f"""
                <html>
                <body>
                <h2 style="color: black;>Recuperación de contraseña SEPA/CAB</h2>
                <p style="color: black;>{nombre} {apellido},</p>
                <p>Usuario con número de documento ({cedula}),</p>
                <p>Su nueva contraseña es: <strong>{clave_generada}</strong></p>
                <img src="cid:logo" width="200" height="auto"> <!-- Este es el identificador para referenciar el logo -->
                </body>
                </html>
                """
                mensaje.attach(MIMEText(cuerpo_html, 'html'))

                # Adjuntar el logo como una parte del correo electrónico
                with open(os.path.join(programa.root_path, 'static', 'imagenes', 'login', 'sena.png'), 'rb') as f:
                    logo = MIMEImage(f.read(), name='logo.png')
                    logo.add_header('Content-ID', '<logo>')  # Asignar un identificador al logo
                mensaje.attach(logo)
                    
                try:
                        with smtplib.SMTP(host=servidor_smtp, port=puerto_smtp) as servidor:
                            servidor.starttls()
                            servidor.login(usuario_smtp, contraseña_smtp)
                            cuerpo_correo = mensaje.as_string()
                            servidor.sendmail(usuario_smtp, destinatario, cuerpo_correo)
                        sql = f"UPDATE `usuario_instructor` SET `clave` = '{clave_envia_cifrada}' WHERE `usuario_instructor`.`correo` = '{destinatario}'"
                        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                        cur = conexion.cursor()
                        cur.execute(sql)
                        conexion.commit()
                        cur.close()
                        conexion.close()
                        mensaje_cambio_contra_bueno = "Su Contraseña ha sido cambiada con exito."
                        cur.close()
                        conexion.close()
                        return render_template('/loginsepa/loginsepa.html', mensaje_cambio_contra_bueno=mensaje_cambio_contra_bueno)
                        
                except Exception as e:
                        mensaje_error = f"Error al enviar el correo: {e}"
                        return render_template('/loginsepa/envia_correo.html', mensaje_error=mensaje_error)
                    
            elif fecha_actual < fecha_30_dias_despues:
                mensaje_error_ingreso = "Upss...no puedes cambiar la contraseña mas de una vez al mes."
                return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
                
        elif len(datexiten_aprendiz) > 0:
                    ##ES APRENDIZ
                    
                    # Obtener la fecha de la base de datos
                    sql = f"SELECT fecha_ultimo_cambio, doc_indentidad FROM usuario_aprendiz WHERE correo = '{destinatario}'"
                    conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                    cur = conexion.cursor()
                    cur.execute(sql)
                    fecha_base_datos = cur.fetchall()
                    cur.close()
                    conexion.close()
                    
                    fechabd_str = fecha_base_datos[0][0]
                    fechabd = datetime.strptime(fechabd_str, '%Y-%m-%d')
                    
                    # Obtener la fecha actual
                    fecha_actual = datetime.now()
                    # Sumar exactamente 30 días a la fecha de la base de datos simulada
                    fecha_30_dias_despues = fechabd + timedelta(days=30)
                    # Verificar si la fecha actual es igual o mayor a la fecha guardada bd
                    if fecha_actual >= fecha_30_dias_despues:
                        
                        cedula = datexiten_aprendiz[0][0]
                        asunto = "Recuperacion de contraseña SEPA/CAB"
                        servidor_smtp = "smtp.gmail.com"
                        puerto_smtp = 587
                        usuario_smtp = "Sepacap2024@gmail.com"
                        contraseña_smtp = "kdcg jmxs kduz tgtn"
                        mensaje = MIMEMultipart()
                        mensaje['From'] = usuario_smtp
                        mensaje['To'] = destinatario
                        mensaje['Subject'] = asunto
                        
                        ##GENERA CLAVE ALEATORIAS
                        longitud = random.randint(8, 10)  # Longitud aleatoria entre 8 y 10 caracteres
                        caracteres = string.ascii_letters + string.digits + string.punctuation
                        clave_generada = ''
                        while True:
                            clave_generada = ''.join(random.choice(caracteres) for i in range(longitud))
                            if (any(c.islower() for c in clave_generada)
                                and any(c.isupper() for c in clave_generada)
                                and any(c.isdigit() for c in clave_generada)
                                and any(c in string.punctuation for c in clave_generada)):
                                break
                            
                        ##TRAER DATOS PERSONALES
                        sql = f"SELECT nombres, apellidos FROM aprendices WHERE doc_identificacion = '{cedula}'"
                        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                        cur = conexion.cursor()
                        cur.execute(sql)
                        datos_aprendiz = cur.fetchall()
                        nombre = datos_aprendiz[0][0]
                        apellido = datos_aprendiz[0][1]
                        
                        # Cifrar contraseña
                        clave_envia_cifrada = hashlib.pbkdf2_hmac('sha256', clave_generada.encode('utf-8'), b'saltsupersegura', 100000).hex()
                        # Crear el cuerpo del mensaje en formato HTML
                        cuerpo_html = f"""
                        <html>
                        <body>
                        <h2 style="color: black;>Recuperación de contraseña SEPA/CAB</h2>
                        <p style="color: black;>{nombre} {apellido},</p>
                        <p>Usuario con número de documento ({cedula}),</p>
                        <p>Su nueva contraseña es: <strong>{clave_generada}</strong></p>
                        <img src="cid:logo" width="200" height="auto"> <!-- Este es el identificador para referenciar el logo -->
                        </body>
                        </html>
                        """
                        mensaje.attach(MIMEText(cuerpo_html, 'html'))
                        # Adjuntar el logo como una parte del correo electrónico
                        with open(os.path.join(programa.root_path, 'static', 'imagenes', 'login', 'sena.png'), 'rb') as f:
                            logo = MIMEImage(f.read(), name='logo.png')
                            logo.add_header('Content-ID', '<logo>')  # Asignar un identificador al logo
                        mensaje.attach(logo)
                        
                        try:
                                with smtplib.SMTP(host=servidor_smtp, port=puerto_smtp) as servidor:
                                    servidor.starttls()
                                    servidor.login(usuario_smtp, contraseña_smtp)
                                    cuerpo_correo = mensaje.as_string()
                                    servidor.sendmail(usuario_smtp, destinatario, cuerpo_correo)
                                sql = f"UPDATE `usuario_aprendiz` SET `clave` = '{clave_envia_cifrada}' WHERE `usuario_aprendiz`.`correo` = '{destinatario}'"
                                conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                                cur = conexion.cursor()
                                cur.execute(sql)
                                conexion.commit()
                                cur.close()
                                conexion.close()
                                mensaje_cambio_contra_bueno = "Su Contraseña ha sido cambiada con exito."
                                return render_template('/loginsepa/loginsepa.html', mensaje_cambio_contra_bueno=mensaje_cambio_contra_bueno)
                                
                        except Exception as e:
                                mensaje_error = f"Error al enviar el correo: {e}"
                                return render_template('/loginsepa/envia_correo.html', mensaje_error=mensaje_error)
                            
                    elif fecha_actual < fecha_30_dias_despues:
                        mensaje_error_ingreso = "Upss...no puedes cambiar la contraseña mas de una vez al mes."
                        return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
                    
        elif len(datexiten_coordi) > 0:
                        
                        ##ES COORDINADOR
                        
                            # Obtener la fecha de la base de datos
                            sql = f"SELECT fecha_ultimo_cambio, doc_indentidad FROM usuario_coordi WHERE correo = '{destinatario}'"
                            conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                            cur = conexion.cursor()
                            cur.execute(sql)
                            fecha_base_datos = cur.fetchall()
                            cur.close()
                            conexion.close()
                            fechabd_str = fecha_base_datos[0][0]
                            fechabd = datetime.strptime(fechabd_str, '%Y-%m-%d')
                            
                            # Obtener la fecha actual
                            fecha_actual = datetime.now()
                            # Sumar exactamente 30 días a la fecha de la base de datos simulada
                            fecha_30_dias_despues = fechabd + timedelta(days=30)
                            # Verificar si la fecha actual es igual o mayor a la fecha guardada bd
                            if fecha_actual >= fecha_30_dias_despues:
                                
                                cedula = datexiten_coordi[0][0]
                                
                                asunto = "Recuperacion de contraseña SEPA/CAB"
                                servidor_smtp = "smtp.gmail.com"
                                puerto_smtp = 587
                                usuario_smtp = "Sepacap2024@gmail.com"
                                contraseña_smtp = "kdcg jmxs kduz tgtn"
                                mensaje = MIMEMultipart()
                                mensaje['From'] = usuario_smtp
                                mensaje['To'] = destinatario
                                mensaje['Subject'] = asunto
                                
                                ##GENERA CLAVE ALEATORIAS
                                longitud = random.randint(8, 10)  # Longitud aleatoria entre 8 y 10 caracteres
                                caracteres = string.ascii_letters + string.digits + string.punctuation
                                clave_generada = ''
                                while True:
                                    clave_generada = ''.join(random.choice(caracteres) for i in range(longitud))
                                    if (any(c.islower() for c in clave_generada)
                                        and any(c.isupper() for c in clave_generada)
                                        and any(c.isdigit() for c in clave_generada)
                                        and any(c in string.punctuation for c in clave_generada)):
                                        break
                                
                                # Cifrar contraseña
                                clave_envia_cifrada = hashlib.pbkdf2_hmac('sha256', clave_generada.encode('utf-8'), b'saltsupersegura', 100000).hex()
                                # Crear el cuerpo del mensaje en formato HTML
                                cuerpo_html = f"""
                                <html>
                                <body>
                                <h2 style="color: black;>Recuperación de contraseña SEPA/CAB</h2>
                                <p style="color: black;>Coordinador/ar,</p>
                                <p>Usuario con número de documento ({cedula}),</p>
                                <p>Su nueva contraseña es: <strong>{clave_generada}</strong></p>
                                <img src="cid:logo" width="200" height="auto"> <!-- Este es el identificador para referenciar el logo -->
                                </body>
                                </html>
                                """
                                mensaje.attach(MIMEText(cuerpo_html, 'html'))
                                
                                # Adjuntar el logo como una parte del correo electrónico
                                with open(os.path.join(programa.root_path, 'static', 'imagenes', 'login', 'sena.png'), 'rb') as f:
                                    logo = MIMEImage(f.read(), name='logo.png')
                                    logo.add_header('Content-ID', '<logo>')  # Asignar un identificador al logo
                                mensaje.attach(logo)
                                try:
                                        with smtplib.SMTP(host=servidor_smtp, port=puerto_smtp) as servidor:
                                            servidor.starttls()
                                            servidor.login(usuario_smtp, contraseña_smtp)
                                            cuerpo_correo = mensaje.as_string()
                                            servidor.sendmail(usuario_smtp, destinatario, cuerpo_correo)
                                        sql = f"UPDATE `usuario_coordi` SET `clave` = '{clave_envia_cifrada}' WHERE `usuario_coordi`.`correo` = '{destinatario}'"
                                        conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
                                        cur = conexion.cursor()
                                        cur.execute(sql)
                                        conexion.commit()
                                        cur.close()
                                        conexion.close()
                                        
                                        mensaje_cambio_contra_bueno = "Su Contraseña ha sido cambiada con exito."
                                        return render_template('/loginsepa/loginsepa.html', mensaje_cambio_contra_bueno=mensaje_cambio_contra_bueno)
                                        
                                except Exception as e:
                                        mensaje_error = f"Error al enviar el correo: {e}"
                                        return render_template('/loginsepa/envia_correo.html', mensaje_error=mensaje_error)
                                    
                            elif fecha_actual < fecha_30_dias_despues:
                                mensaje_error_ingreso = "Upss...no puedes cambiar la contraseña mas de una vez al mes."
                                return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)
        else: 
            mensaje_error_ingreso="Correo no existe o tu usuario esta inactivo!"
            return render_template('/loginsepa/loginsepa.html',mensaje_error_ingreso=mensaje_error_ingreso)
    else:
        
        mensaje_error_ingreso = "Upss... correo invalido!"
        return render_template('/loginsepa/loginsepa.html', mensaje_error_ingreso=mensaje_error_ingreso)    
        
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------

#Subir foto del aprendiz
@programa.route('/agregar_foto', methods=['POST'])
def agregar_foto():

    if 'foto_aprendiz' in request.files:
        foto = request.files['foto_aprendiz']

        if foto.filename != '':
            cedula = session.get("usuario_cedula") 
            
            ahora = datetime.now()
            tiempo = ahora.strftime("%Y%m%d%H%M%S")
            nombre,extension = os.path.splitext(foto.filename)
            nombre_foto = "F" + tiempo + extension
            
            #Guardar la nueva foto
            #foto.save(ruta_foto)
            foto.save("upload/" + nombre_foto)

            sql = f"SELECT foto_aprendiz, doc_identificacion FROM aprendices WHERE doc_identificacion = '{cedula}'"
            # Obtener la foto antigua y eliminarla
            cursor = baseDatos.cursor()
            cursor.execute(sql)

            foto_antigua = cursor.fetchall()
            
            foto_antigua=foto_antigua[0][0]

            filepath = os.path.join(programa.config['CARPETA_IMG'], foto_antigua)
            
            os.remove(filepath)
            
            sqlf = f"UPDATE aprendices SET foto_aprendiz='{nombre_foto}' WHERE doc_identificacion = '{cedula}'"

            cursor.execute(sqlf)
            
            # Actualizar la base de datos con la nueva foto
            
            baseDatos.commit()

            return redirect('/mostrarDatos_aprendiz')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

#Visitas
@programa.route('/visita_aprendiz')
def visita_aprendiz():

    if session.get("logueado"):

        cedula = session.get("aprendiz_cedula")

        sql = f"SELECT fecha_visita_1, fecha_visita_2, fecha_visita_3 FROM visitas WHERE id_aprendiz = '{cedula}'"
    
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        session["usuario_fecha1"] = Datos[0][0]
        session["usuario_fecha2"] = Datos[0][1]
        session["usuario_fecha3"] = Datos[0][2]

        return redirect('/dato_observacion')

    else:
        print("el error se encuenta aca")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        
@programa.route('/dato_observacion')
def dato_observacion():

    cedula = session.get("aprendiz_cedula")

    sql = f"SELECT observacion, fecha FROM observaciones WHERE id_aprendiz = '{cedula}'"

    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()
    
    session["user_observacion"] = Datos[0][0]
    session["user_fecha_ob"] = Datos[0][1]

    return redirect('/dato_visita')
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

@programa.route('/dato_visita')
def dato_visita():

    usuario_fecha_1 = session.get("usuario_fecha1")
    usuario_fecha_2 = session.get("usuario_fecha2")
    usuario_fecha_3 = session.get("usuario_fecha3")

    usuario_observacion = session.get("user_observacion")
    usuario_fecha_ob = session.get("user_fecha_ob")

    return render_template("/aprendiz/C_visitas_aprendiz.html",
                           Fecha_Visita1 = usuario_fecha_1,
                           Fecha_Visita2 = usuario_fecha_2,
                           Fecha_Visita3 = usuario_fecha_3,
                           Obsevacion = usuario_observacion,
                           fecha_observacion = usuario_fecha_ob)
#------------------------------------------------------------------------------------------------------------------------------------------------------------

#Notificaciones

@programa.route('/listado')
def listado():
        
    cedula = session.get("aprendiz_cedula")
    
    sql = f"SELECT nombre_instructor, fecha_envio, asunto, comentario FROM notifi_aprendiz WHERE cedula_aprendiz = '{cedula}' ORDER BY fecha_envio DESC"
    
    cursor = baseDatos.cursor()
    cursor.execute(sql)   
    informacion = cursor.fetchall()
    
    baseDatos.commit()
    return render_template("/aprendiz/D_notificaciones_aprendiz.html", info=informacion)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#Empresa asignada, donde el aprendiz puede observar la informacion
@programa.route('/empresa_asignada')
def Datos_empresa():
    
    if session.get("logueado"):
        
        id_contrato = session.get("user_contrato")

        sql = f"SELECT razon_social, direccion, ciudad, tel1, correo, nombres, apellidos, id_contrato FROM empresa WHERE id_contrato = '{id_contrato}' "

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        session["usuario_nombre_empresa"] = Datos[0][0]
        session["usuario_direccion"] = Datos[0][1]
        session["usuario_ciudad"] = Datos[0][2]
        session["usuario_telefono"] = Datos[0][3]
        session["usuario_correo"] = Datos[0][4]
        session["usuario_nombres"] = Datos[0][5]
        session["usuario_apellidos"] = Datos[0][6]
        session["usuario_id_contrato"] = Datos[0][7]
        
        #Envia las variables segun la tabla

        id_contrato = session.get("user_contrato")

        sql = f"SELECT direccion, tel2, correo, nombres, apellidos, ciudad, razon_social FROM temporal_empresa WHERE id_contrato = '{id_contrato}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql) 
        Datos_temporal = cursor.fetchall()

        if Datos_temporal:

            usuario_direccion_empresa = Datos_temporal[0][0]
            usuario_telefono_empresa = Datos_temporal[0][1]
            usuario_correo_empresa = Datos_temporal[0][2]
            usuario_nombre_jefe = Datos_temporal[0][3]
            usuario_apellidos_jefe = Datos_temporal[0][4]
            usuario_ciudad_empresa = Datos_temporal[0][5]
            usuario_razon_empresa = Datos_temporal[0][6]

            return render_template("/aprendiz/E_empresa_asignada.html",
                           Direccion_empresa = usuario_direccion_empresa,
                           Telefono_empresa = usuario_telefono_empresa,
                           Ciudad_empresa = usuario_ciudad_empresa,
                           Correo_empresa = usuario_correo_empresa,
                           Nombre_Jefe = usuario_nombre_jefe,
                           Apellidos_Jefe = usuario_apellidos_jefe,
                           Nombre_empresa = usuario_razon_empresa)
        
        elif Datos: 

            usuario_empresa = Datos[0][0]
            usuario_direccion_empresa= Datos[0][1]
            usuario_ciudad_empresa = Datos[0][2]
            usuario_telefono_empresa= Datos[0][3]
            usuario_correo_empresa= Datos[0][4]
            usuario_nombre_jefe = Datos[0][5]
            usuario_apellidos_jefe = Datos[0][6]
            
            return render_template("/aprendiz/E_empresa_asignada.html",
                           Nombre_empresa = usuario_empresa,
                           Direccion_empresa = usuario_direccion_empresa,
                           Telefono_empresa = usuario_telefono_empresa,
                           Ciudad_empresa = usuario_ciudad_empresa,
                           Correo_empresa = usuario_correo_empresa,
                           Nombre_Jefe = usuario_nombre_jefe,
                           Apellidos_Jefe = usuario_apellidos_jefe)

#En este apartado es donde el aprendiz puede editar cierta informacion de la empresa

@programa.route('/cambiar_datos_empresa', methods = ['POST'])
def Cambiar_datos_empresa():
        
    if session.get("logueado"):

        direccion = request.form['actualizacion_direccion_empresa']
        telefono = request.form['actualizacion-celular']
        ciudad = request.form['actualizacion_ciudad_empresa']
        correo = request.form['actualizacion_correo_empresa']
        nombres = request.form['actualizacion_nombre_jefe_empresa']
        apellidos = request.form['actualizacion_apellido_jefe_empresa']

        id_contrato = session.get("user_contrato")

        sql = f"SELECT direccion, tel2, correo, nombres, apellidos, ciudad FROM temporal_empresa WHERE id_contrato = '{id_contrato}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql) 
        Dato_consulta = cursor.fetchall()

        if Dato_consulta:

            sql = f"UPDATE temporal_empresa SET direccion = '{direccion}', tel2 = '{telefono}', ciudad = '{ciudad}', correo = '{correo}', nombres = '{nombres}', apellidos= '{apellidos}' WHERE id_contrato = '{id_contrato}'"
            
            cursor = baseDatos.cursor()
            cursor.execute(sql)
            baseDatos.commit()

        else:

            razon_social = session.get('usuario_nombre_empresa')

            sql = f"INSERT INTO temporal_empresa (id_contrato, razon_social, direccion, tel2, ciudad, correo, nombres, apellidos) VALUES ('{id_contrato}', '{razon_social}','{direccion}', '{telefono}', '{ciudad}', '{correo}', '{nombres}', '{apellidos}') WHERE id_contrato = '{id_contrato}'"
            
            cursor = baseDatos.cursor()
            cursor.execute(sql)
            baseDatos.commit()

        return redirect('/empresa_asignada')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#Datos iniciales del programa
@programa.route('/inputRegional')
def bita_cora():

    if session.get("logueado"):

        cedula = session.get("aprendiz_cedula")

        sql = f"SELECT ficha, curso, regional, centro, alternativa FROM contratos WHERE id_aprendiz = '{cedula}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        #Tomar datos del aprendiz como la regional, centro de formacion y nombre
        tomaDatos_aprend()

        session["usuario_ficha"] = Datos[0][0]
        session["usuario_curso"] = Datos[0][1]
        session["usuario_regional"] = Datos[0][2]
        session["usuario_cent"] = Datos[0][3]
        session["usuario_modalidad_productiva"] = Datos[0][4]

    return redirect('/Datos_basico')

def tomaDatos_aprend():

    cedula = session.get("aprendiz_cedula")

    sql = f"SELECT doc_identificacion, nombres, apellidos, correo, telefono FROM aprendices WHERE doc_identificacion = '{cedula}'"

    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()

    session["usuario_identificacion"] = Datos[0][0]
    session["usuario_aprendiz"] = Datos[0][1]
    session["usuario_apellidos"] = Datos[0][2]
    session["usuario_correo"] = Datos[0][3]
    session["usuario_telefono"] = Datos[0][4]

    return Datos
#----------------------------------------------------------------

@programa.route('/Datos_basico')
def basico_empresa():

    if session.get("logueado"):
        
        id_contrato = session.get("user_contrato")
        
        user_ficha = session.get('user_ficha')
        user_curso = session.get('user_curso')
        user_regional = session.get('usuario_regional')
        user_centro = session.get('usuario_cent')
        user_modalidad = session.get('usuario_modalidad_productiva')
        user_identificacion = session.get('usuario_identificacion')
        user_aprendiz = session.get('usuario_aprendiz')
        user_apellido = session.get('usuario_apellidos')
        user_correo = session.get('usuario_correo')
        user_telefono = session.get('usuario_telefono')

        sql = f"SELECT id_contrato, nit, razon_social, nombres, tel1, correo FROM empresa WHERE id_contrato = '{id_contrato}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        user_nit = Datos[0][1]
        user_razon_social = Datos[0][2]
        user_nombres_jefe = Datos[0][3]
        user_tel1 = Datos[0][4]
        user_correo = Datos[0][5]

    return render_template("/aprendiz/F_bitacora.html",
                            regional_aprend  = user_regional,  
                            centro_aprend = user_centro,
                            nombre_aprend = user_aprendiz,
                            modalidad = user_modalidad,

                            #----- Datos Empresa -----

                            nit = user_nit,
                            razon_social = user_razon_social,
                            nombres_jefe = user_nombres_jefe,
                            telefono = user_tel1,
                            correo = user_correo,

                            #----- Datos Aprendiz -----
                            nombre_aprendiz = user_aprendiz,
                            apellido_aprendiz = user_apellido,
                            doc_id = user_identificacion,
                            tel_aprendiz = user_telefono,
                            correo_aprend = user_correo,
                            numero_ficha = user_ficha,
                            programa_formacion = user_curso)
#------------------------------------------------------------------------------------

@programa.route('/inputBitacora', methods = ['POST'])
def enviar_bitacora():
    
    bit_num = request.form['bit-num']
    periodo = request.form['periodo']
    actividad_aprend = request.form['actividad-aprend']
    inicio_aprend = request.form['inicio-aprend']
    fin_aprend = request.form['fin-aprend']
    evidencia_aprend = request.form['evidencia-aprend']
    observacion_aprend = request.form['observacion-aprend']
    
    sql = f"INSERT INTO bitacora (numero_bitacora, periodo, descripcion, fecha_inicio, fecha_fin, evidencia, otros) VALUES ('{bit_num}','{periodo}','{actividad_aprend}','{inicio_aprend}','{fin_aprend}','{evidencia_aprend}','{observacion_aprend}')"
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    datos = cursor.fetchall()
    conexion.commit()
    #Insertar html a retornar al momento de terminar la bitacora
    return render_template('/aprendiz/B_home_aprendiz.html')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

#Final del programa
if __name__ == '__main__':
    programa.run(debug = True)