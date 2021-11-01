from tkinter import Menu

class MenuBars:
  def __init__(self, window):
    window.m = Menu(window.window)
    
    window.menu_file = Menu(window.m)
    window.menu_edit = Menu(window.m)
    window.menu_mode = Menu(window.m)
    window.submenu_image = Menu(window.m)

    window.m.add_cascade(menu=window.menu_file, label="File")
    window.m.add_cascade(menu=window.menu_edit, label="Edit")
    window.m.add_cascade(menu=window.menu_mode, label="Mode")

    window.menu_file.add_cascade(label="Image", menu=window.submenu_image)
    window.submenu_image.add_command(label="New Image", command=window.open_img)

    window.menu_edit.add_cascade(label="Downscale", command= lambda: window.scaleImage(50))
    window.menu_edit.add_cascade(label="Upscale", command= lambda: window.scaleImage(200))
    window.menu_edit.add_cascade(label="Down Sample", command=window.downSampling)
    window.menu_edit.add_cascade(label="Quantisize", command=window.quantization)
    window.menu_edit.add_cascade(label="Negative", command=window.invertNegative)
    window.menu_edit.add_cascade(label="Increase Brightness", command=lambda: window.modifyBrightness(30))
    window.menu_edit.add_cascade(label="Decrease Brightness", command=lambda: window.modifyBrightness(-30))
    window.menu_edit.add_cascade(label="Equalize", command=window.equalize)
    window.menu_edit.add_cascade(label="Clear Edits", command=window.clearEdits)

    window.menu_mode.add_cascade(label="Mode 1", command=lambda: window.changeDisplayMode(1))
    window.menu_mode.add_cascade(label="Mode 2", command=lambda: window.changeDisplayMode(2))

    window.window['menu'] = window.m

