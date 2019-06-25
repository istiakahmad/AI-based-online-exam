from flask import Flask, request, Response, render_template
from face import facerecognitionFunction
import os


PATH_TO_TEST_IMAGES_DIR = './images'

try:
    os.mkdir(PATH_TO_TEST_IMAGES_DIR)
except FileExistsError:
    pass

app = Flask(__name__)
count = 0


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('logincp.html')


@app.route('/recognition')
def recognition():
    return Response(open('./static/getImage.html').read(), mimetype="text/html")


@app.route('/image', methods=['POST'])
def image():
    global count
    i = request.files['image']  # get the image
    print('check0')
    f = ('p.jpeg')
    print('check1')
    i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
    print('check2')
    facerecognitionFunction(count)
    print('check3')
    count += 1
    return Response("%s saved" % f)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    #app.run(host='10.11.201.67', port=5000)
    #app.run(ssl_context=('cert.pem', 'key.pem'))


