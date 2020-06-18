def checkSpecialKill(imgbox,imgname):
	specialHightLight=[]
	killway={
		'killbox':'',
		'grenadebox':'',
		'smokebox':'',
		'headshotbox':'',
		'penetrationbox':'',
		'cardiacbox':''
	}
	for i , box in enumerate(imgbox):
		pts = np.array(box).reshape((-1,1,2))
		cv2.polylines(crop_im,[pts],True,(0,255,255),2)
		newim = affine(im,box,imfn,i,120,32)
		text = recogh_model.infer([newim])
		if text != '':
			cv2.putText(padding_image, text, (pts[1,0,0],20*(i+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1, cv2.LINE_AA)
			res_im = np.concatenate((padding_image, crop_im), axis=0)
			cv2.imwrite("output/{}_text.png".format(imname),res_im)
			if text == 'kill':
				killway['killbox']= pts
			elif text == 'smoke':
				killway['smokebox'] = pts
			elif text == 'grenade':
				killway['grenadebox'] = pts
			elif text == 'cardiac':
				killway['cardiacbox'] = pts
			elif text == 'head':
				killway['headshotbox']=pts
			elif text == 'penetration':
				killway['penetrationbox']=pts
		
	if  killway['killbox']  is not '':
		killpointy = int(killway['killbox'][0][0][1])
		if  killway['grenadebox'] is not '':
			if int( killway['grenadebox'][3][0][1])+20 > killpointy:
				specialHightLight.append('grenade')
		if  killway['smokebox'] is not'':
			if int( killway['smokebox'][3][0][1])+20 > killpointy:
				specialHightLight.append('smoke')
		if  killway['headshotbox'] is not'':
			if int( killway['headshotbox'][3][0][1])+20 > killpointy:
				specialHightLight.append('head')
		if  killway['penetrationbox'] is not '':
			if int( killway['penetrationbox'][3][0][1])+20 > killpointy:
				specialHightLight.append('penetration')
		if  killway['cardiacbox']  is not'':
			specialHightLight.append('cardiac')
	if len(specialHightLight) is not 0:
		print('specialHightLight   ' + imgname + ':'+str(specialHightLight))