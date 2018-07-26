from flask import render_template
from app import app
from app.utils import Utils
from app.forms import LcdForm
from mygpio import gpio
import time


@app.route('/')
@app.route('/index')
def index():
    environment = "Raspberry PI"
    if Utils.is_simulator():
        environment = "Simulator"
    return render_template('index.html', title='Index', env=environment)


@app.route('/gpio')
def route_gpio():
    my_gpio = gpio.MyGPIO()
    my_gpio.configure()
    state = my_gpio.input(25)
    return render_template('result.html', title='Sample GPIO', result_text="State for pin %s is %s" % (25, state))


@app.route('/sample_gpio')
def sample_gpio():
    # sample
    PIN_LED_RED = 17
    PIN_LED_GREEN = 19

    my_gpio = gpio.MyGPIO()
    my_gpio.configure()

    for i in range(3):
        my_gpio.turn_on(PIN_LED_RED)
        time.sleep(1)
        my_gpio.turn_off(PIN_LED_RED)
        time.sleep(1)

    return render_template('result.html', title='Sample GPIO', result_text="GPIO commands executed!")


@app.route('/lcd', methods=['GET', 'POST'])
def lcd():
    form = LcdForm()
    if form.validate_on_submit():
        my_gpio = gpio.MyGPIO()
        my_gpio.lcd_text(form.lcd_text.data)
        return render_template('lcd.html', title='LCD Display', previous_text=form.lcd_text.data, form=form)
    return render_template('lcd.html', title='LCD Display', form=form)


@app.route('/lcd_clear')
def lcd_clear():
    my_gpio = gpio.MyGPIO()
    my_gpio.lcd_clear()
    form = LcdForm()
    return render_template('lcd.html', title='LCD Display', form=form)