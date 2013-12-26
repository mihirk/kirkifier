import numpy as np
import cv2
import sys
from PIL import Image


class Face:
	def __init__(self, point1, point2, point3, point4):
		self.LEFT_UP = point1
		self.RIGHT_DOWN = point2
		self.RIGHT_UP = point3
		self.LEFT_DOWN = point4
	def face_width(self):
		return self.RIGHT_UP[0] - self.LEFT_UP[0]
	def face_height(self):
		return self.RIGHT_DOWN[1] - self.RIGHT_UP[1]
	def __str__(self):
		return str(self.LEFT_UP) + str(self.RIGHT_UP) + str(self.LEFT_DOWN) + str(self.RIGHT_DOWN)

class Kirkify:
	def get_source_image_face_coordinates(self, source_image_name):
		image_to_be_kirkified = cv2.imread(source_image_name)
		face_cascade = cv2.CascadeClassifier("/vagrant/kirkifier/kirkifier/haarcascade_frontalface_alt2.xml") 
		faces = face_cascade.detectMultiScale(image_to_be_kirkified)
		detected_faces = []
		for face in faces:    
			LEFT_UP = (face[0], face[1])
			RIGHT_DOWN = ((face[0]+face[2]), (face[0] + face[3]))
			RIGHT_UP = (face[0]+face[2], face[1])
			LEFT_DOWN = (face[0], face[0]+face[3])
			detected_faces.append(Face(LEFT_UP, RIGHT_DOWN, RIGHT_UP, LEFT_DOWN))
		return detected_faces
	
	def resize_kirk(self, kirk_image_handle, width, height):
		new_kirk_image_size = (width, height)
		return kirk_image_handle.resize(new_kirk_image_size)
		

	def get_source_image_name(self,file):
		with open('/vagrant/kirkifier/kirkifier/source.png','wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		return "/vagrant/kirkifier/kirkifier/source.png"

	def kirkify_faces(self, kirk_image_handle, source_image_handle, faces_coordinates):
		kirkified_image_handle = source_image_handle
		for face_coordinates in faces_coordinates:
			kirkified_image_handle = self.kirkify_face(kirk_image_handle, kirkified_image_handle, face_coordinates)
		return kirkified_image_handle

	def kirkify_face(self, kirk_image_handle, source_image_handle, face_coordinates):
		face_width = face_coordinates.face_width()
		face_height = face_coordinates.face_height()
		kirk_image_handle = self.resize_kirk(kirk_image_handle, face_width, face_height)
		kirk_image_handle = self.ready_for_kirkification(kirk_image_handle)
		source_image_handle = self.ready_for_kirkification(source_image_handle)
		source_image_handle.paste(kirk_image_handle, (face_coordinates.LEFT_UP), mask=kirk_image_handle)
		return source_image_handle

	

	def ready_for_kirkification(self, image_handle):
		image_handle = image_handle.convert('RGBA')
		return image_handle

	def get_image_handle(self,image_name):
		return Image.open(image_name)

	def main(self, file):
		source_image_name = self.get_source_image_name(file)
		kirk_image_handle = self.get_image_handle("/vagrant/kirkifier/kirkifier/kirk.png")
		source_image_handle = self.get_image_handle(source_image_name)
		faces_coordinates = self.get_source_image_face_coordinates(source_image_name)
		kirkified_image_handle = self.kirkify_faces(kirk_image_handle, source_image_handle, faces_coordinates)
		kirkified_image_handle.save("/vagrant/kirkifier/kirkifier/kirkified_image.png")
