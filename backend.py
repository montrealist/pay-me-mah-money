def render_response(kind, message):
    return '["{0}","{1}"]'.format(kind, message)


@application.route('/')
def index():
    return render_template('frontend.html', **{'pk': PUBLISHABLE_KEY})


@application.route('/create_and_charge_customer', methods=['POST'])
def create_and_charge_customer():
    token = request.form['token']
    email = request.form['email']
    amount_in_dollars = float(request.form['amount'])
    amount_in_cents = int(amount_in_dollars)

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
        return render_response("error", e)
    except Exception as e:
        return render_response("error", "backend error")

    return render_response("success", "You made a successful payment!")