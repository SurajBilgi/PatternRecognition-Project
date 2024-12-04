#  Assignment Task - Resolute AI
# Name : Suraj S Bilgi

# Task: Build a pipeline which would process a video and would detect and recognise faces.

# Importing the Required Libraries
import cv2
import os
import pickle


# To check for the assured path
def start_capture(name):
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    vid_cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(
        "model_files/haarcascade_frontalface_default.xml"
    )

    # Using pickle to Import and export the dictionary to maintain the users history
    a_file = open("model_files/data.pkl", "rb")
    output = pickle.load(a_file)
    # print(output)
    a_file.close()

    # Enter the name of the person
    # name = input('Enter the Name: ')

    if name.lower() in output:
        pass
    else:
        output[name.lower()] = len(output) + 1

    a_file = open("model_files/data.pkl", "wb")
    pickle.dump(output, a_file)
    a_file.close()

    face_id = output[name.lower()]

    # Initialize sample face image
    count = 0

    assure_path_exists("dataset/")

    while True:

        _, image_frame = vid_cam.read()

        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for x, y, w, h in faces:

            cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(
                image_frame,
                "Face Detected",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
            )
            cv2.putText(
                image_frame,
                str(str(count) + " images captured"),
                (x, y + h + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
            )
            count += 1
            print("#", end="")

            cv2.imwrite(
                "dataset/User." + str(face_id) + "." + str(count) + ".jpg",
                gray[y : y + h, x : x + w],
            )

        cv2.imshow("frame", image_frame)

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        elif count > 100:
            break

    vid_cam.release()
    print("\n100% Completed\nFace has been added to the DataSet")

    cv2.destroyAllWindows()
