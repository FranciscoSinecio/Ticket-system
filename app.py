from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response,jsonify
from flask_mysqldb import MySQL
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas




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

    print(f'datos enviados son: {clientes}')

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
    rol = datos_usuario['rol']  # Obtener el valor del campo de rol

    print(f"""Datos enviados al back end para editar el usuario con ID {id_usuario} son:\n
        nombre----->{nombre}
        correo---->{correo}
        telefono--->{telefono}
        contrasena--->{contrasena}
        id_departamento---->{id_departamento}
        rol----->{rol}
        """)
    nombre_completo = nombre.split()
    nombre_pila = nombre_completo[0]
    apellido_pat = nombre_completo[1]
    apellido_mat = nombre_completo[2]

    numero = re.search(r'\b(\d+)\b', id_departamento).group(1)
    id_dpto = int(numero)
    print(f'numero -> {id_dpto}')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE cliente SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, correo_electronico = %s, telefono = %s, contrasena = %s, idDepartamento = %s, rol = %s WHERE id = %s",
                    (nombre_pila, apellido_pat, apellido_mat, correo, telefono, contrasena, id_dpto, rol, id_usuario))  # Agregar el campo de rol a la consulta SQL
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Usuario editado exitosamente"}), 200


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
    # Lógica para generar el contenido del PDF
    if reportType == "Tickets":
        # Aquí se genera el contenido del PDF de reporte de tickets
        generar_pdf_tickets()

        return generar_pdf_tickets()
    elif reportType == "Auxiliares":
        # Aquí se genera el contenido del PDF de reporte de auxiliares
        return generar_pdf_auxiliares()
    elif reportType == "Departamentos":
        # Aquí se genera el contenido del PDF de reporte de departamentos
        return generar_pdf_departamentos()
    else:
        return "Tipo de reporte no válido"

# Función para generar el PDF de reporte de tickets
def generar_pdf_tickets():
# Generar el contenido del PDF
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tickets")
    tickets = cur.fetchall()

    tabla_datos = [['ID', 'Problema', 'Descripcion', 'Fecha de expedicion', 'Fecha de termino', 
                    'Status', 'Id cliente', 'Id auxiliar', 'Comentarios']]
    
    for t in tickets:
        fila = [str(field) for field in t]
        tabla_datos.append([
            str(t[0]),
            t[1],
            t[2],
            str(t[3]),
            str(t[4]),
            t[5],
            str(t[6]),
            str(t[7]),
            t[8]
        ])
    
    # Obtener ancho de la página y definir ancho de columnas
    width, height = landscape(letter)
    column_widths = [width / len(tabla_datos[0])] * len(tabla_datos[0])

    # Crear tabla y aplicar estilos
    table = Table(tabla_datos, colWidths=column_widths)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('WORDWRAP', (0, 0), (-1, -1), True)]))

    # Construir el PDF y devolverlo como respuesta Flask
    doc.build([table])
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_tickets.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response

def generar_pdf_auxiliares():
    try:
        # Generar el contenido del PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))
        cur = mysql.connection.cursor()
        
        # Consultar los auxiliares ordenados por departamento
        cur.execute("""
            SELECT idCliente, nombre, apellido_paterno, apellido_materno, correo_electronico, telefono
            FROM cliente
            WHERE rol = 'auxiliar'
            ORDER BY idDepartamento
        """)
        auxiliares = cur.fetchall()

        tabla_datos = [['ID', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Correo Electrónico', 'Teléfono']]
        
        for a in auxiliares:
            fila = [str(field) for field in a]
            tabla_datos.append([
                str(a[0]),
                a[1],
                a[2],
                a[3],
                a[4],
                a[5]
            ])
        
        # Obtener ancho de la página y definir ancho de columnas
        width, height = landscape(letter)
        column_widths = [width / len(tabla_datos[0])] * len(tabla_datos[0])

        # Crear tabla y aplicar estilos
        table = Table(tabla_datos, colWidths=column_widths)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                    ('WORDWRAP', (0, 0), (-1, -1), True)]))

        # Construir el PDF y devolverlo como respuesta Flask
        doc.build([table])
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_auxiliares.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        return response

    except Exception as e:
        return f"Error al generar el PDF de auxiliares: {str(e)}"

def generar_pdf_departamentos():
    try:
        # Generar el contenido del PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))
        cur = mysql.connection.cursor()
        
        # Consultar los tickets ordenados por departamento
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
            ORDER BY d.nombre_departamento, t.id_ticket DESC
        """)
        tickets = cur.fetchall()

        tabla_datos = [['ID Ticket', 'Nombre', 'Apellido', 'Departamento', 'Fecha de expedicion', 
                        'Problema', 'Descripcion', 'Status', 'Comentarios']]
        
        for t in tickets:
            fila = [str(field) for field in t]
            tabla_datos.append([
                str(t[0]),
                t[1],
                t[2],
                t[3],
                str(t[4]),
                t[5],
                t[6],
                t[7],
                t[8]
            ])
        
        # Obtener ancho de la página y definir ancho de columnas
        width, height = landscape(letter)
        column_widths = [width / len(tabla_datos[0])] * len(tabla_datos[0])

        # Crear tabla y aplicar estilos
        table = Table(tabla_datos, colWidths=column_widths)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                    ('WORDWRAP', (0, 0), (-1, -1), True)]))

        # Construir el PDF y devolverlo como respuesta Flask
        doc.build([table])
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_tickets_departamentos.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        return response

    except Exception as e:
        return f"Error al generar el PDF: {str(e)}"


if __name__ =='__main__':
    app.run(debug = True, )
