import os
import cv2
import math
import torch
import random
import argparse
import numpy as np
import torch.nn as nn
from PIL import Image
import torch.nn.functional as F
from stackhourglass import stackhourglass
import torchvision.transforms as transforms

parser = argparse.ArgumentParser(description='PSMNet')
parser.add_argument('--loadmodel', default='./trained_model.tar',
					help='loading model')
parser.add_argument('--left_img_path', default= './kitti_data_tiny/raw/2011_09_26/2011_09_26_drive_0001_sync/image_02/data/',
					help='load model')
parser.add_argument('--right_img_path', default= './kitti_data_tiny/raw/2011_09_26/2011_09_26_drive_0001_sync/image_03/data/',
					help='load model')    

args = parser.parse_args()
cuda_available = torch.cuda.is_available()

# Seed value for cuda
torch.manual_seed(1)
torch.cuda.manual_seed(1)

model = stackhourglass(192)

model = nn.DataParallel(model, device_ids=[0])
model.cuda()

if args.loadmodel is not None:
	print('load PSMNet')
	state_dict = torch.load(args.loadmodel)
	model.load_state_dict(state_dict['state_dict'])

def test(imgL,imgR):
		model.eval()

		if cuda_available:
		   imgL = imgL.cuda()
		   imgR = imgR.cuda()     

		with torch.no_grad():
			disp = model(imgL,imgR)

		disp = torch.squeeze(disp)
		pred_disp = disp.data.cpu().numpy()

		return pred_disp


def main():
	pass
		

if __name__ == '__main__':
	normal_mean_var = {'mean': [0.485, 0.456, 0.406],
						'std': [0.229, 0.224, 0.225]}
	infer_transform = transforms.Compose([transforms.ToTensor(),
										  transforms.Normalize(**normal_mean_var)])    

	left_img_path = args.left_img_path
	right_img_path = args.right_img_path
	left_images = os.listdir(left_img_path)
	right_images = os.listdir(right_img_path)

	for leftimg, rightimg in zip(left_images, right_images):
		img_name = leftimg[:-4]

		imgL_o = Image.open(left_img_path+'/'+leftimg).convert('RGB')
		imgR_o = Image.open(right_img_path+'/'+rightimg).convert('RGB')

		imgL = infer_transform(imgL_o)
		imgR = infer_transform(imgR_o) 
	   

		# pad to width and hight to 16 times
		if imgL.shape[1] % 16 != 0:
			times = imgL.shape[1]//16       
			top_pad = (times+1)*16 -imgL.shape[1]
		else:
			top_pad = 0

		if imgL.shape[2] % 16 != 0:
			times = imgL.shape[2]//16                       
			right_pad = (times+1)*16-imgL.shape[2]
		else:
			right_pad = 0    

		imgL = F.pad(imgL,(0,right_pad, top_pad,0)).unsqueeze(0)
		imgR = F.pad(imgR,(0,right_pad, top_pad,0)).unsqueeze(0)

		pred_disp = test(imgL,imgR)

		
		if top_pad !=0 and right_pad != 0:
			img = pred_disp[top_pad:,:-right_pad]
		elif top_pad ==0 and right_pad != 0:
			img = pred_disp[:,:-right_pad]
		elif top_pad !=0 and right_pad == 0:
			img = pred_disp[top_pad:,:]
		else:
			img = pred_disp
		
		img = (img*256).astype('uint16')
		img = Image.fromarray(img)
		img.save(f'./test_depth_completion_anonymous/image/{img_name}.png') ##### Correct the name





