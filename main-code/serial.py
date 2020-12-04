import time
#import time library.

time.sleep(2)
#wait for the opening of the serial.

import os,sys
# path operating

# Alternate to the working path
print('========= Access the local Path =========')
working_path = os.getcwd()
print("Previous Path:\t"+working_path)
# access the local path
        
print('========= Change the local Path =========')
target_path = "/home/zzp1012/Desktop/Midea/camera"
os.chdir(target_path)   
# change working directory

path = os.getcwd()
print("Changed to:\t"+path)
# verifsy

file_current = "./res.txt"
f = open(file_current, "w+")
f.close
# clear up the file

import serial
#import serial library

ser = serial.Serial('/dev/ttyUSB0',9600)
if ser.isOpen == False:
    ser.open()
print("successfully open the serial")
#open the serial.

initial_weight = ser.readline()
initial_weight = int(bytes.decode(initial_weight))

if initial_weight < 0:
    exit(0)
#force to exit. 

if initial_weight > 1000000:
    recorrect_initial_weight = initial_weight - 1000000
else:
    recorrect_initial_weight = initial_weight

weights = [recorrect_initial_weight]
#define and initialize some varibles relavent to weight

def check_if_capture(temp):
    if temp > 1000000:    
        return True
    else:
        return False
#check the weight of plate.
    
def check_if_stable_weight():
    list_of_weight = []
    while True:
        list_of_weight = []
        for temp in range(3):
            temp = ser.readline()
            temp = int(bytes.decode(temp))
            list_of_weight.append(temp)
        if abs(list_of_weight[0] - list_of_weight[1]) < 30 and abs(list_of_weight[1] - list_of_weight[2]) < 30:
            break
    weights.append((list_of_weight[0] + list_of_weight[1] + list_of_weight[2])/3 - weights[-1])
    print("successfully get the stable weight")

import cv2
import numpy as np
#import opencv2 library.
import threading
#import threading library, muliple processes.
import time
#import time library

camera = cv2.VideoCapture(0)
print("Successfully Open the Camera")
#open the camera.
print("Wait for 2 seconds")
time.sleep(2)
print("------Finish------")
#wait for several seconds to prepare the camera.

camera.set(cv2.CAP_PROP_FRAME_WIDTH,120)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,120)
camera.set(cv2.CAP_PROP_FPS, 25)
#set the resolution of the camera.

thread_lock = threading.Lock()
#define the lock to limit the permission to a shared varibable.

threads = []
#define the list of thread.

frames = []
#shared variables.

class thread_get_frame(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        
        self.switch_weights = 0
         #check if add new weights to the weights list.
        
        self.temp_frame = []
    #constructor
    
    def run(self):
        new_frame_counter = 0
        while True:
            temp_weights = ser.readline()
            temp_weights = int(bytes.decode(temp_weights))
            #get the new weight and the message that if capture new fram
            
            if temp_weights < 0:
                exit(0)
            #force to quit
            if check_if_capture(temp_weights):
                self.switch_weights = 1
                #ban refreshing the weights list.
                
                (ret, new_frame) = camera.read()
                new_frame_counter += 1
                #capture the frame.
                
                new_frame = cv2.resize(new_frame,(224,224),interpolation = cv2.INTER_AREA)
                
                cv2.imwrite("/home/zzp1012/Desktop/Midea/camera/test%d.jpg" % new_frame_counter,new_frame)
                
                new_frame = new_frame.reshape((1, new_frame.shape[0], new_frame.shape[1], new_frame.shape[2]))
                # reshape data for the model
                
                if not ret:
                    print("------no camera------")
                    break
                self.temp_frame.append(new_frame)
                #check if successfully open the camera.
                
                print("---get the new frame---")
            else :
                if self.switch_weights == 1:
                    check_if_stable_weight()
                    self.switch_weights = 0
                if self.temp_frame:
                    thread_lock.acquire()
                    frames.append(self.temp_frame)
                    thread_lock.release()
                self.temp_frame = []
    #main boby
    
    def __del__(self):
        print(self.name + "thread over")
    #destructor
#process to get the frame.
        
def compare_possibility(temp_target_res,temp_target_accuracy):
    return temp_target_res[0],temp_target_accuracy[0]

class thread_analyze_frame(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        self.frame_counter = 1
    #constructor
    
    def run(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        # from keras.applications.vgg16 import VGG16
        # model = VGG16()
        # from keras.applications.vgg16 import preprocess_input
        # from keras.applications.vgg16 import decode_predictions
        #import keras module.

        from keras.applications.resnet50 import ResNet50
        from keras.preprocessing import image
        from keras.applications.resnet50 import preprocess_input, decode_predictions

        model = ResNet50(weights='imagenet')
        
        while True:
            if frames:
                temp_target_res = []
                temp_target_accuracy = []
                
                thread_lock.acquire()
                
                for image in frames[0]:
                    image = preprocess_input(image)
                    # prepare the image for the VGG model.
                    
                    yhat = model.predict(image)
                    # Make a prediction.
                    
                    ## predict the probability across all output classes.
                    label = decode_predictions(yhat)
                    # convert the probabilities to class labels.

                    label = label[0][0]
                    # retrieve the most likely result, e.g. highest probability.

                    target_res = label[1]
                    target_accuracy = label[2]*100

                    print("++++++ Print The Result ++++++")
                    print('Predicted:', decode_predictions(yhat, top=3)[0])
                    #print('%s (%.2f%%)' % (target_res, target_accuracy))
                    # print the classification.
                    
                    temp_target_res.append(target_res)
                    temp_target_accuracy.append(target_accuracy)
                    #include these value into list.
                
                (final_target_res,final_target_accuracy) = compare_possibility(temp_target_res, temp_target_accuracy)
                
                f = open(file_current,"a+")
                f.write("%s %d\n" % (final_target_res,weights[self.frame_counter]))
                f.close()
                # Write into the file.
                
                thread_lock.release()
                    
                print("------ Check the content of file ------")
                f = open(file_current,"r")
                lines = f.readlines()
                result = list()
                for line in lines:
                    line = line.strip('\n')
                    result.append(line)
                print(result)
                f.close()
                # Check the content of the file.

                thread_lock.acquire()
                frames.pop(0)
                thread_lock.release()
                #delete the first element of the list frames.
                
                self.frame_counter += 1
    #main boby
    
    def __del__(self):
        print(self.name + "thread over")
    #destructor
        
thread_capture = thread_get_frame("capture frame")
thread_analyze = thread_analyze_frame("analyze frame")
#get the instance from class.

thread_capture.start()
thread_analyze.start()
#start the threads.

threads.append(thread_capture)
threads.append(thread_analyze)

for thr in threads:
    thr.join()
    
camera.release()
#release all the cameras.

print("all threads over")


#two problems : import another sensor to control getting frame, the weights, the algorithm for comparsion, send the final results to the lcd screen.