from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación
usuarios = {
    'usuario1': 'clave1',
    'usuario2': 'clave2'
}

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['datUsuario']
    clave = request.form['datClave']

    if usuario in usuarios and usuarios[usuario] == clave:
        # Inicio de sesión exitoso
        return ("Inicio de sesión exitoso")
    else:
        # Inicio de sesión fallido
        return print('Inicio de Sesion fallida')

if __name__ == '__main__':
    app.run(debug=True)
