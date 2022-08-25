import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=0.8,trackCon=0.8):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,1,self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
    	if img is not None: 
    		imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    		self.results=self.hands.process(imgRGB)
    		if self.results.multi_hand_landmarks:
    			self.mpDraw.draw_landmarks(img,self.results.multi_hand_landmarks[0],self.mpHands.HAND_CONNECTIONS)
    		return img

        
    def findPostion(self,img,handNo=0):
        h,w,c=img.shape
        lmList=[]
        if self.results.multi_hand_landmarks:
            for idno,lm in enumerate(self.results.multi_hand_landmarks[0].landmark):
                cx,cy=lm.x,lm.y
                lmList.append([idno,cx,cy])
        return lmList
        


def main():
    pass

if __name__=="__main__":
    main()
    
