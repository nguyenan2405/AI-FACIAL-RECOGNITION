import os
import cv2
import time

# Get the number of new labels from the user
num = int(input("The number of new labels you want to add: "))
number_images = 25

# Create the "Dataset" directory if it doesn't exist
os.makedirs("Dataset", exist_ok=True)  # Command: `mkdir -p Dataset` (if using Linux/macOS)

for i in range(num):
    # Get the label name from the user
    name = input("Name of the label: ")
    labelname = os.path.join("Dataset", name)

    # Create the label directory if it doesn't exist
    os.makedirs(labelname, exist_ok=True)  # Command: `mkdir -p Dataset/name`

    # Open the labels.txt file in append mode
    with open("Dataset\\labels.txt", "a") as label:  # Use forward slashes for cross-platform compatibility
        label.write(f"{i} {name}\n")  # Add label information with a newline

    # Open the webcam for capturing images
    cap = cv2.VideoCapture(0)

    for imgnum in range(number_images):
        print("Collecting images {}".format(imgnum))
        ret, frame = cap.read()

        # Construct the image filename
        imgname = os.path.join(labelname, f"Num {imgnum+1} {name}.jpg")

        # Save the captured frame as a JPEG image
        cv2.imwrite(imgname, frame)  # Command: Equivalent to saving an image using an image editing software

        # Display the captured frame in a window
        cv2.imshow("frame", frame)

        # Introduce a slight delay between frames
        time.sleep(0.5)

        # Check for user input to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam resource
    cap.release()  # Command: Equivalent to closing the webcam application

# Close all open windows
cv2.destroyAllWindows()