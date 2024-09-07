import wx
import pywinctl as wc
import sys
from tkinter import filedialog, simpledialog



class Overlay(wx.Frame):
    def __init__(self):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='overlay', style=style)
        self.SetBackgroundColour(wx.TransparentColour)
        self.Size = wx.DisplaySize()
        if 4 == len(sys.argv):
            self.PNGFile = sys.argv[1]
            self.OverlayHeight = int(sys.argv[2])
            self.YOverlap = int(sys.argv[3])
        else:
            self.PNGFile = filedialog.askopenfilename(title="Select Overlay PNG")
            self.OverlayHeight = simpledialog.askinteger("Set Overlay Height", "Set the overlay height in pixels:")
            self.YOverlap = simpledialog.askinteger("Set Overlay Y-Offset", "Set how far below the top of the window should the overlay go:")
        self.Position = (0, 0)
        self.Show(True)
        png = wx.Image(sys.argv[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        awin = wc.getActiveWindow()
        self.bmp = wx.StaticBitmap(self, -1, png, (awin.position[0], (awin.position[1]-self.OverlayHeight)+self.YOverlap), (awin.size[0], self.OverlayHeight))
        self.Show(True)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(100)

    def update(self, _):
        awin = wc.getActiveWindow()
        if awin:
            self.bmp.SetPosition((awin.position[0],  (awin.position[1]-self.OverlayHeight)+self.YOverlap))
            self.bmp.SetSize(wx.Size(awin.size[0], self.OverlayHeight))


app = wx.App()
f = Overlay()
app.MainLoop()
