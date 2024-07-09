from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurações do banco de dados
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'escola'
}

# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alunos WHERE login = %s AND senha = %s', (login, senha))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['nome'] = account[1]
            return redirect(url_for('profile'))
        else:
            return 'Login ou senha incorretos!'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        login = request.form['login']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO alunos (nome, login, senha) VALUES (%s, %s, %s)', (nome, login, senha))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT nome, disciplina_html_css, disciplina_bootstrap, disciplina_javascript, disciplina_nodejs, disciplina_reactjs, disciplina_mongodb, disciplina_mysql, disciplina_postgresql FROM alunos WHERE id = %s', (session['id'],))
        aluno = cursor.fetchone()
        cursor.close()
        conn.close()

        if aluno:
            return render_template('profile.html', aluno=aluno)
        else:
            return 'Aluno não encontrado!'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nome', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
