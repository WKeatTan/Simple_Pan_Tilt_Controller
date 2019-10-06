from __future__ import division
import cv2
import PIL.Image, PIL.ImageTk
import time
import sys
import Adafruit_PCA9685

class App:
	def __init__(self, window, window_title, video_source=0):
		self.window = window
		self.window.title(window_title)
		self.video_source = video_source
		
		# Open video source (by default this will try open the computer webcam)
		self.vid = MyVideoCapture(self.video_source)
		
		# Create a canvas that can fit the above video source size
		self.canvas = tkinter .Canvas(window, width=self.vid.width, height=self.vid.height)
		self.canvas.pack()
		
		# Button that lets the user take a snapshot
		self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
		self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
		
		# Create object servo
		self.servo_btm = MyServoController(0, 90)
		self.servo_upp = MyServoController(1, 0)
		
		# Key that control pan/tilt camera
		self.window.bind("<Key>", key)
		self.window.pack()
		
		# After it is called once the update method will be automatically called every delay milliseconds
		self.delay = 15
		self.update()
		
		self.window.mainloop()
		
	def update():
		# Get a frame from the video source
		ret ,frame = self.vid.get_frame()
		if ret:
			self.photo = PIL.ImageTk.PhotImage(image=PIL.Image.fromarray(frame))
			self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
			
		self.window.after(self.delay, self.update)
		
	def snapshot():
		# Get a frame from the video source
		ret, frame = self.vid.get_frame()
		if ret:
			cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S"))+".jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	
	def key(self, event):
		# angle between 0 -- 180, so the servo move 0, 45, 90, 135, 180
		if event.char == "a":
			# <--- cam 
			if self.servo_btm.angle < 180:
				self.servo_btm.angle += 45
				self.servo_btm.set_servo_angle(self.servo_btm.angle)
		elif event.char == "d":
			# cam --->
			if self.servo_btm.angle > 0:
				self.servo_btm.angle += -45
				self.servo_btm.set_servo_angle(self.servo_btm.angle)
		elif event.char == "w":
			# cam move up
			if self.servo_upp.angle < 180:
				self.servo_upp.angle += 45
				self.servo_upp.set_servo_angle(self.servo_upp.angle)
		elif event.char == "s":
			# cam move down
			if self.servo_upp > 0:
				self.servo_upp.angle += -45
				self.servo_upp.set_servo_angle(self.servo_upp.angle)
		else:
			print(event.char)
	
class MyVideoCapture:
	def __init__(self, video_source=0):
		# Open the video source
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("Unable to open video source", video_source)
			
		# Get video source width and height
		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
	
	def get_frame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				# Return a boolean success flag and the current frame converted to BGR
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)
	
	# Release the video source when the object is destroyed
	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()
			
class MyServoController:
	def __init__(self, channel, angle):
		self.channel = channel
		self.angle = angle
	
	def set_servo_angle(self, angle):
		date=4096*((angle*11)+500)/20000
		pwm.set_pwm(self.channel, 0, date)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
		
# Set frequency to 50hz, good for servos.
pwm.set_pwm_freq(50)

if __name__ == "__main__":
	App(tkinter.Tk(), "Tkiinter and OpenCV")
	sys.exit()