import cv2
import pickle
import os
from keras.models import Sequential, load_model
import keras.utils as image
import numpy as np
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("face_recognizer.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def face_recognizer():
    def assure_path_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created directory at: {path}")

    def mask_validator(im, x, y, w, h):
        try:
            temp_path = "temp.jpg"
            cv2.imwrite(temp_path, im[y : y + h, x : x + w])
            test_image = image.load_img(temp_path, target_size=(150, 150))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            pred = mymodel.predict(test_image)[0][0]
            label = "NO MASK" if pred >= 0.5 else "MASK"
            color = (0, 0, 255) if pred >= 0.5 else (0, 255, 0)
            cv2.putText(
                im, label, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3
            )
            logger.info(f"Mask validation result: {label}")
        except Exception as e:
            logger.error(f"Error in mask_validator: {e}")
        return im

    try:
        # Creating patterns for face recognition
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        assure_path_exists("trainer/")

        # Loading the trained model
        recognizer.read("trainer/trainer.yml")
        mymodel = load_model("model_files/mymodel.h5")
        logger.info("Loaded face recognizer and mask model successfully")

        # Load prebuilt model for Frontal Face
        cascadePath = "model_files/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        if faceCascade.empty():
            raise IOError(f"Failed to load face cascade from {cascadePath}")

        # Initialize and start the video frame capture
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise IOError("Cannot open webcam")

        with open("model_files/data.pkl", "rb") as a_file:
            output = pickle.load(a_file)
        name_list = list(output.keys())
        logger.info("Loaded names from data.pkl successfully")

        # Loop to continuously get frames from the webcam
        while True:
            ret, im = cam.read()
            if not ret:
                logger.warning("Failed to capture frame from webcam")
                break

            # Convert the captured frame into grayscale
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Get all faces from the video frame
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            # For each face in faces
            for x, y, w, h in faces:
                # Create rectangle around the face
                cv2.rectangle(
                    im, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 4
                )

                # Recognize the face
                Id, confidence = recognizer.predict(gray[y : y + h, x : x + w])

                # Check the ID if it exists
                if (
                    Id < len(name_list) and confidence < 70
                ):  # Confidence threshold adjusted
                    name = name_list[Id]
                    Id = f"{name} ({round(100 - confidence, 2)}%)"
                else:
                    Id = "Unknown"

                # Put text describing who is in the picture
                cv2.rectangle(
                    im, (x - 22, y - 90), (x + w + 22, y - 22), (0, 255, 0), -1
                )
                cv2.putText(
                    im,
                    str(Id),
                    (x, y - 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    3,
                )
                logger.info(f"Recognized: {Id}")

                # Validate mask presence
                im = mask_validator(im, x, y, w, h)

            # Display the video frame with the bounded rectangle
            cv2.imshow("Face Recognition", im)

            # If 'q' is pressed, close program
            if cv2.waitKey(10) & 0xFF == ord("q"):
                logger.info("'q' key pressed. Exiting the face recognition loop.")
                break

    except Exception as e:
        logger.error(f"Error during face recognition: {e}")
    finally:
        # Stop the camera
        if "cam" in locals() and cam.isOpened():
            cam.release()
        cv2.destroyAllWindows()
        logger.info("Released webcam and closed all windows")
