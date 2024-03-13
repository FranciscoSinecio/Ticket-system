from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response,jsonify
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'yes'
# -> configuración de la base de datos

app.config['MYSQL_HOST'] = 'baqxkcrfus4cmly944re-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'urlmn58nbq1sptxe'
app.config['MYSQL_PASSWORD'] = '9dV6H0Su93qK6l4wr06u'
app.config['MYSQL_DB'] = 'baqxkcrfus4cmly944re'

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

        return render_template('admincliente.html', datos=datos)
#------------------------------------------------------------------------------------------------
@app.route('/pruebas')
def pruebas():
    print(url_for('pruebas'))
    return render_template('pruebas.html')

#-------------------------------------------------------------------------------------------------
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and request.form['password']:
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
            session['rol'] = account[7]
            #session['rol'] = account[8]

            print('valores de SESSION: ', session)
            if session['rol'] == 'jefe':
                
                return redirect(url_for('panel_jefe')) 
                
            else:
                
                return redirect(url_for('panel_cliente'))
        else:
            error_message = "Usuario o contraseña incorrectos"
            return  render_template('login.html', error_message = error_message)
    return render_template('login.html')

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
        print(id_cliente)
        print(problemas)
        print(descripcion)
        print(time)
        try:
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tickets (Problema, Descripcion_problema, fecha_expedicion, idCliente, status) VALUES (%s, %s, %s, %s, %s)",
            (problemas, descripcion, time, id_cliente, 'abierto'))

            mysql.connection.commit()
            cur.close()
            print("El registro se ha completado exitosamente")

        except Exception as e:
            error_message = "Error al registrar el incidente" + str(e)
            print (error_message)

    return render_template('solicitud_ticket.html')

@app.route('/ver_tickets')
def ver_tickets():
    # Obtener el ID del cliente
    id_cliente = session.get('id', None)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            t.id_ticket,
            c.nombre,
            c.apellido_paterno,
            d.nombre_departamento,
            t.fecha_expedicion,
            t.Problema,
            t.Descripcion_problema,
            t.status,
            t.Comentarios  
        FROM 
            tickets t
        JOIN 
            cliente c ON t.idCliente = c.idCliente
        JOIN
            departamentos d ON c.idDepartamento = d.idDepartamento
        WHERE
            c.idCliente = %s
        ORDER BY t.id_ticket DESC
    """, (id_cliente,))
    tickets = cur.fetchall()
    cur.close()
    print(f'info enviada al front end {tickets}')

    return render_template('mis_tickets.html', tickets=tickets)

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

@app.route('/panel_jefe')
def panel_jefe():
    id_personal = session.get('id',None)
    nombre = session.get('nombre_sh',None)
    paterno = session.get('ap_pat',None)
    materno = session.get('ap_mat', None)
    
    return render_template('panel_jefe.html',id_personal = id_personal, nombre=nombre, paterno = paterno, materno = materno)

@app.route('/consultaJefeTicket')
def consultaJefeTicket():
    #obtnemos todas la consulta de los tickects

    try:
        
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                t.id_ticket,
                c.nombre,
                c.apellido_paterno,
                d.nombre_departamento,
                t.fecha_expedicion,
                t.Problema,
                t.Descripcion_problema,
                t.status
            FROM 
                tickets t
            JOIN 
                cliente c ON t.idCliente = c.idCliente
            JOIN
                departamentos d ON c.idDepartamento = d.idDepartamento
            ORDER BY t.id_ticket DESC
        """)

        #obtnemos el resultado de la consulta

        tickets = cur.fetchall()

        cur.close()

        #realizamos la consulta para obtner a los auxiliares
        cur = mysql.connection.cursor()
        cur.execute("SELECT idCliente, nombre, apellido_paterno FROM cliente WHERE rol = 'auxiliar'")
        auxiliar = cur.fetchall()
        cur.close()
        print (f'Esto se envia al front de auxiliares {auxiliar}')


        return render_template('consultaticket_jefe.html',tickets = tickets, auxiliar = auxiliar )
    
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/reportes')
def reportes():
    
    return render_template('reportes_jefe.html')

