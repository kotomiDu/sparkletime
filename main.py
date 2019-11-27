#coding=utf-8
import cv2
from OVdetection import OVdetection
from OVrecognition import OVrecognition
import os
import argparse



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
				
ap.add_argument("-g", "--gameName", type=str, default='PUBG',
					help="Name of Game: PUBG, LOL")
args = vars(ap.parse_args())


from glob import glob
import numpy as np
from augmentation import *
import os
import time
if __name__=='__main__':
	
	detect_model = OVdetection(args["md"],args["device"],args["cpu_extension"],args["config"], ROI)
	print("loading detection model")
	detect_model.load_model()
	recogh_model = OVrecognition(args["mrh"],args["device"],args["cpu_extension"])
	print("loading recognition model")
	recogh_model.load_model()
	print("models loaded")
	

	totaltime = 0
	detection = 0
	recognition = 0
	
	#default: only  one image 
	imlist = glob('./testinput/*.jpg')
	start = time.time()
	for idx,imfn in enumerate(imlist):
		
		im = cv2.imread(imfn)
		imname = os.path.basename(imfn)
		detect_start = time.time()
		bboxes = detect_model.infer([im])
		predicted = []
		im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		for i , box in enumerate(bboxes[0]):
			
			ori_box = box
			recog_start = time.time()
			newim = affine(im,ori_box,imfn,i,120,32)
			text = recogh_model.infer([newim])
			recog_end = time.time()
			recogntion = recog_end - recog_start
			#print("recog:{}s".format(recogntion))
			predicted.append(text)
		print(imname,predicted)
			
	end = time.time()
	totaltime = end - start
	print("totaltime:{}s".format(totaltime))





	
	
		
