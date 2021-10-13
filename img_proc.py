from tkinter import *
from tkinter import filedialog, NW
from PIL import Image, ImageTk
from menubars import MenuBars
from utils import image_resize
import cv2
import numpy as np

class App:
  def __init__(self, window, window_title, window_size="1920x1080"):
    self.window = window
    self.window.title(window_title)
    self.window.geometry(window_size)
    self.window.option_add('*tearOff', FALSE)

    # Initialize panel for displaying image
    self.panelLeft = None
    self.panelRight = None
    self.size = [1000, 1000]

    MenuBars(self)

    self.window.mainloop()

  def openfn(self):
    filename = filedialog.askopenfilename(title='Open an image', filetypes=[('Image files','*.jpg *.jpeg *.png *.bmp *.tiff *.svg *.gif')])
    return filename

  def open_img(self):
    x = self.openfn()
    self.img = cv2.cvtColor(cv2.imread(x), cv2.COLOR_BGR2RGB)
    self.img2 = self.img
    self.photo = Image.fromarray(self.img)
    self.photo.thumbnail(self.size, Image.ANTIALIAS)
    self.photo = ImageTk.PhotoImage(image = self.photo)
    
    if(self.panelLeft != None and self.panelRight != None):
      self.panelLeft.configure(image=self.photo)
      self.panelLeft.image = self.photo
      self.panelRight.configure(image=self.photo)
      self.panelRight.image = self.photo
    else:
      self.panelLeft = Label(self.window, image=self.photo)
      self.panelLeft.image = self.photo
      self.panelLeft.pack(side="left", padx=10, pady=10)
      self.panelRight = Label(self.window, image=self.photo)
      self.panelRight.image = self.photo
      self.panelRight.pack(side="right", padx=10, pady=10)

  def scaleImage(self, percent):
    scale_percent = percent
    self.height, self.width, no_channels = self.img2.shape
    self.width = int(self.width * (scale_percent / 100))
    self.height = int(self.height * (scale_percent / 100))
    dim = (self.width, self.height)
    print(dim)
      
    npImg = np.array(self.img2)
    resized = cv2.resize(npImg, dim, interpolation = cv2.INTER_NEAREST)
    self.img2 = resized
    resized = Image.fromarray(resized)
    resized = ImageTk.PhotoImage(resized)
    self.panelRight.configure(image=resized)
    self.panelRight.image = resized

  def downSampling(self):
    if(self.img2.shape[0] > 1000 and self.img2.shape[1] > 1000):
      self.img2 = image_resize(self.img2, height = 1000)

    height, width = self.img2.shape[0], self.img2.shape[1]
    new_h, new_w = int(height/2), int(width/2)

    self.img2 = image_resize(self.img2, new_w, new_h)
    self.img2 = image_resize(self.img2, height = 1000)

    self.displayOnRightPanel(self.img2)

  def quantization(self):
    height, width = self.img2.shape[0], self.img2.shape[1]
    new_img = np.zeros((height, width, 3), np.uint8)

    #  Image quantization operation , The quantification level is 2
    for i in range(height):
        for j in range(width):
            for k in range(3):  #  Correspondence BGR Three channels 
                if self.img2[i, j][k] < 128:
                    gray = 0
                else:
                    gray = 129
                new_img[i, j][k] = np.uint8(gray)
    self.img2 = new_img
    self.displayOnRightPanel(self.img2)

  def invertNegative(self):
    self.img2[:,:,0] = 255 - self.img2[:,:,0]
    self.img2[:,:,1] = 255 - self.img2[:,:,1]
    self.img2[:,:,2] = 255 - self.img2[:,:,2]

    self.displayOnRightPanel(self.img2)

  def modifyBrightness(self, value=30):
    hsv = cv2.cvtColor(self.img2, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    self.img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

    self.displayOnRightPanel(self.img2)

  def clearEdits(self):
    self.img2 = self.img
    self.displayOnRightPanel(self.img2)

  def displayOnRightPanel(self, image):
    self.photo = Image.fromarray(image)
    self.photo.thumbnail(self.size, Image.ANTIALIAS)
    self.photo = ImageTk.PhotoImage(image = self.photo)

    self.panelRight.configure(image=self.photo)
    self.panelRight.image = self.photo 

App(Tk(), "Image Processing")