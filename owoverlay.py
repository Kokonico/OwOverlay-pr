import wx
import sys
from tkinter import filedialog, simpledialog
import pathlib
import json
import random
import activewindow as aw
import subprocess
import os

# TODO clean up pngs in main directory

config_path = "config.json"

class Overlay(wx.Frame):
    def __init__(self):
        print(random.choice(strings))
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='overlay', style=style)
        self.SetBackgroundColour(wx.TransparentColour)
        self.Size = wx.DisplaySize()
        if 4 == len(sys.argv):
            self.EarPack = sys.argv[1]
            self.OverlayHeight = int(sys.argv[2])
            self.YOverlap = int(sys.argv[3])
        elif pathlib.Path(config_path).exists():
            cfg = json.load(open(config_path, "r"))
            self.EarPack = cfg.get("ear_pack")
            self.OverlayHeight = cfg.get("height")
            self.YOverlap = cfg.get("y_overlap")
        else:
            self.EarPack = filedialog.askopenfilename(title="Select Overlay PNG")
            self.OverlayHeight = simpledialog.askinteger("Set Overlay Height", "Set the overlay height in pixels:")
            self.YOverlap = simpledialog.askinteger("Set Overlay Y-Offset", "Set how far below the top of the window should the overlay go:")
        print(self.EarPack, self.OverlayHeight, self.YOverlap)
        self.Position = (0, 0)
        self.Show(True)

        # Load images

        pack_directory = os.path.join(os.path.dirname(__file__), "earkits", self.EarPack)

        self.left_png = wx.Image(os.path.join(pack_directory, "left.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.middle_png = wx.Image(os.path.join(pack_directory, "middle.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.right_png = wx.Image(os.path.join(pack_directory, "right.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        while True:
            awin = aw.get_active_window()
            if awin:
                break

        # Create StaticBitmap for each image
        self.left_bmp = wx.StaticBitmap(self, -1, self.left_png, (awin.position[0], (awin.position[1]-self.OverlayHeight)+self.YOverlap), (self.left_png.GetWidth(), self.OverlayHeight))
        self.middle_bmp = wx.StaticBitmap(self, -1, self.middle_png, (awin.position[0] + (awin.size[0] // 2) - (self.middle_png.GetWidth() // 2), (awin.position[1]-self.OverlayHeight)+self.YOverlap), (self.middle_png.GetWidth(), self.OverlayHeight))
        self.right_bmp = wx.StaticBitmap(self, -1, self.right_png, (awin.position[0] + awin.size[0] - self.right_png.GetWidth(), (awin.position[1]-self.OverlayHeight)+self.YOverlap), (self.right_png.GetWidth(), self.OverlayHeight))

        self.Show(True)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(1)

    def update(self, _):
        awin = aw.get_active_window()
        if awin:
            # Update position and size of bitmaps
            # We don't apply y overlap to the left and right bitmaps (they can cover important stuff, experiencing this firsthand in pycharm)
            self.left_bmp.SetPosition((awin.position[0],  (awin.position[1]-self.OverlayHeight)))
            self.middle_bmp.SetPosition((awin.position[0] + (awin.size[0] // 2) - (self.middle_png.GetWidth() // 2), (awin.position[1]-self.OverlayHeight)+self.YOverlap))
            self.right_bmp.SetPosition((awin.position[0] + awin.size[0] - self.right_png.GetWidth(), (awin.position[1]-self.OverlayHeight)))
            self.left_bmp.SetSize(wx.Size(self.left_png.GetWidth(), self.OverlayHeight))
            self.middle_bmp.SetSize(wx.Size(self.middle_png.GetWidth(), self.OverlayHeight))
            self.right_bmp.SetSize(wx.Size(self.right_png.GetWidth(), self.OverlayHeight))

strings = [
    "ฅ^•ﻌ•^ฅ OwOverlay is starting up. Count how many times you can say UwU while you wait.",
    "ദ്ദി（• ˕ •マ.ᐟ This cat is giving you a thumbs up because you dropped a star on GitHub, right? right?",
    "/ᐠ > ˕ <マ ₊˚⊹♡ Enjoy some love from this cat while you wait for OwOverlay to start.",
    "/ᐠﹷ ‸ ﹷ ᐟ\ﾉ Your GitHub stars feed this cat.",
    f" (((;꒪ꈊ꒪;))) <-- live {str(subprocess.check_output(['whoami']))[2:-3]} reaction to OwOverlay starting up.",
]
if "UwU" in sys.argv:
    import time
    print("Super Cat Mode Enabled!")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)
    while True:
        cat_faces = [
            "UwU",
            "/ᐠ - ˕ -マ",
            "ฅ^•ﻌ•^ฅ",
            "/ᐠ > ˕ <マ",
            "/ᐠ˵- ᴗ -˵マ ᶻ 𝗓 𐰁",
            "=^◕⩊◕^="
        ]
        print(random.choice(cat_faces))

app = wx.App()
f = Overlay()
app.MainLoop()