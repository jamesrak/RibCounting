from distutils.core import setup
import py2exe
import cv2
import numpy

setup(
	console=['rib_ui.py'],
	options={
		'py2exe':{
			'packages':['cv2','matplotlib.pyplot','numpy','argparse']
		}
	}
)