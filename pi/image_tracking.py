import cv2                                                                       
import numpy as np                                                               
from gpiozero import Device, Servo                                               
from gpiozero.pins.pigpio import PiGPIOFactory                                   
import time                                                                      

HISTORY_VAR = 10                                                                 
servo_factory = PiGPIOFactory()                                                                                                                                                                                                               

def detect(frame, HOGCV):                                                        
    bounding_box_coordinates, weights = HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)                                                                                  
    person = 1                                                                   
    max_area = -1                                                                
    max_pos = [0,0,0,0]                                                          
    for x,y,w,h in bounding_box_coordinates:                                     
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)                   
        person += 1                                                              
        if w*h > max_area:                                                       
            max_area = w*h                                                       
            max_pos = [x,y,w,h]                                                  
                                                                                 
    cv2.imshow('frame', frame)                                                   
    return frame, max_pos                                                        
                                                                                 
def humanDetector(servo, HOGCV):                                                 
    video = cv2.VideoCapture(0)                                                  
    frame = None                                                                 
                                                                                 
    while True:                                                                  
        check, frame = video.read()                                              
        if cv2.waitKey(1) & 0xFF == ord('q'):                                    
          break                                                                
                                                                                 
        cv2.imshow('frame', frame)                                               
                                                                                 
        if cv2.waitKey(1) & 0xFF == ord('q'):                                    
            break                                                                
        #rotateMotor(servo, frame.shape[:2][0], pos[0])
        
def rotate_motor(servo, pos):                                                    
    servo.value = pos                                                            
    print(pos)                                                                   
    cv2.waitKey(2)                                                              
    
def clear_recognizer(video, object_detector):                                    
    cv2.waitKey(3)                                                               
    for i in range(HISTORY_VAR):                                                 
        ret, frame = video.read()                                                
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                       
        object_detector.apply(img_gray)                                          
        cv2.waitKey(1)       
        
def main():                                                                      
    servo_pos = 0                                                                
    resolution_multiplier = 0.6                                                  
    x_orig = 640*resolution_multiplier/2                                         
    y_orig = 480*resolution_multiplier/2                                         
    servo = Servo(19, pin_factory = servo_factory)                               
    servo.value = servo_pos                                                      
                                                                                 
    video = cv2.VideoCapture(0)                                                  
    object_detector = cv2.createBackgroundSubtractorMOG2(history=HISTORY_VAR, varThreshold=7)         
    video.set(3,640 * resolution_multiplier)                                     
    video.set(4,480 * resolution_multiplier)                                     
                                                                                
    clear_recognizer(video, object_detector)                                     
    counter = 0                                                                  
    while True:                                                                  
        x = x_orig                                                               
        y = y_orig                                                               
        w = h = 0                                                                
        ret, frame = video.read()                                                
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                       
                                                                                 
        mask = object_detector.apply(img_gray)                                   
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)               
        kernel = 255*np.ones((4,4), np.uint8)                                    
        #mask_filter = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)            
        mask_filter = cv2.medianBlur(src=mask, ksize=5)                          
        kernel = 255*np.ones((16, 16), np.uint8)                                 
        mask_blur = cv2.dilate(mask_filter, kernel, iterations=1)                
                                                                                 
        contours, hierarchy = cv2.findContours(mask_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)          
                                                                                 
        max_area = -1                                                            
        max_pos = None                                                           
        for i in contours:                                                       
            if cv2.contourArea(i) > max_area:                                    
                max_pos = cv2.boundingRect(i)                                    
                max_area = cv2.contourArea(i) 
        
        if max_pos:                                                              
            [x,y,w,h] = max_pos                                                  
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)                
                                                                                 
                                                                                 
        if(x < 0.25*640*resolution_multiplier and x+w < 0.5*640*resolution_multiplier ):                                      
            servo_pos = min(servo_pos + 0.1, 0.7)                                
            rotate_motor(servo, servo_pos)                                       
            clear_recognizer(video, object_detector)                             
        elif(x+w > 0.75*640*resolution_multiplier and x > 0.5*640*resolution_multiplier):                                    
            servo_pos = max(servo_pos - 0.1, -0.7)                               
            rotate_motor(servo, servo_pos)                                       
            clear_recognizer(video, object_detector)                             
                                                                                 
        cv2.imshow('frame', frame)                                               
        cv2.imshow('mask', mask)                                                 
        cv2.imshow('mask adj.', mask_blur)                                       
        # mid_x = (2 * x + w) // 2                                               
        # rotateMotor(servo, 120, mid_x)                                         
        key = cv2.waitKey(15)                                                    
        if key == ord('q'):                                                      
            break                                                                
                                                                                 
    video.release()                                                              
    cv2.destroyAllWindows()                                                      

if __name__ == "__main__":                                                       
    main()                        
