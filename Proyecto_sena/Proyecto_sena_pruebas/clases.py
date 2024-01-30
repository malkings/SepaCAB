class Pruebas:
    def __init__(self,miBaseDatos):
        self.mysql = miBaseDatos
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consulta(self):
        sql = "SELECT * FROM aprendiz WHERE id !=1 "
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        self.conexion.commit
        return Datos
    
    def consulta02(self):
        sql = "SELECT * FROM datos_empresa WHERE id !=1 "
        self.cursor.execute(sql)
        Datos = self.cursor.fetchall()
        self.conexion.commit
        return Datos