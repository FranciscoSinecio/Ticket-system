from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

# Ruta para procesar el formulario de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Aquí debes implementar la lógica de autenticación
    # Verifica las credenciales y redirige según el resultado
    if username == 'usuario' and password == 'contraseña':
        # Usuario autenticado, redirige a la página principal, por ejemplo
        return redirect(url_for('home'))
    else:
        # Credenciales incorrectas, vuelve a mostrar el formulario de inicio de sesión con un mensaje de error
        return render_template('login.html', error='Credenciales incorrectas')

# Ruta para la página principal después de iniciar sesión (ejemplo)
@app.route('/home')
def home():
    return '¡Bienvenido a la página principal!'

if __name__ == '__main__':
    app.run(debug=True)
