# import required libraries
import os
import json
import cv2
import matplotlib.pyplot as plt

input_path = "./frames-8864-15fps"
output_path = "./frames-8864-15fps-compressed-txt"
width = 88
height = 64
if not os.path.exists(output_path):
	os.makedirs(output_path)

images = os.listdir(input_path)
images.sort()
frames_file = open(os.path.join(output_path, "frames.txt"), "w")
for image in images: # [56:57]:
	# load the input image
	image_path = os.path.join(input_path, image)
	img = cv2.imread(image_path)

	# convert the input image to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# apply thresholding to convert grayscale to binary image
	ret,thresh = cv2.threshold(gray,70,255,0)
	# thresh[thresh[:,:] == 255] = 1

	# convert BGR to RGB to display using matplotlib
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# output_image_path = os.path.join(output_path, image)
	output_list_path = os.path.join(output_path, image.split(".")[0] + ".txt")
	data = []
	for y in range(height):
		data.append([])
		for x in range(width//8):
			data[y].append(0b00000000)
	for y in range(height):
		for x in range(width):
			b = 7 - (x % 8)
			if thresh[y][x] == 255:
				data[y][x//8] |= (1 << b)
	compressed_255 = []
	for y in range(height):
		compressed_255.append([])
		start_255 = None
		for i, x in enumerate(range(width//8)):
			d = data[y][x]
			if d == 255:
				if start_255 is None:
					compressed_255[y].append(d)
					start_255 = i
			else:
				if start_255 is not None:
					compressed_255[y].append(i - start_255)
					start_255 = None
				compressed_255[y].append(d)
		if start_255 is not None:
			compressed_255[y].append(width//8 - start_255)
	compressed = []
	for y in range(height):
		compressed.append([])
		start_0 = None
		for i, d in enumerate(compressed_255[y]):
			if d == 0:
				if start_0 is None:
					compressed[y].append(d)
					start_0 = i
			else:
				if start_0 is not None:
					compressed[y].append(i - start_0)
					start_0 = None
				compressed[y].append(d)
		if start_0 is not None:
			compressed[y].append(len(compressed_255[y]) - start_0)

	# d = d.replace("255", "1")
	# d = d.replace(" ", "")

	with open(output_list_path, "w") as fp:
		s = str(compressed)
		s = s.replace(" ", "")
		fp.write(s)
		frames_file.write(s + "\n")
frames_file.close()
	# cv2.imwrite(output_image_path, thresh)
	# break

	# display Original, Grayscale and Binary Images
	# plt.subplot(131),plt.imshow(imgRGB,cmap = 'gray'),plt.title('Original Image'), plt.axis('off')
	# plt.subplot(132),plt.imshow(gray,cmap = 'gray'),plt.title('Grayscale Image'),plt.axis('off')
	# plt.subplot(133),plt.imshow(thresh,cmap = 'gray'),plt.title('Binary Image'),plt.axis('off')
	# plt.show()