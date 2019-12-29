# Algoritmo usado no jupyter notebook, pode haver alguma diferença ao tenta-lo executar em outro lugar.

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# Acessar o mysql_db
from flask_mysqldb import MySQL
#Form validação
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# Encriptar passwd
from passlib.hash import sha256_crypt
from functools import wraps
#import mysql.connector


#init app
app = Flask(__name__)

# scret key
app.config['SECRET_KEY'] = "Un1qu0AndS3cr3t3"

# congif MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1996Jcss3'
app.config['MYSQL_DB'] = 'Raidhut'
# Retorna os dados na forma de dicionario ao inves das tuplas(default) quando acessarmos o db.
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

# Função para armazenar logs
def logs(acao,login,password,email):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute("INSERT INTO registros (log_acao,log_login,log_senha,log_email) VALUES(%s,%s,%s,%s)",(acao,login,password,email))
    # Commit to DB - Salva alterações
    mysql.connection.commit()
    # Close connection
    cur.close()    

# Metodos
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    login = StringField('Login',[validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    
# User Register - Metodo de Criação
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        #password = form.password.data
    
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Conta já existe?
        logins = cur.execute("select login from usuario where login = %s",[login])
        if logins > 0:
            flash('Login already exists!', 'success')
        else:
            # Criar Conta
            # Execute query
            cur.execute(f"INSERT INTO usuario (login, senha, email) VALUES(%s, %s, %s)",(login,password,email))
            # Commit to DB - Salva alterações
            mysql.connection.commit()
            # Close connection
            cur.close()

            flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

# Metodo para logar
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        #Informação colocada no form.
        login_candidate = request.form['login']
        password_candidate = request.form['password']
        
        # Informação do Mysql_db
        cur = mysql.connection.cursor()
        # Execute query
        result = cur.execute("select * from usuario where login= %s",[login_candidate])
        
        # Algum registro foi encontrado.
        if result > 0:
            # Informações do select acima - apena o primeiro registro(em caso de multiplos) do result
            data = cur.fetchone()            
            # senha do login selecionado
            # email = data['email']
            password = data['senha']
            # Comparar passwords
            if sha256_crypt.verify(password_candidate,password):
                # app.logger.info('PASSEWORD MATCHED')
                session['logged_in'] = True
                session['login'] = login_candidate
                session['password'] = data['senha']
                session['email'] = data['email']
                
                flash('You are now logged in','success')
                
                # Log de Conexão no Sistema.
                acao = "Usuário conectado no Sistema."
                logs(acao,login_candidate,data['senha'],data['email'])
                
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',error='Invalid Password')
            # Fechando conexão
            cur.close()
        else:
            return render_template('login.html',error="Invalid Login")
            
            
        # Commit to DB - Salva alterações
        mysql.connection.commit()
        # Close connection
        cur.close()
    
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            # log Entrada Forçada no sistema
            logs("Não autorizado","Não Indicado","Não Indicado","Não Indicado")
            
            return redirect(url_for('login'))
    return wrap

class UpdateForm(Form):
    login = StringField('New Login',[validators.Length(min=4, max=25)])
    email = StringField('New Email',[validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm New Password')

# User Update - Metodo de Atualização
@app.route('/update', methods=['GET', 'POST'])
@is_logged_in
def update():
    form = UpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        #password = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()
        
        # Execute query
        cur.execute("UPDATE USUARIO SET login=%s,email=%s,senha=%s WHERE login = %s",(login,email,password,session['login']))
        
        # Salva alterações
        mysql.connection.commit()
        
        # Close connection
        cur.close()

        flash('Updated successfully', 'success')

        return redirect(url_for('login'))
    
    return render_template('update.html', form=form)

# Form delete
class DeleteForm(Form):
    login = StringField('Login',[validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Delete - Metodo de Remoção
@app.route('/deletar', methods=['GET','DELETE'])
@is_logged_in
def delete():
    form = DeleteForm(request.form)
    print(request.method)
    if request.method == 'DELETE' and form.validate():
        
        login = form.login.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        if login == session['login'] and password == session['password']:
            
            # executar metodo de deletar
            
            # Create cursor
            cur = mysql.connection.cursor()            
            # Execute query
            cur.execute("DELETE FROM USUARIO WHERE login = %s",session['login'])
            
            #Salva Alterações
            mysql.connection.commit()
            # Close connection
            cur.close()

            flash('User deleted successfully.', 'success')

        return redirect(url_for('login'))
    
    print('Não entrou no IF !!')
    return render_template('delete.html', form=form)

# Historico
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Login
    login = session['login']
    
    #Create cursor
    cur = mysql.connection.cursor()
    # Execute query
    result = cur.execute("SELECT * FROM registros where log_login= %s order by log_hora_registro desc",[login])
    
    # Get all registros
    registros =  cur.fetchall()
    
    # Existir algum registro
    if result > 0:
        return render_template('dashboard.html',registros=registros)
    else:
        msg = 'No Historico FOUND'
        return render_template('dashboard.html',msg=msg)
    
    #Fechando conexão
    cur.close()

# Metodo para deslogar(logout)
@app.route('/logout')
@is_logged_in
def logout():
    login = session['login']
    password = session['password']
    email = session['email']
    session.clear()
    flash('You are now logged out','success')
    
    # Log de Desconexão do Sistema
    acao = "Usuário desconectou do sistema."
    logs(acao,login,password,email)
    
    return redirect(url_for('login'))

# Run Server
if __name__ =='__main__':
    app.run(debug=True,use_reloader=False)