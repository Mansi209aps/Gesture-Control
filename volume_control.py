import cv2
import mediapipe as mp
import pyautogui

#VideoCapture function will capture the video, webcam is object
x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)

my_hands = mp.solutions.hands.Hands()   # to capture hand
drawing_utils = mp.solutions.drawing_utils # to draw landmarks
while True:
 _ , image = webcam.read()

 # Flip the image in y-direction(1)
 image = cv2.flip(image, 1)
 frame_height, frame_width, _ = image.shape

 #Convert captured image from BGR to RGB
 rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 output = my_hands.process(rgb_image)

 #to capture multi-hands
 hands = output.multi_hand_landmarks

 # iteration through hands
 if hands:
  for hand in hands:
   drawing_utils.draw_landmarks(image, hand) #Draw landmarks or points on hand
   landmarks = hand.landmark
   for id, landmark in enumerate(landmarks):
    x = int(landmark.x * frame_width)
    y = int(landmark.y * frame_height)

    # To define forefinger and thumb tip
    if id == 8:  #If id==8, forfinger
     cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
     x1 = x
     y1 = y
    if id == 4:  #If id==4, thumb
     cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
     x2 = x
     y2 = y
    # else id == 12:
    #  pyautogui.press("esc")

   # Calculate the distance between forefinger and thumb tip
   dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4 #Calculate distance between fingers (0-35)

   # If distance between tips is greater than 50, volume up else volume down
   cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)  # to draw line between forfinger and thumb
   if dist > 50:
    pyautogui.press("VOLUMEUP")
   else:
    pyautogui.press("VOLUMEDOWN")

 cv2.imshow("Hand Volume Control Using Python", image)
 key = cv2.waitKey(10)

 # close camera on ESP button
 if key == 27:
  break
webcam.release()
cv2.destroyAllWindows()