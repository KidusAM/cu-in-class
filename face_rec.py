import face_recognition                                                          
import cv2                                                                       
import numpy as np                                                               
import os                                                                        
import requests, json                                                            
import RPi.GPIO as GPIO                                                          
import time                                                                      
                                                                                  
LED_PIN = 7                                                                      
GPIO.setmode(GPIO.BOARD)                                                         
GPIO.setup(LED_PIN, GPIO.OUT)                                                    
                                                                                 
def LED_confirm_student():                                                       
    GPIO.output(LED_PIN, True)                                                   
    time.sleep(1)                                                                
    GPIO.output(LED_PIN, False)                                                  
                                                                                 
                                                                                 
def get_known_faces():                                                           
    known_face_names = []                                                        
    known_face_encodings = []                                                                                                                                     
    
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]            
    for f in files:                                                              
        if f.endswith(".jpg") or f.endswith(".png"):                             
            face = face_recognition.load_image_file(f)                           
            known_face_encodings.append(face_recognition.face_encodings(face)[0])
            known_face_names.append(f.split(".")[0])                             
                                                                                 
    return known_face_names, known_face_encodings                                
                                                                                 
def send_student(class_name, student_name):                                      
    msg = {"class_id" : class_name, "student_id": student_name}                  
    msg = json.dumps(msg)                                                        
    url = 'https://tiaa5tbuqi.execute-api.us-east-1.amazonaws.com/v1/mark_present'
    send = requests.post(url, data = msg) 
    
def main():                                                                      
    # Initialize some variables                                                  
    video_capture = cv2.VideoCapture(0)                                          
    video_capture.set(3, 320)                                                    
    video_capture.set(4, 240)                                                    
    face_locations = []                                                          
    face_encodings = []                                                          
    face_names = []                                                              
    process_this_frame = True                                                    
                                                                                 
    known_face_names, known_face_encodings = get_known_faces()                   
                                                                                 
    while True:                                                                  
        # Grab a single frame of video                                           
        ret, frame = video_capture.read()                                        
                                                                                 
        # Only process every other frame of video to save time                   
        if process_this_frame:                                                   
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)            
                                                                                 
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]                            
                                                                                 
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)    
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_names = []                                                      
            for face_encoding in face_encodings:                                 
                # See if the face is a match for the known face(s)               
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"                                                 
                                                                                 
                if True in matches:                                              
                    match_index = matches.index(True)                            
                    name = known_face_names[match_index]                         
                                                                                 
                if name != "Unknown":                                            
                    send_student("IoT", name)                                    
                    LED_confirm_student()                                        
                                                                                 
                face_names.append(name)                                          
                                                                                 
        process_this_frame = not process_this_frame
    
        # Display the results                                                    
        for (top, right, bottom, left), name in zip(face_locations, face_names): 
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4                                                             
            right *= 4                                                           
            bottom *= 4                                                          
            left *= 4                                                            
                                                                                 
            # Draw a box around the face                                         
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)   
                                                                                 
            # Draw a label with a name below the face                            
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX                                       
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                                                                                 
                                                                                 
        # Display the resulting image                                            
        cv2.imshow('Video', frame)                                               
                                                                                 
        # Hit 'q' on the keyboard to quit!                                       
        if cv2.waitKey(1) & 0xFF == ord('q'):                                    
            break                                                                
                                                                                 
    # Release handle to the webcam                                               
    video_capture.release()                                                      
    cv2.destroyAllWindows()                                                      
    GPIO.cleanup()                                                               
                                                                                 
if __name__ == "__main__":                                                       
    main()             
