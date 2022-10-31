import random
import string
from multiprocessing import connection

from flask import session, request, app, flash, redirect


def random_string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


from order_gen import random_string_generator


# checkout route
def check_customer():
    pass


@app.route('/proceed_checkout', methods=['POST', 'GET'])
def proceed_checkout():
    if check_customer():
        if 'cart_item' in session:
            if request.method == 'POST':
                mpesa_code = request.form['mpesa_code']
                all_total_price = 0
                all_total_quantity = 0
                # Need to check database******************
                order_code = random_string_generator()
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    product_id = session['cart_item'][key]['product_id']
                    product_name = session['cart_item'][key]['product_name']
                    product_cost = session['cart_item'][key]['product_cost']

                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
                    print('Individual qqty', individual_quantity)
                    print('Individual price', individual_price)
                    print('product_id', product_id)
                    print('product name', product_name)
                    print('Total qtty', all_total_quantity)
                    print('Total price', all_total_price)
                    print("=================")
                    email = session['tel']
                    # session
                    if not email:
                        flash('Sorry, Error Occurred during checkout, Try Again', 'danger')
                        return redirect('/signin')
                    elif not individual_price or not individual_quantity or not product_id or not product_name or not all_total_price or not all_total_quantity:
                        flash('Sorry, Error Occurred during checkout, Try Again', 'danger')
                        return redirect('/cart')
                    else:
                        try:
                            sql = 'INSERT INTO `orders`(`product_name`, `product_qtty`, `product_cost`, `email`, ' \
                                  '`order_code`, `mpesa_confirmation`, `individual_total`, `all_total_price`) VALUES ' \
                                  '(%s,%s,%s,%s,%s,%s,%s,%s) '
                            cursor = connection.cursor()
                            cursor.execute(sql, (
                                product_name, individual_quantity, product_cost, email, order_code, mpesa_code,
                                individual_price, all_total_price))
                            connection.commit()

                        except Exception as e:
                            print(e)
                            flash('Sorry, Error occured during checkout, Please try again', 'danger')
                            return redirect('/cart')

                print('================')
                print('Total qtty', all_total_quantity)
                print('Total price', all_total_price)
                try:
                    sql2 = 'update orders set all_total_price = %s where order_code = %s'
                    cursor = con.cursor()
                    # it updates all the products to have the same price in the same order in the all total price column
                    cursor.execute(sql2, (all_total_price, order_code))
                    con.commit()
                    flash('Your Order is Complete, Please check your Orders in Your Profile', 'success')
                    session.pop('cart_item', None)
                    session.pop('all_total_quantity', None)
                    session.pop('all_total_price', None)
                    print('here')
                    return redirect(url_for('cart'))
                except:
                    flash('Sorry, Error occured during checkout, Please try again', 'danger')
                    session.pop('cart_item', None)
                    session.pop('all_total_quantity', None)
                    session.pop('all_total_price', None)
                    return redirect('/cart')
            else:
                return redirect('/cart')
        else:
            return redirect('/cart')
    else:
        flash('You must be logged in to Make a Purchase, Please Login', 'warning')
        return redirect('/signin')
