""" from B_Conexion import *

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
programa = Flask(__name__)

programa.secret_key = 'clave_secreta'

doc_indentidad="1234567811"
clavecifrada="Pablo%123456"
# Cifrar contraseña
clavecifrada = hashlib.pbkdf2_hmac('sha256', clavecifrada.encode('utf-8'), b'saltsupersegura', 100000).hex()

sql = f"INSERT INTO usuario_aprendiz (`doc_indentidad`,`clave`) VALUES ('{doc_indentidad}','{clavecifrada}')"

conexion = mysql.connector.connect(user='root', password='', host='localhost', database='sepa')
            
cur = conexion.cursor()
cur.execute(sql)
conexion.commit()
cur.close()
conexion.close()

#Final del programa
if __name__ == '__main__':
    programa.run(debug = True) """