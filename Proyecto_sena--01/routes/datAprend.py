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
            session["user_correo"] = Datos[0][6]
            session["user_telefono"] = Datos[0][7] 
            session["user_foto"] = Datos[0][8] 

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

            return redirect('/home_aprendiz')
        else: 
            return redirect('/iniciar_sesion')        
    else: 
        return redirect('/iniciar_sesion')        

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
        
        #foto del aprendiz
        
        usuario_foto = session.get("user_foto")
        cedula = session.get("aprendiz_cedula")

        instructor = session.get("cedula_instructor")

        Dato, Datos, Datos_ins = aprendices.homeAprend(cedula, instructor)

        session["cedula_instructor"] = Dato[0][0]#guarda la cedula del instructor para hacer la validacion en la tabla de asignaciones
    
        nombre_instructor = Datos[0][0]
        apellido_instructor = Datos[0][1]
        correo_instructor = Datos_ins[0][2]
    
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
                               NombreInstructor = nombre_instructor,
                               ApellidosInstructor = apellido_instructor,
                               CorreoInstructor = correo_instructor) 

        #En este apartado logramos que se muestren los datos requeridos en el html
    else:

        return render_template('/loginsepa/loginsepa.html')