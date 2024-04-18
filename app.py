from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response,jsonify,send_file
from jinja2 import Environment, FileSystemLoader
from flask_mysqldb import MySQL
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
import os 
import pdfkit


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

@app.route('/',methods=['POST'])
def logout():
    return redirect(url_for('index'))

@app.route('/panel_cliente')
def panel_cliente():
    id_cliente = session.get('id', None)
    nombre = session.get('nombre_sh', None)
    ap_paterno = session.get('ap_pat', None)
    ap_materno = session.get('ap_mat', None)
    email = session.get('email', None)

    user_photo = obtener_ruta_foto(id_cliente)

    return render_template('panel_cliente.html', id_cliente=id_cliente, nombre=nombre, ap_paterno= ap_paterno, ap_materno = ap_materno, user_photo=user_photo)

# Funcion para la obtencion de la foto
def obtener_ruta_foto(idCliente):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT foto FROM cliente WHERE idCliente = %s",(idCliente,))
    user_photo = cursor.fetchone()
    cursor.close()

    if user_photo and user_photo[0]:
        return str(idCliente) + '.png'
    else:
        return 'default_profile.png'
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
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
@app.route('/admin_jefe')
def admin_jefe():
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

    return render_template(('adminjefe.html'),datos = datos)

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
    
@app.route('/edit_profile_jefe', methods=('GET','POST'))
def edit_profile_jefe():
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

        return render_template('adminjefe.html', datos=datos)


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
            
            elif session['rol'] == 'auxiliar':

                return redirect(url_for('auxiliar'))
                
            else:
                
                return redirect(url_for('panel_cliente'))
        else:
            error_message = "Usuario o contraseña incorrectos"
            return  render_template('login.html', error_message = error_message)
    return render_template('login.html')

#-------------------------------Cambio de password ------------------------------------------------------------------

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'id' in session:
        user_id = session['id']
        clave_actual = request.json.get('passwordActual')
        clave_nueva = request.json.get('passwordNuevo')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE idCliente = %s', (user_id,))
        user = cur.fetchone()
        print(user)

        if isinstance(user, tuple) and user[5] == clave_actual:  # Accede a los elementos de la tupla por índice
            cur.execute('UPDATE cliente SET contrasena = %s WHERE idCliente = %s', (clave_nueva, user_id))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'La contraseña se ha actualizado satisfactoriamente'}), 200
        else:
            return jsonify({'error': 'La contraseña actual es incorrecta'}), 400
    else:
        return jsonify({'error': 'Usuario no autenticado'}), 401


#-------------------------------------------------------------------------------
# -------------------------------------------Actualizacion del perfil -------------------------------------------------------
@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if request.method == 'POST':
        idCliente = session['id']
        telefono = session['telefono']

        if not idCliente:
            return jsonify({'error': 'ID del cliente no porporcionado'}), 400
        
        #Actualizamos el telefono de la persona en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cliente SET telefono = %s WHERE idCliente = %s",(telefono,idCliente))
        mysql.connection.commit()
        cur.close()

    #-> Actualización de la fotografia <-
        
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = os.path.join('static/photos_profile/', str(idCliente) + '.png')
            photo.save(filename)

            #Actualizamos la foto en la base de datos
            cur = mysql.connection.cursor()
            cur.execute("UPDATE cliente SET foto = %s WHERE idCliente = %s", (filename, idCliente))
            mysql.connection.commit() 
            cur.close()
    
    return jsonify({'message': 'Perfil actualizado con éxito'}), 200




