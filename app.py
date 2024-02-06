
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='' # base de datos proporcionada por Jesus pendiente

mysql=MySQL(app)

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

# Ruta para procesar el formulario de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    #creamos el cursor para trabajar
    cur = mysql.connection.cursor()

    #Creamos la consulta de la base de datos
    cur.execute("SELECT * FROM user WHERE username %s AND password =%s",(username, password))

    #Obtnenemos el usuario si existe

    user = cur.fetchone()
    cur.close()

    #comoprobamos el usuario

    if user == :
        return

# Ruta para la página principal después de iniciar sesión (ejemplo)
@app.route('/home')
def home():
    return '¡Bienvenido a la página principal!'

if __name__ == '__main__':
    app.run(debug=True)
