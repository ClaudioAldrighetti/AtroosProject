from flask import Flask, render_template, request, redirect, url_for

import dbToPy as dTP


app = Flask(__name__)

# User data
user = None
cart = []
total_cost = 0.0
order_id = None

# Error message displayed in main page
_err = ""


@app.route('/')
# MAIN PAGE
def main():
    try:
        global user, cart, total_cost, order_id, _err

        # Check if user is already logged in
        if user is None:
            # If not, it is necessary to retrieve its information
            with dTP.db_engine.connect() as db_connection:
                # Account information
                user = dTP.get_logged_in_user(db_connection)

                # Cart information
                cart = dTP.get_cart(db_connection, user.email)
                if not cart:
                    return render_template('error.html', error='Your cart is empty, can not proceed with checkout.')

                # Order information
                for article in cart:
                    if order_id is None:
                        order_id = article.order_id
                    total_cost += (float(article.price) * float(article.quantity))
                total_cost = round(total_cost, ndigits=2)

        # Render to main page
        return render_template('main.html', user=user, cart=cart, order_id=order_id, total_cost=total_cost, error=_err)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/remove_article/<int:article_id>', methods=['GET', 'POST'])
def remove_article(article_id):
    try:
        global cart, total_cost, order_id, user
        if request.method == 'GET' and user is not None:
            with dTP.db_engine.connect() as db_connection:
                # Connect to database and remove article record
                dTP.remove_article_from_orders(db_connection, order_id, article_id)

            for article in cart:
                if article.article_id == article_id:
                    # Recompute total cost of order
                    total_cost -= (float(article.price) * float(article.quantity))
                    total_cost = round(total_cost, ndigits=2)
                    # Remove article from list
                    cart.remove(article)
                    break

            if not cart:
                return render_template('error.html', error='Your cart is empty, can not proceed with checkout.')

        # Reload main page
        return redirect(url_for('main'))

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/update_quantity/<int:article_id>/<int:quantity>', methods=['GET', 'POST'])
def update_quantity(article_id, quantity):
    try:
        global order_id, user
        if request.method == 'GET' and user is not None:
            with dTP.db_engine.connect() as db_connection:
                dTP.update_order_article_quantity(db_connection, order_id, article_id, quantity)

        # Reload main page
        return redirect(url_for('main'))

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/complete_checkout', methods=['GET', 'POST'])
def complete_checkout():
    try:
        global user
        order_state = False
        if request.method == 'GET' and user is not None:
            with dTP.db_engine.connect() as db_connection:
                global order_id
                # Check if articles quantity is available
                av = dTP.check_availability(db_connection, order_id)

            global _err
            if av:
                _err = "Some articles of your cart aren't available"
                return redirect(url_for('main'))
            _err = ""

            with dTP.db_engine.connect() as db_connection:
                # Change order status in database to settled
                dTP.set_settled(db_connection, order_id)
                order_state = dTP.get_order_state(db_connection, order_id)

        # Final page
        return render_template('complete_checkout.html', order_state=order_state)

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
