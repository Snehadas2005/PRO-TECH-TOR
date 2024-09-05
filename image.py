import cv2

# Load the pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize video capture from the default camera
cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

    # Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'XVID' for AVI files
frame_width = int(cap.get(3))  # Width of the frame
frame_height = int(cap.get(4))  # Height of the frame

    # Create VideoWriter object to save the video
out = cv2.VideoWriter('D:/Face_Recognition/SOS_SYSTEM/Eoutput_compressed.avi', fourcc, 20.0, (frame_width, frame_height))

    # To track already detected faces (store their coordinates)
known_faces = []

    # To store the count of saved images
saved_image_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

        # Convert frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over detected faces
    new_faces_detected = False
    for (x, y, w, h) in faces:
            # Draw rectangle around the face (optional for visualization)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Check if this face is new
        new_face = True
        for known_face in known_faces:
            (known_x, known_y, known_w, known_h) = known_face
            if abs(x - known_x) < 50 and abs(y - known_y) < 50:
                new_face = False
                break

        if new_face:
            known_faces.append((x, y, w, h))  # Add new face to the list
            new_faces_detected = True

        # If a new face is detected, save the current frame as a JPG image
    if new_faces_detected:
        saved_image_filename = f'D:/Face_Recognition/SOS_SYSTEM/face_{saved_image_count}.jpg'
        cv2.imwrite(saved_image_filename, frame)
        print(f"New face detected! Saved {saved_image_filename}")
        saved_image_count += 1

        # Write the frame to the video file
    out.write(frame)

        # Show the frame in a window
    cv2.imshow('Recording Video', frame)

        # Press 'q' to stop the recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release everything when the job is finished
cap.release()
out.release()
cv2.destroyAllWindows()


