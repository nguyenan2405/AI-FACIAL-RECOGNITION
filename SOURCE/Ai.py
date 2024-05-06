import pickle  # Import pickle library for data serialization (loading encoded data)
import cv2  # Import OpenCV library for image processing
import face_recognition  # Import face_recognition library for facial recognition
import numpy as np  # Import NumPy library for array manipulation

# Import libraries for Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize Firebase Admin app using service account credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facerecognitionmems-default-rtdb.firebaseio.com/",
    "storageBucket": "gs://facerecognitionmems.appspot.com"
})

# Get a reference to the storage bucket
bucket = storage.bucket()

# Capture video from webcam (replace 0 with video file path if needed)
cap = cv2.VideoCapture(0)
# Set frame width and height for the captured video
cap.set(3, 640)
cap.set(4, 480)

print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIDs = pickle.load(file)
# Separate encoded data and student IDs
encodeListKnown, studentIDs = encodeListKnownWithIDs
print("Encode File Loaded")

# Mode type (unused in this code snippet)
modeType = 0

# Counter (unused in this code snippet)
counter = 0

# Empty lists to store recognized IDs and corresponding student information
ids = []
imgStudents = []

# Filter out None values from encoded list (ensure valid encodings)
encodeListKnown = [encode for encode in encodeListKnown if encode is not None]

# Get reference shape if encoded list is not empty (for comparison later)
reference_shape = encodeListKnown[0].shape if encodeListKnown else None

# Get frame width and height from webcam capture
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Calculate new frame dimensions to maintain aspect ratio (16:10)
new_width = int(height * (16 / 10))
new_height = int(height)

# Create a named window for displaying the video stream
cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
# Resize the window to the calculated dimensions
cv2.resizeWindow("Face Recognition", new_width, new_height)

while True:
    # Read a frame from the webcam capture
    success, img = cap.read()

    # Resize the frame for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Convert the frame to RGB format (required by face_recognition)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Find face locations in the resized frame
    faceCurName = face_recognition.face_locations(imgS)
    # Extract facial encodings for detected faces
    encodeCurName = face_recognition.face_encodings(imgS, faceCurName)

    # Empty lists to store recognized IDs and student information
    ids = []
    imgStudents = []

    for encodeFace, faceLoc in zip(encodeCurName, faceCurName):
        # Convert encodeFace to a NumPy array if it's not already one
        encodeFace = np.array(encodeFace) if not isinstance(encodeFace, np.ndarray) else encodeFace
        # Ensure encodeFace has the same shape as the reference shape (for compatibility)
        if reference_shape and encodeFace.shape == reference_shape:
            # Compare the current encoding with known encodings
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            # Calculate face distances (optional, not used here)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # Find the index of the best match (smallest distance)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                # Get the bounding box coordinates for the recognized face
                y1, x2, y2, x1 = faceLoc
                # Scale the coordinates based on the original frame size
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (x1, y1, x2 - x1, y2 - y1)

                ids.append(studentIDs[matchIndex])
                studentInfo = db.reference(f'Students/{studentIDs[matchIndex]}').get()
                imgStudents.append(studentInfo)

                # Draw rectangle around the face
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 2)

                # Display student information
                # Trong vòng lặp while, phần hiển thị thông tin sinh viên
                cv2.putText(img, f"Name: {studentInfo['Name']}", (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(img, f"ID: {studentInfo['ID']}", (bbox[0], bbox[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(img, f"Major: {studentInfo['Major']}", (bbox[0], bbox[1] + bbox[3] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(img, f"Intake: {studentInfo['Intake']}", (bbox[0], bbox[1] + bbox[3] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    for id, imgStudent in zip(ids, imgStudents):
        print(f"ID: {id}, Student Info: {imgStudent}")

    cv2.imshow("Face Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()