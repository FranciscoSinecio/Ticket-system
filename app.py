from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime

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

@app.route('/panel_cliente')
def panel_cliente():
    id_cliente = session.get('id', None)
    nombre = session.get('nombre_sh', None)
    ap_paterno = session.get('ap_pat', None)
    ap_materno = session.get('ap_mat', None)
    email = session.get('email', None)
    return render_template('panel_cliente.html', id_cliente=id_cliente, nombre=nombre, ap_paterno= ap_paterno, ap_materno = ap_materno)

@app.route('/admin_cliente')
def admin_cliente():
    id_personal = session.get('id', None)
    nombre = session.get('nombre_sh', None)
    ap_paterno = session.get('ap_pat', None)
    ap_materno = session.get('ap_mat', None)
    email = session.get('email', None)
    telefono = session.get('telefono', None)
    departamento = session.get('depto', None)

    datos = {
        'id' : id_personal,
        'nombre' : nombre,
        'ap_paterno' : ap_paterno,
        'ap_materno' : ap_materno,
        'email': email,
        'telefono' : telefono,
        'dpto' : departamento
    }

    return render_template(('admincliente.html'),datos = datos)

@app.route('/edit_profile', methods=('GET','POST'))
def edit_profile():
    if request.method == 'POST':
        id_personal =  session.get['id', None]
        nombre = request.form['name']
        email = request.form['email']
        telefono = request.form['phone']
        departamento = request.form['department']

        #Activamos el cursor para realizar los cambios en base de datos

        cur = mysql.connection.cursor()

        #Actualizo los datos de la base de datos

        cur.execute('UPDATE cliente SET nombre = %s, correo_electronico = %s, telefono = %s, departamento = %s WHERE idCliente=%s',
                    (nombre,email,telefono,departamento,id_personal))
        mysql.connection.commit()
        cur.close()

        #ACTUALIZAMOS LOS DATOS DE LA SESION DE USUARIO

        session['nombre_sh'] = nombre
        session['email'] = email
        session['telefono'] = telefono
        session['depto'] = departamento

        return redirect(url_for('panel_cliente'))
    
    else:

        id_personal = session.get('id', None)
        nombre = session.get('nombre_sh',None)
        email = session.get('email', None)
        telefono = session.get('telefono', None)
        departamento = session.get('depto', None)

        datos= {

            'id': id_personal,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'depto' : departamento
        }

        return redirect(url_for('panel_cliente'))
        



@app.route('/pruebas')
def pruebas():
    print(url_for('pruebas'))
    return render_template('pruebas.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password':
        usuario = request.form['username']
        clave = request.form['password']
        #activo cursor
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE correo_electronico = %s AND contrasena = %s', (usuario,clave,))
        account = cur.fetchone()
        print (account)
        
        

        if account:
            session['logueado']=True
            session['id']=account[0]
            session['nombre_sh']=account[1]
            session['ap_pat'] = account[2]
            session['ap_mat'] = account[3]
            session['email'] = account[4]
            session['telefono'] = account[7]
            session['depto'] = account[8]

            print('valores de SESSION: ', session)
            return redirect(url_for('panel_cliente'))
        else:
            return redirect(url_for('login'))
#-------------------------------------------------------------------------------
# -> Creación de la vista y la ruta para solicitudes de tickets


@app.route('/solicitar_ticket',methods = ['POST'])
def solicitar_ticket():
    if request.method == 'POST':
        incidente = request.form['common_problems']
        descripcion = request.form['description']
        fecha_exp = datetime.now().strftime('%Y-%m-%d')
#proces de registo en base de datos
        #activamos el cursor
        cur = mysql.conecction.cursor()

        #insertamos el ticket en la tabla tickets
        cur.execute('INSERT INTO tickets (Problema,Descripcion_problema,fecha_expedicion) VALUES (%s, %s, %s)',
                    (incidente, descripcion, fecha_exp))
        mysql.connection.commit() #ejecutamos la acción descrita 

        #obtnemos el id del estado solicitado

        cur.execute("SELECT id_status FROM status WHERE nombre_estado = 'Solicitado'")
        id_status_solicitado = cur.fetchone()
        if not id_status_solicitado:
            cur.execute("INSERT INTO status (nombre_estado) VALUES ('solicitado')")
            mysql.connection.comit()
            cur.execute("SELECT_LAST INSERT_ID () AS id_status")
            id_status_solicitado = cur.fetchone()
        else:
            id_status_solicitado = id_status_solicitado['id_status']

            #Actulalización de la tabla tickets

        #->cur.execute

    return render_template('solicitud_ticket.html')





if __name__ =='__main__':
    app.run(debug = True, )
