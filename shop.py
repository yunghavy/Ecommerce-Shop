# Ecommerce project


from flask import Flask, render_template, url_for

import pymysql


# database connection
# parameters -> host='localhost', user='root', password='', database='EcommerceShop'

connection = pymysql.connect(host='localhost', user='root', password='', database='EcommerceShop')
print("Database connection successful")

# start
app = Flask(__name__)


@app.route('/')
def products():
    cursor = connection.cursor()
    sql = 'SELECT * FROM products'
    cursor.execute(sql)

    data = cursor.fetchall()
    print(data)
    return render_template('products.html', mydata=data)


app.run(debug=True)
# end app

# jinja templating Engine in flask -> python code can be written in html files
# variables {{variable}}
# {% python statements%}, if conditions, for loops

# {% for item in mydata%}
# {% endfor %}
