from tkinter import Menu

class MenuBars:
  def __init__(self, window):
    window.m = Menu(window.window)
    
    window.file_menu = Menu(window.m)
    window.edit_menu = Menu(window.m)
    window.image_submenu = Menu(window.m)

    window.m.add_cascade(menu=window.file_menu, label="File")
    window.m.add_cascade(menu=window.edit_menu, label="Edit")

    window.file_menu.add_cascade(label="Image", menu=window.image_submenu)
    window.image_submenu.add_command(label="New Image", command=window.open_img)

    window.edit_menu.add_cascade(label="Downscale", command= lambda: window.scaleImage(50))
    window.edit_menu.add_cascade(label="Upscale", command= lambda: window.scaleImage(200))
    window.edit_menu.add_cascade(label="Down Sample", command=window.downSampling)
    window.edit_menu.add_cascade(label="Quantisize", command=window.quantization)
    window.edit_menu.add_cascade(label="Negative", command=window.invertNegative)
    window.edit_menu.add_cascade(label="Increase Brightness", command=lambda: window.modifyBrightness(30))
    window.edit_menu.add_cascade(label="Decrease Brightness", command=lambda: window.modifyBrightness(30))
    window.edit_menu.add_cascade(label="Clear Edits", command=window.clearEdits)

    window.window['menu'] = window.m

