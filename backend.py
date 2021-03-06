from flask import Flask, render_template, request
import stripe
from dotenv import load_dotenv
from os import environ 

load_dotenv('.env')

stripe.api_key = environ.get('SECRET_KEY')
stripe.publishable_key = environ.get('PUBLISHABLE_KEY')

application = Flask(__name__, template_folder='./templates')

def render_response(kind, message):
    return '["{0}","{1}"]'.format(kind, message)


@application.route('/')
def index():
    return render_template('frontend.html', **{'pk': stripe.publishable_key})


@application.route('/create_and_charge_customer', methods=['POST'])
def create_and_charge_customer():
    token = request.form['token']
    email = request.form['email']

    # amount_in_dollars = float(request.form['amount'])
    amount_in_dollars = 42
    amount_in_cents = int(amount_in_dollars) * 100
    
    try:
        customer = stripe.Customer.create(email=email, source=token)

        customer_id = customer['id']

        charge = stripe.Charge.create(
            amount=amount_in_cents,
            customer=customer_id,
            currency='aud'
        )
    except stripe.error.StripeError as e:
        #body = e.json_body

        print('error status is: %s' % e.http_status)
        print('error code is: %s' % e.code)
        print('error message is: %s' % e.user_message)

        return render_response("error", e.user_message)
    except Exception as e:
        return render_response("error", e)

    return render_response("success", "You made a successful payment!")