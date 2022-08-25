import pyfirmata
import cv2
import time
import hand_tracking_module as htm
detector=htm.handDetector(detectionCon=0.7,trackCon=0.5)
pTime=0
cTime=0
wCam,hCam=430,480
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, wCam)
comp_port="COM4"
tipsid=[4,8,12,16,20]
try:
	board = pyfirmata.Arduino(comp_port)
	iter8 = pyfirmata.util.Iterator(board)
	iter8.start()
	pin3 = board.get_pin('d:3:s')
	pin5 = board.get_pin('d:5:s')
	pin6 = board.get_pin('d:6:s')
	pin9 = board.get_pin('d:9:s')
	pin10 = board.get_pin('d:10:s')
	pin11 = board.get_pin('d:11:s')
except Exception as e:
    print(e)
pTime=time.time()
framepassed=0
fps=0

last_pos=[]
counter=0


def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5
ct=0
while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    
    lmlist=detector.findPostion(img)
    #print(lmlist)
    finger=[]
    if len(lmlist)!=0:
        
        #print(f'd1:{d1},d2:{d2}')
        if lmlist[tipsid[0]][1]>lmlist[tipsid[0]-2][1]:
            finger.append(0)
        else:
            finger.append(1)
        
        for i in range(1,5):
            if lmlist[tipsid[i]][2]<.8*lmlist[tipsid[i]-2][2]:
                finger.append(1)
            else:
                finger.append(0)
        print(finger)
        try:
        	if finger[0]==0:
        		pin3.write(0)
        	else:
        		pin3.write(180)
        except Exception as e:
        	print(e)  		
        try:
        	if finger[1]==0:
        		pin5.write(0)
        	else:
        		pin5.write(180)
        except Exception as e:
        	print(e)
        try:
        	if finger[2]==0:
        		pin6.write(0)
        	else:
        		pin6.write(180)
        except Exception as e:
        	print(e)         
        try:
        	if finger[3]==0:
        		pin9.write(0)
        	else:
        		pin9.write(180)
        except Exception as e:
        	print(e)
        try:
        	if finger[4]==0:
        		
        		pin10.write(0)
        	else:
        		pin10.write(180)
        except Exception as e:
        	print(e)

            
    
    cTime=time.time()
    if (cTime-pTime)>0.5:
        pTime=cTime
        fps=framepassed*2
        framepassed=0
    else:
        framepassed=framepassed+1
        
    total=finger.count(1)
    cv2.putText(img,f'FPS:{str(int(fps))}',(10,475),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 0),2)
    
    cv2.imshow("im",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ct=ct+1
cap.release()
cv2.destroyAllWindows()


