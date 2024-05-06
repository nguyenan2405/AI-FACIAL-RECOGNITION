import cv2
import face_recognition
import pickle
import os


def read_images_from_subdirectories(dataset_dir):
    """
    This function reads images and extracts student IDs from filenames
    within a directory and its subdirectories.

    Args:
        dataset_dir (str): Path to the directory containing images.

    Returns:
        tuple: A tuple containing two lists:
               - imgList (list): A list of loaded images.
               - studentIds (list): A list of correspondinưg student IDs extracted from filenames.
    """

    imgList = []  # Initialize an empty list to store images
    studentIds = []  # Initialize an empty list to store student IDs

    for root, _, files in os.walk(dataset_dir):
        # Loop through all files in the dataset directory and its subdirectories
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                # Check if the file is a JPG or PNG image
                full_path = os.path.join(root, filename)  # Construct the full path to the image
                try:
                    img = cv2.imread(full_path)  # Read the image using OpenCV
                    if img is None:
                        raise ValueError(f"Failed to read image: {full_path}")
                    imgList.append(img)  # Add the image to the list

                    # Extract student ID from the filename (without the extension)
                    student_id = os.path.splitext(filename)[0]
                    studentIds.append(student_id)

                except Exception as e:
                    print(f"Error processing file '{full_path}': {str(e)}")
                    # Handle any errors that might occur during image reading or ID extraction

    return imgList, studentIds  # Return the lists of images and student IDs


def find_encodings(images_list):
    """
    This function finds facial encodings for a list of images,
    handling cases where no faces are detected.

    Args:
        images_list (list): A list of loaded images.

    Returns:
        list: A list of facial encodings corresponding to the input images,
              or an empty list if no faces are detected in any image.
    """

    encode_list = []  # Initialize an empty list to store facial encodings
    for img in images_list:
        try:
            # Convert the image to RGB format (required by face_recognition)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get list of encodings (might be empty)
            encode = face_recognition.face_encodings(img)

            # Handle empty encoding gracefully (no faces detected)
            if len(encode) > 0:
                encode_list.append(encode[0])  # Add the first encoding (if it exists)
            else:
                print(f"No face detected in image.")

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            continue  # Skip to the next image if there's an error

    return encode_list  # Return the list of facial encodings (or empty list)


if __name__ == "__main__":
    dataset_dir = "Dataset"  # Replace with the actual path to your dataset directory

    images, student_ids = read_images_from_subdirectories(dataset_dir)

    if images:
        encodings = find_encodings(images)
        encoded_data = [encodings, student_ids]  # Combine encodings and IDs into a list

        with open("EncodeFile.p", 'wb') as file:
            pickle.dump(encoded_data, file)  # Save the encoded data using pickle
        print("Encoding and saving completed.")
    else:
        print("No images were found in the dataset directory. Please check the path and file structure.")
