# MagnumPi

A simple web application to manage Raspberry PI GPIO.

Actually this is a work in progress, any suggestions will be appreciated!

## Screenshots

![MagnumPi - Homepage](https://user-images.githubusercontent.com/847860/44450788-1652e480-a5f2-11e8-97af-0c1b04f72602.png)

![MagnumPi - GPIO](https://user-images.githubusercontent.com/847860/44653882-40d8df00-a9f0-11e8-83e6-3637a3801c94.png)

![MagnumPi - LED Blinking](https://user-images.githubusercontent.com/847860/44654155-0ae82a80-a9f1-11e8-87cc-7f95c42af675.png)

![MagnumPi - LCD Display](https://user-images.githubusercontent.com/847860/44653939-6b2a9c80-a9f0-11e8-8b8a-cd17fec9aad9.png)

![MagnumPi - Background tasks](https://user-images.githubusercontent.com/847860/44653951-72ea4100-a9f0-11e8-8dfb-c3e7e9f762c4.png)

## Available features

The following feature are already available

- **/gpio**: allows to send high or low signal to a GPIO pin
- **/lcd**: allows to to send a text to a I2C LCD display
- **/led_blink**: allows to blink a led connected to a specific GPIO PIN
- **/tasks**: allows to create background tasks. Actually this is only a demo page, that shows how to create and handle background tasks
- **/camera**: show a live video streaming from a PiCamera (or a simulated one if not available)

## Requirements

This project requires:

- Python 3.6
- Redis

Redis installation depends on your platform:

- *macOS*, you can install with Brew `brew install redis`
- *Linux*, you can install via terminal `sudo apt-get install redis-server`

When Redis is installed, simply start it with this command:

`$ redis-server`

## Development

During the development phase, you can run the web application using flask. These are the commands that you need to run the app:

```bash
$ source venv/bin/activate
(venv) $ cd code
(venv) $ export SIMULATOR=1
(venv) $ export FLASK_APP=magnumpi.py
(venv) $ rq worker magnumpi-tasks
(venv) $ flask run
```

Some notes:

- *SIMULATOR* is a bash variable that allows the application to run outside a Raspberry Pi. Access to GPIO is simulated through mock classes inside *fakeRPi* package. Use `SIMULATOR=1` when the wep application is not running on a Raspberry PI.
- Redis must be running on the same machine in order to start the application (it's possible to change this configuration inside *config.py* file)
- `rq worker magnumpi-tasks` this command start a worker for Redis. You can also start more workers depending on your needs.

## Deployment

To deploy this web application, follow the following steps.

Clone the repository:

```bash
$ git clone git@github.com:BubiDevs/MagnumPi.git
$ cd MagnumPi
```

Create the virtual environment and populate it with all the package dependencies:

```bash
$ python3 -m venv --system-site-packages venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

(The option *--system-site-packages* is necessary to use Raspberry Pi system package as RPi.GPIO or smbus).

Install gunicorn as production web server:

```bash
(venv) $ pip install gunicorn
```

In a separate terminal tab, start redis workers:

```bash
$ cd MagnumPi
$ source venv/bin/activate
(venv) cd code
(venv) rq worker magnumpi-tasks
```

To start MagnumPi under gunicorn:

```bash
(venv) cd code
(venv) $ gunicorn -b localhost:8000 -w 4 magnumpi:app
```

**Note**: If you need to access to web application from outside the deployment machine, you'll need to change *localhost* with the IP of the target machine.

## ToDo

Here is a list of the planning activities. Some are quite simple, other could be a little bit tricky to implement.

- [X] GPIO section: set to low or high a specific pin
- [ ] GPIO section: read a value from a specific pin
- [ ] GPIO section: support for GPIO buttons
- [X] Add the capability to stop a background task (running or queued)
- [X] Display the current status of a running job directly in the task table
- [X] Handle errors if LCD display is not connected
- [ ] Review and improve MyGPIO class

## References

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)
- [Flask Video Streaming Revisited](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)
- [How to setup an I2C LCD on the Raspberry Pi](http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/)
- [Raspberry Pi Pinout](https://it.pinout.xyz)
