from flask import Flask, render_template, request, redirect, url_for, session, flash
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
#----------------------------------------------------------------------------------------------
# -> 15/02/2024

@app.route('/edit_profile', methods=('GET','POST'))
def edit_profile():
    if request.method == 'POST':
        
        id_personal = session.get('id', None)
        nombre = request.form['name']
        email = request.form['email']
        telefono = request.form['phone']
        departamento = request.form['department']

        cur = mysql.connection.cursor()

        #actualización de la base de datos

        cur.execute('UPDATE cliente SET nombre = %s, correo_electronico = %s, telefono = %s, departamento = %s WHERE idCliente =%s',
                    (nombre, email, telefono, departamento, id_personal))
        
        #ejecutamos la sentencia de mysql

        mysql.connection.commit()
        cur.close()

        #Actualizamos los datos de la sesion de usuario 

        session['nombre_sh'] = nombre
        session['email'] = email
        session['telefono'] = telefono
        session['depto'] = departamento

        return redirect(url_for('panel_cliente'))
    
    else:

        id_personal = session.get('id', None)
        nombre = session.get('nombre_sh', None)
        ap_paterno = session.get('ap_pat', None)
        ap_materno = session.get('ap_mat', None)
        email = session.get('email', None)
        telefono = session.get('telefono', None)
        departamento = session.get('depto', None)
        datos = {
            'id': id_personal,
            'nombre': nombre,
            'ap_paterno': ap_paterno,
            'ap_materno': ap_materno,
            'email': email,
            'telefono': telefono,
            'departamento': departamento
        }

        return render_template('edit_profile.html', datos=datos)
#------------------------------------------------------------------------------------------------
@app.route('/pruebas')
def pruebas():
    print(url_for('pruebas'))
    return render_template('pruebas.html')

#-------------------------------------------------------------------------------------------------
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
            session['telefono'] = account[6]
            session['depto'] = account[7]

            print('valores de SESSION: ', session)
            return redirect(url_for('panel_cliente'))
        else:
            return render_template('login.html')
        abort(400)  
#-------------------------------------------------------------------------------
# -> Creación de la vista y la ruta para solicitudes de tickets

@app.route('/solicitar_ticket', methods = ['GET','POST'])
def solicitar_ticket():
    if request.method == 'POST':
        problemas = request.form['common_problems']
        descripcion = request.form['description']
        time = datetime.now().strftime('%Y-%m-%d')
        #obtengo el id de mi cliente
        id_cliente = session.get('id', None)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tickets (Problema, Descripcion_problema, fecha_expedicion, idCliente, status ) VALUES (%s, %s, %s, %s,%s)",
            (problemas, descripcion, time, id_cliente, 'abierto'))
            mysql.connection.commit()
            cur.close()
            flash('Los registros se han cargado satisfactoriamente', 'success')
            return redirect(url_for('panel_cliente'))
        
        except Exception as e:
            error_message = "Error al registrar el incidente" + str(e)
            flash('No se cargaron los registros ' + error_message, 'error')


    return render_template('solicitud_ticket.html')

@app.route('/ver_tickets')
def ver_tickets():
    #obtengo el id del cliente:
    id_cliente = session.get('id',None)
    print(f"Sesion del cliente es ->{id_cliente}")
    cur = mysql.connection.cursor()
    cur.execute("""
                    SELECT 
                        t.id_ticket,
                        c.nombre,
                        c.apellido_paterno,
                        c.departamento,
                        t.fecha_expedicion,
                        t.Problema,
                        t.Descripcion_problema,
                        t.status
                    FROM 
                        tickets t
                    JOIN 
                        cliente c ON t.idCliente = c.idCliente
                    WHERE
                        c.idCliente = %s
                        """,(id_cliente,))
    tickets = cur.fetchall()

    cur.close()

    print(f' esta es la info que se envia al fron {tickets}')
    

    return render_template('mis_tickets.html', tickets = tickets)

@app.route('/cancelar_ticket/<int:id_ticket>', methods=['POST'])
def cancelar_ticket(id_ticket):
    proceso = request.method
    print (f"el proceso es {proceso}")
    if request.method == 'POST':  
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tickets WHERE id_ticket = %s AND status = 'abierto'",
                    (id_ticket,))
        ticket = cur.fetchone()
        if ticket:
            # Actualizar el estado del ticket a 'cancelado'
            cur.execute("UPDATE tickets SET status = 'cancelado' WHERE id_ticket = %s", (id_ticket,))
            mysql.connection.commit()
            cur.close()
            flash('El ticket ha sido cancelado exitosamente', 'success')
        else:
            flash('No se pudo cancelar el ticket. Puede que ya esté cerrado o no exista.', 'error')
        return redirect(url_for('ver_tickets'))


if __name__ =='__main__':
    app.run(debug = True, )
