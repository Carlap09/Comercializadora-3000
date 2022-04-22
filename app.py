from flask import Flask
from flask import render_template,request,redirect,url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key="Develoteca"

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='8339596Koc.'
app.config['MYSQL_DATABASE_DB']='ganga3000'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
   return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/')
def index():

    sql ="SELECT * FROM `articulos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    articulos=cursor.fetchall()
    print(articulos)

    conn.commit()
    return render_template('articulos/index.html', articulos=articulos)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT foto FROM articulos WHERE id=%s", id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

    cursor.execute("DELETE FROM articulos WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM articulos WHERE id=%s",(id))
    articulos=cursor.fetchall()
    conn.commit()
    
    return render_template('articulos/edit.html',articulos=articulos)

@app.route('/update', methods=['POST'])     
def  update():

    _nombre=request.form['txtNombre']  
    _precio=request.form['txtPrecio']  
    _foto=request.files['txtFoto']     
    id=request.form['txtId']

    sql="UPDATE  `ganga3000` .`articulos` SET  `nombre`=%s,`precio`=%s WHERE id=%s;"

    datos=(_nombre,_precio,id)  

    conn= mysql.connect()
    cursor=conn.cursor()

    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':

        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM articulos WHERE id=%s", id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE articulos SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()


    cursor.execute(sql,datos)

    conn.commit()

    return redirect('/')
   
@app.route('/create')
def create():
   return render_template('articulos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _precio=request.form['txtPrecio']
    _foto=request.files['txtFoto']

    if _nombre=='' or _precio =='' or _foto=='':
        flash('Recuerda llenar los datos de  los campos')
        return redirect(url_for('create'))


    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
  
    sql ="INSERT INTO `ganga3000`.`articulos` (`Nombre`, `Precio`, `Foto`) VALUES (%s, %s, %s);"

    datos=(_nombre,_precio,nuevoNombreFoto)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)
