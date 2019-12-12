from pyimagesearch.keyclipwriter import KeyClipWriter
import datetime
import time
import cv2
from threading import Thread
from queue import Queue
from OVdetection import OVdetection
from OVrecognition import OVrecognition
import argparse
import numpy as np

from augmentation import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-md", "--md", help="Required. Path to an .xml file with a trained model.",
				 default="model/INT8/detection.xml",
				  type=str) 
ap.add_argument("-mrh", "--mrh", help="Required. Path to an .xml file with a trained model.",
				 default="model/FP32/recognition.xml",
				  type=str)   


ap.add_argument("-l", "--cpu_extension",
					help="Optional. Required for CPU custom layers. Absolute path to a shared library with the "
						"kernels implementations.", type=str, default="./cpu_extension_avx2.dll")

ap.add_argument("-d", "--device",
					help="Optional. Specify the target device to infer on; CPU, GPU, FPGA, HDDL or MYRIAD is "
						"acceptable. The demo will look for a suitable plugin for device specified. "
						"Default value is CPU", default="CPU", type=str)
ap.add_argument("-c", "--config",
					help="Optional. depend on different model", default="config/detection.yml", type=str)
ap.add_argument("-i", "--input", 
	help="path to input video", default='testinput/test_WoT_1.mp4')
ap.add_argument("-o", "--output",
	help="path to output directory", default='D:/output/')
ap.add_argument("-b", "--buffer_size", type=int, default=240,
	help="buffer size of video clip writer")
ap.add_argument("-cd", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-f", "--fps", type=int, default=30,
	help="FPS of output video")
ap.add_argument("-g", "--gameName", type=str, default='WoT',
	help="Name of Game: PUBG, LOL, WoT")
ap.add_argument("-df", "--detectFrames", type=int, default=15,
	help="How many frames detect once")
args = vars(ap.parse_args())

do_detect_flag = True
#ROI [y, offset_y, x, offset_x]
if args["gameName"] == 'PUBG':
	ROI = [712,96,720,512]
if args["gameName"] == 'LOL':
	ROI = [0,32,1665,96]
if args["gameName"] == 'WoT':
	ROI = [852,64,252,32]

print("[INFO] loading video...")
cap = cv2.VideoCapture(args["input"])
frames_num = cap.get(7)
stop_frame = int(frames_num - frames_num%args["detectFrames"])
print("stop frame:", frames_num, stop_frame)

print("load model")
detect_model = OVdetection(args["md"],args["device"],args["cpu_extension"],args["config"],ROI)
detect_model.load_model()
recogh_model = OVrecognition(args["mrh"],args["device"],args["cpu_extension"])
recogh_model.load_model()

