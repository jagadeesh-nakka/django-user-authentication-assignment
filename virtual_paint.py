import mediapipe as mp
import cv2
import numpy as np
import time

# Constants
ml = 150
max_x, max_y = 250 + ml, 50
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 4
prevx, prevy = 0, 0

# Trackbar callback function
def setValues(x):
    pass

# Create a window for trackbars
cv2.namedWindow("Trackbars")
cv2.createTrackbar("R", "Trackbars", 0, 255, setValues)
cv2.createTrackbar("G", "Trackbars", 0, 255, setValues)
cv2.createTrackbar("B", "Trackbars", 0, 255, setValues)

# Get the color from trackbars
def getColor():
    r = cv2.getTrackbarPos("R", "Trackbars")
    g = cv2.getTrackbarPos("G", "Trackbars")
    b = cv2.getTrackbarPos("B", "Trackbars")
    return (b, g, r)

# Get tool function
def getTool(x):
    if x < 50 + ml:
        return "line"
    elif x < 100 + ml:
        return "rectangle"
    elif x < 150 + ml:
        return "draw"
    elif x < 200 + ml:
        return "circle"
    elif x < 250 + ml:
        return "erase"
    elif x < 300 + ml:
        return "whiteboard"
    elif x < 350 + ml:
        return "blackboard"
    else:
        return "clear"

def index_raised(yi, y9):
    return (y9 - yi) > 40

# Initialize Mediapipe hands
hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils

# Load tool images
tools = cv2.imread("tools.png")
tools = tools.astype('uint8')

mask = np.ones((480, 640, 3), dtype=np.uint8) * 255

cap = cv2.VideoCapture(0)
while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    op = hand_landmark.process(rgb)

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)
            x, y = int(i.landmark[8].x * 640), int(i.landmark[8].y * 480)

            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()
                    time_init = False
                ptime = time.time()

                cv2.circle(frm, (x, y), rad, (0, 255, 255), 2)
                rad -= 1

                if (ptime - ctime) > 0.8:
                    curr_tool = getTool(x)
                    print("Your current tool set to:", curr_tool)
                    time_init = True
                    rad = 40

            else:
                time_init = True
                rad = 40

            if curr_tool == "draw":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    color = getColor()
                    cv2.line(mask, (prevx, prevy), (x, y), color, thick)
                    prevx, prevy = x, y
                else:
                    prevx = x
                    prevy = y

            elif curr_tool == "line":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True

                    color = getColor()
                    cv2.line(frm, (xii, yii), (x, y), color, thick)
                else:
                    if var_inits:
                        color = getColor()
                        cv2.line(mask, (xii, yii), (x, y), color, thick)
                        var_inits = False

            elif curr_tool == "rectangle":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True

                    color = getColor()
                    cv2.rectangle(frm, (xii, yii), (x, y), color, thick)
                else:
                    if var_inits:
                        color = getColor()
                        cv2.rectangle(mask, (xii, yii), (x, y), color, thick)
                        var_inits = False

            elif curr_tool == "circle":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True

                    color = getColor()
                    cv2.circle(frm, (xii, yii), int(((xii - x)**2 + (yii - y)**2)**0.5), color, thick)
                else:
                    if var_inits:
                        color = getColor()
                        cv2.circle(mask, (xii, yii), int(((xii - x)**2 + (yii - y)**2)**0.5), color, thick)
                        var_inits = False

            elif curr_tool == "erase":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    cv2.circle(frm, (x, y), 30, (0, 0, 0), -1)
                    cv2.circle(mask, (x, y), 30, (255, 255, 255), -1)

            elif curr_tool == "whiteboard":
                mask[:] = 255

            elif curr_tool == "blackboard":
                mask[:] = 0

            elif curr_tool == "clear":
                mask[:] = 255

    op = cv2.bitwise_and(frm, frm, mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY))
    frm[:, :, 1] = op[:, :, 1]
    frm[:, :, 2] = op[:, :, 2]

    # Draw the eraser circle on the frame at the top right corner
    eraser_center = (600, 50)  # Top right corner, adjust as needed
    cv2.circle(frm, eraser_center, 30, (255, 255, 255), 2)
    cv2.putText(frm, "Erase All", (eraser_center[0] - 40, eraser_center[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Detect if the eraser gesture is triggered
    if curr_tool == "erase" and index_raised(int(i.landmark[8].y * 480), int(i.landmark[9].y * 480)):
        distance = ((eraser_center[0] - x) ** 2 + (eraser_center[1] - y) ** 2) ** 0.5
        if distance < 30:
            mask[:] = 255
            print("Screen cleared!")

    frm[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, frm[:max_y, ml:max_x], 0.3, 0)

    cv2.putText(frm, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frm, "Press 's' to save", (270 + ml, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    cv2.imshow("Paint App", frm)
    cv2.imshow("Paint Window", mask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'ESC' to exit
        break
    elif key == ord('s'):  # Press 's' to save the image
        cv2.imwrite("painted_image.png", mask)
        print("Image saved as 'painted_image.png'")

cv2.destroyAllWindows()
cap.release()
