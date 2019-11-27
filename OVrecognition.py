from openvino.inference_engine import IENetwork, IECore
import logging as log
import sys
import cv2
import yaml
import os
import numpy as np
from metrics import *
import time
np.set_printoptions(threshold = np.inf)
class OVrecognition:
	def __init__(self,model_path,  device, cpu_extension):
		self.model_path = model_path
		self.cpu_extension = cpu_extension
		self.device = device
		self.characters = self.create_character_maps()
		self.nclass = len(self.characters)
		
		self.input_blob = None
		self.out_blob = None
		self.ie = None
		self.net = None
		self.n = None
		self.c = None
		self.h = None
		self.w = None

	def load_config(self,path):
		""" Load saved configuration from yaml file. """

		with open(path,'r') as read_file:

			config = yaml.load(read_file)
		return config

	def load_model(self):
		model_xml = self.model_path
		model_bin = os.path.splitext(model_xml)[0] + ".bin"

		# Plugin initialization for specified device and load extensions library if specified
		log.info("Creating Inference Engine")
		ie = IECore()
		if self.cpu_extension and 'CPU' in self.device:
			ie.add_extension(self.cpu_extension, "CPU")
		# Read IR
		log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
		net = IENetwork(model=model_xml, weights=model_bin)

		if "CPU" in self.device:
			supported_layers = ie.query_network(net, "CPU")
			not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
			if len(not_supported_layers) != 0:
				log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
						  format(args.device, ', '.join(not_supported_layers)))
				log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
						  "or --cpu_extension command line argument")
				sys.exit(1)

		log.info("Preparing input blobs")
		
		self.out_blob = next(iter(net.outputs))
		self.input_blob = next(iter(net.inputs))
		self.net = net
		self.ie = ie
		t1 = time.time()
		self.exec_net = self.ie.load_network(network=self.net, device_name=self.device)
		t2 = time.time()
		print("cost", t2-t1)
		
	def infer(self, inputdata):
		
		self.net.batch_size = len(inputdata)
		
		n,c,h,w =  self.net.inputs[self.input_blob].shape
		seq_len = int(w/4)
		images = np.ndarray(shape=(n,c,h,w))
		for i in range(n):
			#image = cv2.imread(inputdata[i],cv2.IMREAD_COLOR)
			image = inputdata[i]
			if image.shape[:-1] != (h, w):
				#log.warning("Image {} is resized from {} to {}".format(i, image.shape, (h, w)))
				image = cv2.resize(image, (w, h))
				image = np.expand_dims(image, axis=-1)
			#print(image.shape)
			image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
			images[i] = image
		log.info("Batch size is {}".format(n))

		# Start sync inference
		log.info("Starting inference in synchronous mode")
		 # Loading model to the plugin
		log.info("Loading model to the plugin")
		start = time.time()
		
		res = self.exec_net.infer(inputs={self.input_blob: images})
		end = time.time()
		#print("recog1:{}s".format(end-start))

		# Processing output blob
		log.info("Processing output blob")
		output = res[self.out_blob]
		#print(output.shape)
		output = output.transpose((1,0,2)).reshape((n,seq_len,37))
		
		text = self.decode(output[0,:,:])
		
		return text


	def create_character_maps(self):
		""" Creates character-to-int and int-to-character maps. """
		alfabet = '0123456789abcdefghijklmnopqrstuvwxyz'
		char_to_int = {}
		
		int_to_char = []
		for i, l in enumerate(alfabet):
			char_to_int[l] = i
			int_to_char.append(l)
		int_to_char.append(u'卍')
		return int_to_char

	def decode(self,pred):
		char_list = []
		res = ""
		prev_pad = False
		pred = np.expand_dims(pred, axis=0)
		pred_idx = pred.argmax(axis=2)[0]
		'''
		pred_text = pred.argmax(axis=2)[0]
		for i in range(len(pred_text)):
			if pred_text[i] != self.nclass - 1 and ((not (i > 0 and pred_text[i] == pred_text[i - 1])) or (i > 1 and pred_text[i] == pred_text[i - 2])):
				char_list.append(self.characters[pred_text[i]])
		return u''.join(char_list)
		'''
		for idx in pred_idx:
			pred_text = self.characters[idx]
			if pred_text != u'卍':
				if(len(res) == 0 or prev_pad or (len(res)!= 0 and pred_text!= res[-1])):
					prev_pad = False
					res = res + pred_text
			else:
				prev_pad = True
		return res
		
		

	