@app.route('/eliminar_ticket/<int:ticket_id>', methods=['POST'])
def eliminar_ticket(ticket_id):
    if request.method == 'POST':
        try:
            # Conectar a la base de datos
            cur = mysql.connection.cursor()

            # Verificar si el ticket existe
            cur.execute("SELECT * FROM tickets WHERE id_ticket = %s", (ticket_id,))
            ticket = cur.fetchone()

            if ticket:
                # Eliminar el ticket de la base de datos
                cur.execute("DELETE FROM tickets WHERE id_ticket = %s", (ticket_id,))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message': 'El ticket ha sido eliminado exitosamente'}), 200
            else:
                return jsonify({'error': 'No se pudo eliminar el ticket. Puede que no exista.'}), 404
        except Exception as e:
            return jsonify({'error': f"Error al eliminar el ticket: {str(e)}"}), 500
    else:
        return jsonify({'error': 'Método no permitido'}), 405
    
from flask import jsonify

@app.route('/actualizar_ticket', methods=['POST'])
def actualizar_ticket():
    data = request.json

    # Obtenemos los datos del JSON
    ticket_id = data.get('ticketId')
    id_auxiliar = data.get('auxiliar')
    status = data.get('status')
    print(f'Estos son los datos obtenidos --->  ticket_id ->{ticket_id} ----> Id_auxiliar {id_auxiliar} ----> status {status}')

    #obtenidos los datos paso a llenar la base de datos
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tickets SET idAuxiliar =%s, status =%s WHERE id_ticket=%s", (id_auxiliar,status,ticket_id))
    mysql.connection.commit()
    cur.close()


    # Devolvemos el mensaje de actualizacion con Json
    response = {'message': 'Ticket actualizado exitosamente'}
    return jsonify(response), 200


    
@app.route('/comentarios', methods=['POST'])
def comentarios():
    if request.method == 'POST':
        data = request.get_json()
        comentarios = data['comentarios']
        id_ticket = data['id_ticket']

        try:
            # Conectar a la base de datos
            cur = mysql.connection.cursor()

            # Actualizar el campo de comentarios en la tabla tickets
            cur.execute("UPDATE tickets SET Comentarios = %s WHERE id_ticket = %s", (comentarios, id_ticket))
            mysql.connection.commit()
            cur.close()

            return 'Comentario enviado correctamente'

        except Exception as e:
            return f"Error al enviar el comentario: {str(e)}"

    else:
        return 'Método no permitido'


@app.route('/departamentos')
def departamentos():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM departamentos')
    departamentos = cur.fetchall()
    cur.close()
    print (departamentos)

    return render_template('admindepartamentos.html', departamentos = departamentos)


@app.route('/guardar_departamento', methods=['POST'])
def guardar_departamento():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data.get('descripcion','')
    
    print(f'nombre -> {nombre} --- descripcion -> {descripcion}')

    cur = mysql.connection.cursor()
    add_departamento = ("INSERT INTO departamentos"
                        "(nombre_departamento, descripcion)"
                        "VALUES (%s, %s)")
    cur.execute(add_departamento,(nombre, descripcion))
    mysql.connection.commit()
    cur.close()

@app.route('/actualizar_departamento', methods=['POST'])
def actualizar_departamento():
    data = request.get_json()
    id_departamento = data['idDepartamento']
    nombre = ['nombre']
    descripcion = data['descripcion']

    print(f'el id es ->{id_departamento}\n el nombre es ---> {nombre}\n la descripcion es ---> {descripcion}')
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE departamentos SET nombre_departamento = %s, descripcion = %s WHERE idDepartamento = %s", (nombre, descripcion, id_departamento))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Departamento actualizado exitosamente'}), 200


    return jsonify({'message': 'Departamento guardado exitosamente'}), 200
if __name__ =='__main__':
    app.run(debug = True, )
