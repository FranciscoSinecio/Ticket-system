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
    return redirect(url_for('login'))

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
@app.route('/acces-login',methods=["GET","POST"])
def login():
    if request.method == 'POST'and 'txtcorreo'in request.form and 'txtpassword':
        _correo = request.form['txtcorreo']
        _password = request.form['txtpassword']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE correo_electronico =%s AND contrasena = %s', (_correo,_password,))
        account = cur.fetchone()
        cur.close()
        print (account)  # debe de borrarse una vez que haya conectado 

        if account:
            session['logueado'] = True
            session['id'] = account[0]
        return redirect(url_for('panelCliente'))
    else:
            return 'Hola'
    
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
if __name__ =='__main__':
    app.run(debug = True, )
