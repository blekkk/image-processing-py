from tkinter import Menu

class MenuBars:
  def __init__(self, window):
    window.m = Menu(window.window)
    
    window.menu_file = Menu(window.m)
    window.menu_edit = Menu(window.m)
    window.menu_mode = Menu(window.m)
    window.submenu_image = Menu(window.m)
    window.submenu_elementary = Menu(window.m)
    window.sub_submenu_rgb_increase = Menu(window.m)
    window.sub_submenu_rgb_decrease = Menu(window.m)

    window.m.add_cascade(menu=window.menu_file, label="File")
    window.m.add_cascade(menu=window.menu_edit, label="Edit")
    window.m.add_cascade(menu=window.menu_mode, label="Mode")

    window.menu_file.add_cascade(label="Image", menu=window.submenu_image)
    window.submenu_image.add_command(label="New Image", command=window.open_img)

    window.menu_edit.add_cascade(label="Elementary Operation", menu=window.submenu_elementary)
    window.submenu_elementary.add_cascade(label="Increase", menu=window.sub_submenu_rgb_increase)
    window.submenu_elementary.add_cascade(label="Decrease", menu=window.sub_submenu_rgb_decrease)

    window.sub_submenu_rgb_increase.add_cascade(label="Red", command= lambda:window.increaseColorValue(0))
    window.sub_submenu_rgb_increase.add_cascade(label="Green", command= lambda:window.increaseColorValue(1))
    window.sub_submenu_rgb_increase.add_cascade(label="Blue", command= lambda:window.increaseColorValue(2))
    window.sub_submenu_rgb_decrease.add_cascade(label="Red", command= lambda:window.decreaseColorValue(0))
    window.sub_submenu_rgb_decrease.add_cascade(label="Green", command= lambda:window.decreaseColorValue(1))
    window.sub_submenu_rgb_decrease.add_cascade(label="Blue", command= lambda:window.decreaseColorValue(2))

    window.menu_edit.add_cascade(label="Downscale", command= lambda: window.scaleImage(50))
    window.menu_edit.add_cascade(label="Upscale", command= lambda: window.scaleImage(200))
    window.menu_edit.add_cascade(label="Down Sample", command=window.downSampling)
    window.menu_edit.add_cascade(label="Quantisize", command=window.quantization)
    window.menu_edit.add_cascade(label="Negative", command=window.invertNegative)
    window.menu_edit.add_cascade(label="Increase Brightness", command=lambda: window.modifyBrightness(30))
    window.menu_edit.add_cascade(label="Decrease Brightness", command=lambda: window.modifyBrightness(-30))
    window.menu_edit.add_cascade(label="Equalize", command=window.equalize)
    window.menu_edit.add_cascade(label="Low Pass Filter", command=window.lowPassFilter)
    window.menu_edit.add_cascade(label="High Pass Filter", command=window.highPassFilter)
    window.menu_edit.add_cascade(label="Band Pass Filter", command=window.bandPassFilter)
    window.menu_edit.add_cascade(label="Clear Edits", command=window.clearEdits)

    window.menu_mode.add_cascade(label="Mode 1", command=lambda: window.changeDisplayMode(1), state="disabled")
    window.menu_mode.add_cascade(label="Mode 2", command=lambda: window.changeDisplayMode(2))

    window.window['menu'] = window.m

  @staticmethod
  def disableModeOne(self):
    self.menu_mode.entryconfig("Mode 1", state="disabled")

  @staticmethod
  def enableModeOne(self):
    self.menu_mode.entryconfig("Mode 1", state="normal")

  @staticmethod
  def disableModeTwo(self):
    self.menu_mode.entryconfig("Mode 2", state="disabled")

  @staticmethod
  def enableModeTwo(self):
    self.menu_mode.entryconfig("Mode 2", state="normal")

