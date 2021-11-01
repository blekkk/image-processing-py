from tkinter import *
from tkinter import filedialog, NW
from PIL import Image, ImageTk
from menubars import MenuBars
from utils import image_resize
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
  def __init__(self, window, window_title, window_size="1920x1080"):
    self.window = window
    self.window.title(window_title)
    self.window.geometry(window_size)
    self.window.option_add('*tearOff', FALSE)

    # Initialize panel for displaying image
    self.labelLeft = None
    self.labelRight = None

    # Initialize panel for histogram
    self.histogramFigure = Figure(figsize=(6,6), dpi=100)
    self.histogramCanvas = FigureCanvasTkAgg(self.histogramFigure, self.window)
    
    # size and mode
    self.size = [900, 900]
    self.displayMode = 1

    MenuBars(self)

    self.window.mainloop()

  def openfn(self):
    filename = filedialog.askopenfilename(title='Open an image', filetypes=[('Image files','*.jpg *.jpeg *.png *.bmp *.tiff *.svg *.gif')])
    return filename

  def open_img(self):
    self.x = self.openfn()
    self.ORIGINAL_IMAGE = cv2.cvtColor(cv2.imread(self.x), cv2.COLOR_BGR2RGB)
    self.modifiableImage = cv2.cvtColor(cv2.imread(self.x), cv2.COLOR_BGR2RGB)
    self.photo = Image.fromarray(self.ORIGINAL_IMAGE)
    self.photo.thumbnail(self.size, Image.ANTIALIAS)
    self.photo = ImageTk.PhotoImage(image = self.photo)
    
    if(self.labelLeft != None and self.labelRight != None):
      self.labelLeft.configure(image=self.photo)
      self.labelLeft.image = self.photo
      self.labelRight.configure(image=self.photo)
      self.labelRight.image = self.photo
    else:
      self.labelLeft = Label(self.window, image=self.photo)
      self.labelLeft.image = self.photo
      self.labelLeft.pack(side="left", padx=10, pady=10)
      self.labelRight = Label(self.window, image=self.photo)
      self.labelRight.image = self.photo
      self.labelRight.pack(side="right", padx=10, pady=10)

  def increaseColorValue(self, color, value=30):
    lim = 255
    self.modifiableImage[:,:,color] = np.clip(self.modifiableImage[:,:,color]+value, 0, lim)
    self.displayImage()

  def decreaseColorValue(self, color, value=30):
    lim = 0
    self.modifiableImage[:,:,color] = np.clip(self.modifiableImage[:,:,color]-value, lim, 255)
    self.displayImage()

  def scaleImage(self, percent):
    scale_percent = percent
    self.height, self.width, no_channels = self.modifiableImage.shape
    self.width = int(self.width * (scale_percent / 100))
    self.height = int(self.height * (scale_percent / 100))
    dim = (self.width, self.height)
      
    npImg = np.array(self.modifiableImage)
    resized = cv2.resize(npImg, dim, interpolation = cv2.INTER_NEAREST)
    self.modifiableImage = resized
    resized = Image.fromarray(resized)
    resized = ImageTk.PhotoImage(resized)
    self.labelRight.configure(image=resized)
    self.labelRight.image = resized

  def downSampling(self):
    if(self.modifiableImage.shape[0] > 1000 and self.modifiableImage.shape[1] > 1000):
      self.modifiableImage = image_resize(self.modifiableImage, height = 1000)

    height, width = self.modifiableImage.shape[0], self.modifiableImage.shape[1]
    new_h, new_w = int(height/2), int(width/2)

    self.modifiableImage = image_resize(self.modifiableImage, new_w, new_h)
    self.modifiableImage = image_resize(self.modifiableImage, height = 1000)

    self.displayImage()

  def quantization(self):
    height, width = self.modifiableImage.shape[0], self.modifiableImage.shape[1]
    new_img = np.zeros((height, width, 3), np.uint8)

    #  Image quantization operation , The quantification level is 2
    for i in range(height):
        for j in range(width):
            for k in range(3):  #  Correspondence BGR Three channels 
                if self.modifiableImage[i, j][k] < 128:
                    gray = 0
                else:
                    gray = 129
                new_img[i, j][k] = np.uint8(gray)
    self.modifiableImage = new_img
    self.displayImage()

  def invertNegative(self):
    self.modifiableImage[:,:,0] = 255 - self.modifiableImage[:,:,0]
    self.modifiableImage[:,:,1] = 255 - self.modifiableImage[:,:,1]
    self.modifiableImage[:,:,2] = 255 - self.modifiableImage[:,:,2]

    self.displayImage()

  def modifyBrightness(self, value=30):
    hsv = cv2.cvtColor(self.modifiableImage, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    if value >= 0:
      lim = 255 - value
      v[v > lim] = 255
      v[v <= lim] += value
    else:
      value = abs(value)
      lim = 0 + value
      v[v < lim] = 0
      v[v >= lim] -= value

    final_hsv = cv2.merge((h, s, v))
    self.modifiableImage = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

    self.displayImage()

  def lowPassFilter(self):
    kernel = np.ones((5,5),np.float32)/25
    self.modifiableImage = cv2.filter2D(self.modifiableImage,-1,kernel)

    self.displayImage()

  def highPassFilter(self):
    kernel = np.array([[0.0, -1.0, 0.0], 
                      [-1.0, 4.0, -1.0],
                      [0.0, -1.0, 0.0]])
    kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)

    self.modifiableImage = cv2.filter2D(self.modifiableImage,-1,kernel)

    self.displayImage()

  def bandPassFilter(self):
    kernel = np.array([[0, -1, 0], 
                      [-1, 5, -1],
                      [0, -1, 0]])
    kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)

    self.modifiableImage = cv2.filter2D(self.modifiableImage,-1,kernel)
    
    self.displayImage()

  def clearEdits(self):
    self.modifiableImage = cv2.cvtColor(cv2.imread(self.x), cv2.COLOR_BGR2RGB)
    self.displayImage()

  def displayOnLeftLabel(self, image):
    self.photo2 = Image.fromarray(image)
    self.photo2.thumbnail(self.size, Image.ANTIALIAS)
    self.photo2 = ImageTk.PhotoImage(image = self.photo2)

    self.labelLeft.configure(image=self.photo2)
    self.labelLeft.image = self.photo2 

  def displayOnRightLabel(self, image):
    self.photo = Image.fromarray(image)
    self.photo.thumbnail(self.size, Image.ANTIALIAS)
    self.photo = ImageTk.PhotoImage(image = self.photo)

    self.labelRight.configure(image=self.photo)
    self.labelRight.image = self.photo

  def displayImage(self):
    if self.displayMode == 1:
      self.displayOnLeftLabel(self.ORIGINAL_IMAGE)
      self.displayOnRightLabel(self.modifiableImage)
    elif self.displayMode == 2:
      self.displayOnLeftLabel(self.modifiableImage)
      self.showHistogram(self.modifiableImage)

  def changeDisplayMode(self, mode):
    self.displayMode = mode
    if self.displayMode == 1:
      MenuBars.disableModeOne(self)
      MenuBars.enableModeTwo(self)
      self.histogramCanvas.get_tk_widget().pack_forget()
      self.labelRight = Label(self.window, image=self.photo)
      self.labelRight.image = self.photo
      self.labelRight.pack(side="right", padx=10, pady=10)
    elif self.displayMode == 2:
      MenuBars.disableModeTwo(self)
      MenuBars.enableModeOne(self)
      self.labelRight.pack_forget()
    self.displayImage()
  
  def showHistogram(self, image):
    self.histogramCanvas.get_tk_widget().pack_forget()
    subplot = 221

    self.histogramFigure = Figure(figsize=(6,6), dpi=100)

    for i, color in enumerate(['r', 'g', 'b']):
      self.histogramFigure.add_subplot(subplot).plot(cv2.calcHist([image],[i],None,[256],[0,256]), color = color)
      subplot = subplot + 1
    
    self.histogramCanvas = FigureCanvasTkAgg(self.histogramFigure, self.window)
    self.histogramCanvas.get_tk_widget().pack(side="right")

  def equalize(self):
    channels = cv2.split(self.modifiableImage)
    eq_channels = []
    for ch, color in zip(channels, ['R', 'G', 'B']):
        eq_channels.append(cv2.equalizeHist(ch))

    self.modifiableImage = cv2.merge(eq_channels)
    self.displayImage()

App(Tk(), "Image Processing")