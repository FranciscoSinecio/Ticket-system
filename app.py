from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'
# -> configuración de la base de datos

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flask_test'

mysql = MySQL(app)

#definimos una funcion para el manejo de tupla a diccionario
#----------------------------------------------------------------------------------------------------
def dict_factory(cursor,row):
    d ={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d
#----------------------------------------------------------------------------------------------------
@app.before_request
def configure_row_factory():
    mysql.connection.cursor().row_factory = dict_factory

#----------------------------------------------------------------------------------------------------   
# ->Vistas
#----------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('login.html')

#----------------------------------------------------------------------------------------------------
@app.route('/panelCliente')
def panelCliente():
    if 'logueado' in session and session['logueado']:
        #conecto a la base de datos para la consulta para la obtencion de la informacion del cliente 
        cur = mysql.connect.cursor()
        cur.execute('SELECT * FROM cliente WHERE nombre =%s',(session['id'],))
        user_info = cur.fetchone()
        cur.close()

        return render_template('panelcliente.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

#----------------------------------------------------------------------------------------------------

#-> Logica de acceso

#----------------------------------------------------------------------------------------------------
# Lógica de acceso
@app.route('/acces-login', methods=["POST"])
def login():
    if request.method == 'POST' and 'txtcorreo' in request.form and 'txtpassword' in request.form:
        _correo = request.form['txtcorreo']
        _password = request.form['txtpassword']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE correo_electronico = %s', (_correo,))
        account = cur.fetchone()
        cur.close()

        if account and account['contrasena'] == _password:
            session['logueado'] = True
            session['id'] = account['idCliente']
            print('Datos obtenidos en la session son :', session)
            #return redirect(url_for('panelCliente'))  # Redirigir al panel del cliente si la autenticación es exitosa
            return render_template('panelcliente.html')
        else:
            error = 'Credenciales incorrectas. Por favor, inténtelo de nuevo.'
            return render_template('login.html', error=error)  # Mostrar mensaje de error en el formulario de inicio de sesión
    else:
        return redirect(url_for('index'))  # Redirigir al inicio si no se envió una solicitud POST o faltan campos en el formulario

    
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
if __name__ =='__main__':
    app.run(debug = True, )
