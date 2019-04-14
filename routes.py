from src.forms import BookingForm
from src.booking import Booking
from src.customer import Customer
from src.location import Location
from flask import render_template, request, redirect, url_for, abort
from server import app, system
from datetime import datetime
from src.location import Location
# from src.error import BookingError, LoginError
from src.customer import Customer


'''
Dedicated page for "page not found"
'''


@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


'''
Search for Cars
'''


@app.route('/', methods=["GET", "POST"])
def cars():

    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')

        if make == '':
            make = None

        if model == '':
            model = None

        cars = system.search_car(make, model)
        return render_template('cars.html', cars=cars)

    return render_template('cars.html', cars=system.cars)


'''
Display car details for the car with given rego
'''


@app.route('/cars/<rego>')
def car(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)

    return render_template('car_details.html', car=car)


'''
Make a booking for a car with given rego
'''


@app.route('/cars/book/<rego>', methods=["GET", "POST"])
def book(rego):
    car = system.get_car(rego)
    errors = dict()

    if not car:
        abort(404)

    if request.method == 'POST':
        form = BookingForm(request.form)
        fields = ['customer_name', 'customer_license',
                  'start_location', 'end_location', 'start_date', 'end_date']
        

        '''
        IMPLEMENT THIS SECTION
        '''



        # 1. If form is not valid, then display appropriate error messages
        if not form.is_valid:
            for field in fields:
                if form.has_error(field):
                    errors[field + "_error"] = form.get_error(field)

        # 2. If the user has pressed the 'check' button, then display the fee
        customer = Customer(name=form.customer_name, license=form.customer_licence)
        loc = Location(pickup=form.start_location, dropoff=form.end_location)
        booking = Booking(customer=customer, period=form.end_date - form.start_date, car=car, location=loc)

        if request.form['submitButton'] == "Check Booking":
            return render_template('booking_form.html', car = car, **errors, fee= booking.fee)

        # 3. Otherwise, if the user has pressed the 'confirm' button, then
        #   make the booking and display the confirmation page
        if request.form['submitButton'] == "Submit":
            return render_template('booking_confirm.html',  customer=customer, car=car, duration=form.end_date-form.start_date, locations=loc, fee=booking.fee)

        return render_template('booking_confirm.html')

    return render_template('booking_form.html', car=car, **errors, fee=0)


'''
Display list of all bookings for the car with given 'rego'
'''


@app.route('/cars/bookings/<rego>')
def car_bookings(rego):
    return render_template('bookings.html', bookings=system.get_bookings_by_car_rego(rego))
