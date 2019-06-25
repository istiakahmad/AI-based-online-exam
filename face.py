from __future__ import print_function
import face_recognition
import os
import glob
import cv2
import time


def facerecognitionFunction(username):

    def scan_known_people(known_people_folder):
        known_names = []
        known_face_encodings = []

        for file in known_people_folder:
            basename = os.path.splitext(os.path.basename(file))[0]
            if basename == username:
                img = face_recognition.load_image_file(file)
                encodings = face_recognition.face_encodings(img)
                known_names.append(basename)
                known_face_encodings.append(encodings[0])

        return known_names, known_face_encodings

    # Multiple Image read  from Folder
    path = os.path.join("image/", '*g')
    known_people_folder = glob.glob(path)

    known_face_names, known_face_encodings = scan_known_people(known_people_folder)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    count = time.strftime("%Y%m%d-%H%M%S")
    flag = 0  # Identification Value

    frame_image = face_recognition.load_image_file('./images/'+username+'.jpeg')

    PATH_IMAGES_DIR = './data/' + username + '/'

    try:
        os.mkdir(PATH_IMAGES_DIR)
    except FileExistsError:
        pass

    cv2.imwrite(PATH_IMAGES_DIR + str(count) + ".jpg", frame_image)

    # Only process every other frame of video to save time
    if process_this_frame:

        flag = 0
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame_image)
        try:
            if len(face_locations) < 1:
                string = 'No face Found!!! Please Come closure.'
                print("Found {0} faces!".format(len(face_locations)))
        except:
            print("Error flash message")

        face_encodings = face_recognition.face_encodings(frame_image, face_locations)

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
            #distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            #print("distance of frame from camera: {}.".format(distance))

    process_this_frame = not process_this_frame


