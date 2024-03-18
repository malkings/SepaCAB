from B_Conexion import *
from models.datAprend import aprendices

@programa.route('/mostrarDatos_aprendiz')    
def mostrarDatos_aprendiz():

    if session.get("logueado"):  
        
        cedula = session.get("aprendiz_cedula")
        Datos = aprendices.mostrar(cedula)
      
        if Datos:
            
            session["usuario_cedula"] = Datos[0][0]
            session["usuario_tipo_doc"] = Datos[0][1]
            session["usuario_nombres"] = Datos[0][2]
            session["usuario_apellidos"] = Datos[0][3]
            #En este apartado se han separado los datos para evitar confucion
            session["user_municipio"] = Datos[0][4]
            session["user_direccion"] = Datos[0][5]
            session["user_telefono"] = Datos[0][6] 
            session["user_foto"] = Datos[0][7] 

            return redirect('/mostrar_contrato')   
        
        else:
            print(f"no se encontro datos", cedula)
    else:
        print("Error en el redirect", cedula)        

#-------------------------------------------------------------------------------------------------------------------------------------------
@programa.route('/mostrar_contrato')
def mostrar_contrato():

    if session.get("logueado"):

        cedula = session.get("aprendiz_cedula")
        Datos = aprendices.contrato(cedula)

        if Datos:
            session["user_contrato"] = Datos[0][0]
            session["user_ficha"] = Datos[0][1]
            session["user_curso"] = Datos[0][2]
            session["user_nivel"] = Datos[0][3]

            return redirect('/datInstructor')
        else: 
            return redirect('/iniciar_sesion')        
    else: 
        return redirect('/iniciar_sesion')        

#-------------------------------------------------------------------------------------
#Home aprendiz -- Datos del instructor de seguimiento  
@programa.route('/datInstructor')
def datInstructor():
    if session.get("logueado"):

        cedula = session.get("aprendiz_cedula")
        sql = f"SELECT id_instructor, id_aprendiz FROM asignaciones WHERE id_aprendiz = '{cedula}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Datos = cursor.fetchall()

        if Datos:
            session["id_instructor"] = Datos[0][0]
            return redirect('/home_aprendiz')
        else:
            print("Error al guardar la cedula del instructor", Datos)

#Home Aprendiz-- Perfil
@programa.route('/home_aprendiz')
def home_aprendiz():

    if session.get("logueado"):
        
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
        usuario_foto = session.get("user_foto")

        cedula = session.get("aprendiz_cedula")
        instructor = session.get("id_instructor")

        sql = f"SELECT id_instructor, id_aprendiz FROM asignaciones WHERE id_aprendiz = '{cedula}'"

        cursor = baseDatos.cursor()
        cursor.execute(sql)
        Dato = cursor.fetchall()

        if Dato:
            sql = f"SELECT id_instructor, nombres, apellidos FROM datos_instructor WHERE id_instructor = '{instructor}'" 
            cursor = baseDatos.cursor()
            cursor.execute(sql)
            Datos = cursor.fetchall()

            if Datos:
                session["nombres"] = Datos[0][1]
                session["apellidos"] = Datos[0][2]

                nombres = session.get("nombres")
                apellidos = session.get("apellidos")

                sql = f"SELECT doc_indentidad, correo FROM usuario_instructor WHERE doc_indentidad='{instructor}'"
                cursor.execute(sql)
                Datos_ins = cursor.fetchall()

                if Datos_ins:
                    session["correo"] = Datos_ins[0][1] 
                    correo = session.get("correo")
                else:
                    raise ValueError("No se encontraron datos del instructor", sql, instructor)
            else:
                raise ValueError("No se encontraron datos del instructor", sql, instructor)
        else:
            raise ValueError("No se encontraron datos del instructor", sql, instructor)
        """Dato, Datos, Datos_ins = aprendices.homeAprend(cedula, instructor) 
        print("Error al traer datos de la base de datos")

        if Datos:
            nombre_instructor = Datos[0][1]
            apellido_instructor = Datos[0][2]
        else:
            print("Error al tratar de guardar y obtener datos basicos del instructor")

        nombre_instructor = session.get("nombre_instructor")
        apellido_instructor = session.get("apellido_instructor")

        if Datos_ins:
            correo_instructor = Datos_ins[0][2]
        else:
            print("Error al guardar el correo del instructor")"""

        return render_template("/aprendiz/B_home_aprendiz.html",
                               
                               #Datos Aprendiz
                               NombreAprendiz = usuario_nombre, 
                               ApellidoAprendiz = usuario_apellidos, 
                               CedulaAprendiz = usuario_id_cedula,
                               tipo_doc = usuario_tipo_documento,
                               
                               FotoAprendiz = usuario_foto,

                               Municipio = user_municipio,
                               dir = user_dir,
                               CorreoAprendiz = user_correo,
                               TelefonoAprendiz = user_telefono,
                               
                               Ficha = usuario_ficha,
                               curso = usuario_curso,
                               nivel = usuario_formacion,

                               #Datos Instructor
                               NombreInstructor = nombres,
                               ApellidosInstructor = apellidos,
                               CorreoInstructor = correo) 

        #En este apartado logramos que se muestren los datos requeridos en el html
    else:

        return render_template('/loginsepa/loginsepa.html')
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

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

        usuario_foto = session.get("user_foto")

        user_telefono = session.get("user_telefono2")
        user_correo = session.get("user_correo2")
        user_municipio = session.get("user_municipio")
        user_dir = session.get("user_direccion")

        usuario_ficha = session.get("user_ficha")
        usuario_curso = session.get("user_curso")
        usuario_formacion = session.get("user_nivel")

        #Datos Instructor
        nombre_instructor = session.get("nombre_instructor")
        apellido_instructor = session.get("apellidos_instructor")
        correo_instructor = session.get("correo_instructor")

    else:
        print("El aprendiz no esta logueado")

    return render_template("/aprendiz/B_home_aprendiz.html",
                           
                               #Datos Aprendiz
                               NombreAprendiz = usuario_nombre, 
                               ApellidoAprendiz = usuario_apellido, 
                               CedulaAprendiz = usuario_id_cedula,
                               tipo_doc = usuario_tipo_documento,

                               FotoAprendiz = usuario_foto,

                               TelefonoAprendiz = user_telefono,
                               CorreoAprendiz = user_correo,
                               Municipio = user_municipio, 
                               dir = user_dir, 

                               Ficha = usuario_ficha,
                               curso = usuario_curso,
                               nivel = usuario_formacion,   
                               
                               #Datos Instructor
                               NombreInstructor = nombre_instructor,
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