from B_Conexion import *

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
programa = Flask(__name__)

CARPETA_IMG = os.path.join('upload')
programa.config['CARPETA_IMG'] = CARPETA_IMG

programa.secret_key = 'clave_secreta'

baseDatos = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "sepa",
)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

@programa.route('/upload/<nombre>')
def upload(nombre):
    return send_from_directory(programa.config['CARPETA_IMG'],nombre)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Inicio del programa
@programa.route('/')
def index():
    return render_template('A_login.html')
    #Ruta en la que inicia el html

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Login
@programa.route('/login', methods = ['POST'])
def Login():
    
    cedula = request.form['cedula']
    clave = request.form['clave']
    
    if cedula and clave:
        
        sql = f"SELECT  cedula, clave FROM usuario_aprendiz WHERE cedula = '{cedula}' AND clave = '{clave}'"
              
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        
        resultado = cursor.fetchall()        
        if resultado:
            # Almacenar la cédula en la sesión
            session["logueado"] = True
            session["user_cedula"] = resultado[0][0]
            session["user_clave"] = resultado[0][1]

            return redirect('/mostrarDatos_aprendiz')
        
        else:
            print("Credenciales incorrectas")
          
        return redirect('/mostrarDatos_aprendiz')
        
    else:
        print("error en la dijitacion de datos")
            
    return render_template('A_login.html')    
    
    
    #En el siguiente apartado es donde se tomaran los datos que se van a mostrar en el home
    
@programa.route('/mostrarDatos_aprendiz')    
def mostrarDatos_aprendiz():

    if session.get("logueado"):

        sql = f"SELECT doc_identificacion, tipo_documento, nombres, apellidos, municipio, direccion, correo, telefono FROM aprendices WHERE "  
        
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        if Datos:
            
            session["usuario_cedula"] = Datos[0][0]
            session["usuario_tipo_doc"] = Datos[0][1]
            session["usuario_nombres"] = Datos[0][2]
            session["usuario_apellidos"] = Datos[0][3]
            #En este apartado se han separado los datos para evitar confucion
            
            session["user_municipio"] = Datos[0][4]
            session["user_direccion"] = Datos[0][5]
            session["user_correo"] = Datos[0][6]
            session["user_telefono"] = Datos[0][7] 

            return redirect('/mostrar_contrato')   
        
        else:
            print(f"no se encontro datos")

#-------------------------------------------------------------------------------------------------------------------------------------------

@programa.route('/mostrar_contrato')
def mostrar_contrato():

    if session.get("logueado"):

        sql = f"SELECT ficha, curso, nivel_formacion FROM contratos"

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        if Datos:
            session["user_ficha"] = Datos[0][0]
            session["user_curso"] = Datos[0][1]
            session["user_nivel"] = Datos[0][2]

            return redirect('/home_aprendiz')
    else:
        print("hola mundo")

#-------------------------------------------------------------------------------------------------------------------------------------------

#Home Aprendiz-- Perfil
@programa.route('/home_aprendiz')
def home_aprendiz():

    if session.get("logueado"):#Trae los datos de session de arriba
        
        usuario_nombre = session.get("usuario_nombres")
        usuario_apellidos = session.get("usuario_apellidos")
        usuario_id_cedula = session.get("usuario_cedula")
        usuario_tipo_documento = session.get("usuario_tipo_doc")

        user_municipio = session.get("user_municipio")
        user_dir = session.get("user_direccion")
        user_correo = session.get("user_correo")
        user_telefono = session.get("user_telefono")

        usuario_ficha = session.get("user_ficha")
        usuario_curso = session.get("user_curso")
        usuario_formacion = session.get("user_nivel")
                
        sql = f"SELECT nombres, apellidos, correo FROM datos_instructor"
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()
                
        session["nombre_instructor"] = Datos[0][0]
        session["apellido_instructor"] = Datos[0][1]
        session["correo_instructor"] = Datos[0][2]

        nombreInstructor = session.get("nombre_instructor")
        apellidoInstructor = session.get("apellido_instructor")
        correoInstructor = session.get("correo_instructor")
        
        return render_template("B_home_aprendiz.html",
                               
                               #Datos Aprendiz
                               NombreAprendiz = usuario_nombre, 
                               ApellidoAprendiz = usuario_apellidos, 
                               CedulaAprendiz = usuario_id_cedula,
                               tipo_doc = usuario_tipo_documento,

                               Municipio = user_municipio,
                               dir = user_dir,
                               CorreoAprendiz = user_correo,
                               TelefonoAprendiz = user_telefono,
                               
                               Ficha = usuario_ficha,
                               curso = usuario_curso,
                               nivel = usuario_formacion,


                               #Datos Instructor
                               NombreInstructor = nombreInstructor,
                               ApellidosInstructor = apellidoInstructor,
                               CorreoInstructor = correoInstructor) 

        #En este apartado logramos que se muestren los datos requeridos en el html
    else:

        return render_template("A_login.html")

