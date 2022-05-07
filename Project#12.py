"""
Usain Bolt Pose Detection Project

This program chooses between sample videos and camera input to
detect the number of times pose has been pulled off with a little leniency.
Written by:
2020-MC-28 Ibrahim Haroon
2020-MC-01 Rana Umer

ibrahimharoon258@gmail.com
"""

#import libraries
import tkinter
import cv2
from tkinter import*
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np

wangles=[]

def calculate_angle(a,b,c):     #Joint Angle Calculator
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360-angle

    return angle


#GUI Window Setup
win = Tk()
win.title('Usain Bolt Pose Detector')
win.geometry('800x650+30+30')
win.resizable(False,False)
win.config(cursor='box_spiral')
bg = PhotoImage(file = "bg.png")

label1 = Label( win, image = bg)
label1.place(x = 0, y = 0)

l1=Label(win, text = "Usain Bolt Pose Detector", font = ("Helvetica 15 Bold", 35))
l1.place(x = 100, y = 25, width=550, height=40)

var1 = IntVar()
l_h = Scale(win, label="Resize", from_=300, to=650, orient=HORIZONTAL, variable=var1, activebackground='#339999')
l_h.set(0)
l_h.place(x=10, y=120)

#variables
detected=False
counter=0
w = 300
h = 300


mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
pose= mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)

#Reference Image
image=cv2.imread("usainbolt2.jpeg")  #Reference Image
results=pose.process(image)

landmarks=results.pose_landmarks.landmark

#Joints

l_shoulder  =[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
l_elbow     =[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
l_wrist     =[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
r_shoulder  =[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
r_elbow     =[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
r_wrist     =[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
r_hip=      [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
l_hip=      [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
r_knee=     [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
l_knee=     [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
r_ankle=    [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
l_ankle=    [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
r_heel=     [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
l_heel=     [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
r_footindex=[landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
l_footindex=[landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
ijoints=[l_shoulder,l_elbow,l_wrist,r_shoulder,r_elbow,r_wrist,r_hip,l_hip,r_knee,l_knee,r_ankle,
l_ankle,r_heel,l_heel,r_footindex,l_footindex]

#Angles

right_arm=calculate_angle(r_shoulder,r_elbow,r_wrist)
left_arm=calculate_angle(l_shoulder,l_elbow,l_wrist)
right_arm_hip=calculate_angle(r_elbow,r_shoulder,r_hip)
left_arm_hip=calculate_angle(l_elbow,l_shoulder,l_hip)
right_hip_knee=calculate_angle(r_shoulder,r_hip,r_knee)
left_hip_knee=calculate_angle(l_shoulder,l_hip,l_knee)
right_knee_ankle=calculate_angle(r_hip,r_knee,r_ankle)
left_knee_ankle=calculate_angle(l_hip,l_knee,l_ankle)
right_ankle_heel=calculate_angle(r_knee,r_ankle,r_heel)
left_ankle_heel=calculate_angle(l_knee,l_ankle,l_heel)
right_heel_fi=calculate_angle(r_ankle,r_heel,r_footindex)
left_heel_fi=calculate_angle(l_ankle,l_heel,l_footindex)

#ref image angles
iangles=[right_arm,left_arm,right_arm_hip,left_arm_hip]#,right_hip_knee,left_hip_knee]

mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
mp_drawing.DrawingSpec(color=(194, 100, 64),thickness=2,circle_radius=2),
mp_drawing.DrawingSpec(color=(200, 122, 30),thickness=2,circle_radius=2))

global cap,waja
waja=0 #initially zero

def vout(vname):
    global cap,waja
    waja +=1 #value change to 1 when video is run
    cap = cv2.VideoCapture(vname)
    cap.set(cv2.CAP_PROP_FPS, 30)

    def select_img():
        global wangles
        global counter,detected
        global w,h
        _, img = cap.read()
        img = cv2.resize(img, (w, h))
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results=pose.process(rgb)
        w = l_h.get()

        #set resize
        if w>350:
            h=400
        else:
            h=300


        label2 = Label(win, width=w, height=h)
        label2.place(x=10, y=200)


        try:
                landmarks=results.pose_landmarks.landmark

                #Joints

                l_shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                l_wrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                r_shoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                r_wrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                r_hip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                l_hip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                r_knee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                l_knee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                r_ankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                l_ankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                r_heel=[landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                l_heel=[landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                r_footindex=[landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                l_footindex=[landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

                wjoints=[l_shoulder,l_elbow,l_wrist,r_shoulder,r_elbow,r_wrist,r_hip,l_hip,r_knee,l_knee,r_ankle,
                l_ankle,r_heel,l_heel,r_footindex,l_footindex]

                #Angles

                right_arm=calculate_angle(r_shoulder,r_elbow,r_wrist)
                left_arm=calculate_angle(l_shoulder,l_elbow,l_wrist)
                right_arm_hip=calculate_angle(r_elbow,r_shoulder,r_hip)
                left_arm_hip=calculate_angle(l_elbow,l_shoulder,l_hip)
                right_hip_knee=calculate_angle(r_shoulder,r_hip,r_knee)
                left_hip_knee=calculate_angle(l_shoulder,l_hip,l_knee)
                right_knee_ankle=calculate_angle(r_hip,r_knee,r_ankle)
                left_knee_ankle=calculate_angle(l_hip,l_knee,l_ankle)
                right_ankle_heel=calculate_angle(r_knee,r_ankle,r_heel)
                left_ankle_heel=calculate_angle(l_knee,l_ankle,l_heel)
                right_heel_fi=calculate_angle(r_ankle,r_heel,r_footindex)
                left_heel_fi=calculate_angle(l_ankle,l_heel,l_footindex)

                #webcam calculated angles
                wangles=[right_arm,left_arm,right_arm_hip]#,left_arm_hip]#,right_hip_knee,left_hip_knee]

        except:
            pass
        mp_drawing.draw_landmarks(rgb,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(194, 0, 64),thickness=2,circle_radius=2),
        mp_drawing.DrawingSpec(color=(27, 122, 30),thickness=2,circle_radius=2))

        i=0
        dev=[] #Deviation


        while(i<len(wangles)):
            dev.append(abs(wangles[i]-iangles[i])) #Find deviation
            i=i+1

        devp=np.mean(dev)
        if(devp<50):    #Leniency
            displayp=100-((devp/50)*100)    #Angle to Accuracy Percentage Calculator
            if(displayp>=70):           #Success Threshold
                if(displayp>=75): # Counting success threshold
                    if(detected==False):
                        counter=counter+1
                        detected=True
                        countlabel=Label(win,text=str(counter),borderwidth=2, relief="groove")
                        countlabel.place(x = 600, y = 80, width=60, height=25)

                cv2.putText(rgb,str(int(displayp))+"%",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(176, 144, 39),2,cv2.LINE_AA)
            elif(displayp<=50):

                cv2.putText(rgb,str(int(displayp))+"%",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(138, 20, 1),2,cv2.LINE_AA)
            else:
                cv2.putText(rgb,str(int(displayp))+"%",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(44, 140, 6),2,cv2.LINE_AA)
        else:
            detected=False
            cv2.putText(rgb,"0%",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)

        cv2.putText(rgb,str(counter),(300,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)

        #showing on window screen
        image = Image.fromarray(rgb)
        finalImage = ImageTk.PhotoImage(image)
        label2.configure(image=finalImage)
        label2.image = finalImage

        win.after(1, select_img)

    select_img()




def clicked1():
    #if not first time, release previous video first
    global waja,cap

    if waja:
        cap.release()

    vout(0)

def clicked2():
    global waja,cap

    if waja:
        cap.release()

    vout("Test1.mp4")

def clicked3():
    global waja,cap

    if waja:
        cap.release()

    vout("Test2.mp4")

def clicked4():
    global waja,cap

    if waja:
        cap.release()

    vout("Test3.mp4")

def clicked5():
    #set counter to 0
    global counter
    counter=0
    countlabel=Label(win,text=str(counter),borderwidth=2, relief="groove")
    countlabel.place(x = 600, y = 80, width=60, height=25)
def clicked6():
    global waja,cap

    if waja:
        cap.release()
    win.destroy()

#buttons and placement
button1=Button(win,text='Camera',padx=20,pady=20,command=clicked1,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button1.place(x = 10, y = 80, width=65, height=35)
button2=Button(win,text='Sample 1',padx=20,pady=20,command=clicked2,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button2.place(x = 100, y = 80, width=65, height=35)
button3=Button(win,text='Sample 2',padx=20,pady=20,command=clicked3,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button3.place(x = 190, y = 80, width=65, height=35)
button4=Button(win,text='Sample 3',padx=20,pady=20,command=clicked4,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button4.place(x = 280, y = 80, width=65, height=35)
button5=Button(win,text='Reset',padx=20,pady=20,command=clicked5,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button5.place(x = 370, y = 80, width=65, height=35)
button6=Button(win,text='Exit',padx=20,pady=20,command=clicked6,font = ("Helvetica 15 Bold", 10),activebackground='#78d6ff')
button6.place(x = 460, y = 80, width=65, height=35)

l3=Label(win, text = "Count :", font = ("Times New Roman", 10))
l3.place(x = 525, y = 80, width=60, height=25)

win.mainloop()