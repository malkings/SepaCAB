from A_Imports import *
#---------------------------------------------------

#B_Conexion contiene la conexion a la base de datos

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

#La siguiente funcion sirve para comprobar
#la conexion con la base de datos de manera exitosa