#Inicio donde el aprendiz puede actualizar datos
@programa.route('/Datos_aprendiz', methods = ['POST'])
def Cambiar_datos_aprendiz():

    if session.get("logueado"):
        
        cedula = session.get("usuario_cedula")
        telefono = request.form['actualizacion_celular']
        correo = request.form['actualizacion_correo']

        sql = f"UPDATE aprendices SET telefono = '{telefono}', correo = '{correo}' WHERE doc_identificacion = '{cedula}'"#En este apartado se tendra que implementar el id, al igual que en el request. form, de igual manera en el html
        #Para poder hacer correcta el comprobante y que el update sea en un solo id y no en dos

        cursor = baseDatos.cursor()
        
        cursor.execute(sql)

        TomaDatos()

        #Datos Aprendiz        

        usuario_nombre = session.get("usuario_nombres")
        usuario_apellido = session.get("usuario_apellidos")
        usuario_id_cedula = session.get("usuario_cedula")
        usuario_tipo_documento = session.get("usuario_tipo_doc")

        user_telefono = session.get("user_telefono2")
        user_correo = session.get("user_correo2")
       
        user_municipio = session.get("user_municipio")
        user_dir = session.get("user_direccion")

        #Datos Instructor
        nombres_instructor = session.get("nombre_instructor")
        apellido_instructor = session.get("apellidos_instructor")
        correo_instructor = session.get("correo_instructor")
    
    return render_template("B_home_aprendiz.html",
                           
                               #Datos Aprendiz
                               NombreAprendiz = usuario_nombre, 
                               ApellidoAprendiz = usuario_apellido, 
                               CedulaAprendiz = usuario_id_cedula,
                               tipo_doc = usuario_tipo_documento,

                               TelefonoAprendiz = user_telefono,
                               CorreoAprendiz = user_correo,
                               Municipio = user_municipio, 
                               dir = user_dir,    
                               
                               #Datos Instructor
                               NombreInstructor = nombres_instructor,
                               ApellidosInstructor = apellido_instructor,
                               CorreoInstructor = correo_instructor)

def TomaDatos():

    cedula = session.get("usuario_cedula")    

    sql = f"SELECT telefono, correo FROM aprendices WHERE doc_identificacion = '{cedula}'"

    cursor = baseDatos.cursor()

    cursor.execute(sql)

    Datos = cursor.fetchall()

    session["user_telefono2"]=Datos[0][0]
    session["user_correo2"]=Datos[0][1]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Subir foto del aprendiz
@programa.route('/agregar_foto', methods=['POST'])
def agregar_foto():

    if 'foto_aprendiz' in request.files:
        foto = request.files['foto_aprendiz']

        if foto.filename != '':
            ahora = datetime.now()
            tiempo = ahora.strftime("%Y%m%d%H%M%S")
            nombre, extension = os.path.splitext(foto.filename)
            nombre_foto = "F" + tiempo + extension
            #ruta_foto = os.path.join('upload', nombre_foto)
            
            #Guardar la nueva foto
            #foto.save(ruta_foto)
            foto.save("upload/" + nombre_foto)

            # Obtener la foto antigua y eliminarla
            cursor = baseDatos.cursor()

            cursor.execute("SELECT foto_aprendiz FROM aprendices")
            foto_antigua = cursor.fetchall()
            
            os.remove(os.path.join(programa.config['CARPETA_IMG'], foto_antigua[0][0]))

            # Actualizar la base de datos con la nueva foto
            cursor.execute(f"UPDATE aprendices SET foto_aprendiz='{nombre_foto}'")
            baseDatos.commit()

            return redirect('/mostrarDatos_aprendiz')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Visitas
@programa.route('/visita_aprendiz')
def dato_visita_aprendiz():

    if session.get("logueado"):

        sql = f"SELECT id_aprendiz, fecha_visita_1, fecha_visita_2, fecha_visita_3 FROM visitas"
    
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        session["usuario_fecha1"] = Datos[0][1]
        session["usuario_fecha2"] = Datos[0][2]
        session["usuario_fecha3"] = Datos[0][3]

        return redirect('/dato_observacion')

    else:
        print("el error se encuenta aca")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""@programa.route('/dato_visitas')
def dato_visita():

    if session.get("logueado"):

        sql = f"SELECT visita_1, visita_2, visita_3 FROM visitas"
    
        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        session["usuario_fecha1"] = Datos[0][0]
        session["usuario_fecha2"] = Datos[0][1]
        session["usuario_fecha3"] = Datos[0][2]

        return redirect('/dato_observacion')

    else:
        print("el error se encuenta aca")

