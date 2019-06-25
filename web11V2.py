# from flask import Flask, request, Response, render_template, redirect, session, url_for, Session
from flask import *
from face import facerecognitionFunction
import os

PATH_TO_TEST_IMAGES_DIR = './images'

try:
    os.mkdir(PATH_TO_TEST_IMAGES_DIR)
except FileExistsError:
    pass

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>" + '<br>' + \
               "<a href = '/recognition'> click here for face recognition</a>"
    return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Video streaming home page."""
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('logincp.html')


@app.route('/recognition')
def recognition():
    return Response(open('./templates/getImage.html').read(), mimetype="text/html")


@app.route('/image', methods=['POST'])
def image():
    if 'username' in session:
        username = session['username']
        i = request.files['image']  # get the image
        #print('check0')
        f = (username + '.jpeg')
        #print('check1')
        i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
        #print('check2')
        # print(username)
        facerecognitionFunction(username)
        #print('check3')
        return Response("%s saved" % f)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host='10.11.201.67', port=5000)
    # app.run(ssl_context=('cert.pem', 'key.pem'))