# -------------------------------------------Fin de la actuzlizacion de perfil-----------------------------------------------

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
            t.comentarios_cliente  
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

    user_photo = obtener_ruta_foto(id_personal)
    
    return render_template('panel_jefe.html',id_personal = id_personal, nombre=nombre, paterno = paterno, materno = materno, user_photo=user_photo)

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
    try:
        data = request.json
        id_ticket = data['id_ticket']
        tipoUsuario = data['tipoUsuario']
        comentarios = data['comentarios']

        print(f'la info enviada desde front es ---> {id_ticket} ----> {tipoUsuario}  -----> {comentarios}')

        if tipoUsuario == 'cliente':
            cur = mysql.connection.cursor()
            cur.execute("""
                        UPDATE tickets
                        SET comentarios_cliente = %s
                        WHERE id_ticket = %s""",
                        (comentarios,id_ticket))
            mysql.connection.commit()
            cur.close()
        elif tipoUsuario == 'auxiliar':
            cur = mysql.connection.cursor()
            cur.execute("""
                        UPDATE tickets
                        SET comentarios_auxiliar = %s
                        WHERE id_ticket = %s""",
                        (comentarios,id_ticket))
            mysql.connection.commit()
            cur.close()

        return jsonify({"message": "Comentarios guardados correctamente"}, 200)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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

    return jsonify({'message':'Departamento guradado exitosamente'}), 200


@app.route('/actualizar_departamento', methods=['POST'])
def actualizar_departamento():
    data = request.get_json()
    id_departamento = data['idDepartamento']
    nombre = data['nombre']  # Fetching the value of 'nombre' from JSON data
    descripcion = data['descripcion']

    print(f'el id es ->{id_departamento}\n el nombre es ---> {nombre}\n la descripcion es ---> {descripcion}')
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE departamentos SET nombre_departamento = %s, descripcion = %s WHERE idDepartamento = %s", (nombre, descripcion, id_departamento))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Departamento actualizado exitosamente'}), 200


@app.route('/verificar_clientes/<int:idDepartamento>', methods=['GET'])
def verificar_clientes(idDepartamento):


    try:
        #Creamos un cursor para ejecutar las consultas
        cursor = mysql.connection.cursor()

        #consulta de MySQL para contar el numero de lientes relacionados con el departamento 
        cursor.execute("SELECT COUNT(*) FROM cliente WHERE idDepartamento = %s", (idDepartamento,))
        result = cursor.fetchone()

        if result is not None:
            num_clientes = result[0]
        else:
            num_clientes = 0

        #cerramos el cursor
        cursor.close()

        #Mandamos un Json para indicar si existe clientes relacionados o no
        return jsonify({'clientes_relacionados': num_clientes > 0}), 200
    
    except Exception as e:
        return jsonify({'success': False, 
                        'error': str(e)}), 500


@app.route('/eliminar_departamento/<int:id_departamento>', methods=['DELETE'])
def eliminar_departamento(id_departamento):
    try:
        # Creamos un cursor para ejecutar las consultas
        cursor = mysql.connection.cursor()

        # Verificamos si existen clientes relacionados con el departamento
        cursor.execute("SELECT COUNT(*) FROM cliente WHERE idDepartamento = %s", (id_departamento,))
        num_clientes = cursor.fetchone()[0]

        if num_clientes > 0:
            return jsonify({'success': False, 'message': 'Existen clientes relacionados con este departamento.'}), 400
        else:
            # Si no hay clientes relacionados al departamento procedemos a borrar
            cursor.execute("DELETE FROM departamentos WHERE idDepartamento = %s", (id_departamento,))
            mysql.connection.commit()

            # Devolvemos el JSON con éxito
            return jsonify({'success': True}), 200

    except Exception as e:
        # En el caso de error, revertimos la transacción y devolvemos un mensaje de error
        mysql.connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/gestion_usuarios')
def gestion_usuarios():

    
    #Paso1-> crear un cursor para efectuar la consulta
    cur = mysql.connection.cursor()
    #Paso2 -> ejecutar la consulta de todos las personas en la tabla clientes
    cur.execute("""
            SELECT 
                c.idCliente, 
                c.nombre,
                c.apellido_paterno,
                c.apellido_materno,
                c.correo_electronico,
                c.telefono,
                c.rol,
                c.contrasena,
                d.nombre_departamento
            FROM 
                cliente c
            JOIN
                departamentos d ON c.idDepartamento = d.idDepartamento
            ORDER BY
                d.nombre_departamento
            """)
    #paso3 -> Guardamos todos los datos obtenidos en una variable
    clientes = cur.fetchall()
    #paso4 -> Cierro la consulta 
    cur.close()

    #print(f'datos enviados son: {clientes}')

    cur = mysql.connection.cursor()
    cur.execute("SELECT idDepartamento , nombre_departamento from departamentos")
    depart = cur.fetchall()
    cur.close()

    return render_template('gestion_usuarios.html',clientes = clientes, depart = depart)

