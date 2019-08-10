import wx


class DeskUnityGui(wx.Frame):

    title = "DeskUnity"
    version = "v1.0"

    def __init__(self, start_handler=None, exit_handler=None):
        self.start_handler = start_handler
        self.exit_handler = exit_handler
        wx.Frame.__init__(self, None, wx.ID_ANY, title=self.title)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel = wx.Panel(self, wx.ID_ANY)
        title = wx.StaticText(self.panel, wx.ID_ANY, f'{self.title} {self.version}')
        title.SetFont(wx.Font(12, 74, 90, wx.FONTWEIGHT_BOLD, False, "Arial Rounded"))

        self.status = wx.StaticText(self.panel, wx.ID_ANY, label="Searching...")
        self.status.SetFont(wx.Font(10, 74, 90, wx.FONTWEIGHT_BOLD, False, "Arial Rounded"))

        self.top_sizer = wx.BoxSizer(wx.VERTICAL)
        self.title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title_sizer.Add(title, 0, wx.ALL, 5)
        self.status_sizer.Add(self.status, 0, wx.ALL, 5)

        self.top_sizer.Add(self.title_sizer, 0, wx.CENTER)
        self.top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
        self.top_sizer.Add(self.status_sizer, 0, wx.CENTER)

        # SetSizeHints(minW, minH, maxW, maxH)
        self.SetSizeHints(450, 200, 450, 200)

        self.panel.SetSizer(self.top_sizer)
        self.top_sizer.Fit(self)

        self.CreateStatusBar()  # A Statusbar in the bottom of the window

    def set_status(self, status):
        self.status.SetLabel(status)
        self.top_sizer.Layout()

    def on_start(self, event):
        if self.start_handler:
            self.start_handler()

    def on_close(self, event):
        if self.exit_handler:
            self.exit_handler()
        self.Destroy()


class GUI:
    def __init__(self, start_handler=None, exit_handler=None):
        self.__app = wx.App()
        self.ui = DeskUnityGui(start_handler, exit_handler)

    def show(self):
        self.ui.Show()
        self.__app.MainLoop()