#init for save video
kcw = KeyClipWriter(bufSize=args["buffer_size"])
consecFrames = 0
frame_idx = 0
frozen_detect = False
frozen_frame = 0
log = open('log.txt', 'w')
def model_inference(kcw,Q):
	print("do inference")
	detection_time = 0
	recogntion_time = 0
	inference_idx = 0
	consecFrames = 0
	frame_idx = 0
	frozen_frame = 0
	frozen_detect = False
	killNum = 0
	rec_kill = 0
	assNum = 0
	WoT_log = [0,0,0]
	WoT_damage = 0
	WoT_block = 0
	WoT_assist = 0
	# kill_list = []
	# global all_kill
	# ass_list = []
	while True:
		if frame_idx == stop_frame:
			break
		if not Q.empty():
			#frame_idx += 1
			updateConsecFrames = True
			if args["gameName"] == 'PUBG':
				for i in range(args["detectFrames"]):
					temp = Q.get()
					frame_idx += 1
					if frozen_detect and frozen_frame < 9*args["detectFrames"]:
						frozen_frame += 1
						continue
					kcw.update(temp)
				if frozen_detect and frozen_frame < 9*args["detectFrames"]:
					continue
			if args["gameName"] == 'LOL' or args["gameName"] == 'WoT':
				for i in range(args["detectFrames"]):
					temp = Q.get()
					frame_idx += 1
					kcw.update(temp)

			#cur_frame = temp.copy()
			#cur_frame = temp[712:712+96, 720:720+512].copy()
			#print(frame_idx)
			cur_frame = temp[ROI[0]:ROI[0]+ROI[1], ROI[2]:ROI[2]+ROI[3]].copy()
			#cv2.imwrite(str(frame_idx) + '.jpg', cur_frame)
			detect_flag = False
			start = time.time()
			inference_idx += 1
			bboxes = detect_model.infer([cur_frame])
			end = time.time()
			detection_time += end - start
			predicted = []
			cur_frame = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
			for i , box in enumerate(bboxes[0]):
				recog_start = time.time()
				newim = affine(cur_frame,box,None,i,120,32)
				text = recogh_model.infer([newim])
				recog_end = time.time()
				recogntion_time += recog_end - recog_start
				#print("recog:{}s".format(recogntion))
				predicted.append(text)
				if args["gameName"] == 'PUBG':
					if text == "killed" or text == "kill":
						print(text)
						detect_flag = True
						break
				if args["gameName"] == 'LOL':
					if len(text) == 5 and int(text[0]) != rec_kill:
						killNum += 1
						rec_kill = int(text[0])
						print(killNum, 'Kill')
						detect_flag = True
						# kill_list.append(frame_idx)
						# new_kill = {f for f in range(frame_idx - 180, frame_idx + 180)}
						# all_kill = all_kill | new_kill
						cv2.imwrite(str(killNum) + '.jpg', temp)
						break
					if len(text) > 5 and int(text[0]) > 0 and int(text[:2]) != rec_kill:
						killNum += 1
						rec_kill = int(text[:2])
						print(killNum, 'Kill')
						detect_flag = True
						# kill_list.append(frame_idx)
						# new_kill = {f for f in range(frame_idx-180, frame_idx+180)}
						# all_kill = all_kill | new_kill
						cv2.imwrite(str(killNum) + '.jpg', temp)
						break
					if int(text[-1]) > assNum and assNum < 9:
						assNum += 1
						print(assNum, 'Assist')
						detect_flag = True
						# ass_list.append(frame_idx)
						break
					if int(text[-2:]) > assNum and assNum >= 10:
						assNum += 1
						print(assNum, 'Assist')
						detect_flag = True
						# ass_list.append(frame_idx)
						break
				if args["gameName"] == 'WoT':
					text =  text.replace('z', '2')
					if int(text) !=  WoT_log[i]:
						WoT_log[i] = int(text)
						detect_flag = True
						print("Damage: ", WoT_log[0])
						print("Block: ", WoT_log[1])
						print("Assist: ", WoT_log[2])
			#print(kills)
			line = 'frame' + str(frame_idx) + ' ' + str(WoT_log[0]) + ' ' + str(WoT_log[1]) + ' ' + str(WoT_log[2]) + '\n'
			log.write(line)
			updateConsecFrames = not detect_flag
			frozen_detect = detect_flag
			# only proceed if at least one contour was found
			if detect_flag:
				# cv2.imwrite("output/" + str(frame_idx) + ".png",crop_area[:, :, ::-1])
				# reset the number of consecutive frames with
				# *no* action to zero 
				# froze next frame 
				consecFrames = 0
				frozen_frame = 0
				# if we are not already recording, start recording
				if not kcw.recording:
					print("record")
					detect_flag = False
					timestamp = datetime.datetime.now()
					p = "{}/{}.avi".format(args["output"], timestamp.strftime("%Y-%m-%d-%H-%M-%S") + '-sparkletime')
					kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),
						args["fps"])
					if kcw.first_flag:
						kcw.first_flag = False
			# otherwise, no action has taken place in this frame, so
			# increment the number of consecutive frames that contain
			# no action
			if updateConsecFrames:
				consecFrames += 1
			
			# if we are recording and reached a threshold on consecutive
			# number of frames with no action, stop recording the clip
			if kcw.recording and consecFrames == 3:
				print("finish")
				kcw.finish()

		if inference_idx == 100:
			print(inference_idx,detection_time,recogntion_time)
			if detection_time == 0 and recogntion_time == 0 :
				print("fps:{}".format("inference in 0s"))
			else:
				print("fps:{}".format(inference_idx/(detection_time + recogntion_time)))
			inference_idx = 0
			detection_time = 0
			recogntion_time = 0
TQ = Queue()
thread = Thread(target=model_inference,args=(kcw,TQ))
thread.daemon = True
thread.start()

while True:
	# grab the current frame, crop area, resize it, and initialize a
	# boolean used to indicate if the consecutive frames
	# counter should be updated
	frame_idx += 1
	ret, frame = cap.read()
	if ret is False:
		break

	TQ.put(frame)
	cv2.imshow(args["gameName"], frame)
	key = cv2.waitKey(5) & 0xFF

	#if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# for key_frame in all_kill:
# 	print(key_frame)
# 	cap.set(cv2.CAP_PROP_POS_FRAMES,key_frame)
# 	ret, frame = cap.read()
# 	#writer = cv2.VideoWriter(pp, 'MJPG', args["fps"], (frame.shape[1], frame.shape[0]), True)
# 	out.write(frame)

# while True:
# 	# grab the current frame, crop area, resize it, and initialize a
# 	# boolean used to indicate if the consecutive frames
# 	# counter should be updated
# 	frame_idx += 1
# 	print(frame_idx)
# 	ret, frame = cap.read()
# 	if ret is False:
# 		break
# 	if frame_idx in all_kill:
# 		print('record')
# 		out.write(frame)
print('Done')
thread.join()

# do a bit of cleanup
cv2.destroyAllWindows()
