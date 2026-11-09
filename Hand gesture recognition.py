import cv2
import mediapipe as mp
import requests
import os


# =========================================================
# 1. DOWNLOAD HAND MODEL AUTOMATICALLY
# =========================================================

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

MODEL_FILE = "hand_landmarker.task"


if not os.path.exists(MODEL_FILE):

    print("Downloading hand model...")

    response = requests.get(MODEL_URL)

    if response.status_code != 200:
        print("Could not download hand model.")
        exit()

    with open(MODEL_FILE, "wb") as file:
        file.write(response.content)

    print("Model downloaded successfully.")


# =========================================================
# 2. MEDIAPIPE SETUP
# =========================================================

BaseOptions = mp.tasks.BaseOptions

HandLandmarker = mp.tasks.vision.HandLandmarker

HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

RunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path=MODEL_FILE
    ),

    running_mode=RunningMode.IMAGE,

    num_hands=1,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5
)


# =========================================================
# 3. GESTURE RECOGNITION
# =========================================================

def recognize_gesture(hand):

    # -----------------------------------------------------
    # Detect the four normal fingers
    # -----------------------------------------------------

    index = hand[8].y < hand[6].y

    middle = hand[12].y < hand[10].y

    ring = hand[16].y < hand[14].y

    pinky = hand[20].y < hand[18].y


    # -----------------------------------------------------
    # Detect thumb
    # -----------------------------------------------------

    thumb = abs(hand[4].x - hand[2].x) > 0.05


    # -----------------------------------------------------
    # PEACE
    # Index + Middle
    # -----------------------------------------------------

    if index and middle and not ring and not pinky:

        return "PEACE"


    # -----------------------------------------------------
    # STOP
    # All five fingers
    # -----------------------------------------------------

    if index and middle and ring and pinky and thumb:

        return "STOP"


    # -----------------------------------------------------
    # CHILL
    # Thumb + Pinky
    # -----------------------------------------------------

    if thumb and pinky and not index and not middle and not ring:

        return "CHILL"


    return "UNKNOWN"


# =========================================================
# 4. WEBCAM
# =========================================================

camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("ERROR: Could not open webcam.")

    exit()


print()
print("======================================")
print("       AI HAND GESTURE RECOGNITION")
print("======================================")
print()
print("Gestures:")
print("  PEACE  -> Two fingers")
print("  STOP   -> Open palm")
print("  CHILL  -> Thumb + Pinky")
print()
print("Press Q to quit.")
print()


# =========================================================
# 5. STABILITY SYSTEM
# =========================================================

last_gesture = ""

stable_gesture = "UNKNOWN"

counter = 0

REQUIRED_FRAMES = 5


# =========================================================
# 6. START MEDIAPIPE
# =========================================================

with HandLandmarker.create_from_options(options) as detector:

    while True:

        # -------------------------------------------------
        # Read webcam
        # -------------------------------------------------

        success, frame = camera.read()


        if not success:

            print("Could not read webcam.")

            break


        # Mirror webcam

        frame = cv2.flip(frame, 1)


        # -------------------------------------------------
        # Convert BGR → RGB
        # -------------------------------------------------

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # Create MediaPipe image

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )


        # -------------------------------------------------
        # Detect hand
        # -------------------------------------------------

        result = detector.detect(image)


        gesture = "NO HAND"


        # -------------------------------------------------
        # If hand detected
        # -------------------------------------------------

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]


            gesture = recognize_gesture(hand)


            # -------------------------------------------------
            # Stability filter
            # -------------------------------------------------

            if gesture == last_gesture:

                counter += 1

            else:

                counter = 0

                last_gesture = gesture


            if counter >= REQUIRED_FRAMES:

                stable_gesture = gesture


            # -------------------------------------------------
            # Draw landmarks
            # -------------------------------------------------

            height, width, _ = frame.shape


            for point in hand:

                x = int(point.x * width)

                y = int(point.y * height)


                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )


        else:

            last_gesture = ""

            counter = 0

            stable_gesture = "NO HAND"


        # =====================================================
        # DISPLAY
        # =====================================================

        cv2.rectangle(
            frame,
            (10, 10),
            (550, 100),
            (0, 0, 0),
            -1
        )


        cv2.putText(
            frame,
            "AI HAND GESTURE RECOGNITION",
            (25, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            "Gesture: " + stable_gesture,
            (25, 82),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


        # -------------------------------------------------
        # Show camera
        # -------------------------------------------------

        cv2.imshow(
            "AI Hand Gesture Recognition",
            frame
        )


        # -------------------------------------------------
        # Quit
        # -------------------------------------------------

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


# =========================================================
# 7. CLEANUP
# =========================================================

camera.release()

cv2.destroyAllWindows()

print("Program stopped.")