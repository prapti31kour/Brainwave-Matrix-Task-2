from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object('config.Config')

# Configure MySQL connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        if conn is None:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('index'))

        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO pompom (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred while signing up. Please try again.', 'danger')
        finally:
            cursor.close()
            conn.close()

        flash('You have successfully signed up!', 'success')
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn is None:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('index'))

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM pompom WHERE username = %s', (username,))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred while logging in. Please try again.', 'danger')
            return redirect(url_for('login'))
        finally:
            cursor.close()
            conn.close()

        if user and check_password_hash(user[3], password):
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

if __name__ == '__main__':
    app.run(debug=True)
