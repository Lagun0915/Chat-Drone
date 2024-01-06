from djitellopy import tello
import time
import cv2

def camera(drone):
    drone.streamon()

    frame_reader = drone.get_frame_read()
    time.sleep(3)

    frame = frame_reader.frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.imwrite("drone_img.png", frame)
    
    drone.streamoff()