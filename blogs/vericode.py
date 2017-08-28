#verification code

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random


def randomcode(lenght = 1):
	code = ""
	for char in range(lenght):
		code += chr(random.randint(65,90))
	return code

def randbgcolor():
	return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def randfontcolor():
	return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def vericode(length=4,width=160,height=40):
	image = Image.new('RGB',(width,height),(255,255,255))
#	font = ImageFont.truetype('Arial.ttf',32)
	font = ImageFont.truetype('DejaVuSerif.ttf',32)
	draw = ImageDraw.Draw(image)
	for x in range(width):
		for y in range(height):
			draw.point((x,y),fill=randbgcolor())
	code = randomcode(length)
	for t in range(4):
		draw.text((40 * t + 5,5),code[t],font=font,fill=randfontcolor())
	image = image.filter(ImageFilter.BLUR)

#	image.save(filepath+filename+'.jpg','jpeg')
	return code,image

if __name__ == '__main__':
	print(vericode()[0])