# Ruta para registrar un nuevo usuario
@app.route('/registrar_usuario', methods = ['POST'])
def registrar_usuario():
    import re
    datos_usuario = request.json
    nombre = datos_usuario['nombre']
    correo = datos_usuario['correo']
    telefono = datos_usuario['telefono']
    contrasena = datos_usuario['contrasena']
    id_departamento = datos_usuario['id_departamento']
    rol = datos_usuario['rol']

    print(f"""Datos enviados al back end son:\n
        nombre----->{nombre}
        correo---->{correo}
        telefono--->{telefono}
        contrasena--->{contrasena}
        id_departamento---->{id_departamento}
        rol-----> {rol}
        """)
    nombre_completo = nombre.split()
    nombre_pila = nombre_completo[0]
    apellido_pat = nombre_completo[1]
    apellido_mat = nombre_completo[2]

    numero = re.search(r'\b(\d+)\b', id_departamento).group(1)
    id_dpto = int(numero)
    print(f'numero -> {id_dpto}')
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO cliente (nombre, apellido_paterno, apellido_materno, correo_electronico, telefono, contrasena, idDepartamento, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nombre_pila, apellido_pat, apellido_mat, correo, telefono, contrasena, id_dpto, rol))
    mysql.connection.commit()
    cursor.close()
        
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/editar_usuario/<int:id_usuario>', methods=['PUT'])
def editar_usuario(id_usuario):
    import re
    datos_usuario = request.json
    nombre = datos_usuario['nombre']
    correo = datos_usuario['correo']
    telefono = datos_usuario['telefono']
    contrasena = datos_usuario['contrasena']
    id_departamento = datos_usuario['id_departamento']
    rol = datos_usuario['rol']

    print(f"""Datos enviados al back end para editar el usuario con ID {id_usuario} son:\n
        nombre----->{nombre}
        correo---->{correo}
        telefono--->{telefono}
        contrasena--->{contrasena}
        id_departamento---->{id_departamento}
        rol-----> {rol}
        """)

    nombre_completo = nombre.split()
    nombre_pila = nombre_completo[0] if len(nombre_completo) > 0 else ''
    apellido_pat = nombre_completo[1] if len(nombre_completo) > 1 else ''
    apellido_mat = nombre_completo[2] if len(nombre_completo) > 2 else ''

    numero = re.search(r'\b(\d+)\b', id_departamento).group(1)
    id_dpto = int(numero)
    #print(f'numero -> {id_dpto}')
    
    cursor = mysql.connection.cursor()
    cursor.execute("""
                    UPDATE cliente
                    SET 
                        nombre = %s,
                        apellido_paterno = %s,
                        apellido_materno = %s,
                        telefono = %s,
                        contrasena = %s,
                        idDepartamento = %s,
                        rol = %s
                    WHERE idCliente = %s""",(nombre_pila, apellido_pat, apellido_mat, telefono, contrasena, id_dpto, rol, id_usuario))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Usuario editado exitosamente"}), 200

