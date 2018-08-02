#!/usr/bin/env python

import roslib; roslib.load_manifest('qt_basic_demo')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray

import math

from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

from random import randint



from qt_face.srv import *


import os

DEBUG=1
GESTURE_ACTIVATION=True

# Node example class.
class NodeGame():
    
    def game_start_callback(self, event):
        #print 'Timer called at ' + str(event.current_real)
        print 'Starting the game: ' + str(event.data)
        self.game_mode = int (event.data) 
        
        if( self.game_mode == 0 ):
           self.pub.publish("Robot in Waiting mode")
        elif( self.game_mode == 1 ):
            self.pub.publish("Lateral training selected")
        elif( self.game_mode == 2 ):
            self.pub.publish("Frontal training selected")
            
        self.movementGo == False    
        self.loop
        
    ##This timer is to reset the old picture, or it can flood the text to speech system
    def timer_callback(self, event):
        #print 'Timer called at ' + str(event.current_real)
        if (self.recognition_locked == 0):
            self.old_action = ""

        
        
    def face_and_sound_call(self,face, audio):
        print ("trying to call the service")

        # rospy.wait_for_service('ChangeQTFace')
        rospy.wait_for_service('call_new_face')
        try:
            # call_new_face = rospy.ServiceProxy('ChangeQTFace', ChangeQTFace)
            call_new_face = rospy.ServiceProxy('call_new_face', ChangeQTFace)
            self.play_sound_pub.publish(str(audio))
            resp1 = call_new_face(face,str(audio),0)
            print 'success equals {}'.format(resp1)
        except rospy.ServiceException, e:
            # print "Service call failed: %s"%e
            print "Service call failed: {}".e
        
        
    def objectCallback(self, data):
        
        if self.recognition_locked == 0 :
            self.recognition_locked += 1
            if (False):
                rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
                rospy.loginfo("====")
                
            
            if data.data:
                # image_id = int(data.data[0])
                image_id = int(data.data)
                recognized_value = image_id - 1
                new_action = self.faces[recognized_value]
                
                
                if (DEBUG):
                    print image_id
                    print new_action
                
                if self.old_action != new_action:
                    self.old_action = new_action
                    
                    ##START Commands##
                    if image_id == 1 :
                        rospy.loginfo("Action 1 initiated ...........")
                        self.face_and_sound_call("ava_talking", 1)
                        v_gesture = "bye_bye_gesture"
                        self.gesture_player_pub.publish(v_gesture)
                        self.face_and_sound_call("ava_talking", 2)
                        self.face_and_sound_call("ava_happy", "NOSOUND")
                        self.face_and_sound_call("ava_talking", 3)
                        self.face_and_sound_call("ava_talking", 4)
                        rospy.loginfo("Action 1 ended ...........")
                    elif image_id == 2 :
                        rospy.loginfo("Action 2 initiated ...........")
                        self.face_and_sound_call("ava_talking", 5)
                        self.face_and_sound_call("ava_surprise", "NOSOUND")
                        rospy.loginfo("Action 2 ended ...........")
                    elif image_id == 3 :
                        rospy.loginfo("Action 3 initiated ...........")
                        self.face_and_sound_call("ava_talking", 6)
                        v_gesture = "bye_bye_gesture"
                        self.gesture_player_pub.publish(v_gesture)
                        self.face_and_sound_call("ava_talking", 7)
                        self.face_and_sound_call("ava_talking", 8)
                        self.face_and_sound_call("ava_sad", 9)
                        rospy.loginfo("Action 3 ended ...........")
                    
                    ##END Commands##
                    
            self.recognition_locked -= 1
        
            

    def __init__(self):
        self.game_mode = 0
        self.game_status = False
        self.last_moment = 0        
        self.moment_status = 0  
        self.last_moment_status = 0
        self.loop = 0
        self.enc_sentences = []
        self.faces = ["sad", "happy", "surprise", "disgusted", "angry"]

        self.movementGo = False
        self.old_action = ""
        self.recognition_locked = 0
        
        
        #self.sound_relevant_path = "/home/odroid/catkin_ws/src/qt_basic_system/qt_emahid_demo/config/Audio/"

        
        
        rospy.Timer(rospy.Duration(8), self.timer_callback)

        # rospy.Subscriber("/objects", Float32MultiArray, self.objectCallback)
        rospy.Subscriber("/trigger", String, self.objectCallback)
        
        rospy.Subscriber("/qt_basic_demo/mode", String, self.game_start_callback)
        
        self.voice_pub = rospy.Publisher('/robot/voice', String, queue_size=10)
        self.play_sound_pub = rospy.Publisher('/qt_playsound/play_song', String, queue_size=10)
        self.gesture_player_pub = rospy.Publisher('/qt_movement/playGestureFromFile', String, queue_size=10)
        self.emotion_generation_pub = rospy.Publisher('/qt_face/setEmotion', String, queue_size=10)
        
        rospy.loginfo("Starting QT Basic game")
        
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()
        print "exit"

    
# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('qt_game', anonymous=True)
    rospy.loginfo("This node is updated")
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        ne = NodeGame()
    except rospy.ROSInterruptException: pass
    
