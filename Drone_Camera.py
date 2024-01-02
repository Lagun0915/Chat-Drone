from djitellopy import tello
import time
import cv2

def drone_camera(drone):
    drone.streamon()

    frame_reader = drone.get_frame_read()

    cv2.namedWindow("Drone Camera")

    while True:
        frame = frame_reader.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if frame is not None:
            cv2.imshow("Drone Camera", frame)

            # frame 값이 들어오고 일정 시간이 지났을 때 png로 저장시키기.

            # drone.land()
            # break
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("drone_img.png", frame)
            drone.land()
            break