from B_Conexion import *

class Aprendiz:
    def __init__(self, mybaseDatos, programa):
        self.baseDatos = mybaseDatos
        self.programa = programa
        self.conexion = self.baseDatos.connect()
        self.cursor = self.baseDatos.cursor()#cambien conexion por baseDatos, no acepta que conexion sea de tipo cursor

    def mostrar(self, cedula):
        sql = f"SELECT doc_identificacion, tipo_documento, nombres, apellidos, municipio, direccion, telefono, foto_aprendiz FROM aprendices WHERE doc_identificacion = '{cedula}'"  
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos
    
    def contrato(self, cedula):
        sql = f"SELECT id_contrato, ficha, curso, nivel_formacion FROM contratos WHERE id_aprendiz = '{cedula}'"
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos

    def datInstructor(self, instructor):
        sql = f"SELECT datos_instructor.id_instructor, datos_instructor.nombres, datos_instructor.apellidos, usuario_instructor.correo FROM datos_instructor JOIN usuario_instructor ON datos_instructor.id_instructor = usuario_instructor.doc_indentidad WHERE id_instructor = '{instructor}'" 
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos
    
    def datBasico(self, cedula):
        sql = f"SELECT id_instructor, id_aprendiz FROM asignaciones WHERE id_aprendiz = '{cedula}'"
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        return Datos
    
    def actualizarAprend(self, cedula, telefono, correo):
        sql = f"UPDATE aprendices JOIN usuario_aprendiz ON aprendices.doc_identificacion = usuario_aprendiz.doc_indentidad SET aprendices.telefono = '{telefono}', usuario_aprendiz.correo = '{correo}' WHERE aprendices.doc_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        self.baseDatos.commit()
        return Datos

aprendices = Aprendiz(baseDatos, programa)    