from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw
import cv2





def drawProgressBar(canvas, x, y, w, h, perc):
	draw.rectangle((x, y, x+w-1, y+h-1), outline=1, fill=0)
	draw.rectangle((x+1, y+1, x+1+(w-3)*perc, y+h-2), outline=0, fill=1)

def drawText(canvas, x, y, max_w, text, font, lineDst):
	begin = 0
	while begin < len(text):
		end = min(begin + max_w, len(text))
		draw.text((x,y), text[begin:end], font=font, fill=255)
		begin = end
		y += lineDst


if __name__ == "__main__" :
	device = ssd1306(port=3, address=0x3C)
	video_object = cv2.VideoCapture(1)

	perc = 0.0
	inc = True

	while True:
		_, frame = video_object.read()
		qrDetector = cv2.QRCodeDetector()
		qrValue, *_ = qrDetector.detectAndDecode(frame)

		with canvas(device) as draw:
			font = ImageFont.truetype("ProFontWindows.ttf", size=10)
			draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
			drawText(canvas, 32, 16, 8, f'qr code: {qrValue}', font, 8)
			drawProgressBar(canvas, 32, 48, 64, 8, perc)
		if inc:
			if perc >= 0.9:
				inc = False
			else:
				perc += 0.1
		else:
			if perc <= 0.1:
				inc = True
			else:
				perc -= 0.1
