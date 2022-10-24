# Ecommerce project


from flask import Flask, render_template, url_for, request, redirect, session

import pymysql

# database connection
# parameters -> host='localhost', user='root', password='', database='EcommerceShop'

connection = pymysql.connect(host='localhost', user='root', password='', database='EcommerceShop')
print("Database connection successful")

# start
app = Flask(__name__)
app.secret_key = "IloveProgramming"


@app.route('/')
def products():
    if 'key' in session:

        cursor_phones = connection.cursor()
        sql_phones = 'SELECT * FROM products WHERE product_category = "phones" LIMIT 6'
        cursor_phones.execute(sql_phones)
        phones = cursor_phones.fetchall()

        cursor_electronic = connection.cursor()
        sql_electronic = 'SELECT * FROM products WHERE product_category = "electronic" LIMIT 6'
        cursor_electronic.execute(sql_electronic)
        electronics = cursor_electronic.fetchall()

        cursor_sneakers = connection.cursor()
        sql_sneakers = 'SELECT * FROM products WHERE product_category = "Sneakers" LIMIT 6'
        cursor_sneakers.execute(sql_sneakers)
        sneakers = cursor_sneakers.fetchall()

        return render_template('myproducts.html', phones=phones, electronics=electronics, sneakers=sneakers)
    else:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['pswd']

        cursor = connection.cursor()
        sql = 'SELECT * FROM users WHERE user_email =%s AND user_password =%s'
        cursor.execute(sql, (user_email, user_password))

        if cursor.rowcount == 0:
            return render_template('login_signup.html', error="Invalid Credentials, Try Again")
        elif cursor.rowcount == 1:
            row = cursor.fetchone()
            session['key'] = row[1]  # user_name
            session['email'] = row[2]  # user_email
            return redirect('/')
        else:
            return render_template('login_signup.html', error="Something wrong with credentials")
    else:
        return render_template('login_signup.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['txt']
        user_email = request.form['email']
        user_password = request.form['pswd']
        cursor = connection.cursor()
        sql = 'INSERT INTO users (user_name, user_email, user_password) VALUES (%s,%s,%s)'
        cursor.execute(sql, (user_name, user_email, user_password))
        connection.commit()
        return render_template('login_signup.html', message="Registered successfully")
    else:
        return render_template('login_signup.html')


@app.route('/logout')
def logout():
    if 'key' in session:
        session.clear()
        return redirect('/login')


@app.route('/single/<product_id>')
def single(product_id):
    if 'key' in session:
        cursor = connection.cursor()
        sql = 'SELECT * FROM products WHERE product_id=%s'
        cursor.execute(sql, product_id)
        row = cursor.fetchone()
        return render_template('single.html', item_data=row)
    else:
        return redirect('/login')


app.run(debug=True)
# end app

# jinja templating Engine in flask -> python code can be written in html files
# variables {{variable}}
# {% python statements%}, if conditions, for loops

# {% for item in mydata%}
# {% endfor %}

# sessions

# {% for item in mydata%}
# {% endfor %}

# sessions
# {% for item in mydata%}
# {% endfor %}

# sessions
