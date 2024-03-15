from B_Conexion import *

class Aprendiz:
    def __init__(self, mybaseDatos, programa):
        self.baseDatos = mybaseDatos
        self.programa = programa
        self.conexion = self.baseDatos.connect()
        self.cursor = self.baseDatos.cursor()#cambien conexion por baseDatos, no acepta que conexion sea de tipo cursor

    def mostrar(self, cedula):
        sql = f"SELECT doc_identificacion, tipo_documento, nombres, apellidos, municipio, direccion, correo, telefono, foto_aprendiz FROM aprendices WHERE doc_identificacion = '{cedula}'"  
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos
    
    def contrato(self, cedula):
        sql = f"SELECT id_contrato, ficha, curso, nivel_formacion FROM contratos WHERE id_aprendiz = '{cedula}'"
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos

    def homeAprend(self, cedula, instructor):
        sql = f"SELECT  id_instructor, id_aprendiz FROM asignaciones WHERE id_aprendiz = '{cedula}'"
        self.cursor.execute(sql)
        Dato = self.cursor.fetchall()

        if Dato:
            sql = f"SELECT nombres, apellidos FROM datos_instructor WHERE id_instructor = '{instructor}'"
            self.cursor.execute(sql)
            Datos = self.cursor.fetchall()

            sql = f"SELECT * FROM usuario_instructor WHERE doc_indentidad='{instructor}'"
            self.cursor.execute(sql)
            Datos_ins = self.cursor.fetchall()
        
            return Dato, Datos, Datos_ins

        else: 
            return None, None, None
 
aprendices = Aprendiz(baseDatos, programa)    