"""
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@programa.route('/dato_observacion')
def dato_observacion():

    sql = f"SELECT observacion, fecha FROM observaciones"

    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()

    if Datos and len(Datos) > 0:
        session["user_observacion"] = Datos[0][0]
        session["user_fecha_ob"] = Datos[0][1]

        return redirect('/dato_visita')
    
    else:
        print("hola mundo")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

@programa.route('/dato_visita')
def dato_visita():

    usuario_fecha_1 = session.get("usuario_fecha1")
    usuario_fecha_2 = session.get("usuario_fecha2")
    usuario_fecha_3 = session.get("usuario_fecha3")

    usuario_observacion = session.get("user_observacion")
    usuario_fecha_ob = session.get("user_fecha_ob")

    return render_template("C_visitas_aprendiz.html",
                           Fecha_Visita1 = usuario_fecha_1,
                           Fecha_Visita2 = usuario_fecha_2,
                           Fecha_Visita3 = usuario_fecha_3,

                           Obsevacion = usuario_observacion,
                           fecha_observacion = usuario_fecha_ob)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Notificaciones
@programa.route('/Notificaciones', methods = ['POST'])
def Notificaciones(id):

    id = id
    para = request.form['persona_dirijido']#Para, es decir, para quien va dirigido el correo
    asunto = request.form['asunto']#el asunto del correo
    contenido_correo = request.form['contenido_correo']
    sql = f"SELECT * FROM '' WHERE id = {id}, para = {para}, asunto = {asunto}, contenido_correo = {contenido_correo}"
    #Cambiar el '' por el nombre de la tabla

    cursor = baseDatos.cursor()

    cursor.execute(sql)
    
    Datos = cursor.fetchall()
    
    print(Datos)
    #Prueba de la toma de los datos

    return render_template('B_home_aprendiz.html')
    #Cambiar '' por el html a retornar

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Empresa asignada, donde el aprendiz puede observar la informacion
@programa.route('/empresa_asignada')
def Datos_empresa():
    
    if session.get("logueado"):

        usuario_empresa = session.get("usuario_nombre_empresa")
        usuario_direccion_empresa = session.get("usuario_direccion")
        usuario_telefono_empresa = session.get("usuario_telefono")
        usuario_departamento_empresa = session.get("usuario_municipio")
        usuario_correo_empresa = session.get("usuario_correo")
        usuario_nombre_jefe = session.get("usuario_nombres")
        usuario_apellidos_jefe = session.get("usuario_apellidos")

        sql = f"SELECT razon_social, direccion, ciudad, tel1, correo, nombres, apellidos, municipio FROM empresa"

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
        session["usuario_municipio"] = Datos[0][7]

    return render_template("E_empresa_asignada.html",
                           Nombre_empresa = usuario_empresa,
                           Direccion_empresa = usuario_direccion_empresa,
                           Telefono_empresa = usuario_telefono_empresa,
                           Departamento_empresa = usuario_departamento_empresa,
                           Correo_empresa = usuario_correo_empresa,
                           Nombre_Jefe = usuario_nombre_jefe,
                           Apellidos_Jefe = usuario_apellidos_jefe)


#En este apartado es donde el aprendiz puede editar cierta informacion de la empresa


@programa.route('/cambiar_datos_empresa', methods = ['POST'])
def Cambiar_datos_empresa():
        
    if session.get("logueado"):

        direccion = request.form['actualizacion_direccion_empresa']
        telefono = request.form['actualizacion-celular']
        departamento = request.form['actualizacion_ciudad_empresa']
        correo = request.form['actualizacion_correo_empresa']
        nombre_conformador = request.form['actualizacion_nombre_jefe_empresa']
        apellidos_conformador = request.form['actualizacion_apellido_jefe_empresa']

        sql = f"UPDATE empresa SET direccion = '{direccion}', tel1 = '{telefono}', municipio = '{departamento}', correo = '{correo}', nombre_conformador = '{nombre_conformador}', apellidos_conformador = '{apellidos_conformador}'"
        
        cursor = baseDatos.cursor()

        cursor.execute(sql)
        
        tomaDatos_empresa()

        usuario_empresas = session.get("usuario_nombre_empresa")
        usuario_direccion_empresas = session.get("usuario_direccion")
        usuario_telefono_empresas = session.get("usuario_telefono_")
        usuario_departamento_empresas = session.get("usuario_departamento")
        usuario_correo_empresas = session.get("usuario_correo")
        usuario_nombre_jefes = session.get("usuario_nombre")
        usuario_apellidos_jefes = session.get("usuario_apellidos")

    return render_template("E_empresa_asignada.html",
                           Nombre_empresa = usuario_empresas,
                           Direccion_empresa = usuario_direccion_empresas,
                           Telefono_empresa = usuario_telefono_empresas,
                           Departamento_empresa = usuario_departamento_empresas,
                           Correo_empresa = usuario_correo_empresas,
                           Nombre_Jefe = usuario_nombre_jefes,
                           Apellidos_Jefe = usuario_apellidos_jefes)

def tomaDatos_empresa():

    sql = f"SELECT direccion, tel1, municipio, correo, nombres, apellidos FROM empresa"
    
    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()

    session["usuario_direccion_"] = Datos[0][0]
    session["usuario_telefono_"] = Datos[0][1]
    session["usuario_departamento_"] = Datos[0][2]
    session["usuario_correo_"] = Datos[0][3]
    session["usuario_nombre_"] = Datos[0][4]
    session["usuario_apellidos_"] = Datos[0][5]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#Datos iniciales del programa
@programa.route('/inputRegional')
def bita_cora():

    sql = f"SELECT ficha, curso, regional, centro, modalidad_productiva FROM contratos"

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

    sql = f"SELECT doc_identificacion, nombres, correo, telefono FROM aprendices"

    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()

    session["usuario_identificacion"] = Datos[0][0]
    session["usuario_aprendiz"] = Datos[0][1]
    session["usuario_correo"] = Datos[0][2]
    session["usuario_telefono"] = Datos[0][3]

    return Datos

##----------------------------------------------------------------

@programa.route('/Datos_basico')
def basico_empresa():

    user_ficha = session.get('user_ficha')
    user_curso = session.get('user_curso')
    user_regional = session.get('usuario_regional')
    user_centro = session.get('usuario_cent')
    user_modalidad = session.get('usuario_modalidad_productiva')

    user_identificacion = session.get('usuario_identificacion')
    user_aprendiz = session.get('usuario_aprendiz')
    user_correo = session.get('usuario_correo')
    user_telefono = session.get('usuario_telefono')

    sql = f"SELECT nit, razon_social, nombres, tel1, correo FROM empresa"

    cursor = baseDatos.cursor()
    cursor.execute(sql)
    Datos = cursor.fetchall()

    session["user_nit"] = Datos[0][0]
    session["user_razon_social"] = Datos[0][1]
    session["user_nombres_jefe"] = Datos[0][2]
    session["user_tel1"] = Datos[0][3]
    session["user_correo"] = Datos[0][4]

    usuario_nit = session.get('user_nit')
    usuario_razon_social = session.get('user_razon_social')
    usuario_nombres_jefe = session.get('user_nombres_jefe')
    usuario_tel1 = session.get('user_tel1')
    usuario_correo = session.get('user_correo')

    return render_template("F_bitacora.html",
                            regional_aprend  = user_regional,  
                            centro_aprend = user_centro,
                            nombre_aprend = user_aprendiz,
                            modalidad = user_modalidad,
                            #----- Datos Empresa -----
                            nit = usuario_nit,
                            razon_social = usuario_razon_social,
                            nombres_jefe = usuario_nombres_jefe,
                            telefono = usuario_tel1,
                            correo = usuario_correo,
                            )
#------------------------------------------------------------------------------------


##----------------------------------------------------------------
@programa.route('/inputBitacora',method = '')
def enviar_bitacora():
    
    empresa = request.form['bit_aprend']
    nit = request.form['nit']
    bit_num = request.form['bit-num']
    periodo = request.form['periodo']
    nom_jefe = request.form['nom-jefe']
    telefono_con = request.form['telefono-con']
    correo_elect = request.form['correo-elect']
    modalidades = request.form['modalidades']
    nombre = request.form['nom-aprend']
    documento = request.form['documento-aprend']
    telefono_aprend = request.form['telefono-aprend']
    correo_aprend = request.form['correo-aprend']
    num_ficha = request.form['num-ficha']
    programa_aprend = request.form['programa-aprend']
    actividad_aprend = request.form['actividad-aprend']
    inicio_aprend = request.form['inicio-aprend']
    fin_aprend = request.form['fin-aprend']
    evidencia_aprend = request.form['evidencia-aprend']
    observacion_aprend = request.form['observacion-aprend']
    
    sql = f"INSERT INTO * (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) VALUES ('{empresa}','{nit}','{bit_num}','{periodo}','{nom_jefe}','{telefono_con}',
    '{correo_elect}','{modalidades}','{nombre}','{documento}','{telefono_aprend}','{correo_aprend}','{num_ficha}','{programa_aprend}','{actividad_aprend}',
    '{inicio_aprend}','{fin_aprend}','{evidencia_aprend}','{observacion_aprend}')"
    #Cambiar "*" por el nombre de la tabla y cambiar cada "?" por el nombre de la columna a asignar
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    
    datos = cursor.fetchall()
    
    conexion.commit()
    
    #Insertar html a retornar al momento de terminar la bitacora
    return render_template('')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Final del programa
if __name__ == '__main__':
    programa.run(debug = True)