from __future__ import print_function
from flask import Flask, render_template, Response
import cv2
import face_recognition
import click
import os
import glob
#import js2py

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():

    """Video streaming generator function."""
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        raise IOError("Cannot open webcam")

    def scan_known_people(known_people_folder):
        known_names = []
        known_face_encodings = []

        for file in known_people_folder:
            basename = os.path.splitext(os.path.basename(file))[0]
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 1:
                click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

            if len(encodings) == 0:
                click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_names.append(basename)
                known_face_encodings.append(encodings[0])

        return known_names, known_face_encodings

    # Multiple Image read  from Folder
    path = os.path.join("image/", '*g')
    known_people_folder = glob.glob(path)

    known_face_names, known_face_encodings = scan_known_people(known_people_folder)


    """
    i_image = face_recognition.load_image_file("i1.jpg")
    i_face_encoding = face_recognition.face_encodings(i_image)[0]

    #print(type(i_face_encoding))
    #print(i_face_encoding)
    
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        i_face_encoding
    ]

    known_face_names = [
        "Ahmad"
    ]

    """


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    count = 0  # Frame Count
    falsecount = 0
    flag = 0  # Identification Value

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # ..

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            if count % 10 == 0:
                cv2.imwrite("data/" + str(count) + ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 10])

            flag = 0
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            print("Found {0} faces!".format(len(face_locations)))
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    flag = 1
                face_names.append(name)
                print("Face Identified Value: " + str(flag) + ' name ' + name)



        process_this_frame = not process_this_frame

        count += 1

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
            cv2.rectangle(frame, (left, bottom - 6), (right, bottom), (0, 0, 255), cv2.FILLED)

        #cv2.imwrite("checkdata/" + str(count) + ".jpg", frame)
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                #b'Content-Type: image/jpeg\r\n\r\n' + open("checkdata/" + str(count) + ".jpg", 'rb').read() + b'\r\n')

    video_capture.release()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', thread=True)

