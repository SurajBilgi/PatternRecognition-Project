# PatternRecognition-Project

# Face Recognition and Mask Detection System

The project is a Face Recognition System with integrated Mask Detection, designed to provide an enhanced level of security and safety by identifying individuals and ensuring compliance with mask-wearing policies. This application utilizes a combination of face recognition and mask detection models, implemented in Python with the help of OpenCV, Keras, and Tkinter. The system can be used in various settings such as workplaces, educational institutions, and public areas to monitor access control and adherence to health protocols.

## Key Features

1. **Face Recognition**: The project uses a pre-trained Local Binary Patterns Histogram (LBPH) face recognizer, implemented using OpenCV, to identify registered individuals. The LBPH model is trained with a dataset of faces, and upon recognition, the system can match the individual with the corresponding name stored in a database.

2. **Mask Detection**: The system also features a mask detection component. This part of the application uses a Convolutional Neural Network (CNN) model built with Keras, capable of determining if an individual is wearing a mask or not. The CNN model is trained on a dataset of masked and unmasked faces to ensure reliable predictions.

3. **User Registration**: The system provides an easy-to-use GUI built with Tkinter, where users can register themselves by capturing their images through the system's camera. The registered data is used to create a personalized dataset for each user, which can be utilized for training and recognition purposes.

4. **Integrated GUI**: The interface is designed using Tkinter, which allows users to navigate through different functionalities of the application, such as registering a new user, starting face recognition, and viewing mask detection results. The GUI also includes functionalities for handling the camera feed and recognizing registered individuals in real-time.

5. **Real-time Camera Feed**: The system uses the laptop's built-in camera to capture live video feed. The face recognition and mask detection components are applied in real-time, allowing immediate identification and feedback on mask-wearing.

## Technical Components

1. **OpenCV for Face Recognition**: The face recognition module relies on OpenCV's LBPH face recognizer. The system reads the face data from the `trainer.yml` file, which contains the trained face embeddings. Haar cascades are used for face detection, specifically using the pre-trained `model_files/haarcascade_frontalface_default.xml` classifier to locate faces in the video stream.

2. **Keras for Mask Detection**: The mask detection functionality uses a CNN model implemented in Keras. This model is loaded from `mymodel.h5` and performs predictions on cropped face images captured during the recognition process. Based on the output, the system labels the detected faces with either "MASK" or "NO MASK."

3. **Data Management**: The system saves registered users' names in a file called `data.pkl`, allowing easy access and retrieval during the face recognition process. The captured face data is saved and used to update the `trainer.yml` file, enabling the system to recognize the faces that have been added.

4. **Logging and Error Handling**: The project uses Python's logging module to log key actions and errors throughout the application. Logs are written to a file (`face_recognizer.log`), which helps in tracking issues and debugging the program when errors occur.

5. **GUI Interaction**: The Tkinter GUI presents a user-friendly interface for navigating through the system. Users can register new faces, initiate face recognition, and manage the system without needing to interact with the command line.

## Workflow

1. **User Registration**: A new user is registered by capturing multiple images of their face. These images are stored, and the model is updated to recognize the newly added user.

2. **Face Recognition**: The system captures a live video stream, detects faces in the frame, and identifies the individual by comparing with the trained model. The recognized user's name is displayed on the screen.

3. **Mask Detection**: Once a face is detected, the system checks for mask compliance using the CNN model. Depending on whether a mask is detected or not, the appropriate label ("MASK" or "NO MASK") is displayed.

4. **Logging and Debugging**: Every major action, such as user registration, recognition attempts, and mask validation, is logged. In case of errors (e.g., failure to load the camera or model files), detailed error messages are recorded in the log file to assist in troubleshooting.

## Challenges and Improvements

1. **Lighting and Environment Variability**: Real-time face recognition is often influenced by lighting conditions and background clutter. The Haar cascades used for face detection might face challenges in poor lighting. An improvement could involve using more advanced detection methods such as DNN-based face detectors.

2. **Mask Detection Accuracy**: The accuracy of mask detection depends on the quality of the training data. Further training with a larger dataset, including diverse mask styles and wearing conditions, would improve the system's robustness.

3. **Scaling the System**: The current system operates with a small dataset and is designed for demonstration purposes. Scaling the system for production would involve improving the face recognition model, handling larger datasets, and optimizing the GUI for better user experience.

## Applications

- **Access Control**: The system can be used in offices or workplaces to ensure that only registered individuals can enter, and that they are wearing a mask if required.
- **Attendance Management**: The face recognition component can be used to automate attendance marking in schools or workplaces.
- **Health Compliance**: In public areas or healthcare facilities, this system could ensure individuals are adhering to mask-wearing policies, thereby improving public health compliance.

## Conclusion

The project combines key aspects of computer vision and deep learning, making it a valuable solution in the context of security and health monitoring. Its real-time capabilities, integrated GUI, and ability to recognize and validate users based on face masks make it highly relevant in the current scenario where mask-wearing has become a crucial public health measure.

## How to Run the Project

1. **Install Dependencies**: Make sure you have Python installed. Install the required libraries using the following command:
   ```
   pip install -r requirements.txt
   ```

2. **Prepare the Dataset**: Register new users through the GUI to create a dataset of faces.

3. **Train the Model**: Run the script to train the face recognizer model.

4. **Run the Application**: Start the GUI application to begin face recognition and mask detection.
   ```
   python main.py
   ```

## Requirements

- Python 3.7+
- OpenCV
- Keras
- Tkinter
- Numpy
- Pickle

## License

This project is licensed under the MIT License - see the LICENSE file for details.

