import cv2
import math
import mediapipe as mp

def distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.

    Args:
        p1: A tuple representing the coordinates of the first point.
        p2: A tuple representing the coordinates of the second point.

    Returns:
        The Euclidean distance
    """
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def get_lm_coordinates(lm):
    """
    Extracts the coordinates of specific facial landmarks.

    Args:
        lm: A list of facial landmarks.

    Returns:
        A tuple containing the left mouth corner, right mouth corner,
        upper lip center, lower lip center, left eye, and right eye landmarks.
    """
    left = lm[61]
    right = lm[291]
    top = lm[13]
    bottom = lm[14]
    left_eye = lm[33]
    right_eye = lm[263]
    return left, right, top, bottom, left_eye, right_eye

def calculate_smile(left, right, top, bottom, left_eye, right_eye):
    """
    Calculates whether a person is smiling based on facial landmark distances.

    Args:
        left: The left mouth corner landmark.
        right: The right mouth corner landmark.
        top: The upper lip center landmark.
        bottom: The lower lip center landmark.
        left_eye: The left eye landmark.
        right_eye: The right eye landmark.

    Returns:
        True if the person is smiling, False otherwise.
    """
    mouth_width = distance(left, right)
    mouth_height = distance(top, bottom)
    eye_distance = distance(left_eye, right_eye)
    normalized_width = mouth_width / eye_distance
    normalized_height = mouth_height / eye_distance

    print(f"Width Ratio: {normalized_width}")
    print(f"Height Ratio: {normalized_height}")

    smile_height = 0.10 < normalized_height < 0.35
    smile_width = normalized_width > 0.50
    return smile_height and smile_width


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels_number = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for landmark in result.multi_face_landmarks:
            try:
                left, right, top, bottom, left_eye, right_eye = get_lm_coordinates(landmark.landmark)
                x_center = int((left.x + right.x) / 2 * width)
                y_center = int((top.y + bottom.y) / 2 * height)
                center = (x_center, y_center)

                is_smiling = calculate_smile(left, right, top, bottom, left_eye, right_eye)

                color = (0, 255, 0) if is_smiling else (0, 0, 255) # (B, G, R)
                label = "Smile" if is_smiling else ""
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                text_x = (width - text_size[0][0]) // 2
                text_y = height - 20
                cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            except IndexError:
                # In case landmarks are incomplete
                pass

    cv2.imshow('Smile Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