@app.route('/obtener_usuario/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        
        if usuario:
            usuario_dict = {
                "id": usuario[0],
                "nombre": usuario[1],
                "apellido_paterno": usuario[2],
                "apellido_materno": usuario[3],
                "correo_electronico": usuario[4],
                "telefono": usuario[5],
                "contrasena": usuario[6],
                "idDepartamento": usuario[7],
                "rol": usuario[8]
            }
            return jsonify(usuario_dict), 200
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404

    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return jsonify({"message": "Error al obtener usuario"}), 500


@app.route('/eliminar_usuario/<int:idUsuario>', methods=['DELETE'])
def eliminar_usuario(idUsuario):
    try:
        # Conectar a la base de datos
        cur = mysql.connection.cursor()

        # Eliminar registros relacionados en la tabla 'tickets'
        cur.execute("DELETE FROM tickets WHERE idCliente = %s", (idUsuario,))
        mysql.connection.commit()

        # Eliminar el usuario de la tabla 'cliente'
        cur.execute("DELETE FROM cliente WHERE idCliente = %s", (idUsuario,))
        mysql.connection.commit()

        cur.close()

        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': f"Error al eliminar el usuario: {str(e)}"}), 500
    
# Ruta para generar el PDF
@app.route('/generar_pdf/<reportType>')
def generar_pdf(reportType):

    report_type_valor = reportType

    #print(f"El valor impreso de report type es ---> {report_type_valor}")
    # Lógica para generar el contenido del PDF
    if reportType == "Tickets":
        # Aquí se genera el contenido del PDF de reporte de tickets
        pdf_path = generar_pdf_tickets()
        
    
    elif reportType == "Auxiliares":
        # Aquí se genera el contenido del PDF de reporte de auxiliares
        pdf_path = generar_pdf_auxiliar()
    
    elif reportType == "Departamentos":
        # Aquí se genera el contenido del PDF de reporte de departamentos
        pdf_path = generar_pdf_dptos()

    elif reportType == "Fechas":
        fecha_inio = request.args.get('start')
        fecha_fin = request.args.get('end')
        direccion_pdf = generar_pdf_fechas(fechas_inicio, fechas_fin)
    else:
        return jsonify({"error": "Tipo de reporte no valido"}), 400
    
    return jsonify({"filePath": pdf_path}), 200
    
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& FUnciones para hacer los pdf's&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&    
# Función para generar el PDF de reporte de tickets
def generar_pdf_tickets():

    #carpetas para la generacion de pdf
    path_to_wkhtmltopdf =  r"C:\Program Files\wkhtmltopdf\bin"
    path_to_executable = os.path.join(path_to_wkhtmltopdf, "wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=path_to_executable)

    
    amb = Environment(loader=FileSystemLoader("templates"))
    #obtenemos la plantilla a utilizar
    template = amb.get_template("template1_topdf.html")
    #Obtenemos los datos de la base de datps
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT
                    t.id_ticket,
                    t.Problema,
                    t.Descripcion_problema,
                    t.fecha_expedicion,
                    t.fecha_termino,
                    t.status,
                    COALESCE(c.nombre, 'N/A') AS nombre_cliente,
                    COALESCE(a.nombre, 'N/A') AS nombre_auxiliar
                FROM 
                    tickets t
                LEFT JOIN 
                    cliente c ON t.idCliente = c.idCliente AND c.rol = 'cliente'
                LEFT JOIN 
                    cliente a ON t.idAuxiliar = a.idCliente AND a.rol = 'auxiliar'
                """)
    # Obtenemos los datos de la consulta
    data = cur.fetchall()
    cur.close()
    #obtenemos la fecha actual
    fecha_now = datetime.now().date()
    fecha_formato = fecha_now.strftime("%Y-%m-%d")
    #print(fecha_formato)
    #print (data) #Borrar cuando veas que te ha enviado
    html = render_template('template1_topdf.html', data = data, fecha_formato=fecha_formato)
    #print (html)
    pdfkit.from_string(html,'Reporte_tickets.pdf', configuration = config)
    
    pdf_path = os.path.join(os.getcwd(), 'Reporte_tickets.pdf')
    
    return pdf_path

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
def generar_pdf_auxiliar():
    path_to_wkhtmltopdf =  r"C:\Program Files\wkhtmltopdf\bin"
    path_to_executable = os.path.join(path_to_wkhtmltopdf, "wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=path_to_executable)

    amb = Environment(loader=FileSystemLoader("templates"))
    template = amb.get_template("reporte_jefe_aux.html")

    cur = mysql.connection.cursor()
    consulta = """SELECT
                    c.nombre,
                    c.apellido_paterno,
                    t.id_ticket,
                    t.Problema,
                    t.Descripcion_problema,
                    t.fecha_expedicion,
                    t.status,
                    t.comentarios_auxiliar
                FROM
                    cliente c
                JOIN
                    `tickets` t ON c.idCliente = t.idAuxiliar
                WHERE
                    c.rol = 'auxiliar'
                    """
    cur.execute(consulta)

    auxiliar_tickets = cur.fetchall()
    cur.close()

    auxiliares = {}
    for ticket in auxiliar_tickets:
        nombre_auxiliar = f"{ticket[0]} {ticket[1]}"  # Acceder a los elementos por índice numérico
        if nombre_auxiliar not in auxiliares:
            auxiliares[nombre_auxiliar] = {
                'tickets': []
            }
        
        auxiliares[nombre_auxiliar]['tickets'].append({
            'id_ticket': ticket[2],
            'Problema': ticket[3],
            'Descripcion_problema': ticket[4],
            'fecha_expedicion': ticket[5].strftime('%Y-%m-%d'),
            'status': ticket[6],
            'comentarios_auxiliar': ticket[7]
        })

    fecha_hoy = datetime.now().date()
    fecha_formato = fecha_hoy.strftime('%Y-%m-%d')
    nombre_jefe = {
        'jefe_nombre': session.get('nombre_sh', None),
        'jefe_apellido': session.get('ap_pat', None)
    }

    html = render_template('reporte_jefe_aux.html',
                            fecha_formato=fecha_formato,
                            nombre_jefe=nombre_jefe,
                            auxiliares=auxiliares)
    
    pdfkit.from_string(html, 'Reporte_auxiliares_jefe.pdf', configuration=config)
    
    pdf_path = os.path.join(os.getcwd(), 'Reporte_auxiliares_jefe.pdf')

    return pdf_path

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def generar_pdf_dptos():
    
    path_to_wkhtmltopdf =  r"C:\Program Files\wkhtmltopdf\bin"
    path_to_executable = os.path.join(path_to_wkhtmltopdf, "wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=path_to_executable)
    amb = Environment(loader=FileSystemLoader("templates"))
    template = amb.get_template("reporte_jefe_x_dpto.html")

    #activo el cursor para realizar las consultas

    cur = mysql.connection.cursor()
    consult = """
                    SELECT
                            c.IdCliente,
                            c.nombre,
                            c.apellido_paterno,
                            c.apellido_materno,
                            c.correo_electronico,
                            c.telefono, 
                            d.nombre_departamento
                    FROM
                            cliente c
                    JOIN
                            departamentos d ON c.idDepartamento = d.idDepartamento
                    WHERE
                            c.rol = 'cliente'
                            """
    cur.execute(consult)
    departamentos_data = cur.fetchall()
    cur.close()
    #print(f'esta es la info de la base de datos obtenida---->{departamentos_data}')
    departamentos= {}

    for cliente in departamentos_data:
        nombre_departamento = cliente[6]
        if nombre_departamento not in departamentos:
            departamentos[nombre_departamento]={
                'clientes':[]
            }
        departamentos[nombre_departamento]['clientes'].append({
            
            'idCliente':cliente[0],
            'nombre':cliente[1],
            'apellido_paterno':cliente[2],
            'apellido_materno':cliente[3],
            'correo_electronico':cliente[4],
            'telefono':cliente[5]

        })
    fecha_hoy = datetime.now().date()
    fecha_formato = fecha_hoy.strftime('%Y-%m-%d')
    nombre_jefe={
        
        'jefe_nombre':session.get('nombre_sh',None),
        'jefe_apellido':session.get('ap_pat',None)
        
    }

    html = render_template('reporte_jefe_x_dpto.html',
                            fecha_formato = fecha_formato,
                            nombre_jefe = nombre_jefe,
                            departamentos = departamentos)
    pdfkit.from_string(html,'Reporte_dptos_jefe.pdf',configuration=config)
    
    pdf_path = os.path.join(os.getcwd(),'Reporte_dptos_jefe.pdf')
    
    return pdf_path

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def generar_pdf_fechas(fecha_inicio, fecha_fin):

    path_to_wkhtmltopdf =  r"C:\Program Files\wkhtmltopdf\bin"
    path_to_executable = os.path.join(path_to_wkhtmltopdf, "wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=path_to_executable)

    amb = Environment(loader=FileSystemLoader("templates"))
    template = amb.get_template("template_fechas.html")

    cur = mysql.connection.cursor()
    consulta = """
                    SELECT
                    t.id_ticket,
                    t.Problema,
                    t.Descripcion_problema,
                    t.fecha_expedicion,
                    t.fecha_termino,
                    t.status,
                    COALESCE(c.nombre, 'N/A') AS nombre_cliente,
                    COALESCE(a.nombre, 'N/A') AS nombre_auxiliar
                FROM 
                    tickets t
                LEFT JOIN 
                    cliente c ON t.idCliente = c.idCliente AND c.rol = 'cliente'
                LEFT JOIN 
                    cliente a ON t.idAuxiliar = a.idCliente AND a.rol = 'auxiliar'
                WHERE
                    t.fecha_expedicion BETWEEN %s AND %s
                """
    cur.execute(consulta, (fecha_inicio, fecha_fin))
    data = cur.fetchall()
    cur.close
    
    fecha_formato = datetime.now().strftime('%Y-%m-%d')
    
    html = render_template('template_fechas.html', data=data, fecha_formato = fecha_formato)

    pdfkit.from_string(html,'Reporte_fechas.pdf',configuration = config)
    pdf_path = os.path.join(os.getcwd(),'Reporte_fechas.pdf')

    return pdf_path
    

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# -----------------------------------------------------------------------Visstas y urls para auxiliares -------------------------------------------------------------------------------------------------//
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//

@app.route('/auxiliar')
def auxiliar():
    id_personal = session.get('id',None)

    if id_personal == None:

        return jsonify({"error": "No se proporciono el ID del personal"}),400
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE idCliente=%s',(id_personal,))
    auxiliar = cur.fetchone()
    
    if auxiliar is None:
        return jsonify({"error":"No se encontró el auxiliar en la base de datos con el ID proporcionado"})
    
    auxiliar_data ={
        'id': auxiliar[0],
        'nombre':auxiliar[1],
        'paterno': auxiliar[2],
        'materno': auxiliar[3],
        'mail': auxiliar[4],
        'tel': auxiliar[6],
        'rol':auxiliar[7],
        'dpto':auxiliar[8],
    }

    return render_template('panel_auxiliar.html',datos = auxiliar_data, id_personal=id_personal)

@app.route('/consultar_tickets')
def consultar_tickets():
    id_cliente = session.get('id', None)
    query = """
        SELECT 
            t.id_ticket,
            c.nombre AS nombre_cliente,
            c.apellido_paterno AS apellido_paterno_cliente,
            d.nombre_departamento,
            t.fecha_expedicion,
            t.Problema,
            t.Descripcion_problema,
            t.status,
            t.comentarios_auxiliar 
        FROM 
            tickets t
        JOIN 
            cliente c ON t.idCliente = c.idCliente
        JOIN
            departamentos d ON c.idDepartamento = d.idDepartamento
        WHERE
            t.idAuxiliar = %s
        ORDER BY t.id_ticket DESC;
    """
    cur = mysql.connection.cursor()
    cur.execute(query, (id_cliente,))
    tickets = cur.fetchall()
    cur.close()
    print(f'info enviada al front end {tickets}')
    return render_template('tickets_auxiliar.html', tickets=tickets)

if __name__ =='__main__':
    app.run(debug = True )
