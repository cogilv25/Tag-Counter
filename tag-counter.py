# Written by Calum Lindsay.

# It is a simple application to 
# count the number of tags that have
# been printed by the Laser Printer
# we use at work. It is still very
# early in development acting as something
# of a Sandbox for me playing with Python
# and wxPython. There will be errors but
# it does mostly do what it's supposed to

# TODO:
# 1)Saving and loading of current state
# 2)Tidy up & comment
# 3)Bug testing
# 4)Tag code generation
# 5)Store sites / packing stations in a
# file for easy adding / editing
# 6)Move functionality which can be
# controlled by events into onEvent
# functions

import wx
import wx.adv
import time

version = "2.0.1b"

# Custom Status Bar to Allow centre aligning of timeLabel and right
# aligning of versionLabel 
class CustomStatusBar(wx.StatusBar):
	def __init__(self, parent):
		wx.StatusBar.__init__(self, parent, -1)

		self.SetFieldsCount(3)
		self.SetStatusWidths([-1,-1,-1])

		self.versionLabel = wx.StaticText(self, -1, "Version: " + version)
		self.timeLabel = wx.StaticText(self, -1, time.strftime("%H:%M:%S",time.localtime(time.time())))
		self.repositionFields()

		self.Bind(wx.EVT_SIZE, self.onResize)

	def onResize(self, event):
		self.repositionFields()


	def repositionVersionField(self):
		versionFieldRect = self.GetFieldRect(2)
		versionLabelRect = self.versionLabel.GetRect()

		# Transform Rect to the right by the difference between the
		# Status bar's right field's width and the Static Text's width.
		# Essentially this right aligns the text.
		versionFieldRect.x += versionFieldRect.width - versionLabelRect.width
		# Set the Rect's width to the width of the text
		versionFieldRect.width = versionLabelRect.width
		# Move it up slightly to align with text drawn by 
		# SetStatusText() calls
		versionFieldRect.y += 3

		self.versionLabel.SetRect(versionFieldRect)

	def repositionTimeField(self):
		timeFieldRect = self.GetFieldRect(1)
		timeLabelRect = self.timeLabel.GetRect()

		# Transform Rect to the right by the difference between the
		# Status bar's middle field's width/2 and the Static Text's
		# width/2. Essentially this centre aligns the text.
		timeFieldRect.x += timeFieldRect.width/2 - timeLabelRect.width/2
		# Set the Rect's width to the width of the text
		timeFieldRect.width = timeLabelRect.width
		# Move it up slightly to align with text drawn by 
		# SetStatusText() calls
		timeFieldRect.y += 3

		self.timeLabel.SetRect(timeFieldRect)

	def repositionFields(self):
		self.repositionTimeField()
		self.repositionVersionField()
		


class Frame(wx.Frame):
	def __init__(self, *args, **kw):
		super(Frame, self).__init__(*args, **kw)

		self.panel = wx.Panel(self)
		headerFont = wx.Font(wx.FontInfo(15).Bold())
		#Left List
		self.leftListHeader = wx.StaticText(self.panel, label="Modifiable Parameters", pos=(25,25))
		self.leftListHeader.SetFont(headerFont)

		wx.StaticText(self.panel, label="Number of tags per tray", pos = (25,60))
		self.tagsPerTray = wx.SpinCtrl(self.panel, min=0, max=1000, initial=196, pos =(25,80))
		wx.StaticText(self.panel, label="Number of tags to print", pos = (25,110))
		self.tagTarget = wx.SpinCtrl(self.panel, min=0, max=100000, initial=5000, pos =(25,130))
		wx.StaticText(self.panel, label="Tags Printed", pos = (25,160))
		self.tagsPrinted = wx.SpinCtrl(self.panel, min=0, max=100000, initial=0, pos =(25,180))
		wx.StaticText(self.panel, label="Time to Print 1 Tray", pos = (25,210))
		self.trayTime = wx.adv.TimePickerCtrl(self.panel, pos =(25,230), dt = wx.DateTime(1,0,minute=12,second=52))
		self.button = wx.Button(self.panel, label="Tray Complete", pos=(25, 600))
		self.Bind(wx.EVT_BUTTON, self.OnButtonPress, self.button)

		#Right List
		self.rightListHeader = wx.StaticText(self.panel, label="Information", pos =(350,25))
		self.rightListHeader.SetFont(headerFont)

		wx.StaticText(self.panel, label="Progress", pos = (350,60))
		self.gauge = wx.Gauge(self.panel, pos = (350,80))
		wx.StaticText(self.panel, label="Time to Go", pos = (350,110))
		self.timeToGo = time.strptime((self.trayTime.GetValue()).FormatISOTime(), "%H:%M:%S")
		self.timeToGoLabel = wx.StaticText(self.panel, label = time.strftime("%H:%M:%S",self.timeToGo), pos = (350,130))

		#Status Bar Creation
		self.statusbar = CustomStatusBar(self)
		self.SetStatusBar(self.statusbar)
		self.statusbar.SetStatusText("Running")
		self.MakeMenuBar()
		self.Bind(wx.EVT_CLOSE, self.onExit)

		#Update Timer
		self.updateTimer = wx.Timer()
		self.updateTimer.Notify = self.update
		self.update()

	def MakeMenuBar(self):
		fileMenu = wx.Menu()
		saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S", 
			"Save current parameters as default")
		fileMenu.AppendSeparator()
		exitItem = fileMenu.Append(wx.ID_EXIT)
		helpMenu = wx.Menu()
		aboutItem = helpMenu.Append(wx.ID_ABOUT)
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(helpMenu, "&Help")
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
		self.Bind(wx.EVT_MENU, self.OnExitPressed,  exitItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


	def OnExitPressed(self, event):
		self.Close(True)

	def onExit(self, event):
		#TODO: Message box asking if you want to save
		event.Skip()


	def OnSave(self, event):
		wx.MessageBox("Currently not implemented... sorry!")


	def OnAbout(self, event):
		wx.MessageBox("This is a tool to help keep track of the tag printing process",
			"About Tag Counter " + version,
			wx.OK|wx.ICON_INFORMATION)

	def OnButtonPress(self, event):
		self.tagsPrinted.SetValue(self.tagsPrinted.GetValue() + self.tagsPerTray.GetValue())


	def update(self):
		#Calculate the number of trays of tags still to be completed
		traysToGo = int((self.tagTarget.GetValue() - self.tagsPrinted.GetValue()) / self.tagsPerTray.GetValue() + .99)
		self.gauge.SetValue(self.tagsPrinted.GetValue()/self.tagTarget.GetValue()*100)

		#Calculate time to finish all tags
		timetuple = self.trayTime.GetTime()
		timespan = wx.TimeSpan(timetuple[0],timetuple[1],timetuple[2]) * traysToGo
		self.timeToGoLabel.SetLabel(timespan.Format("%H:%M:%S"))

		#Update current time
		self.statusbar.timeLabel.SetLabel(time.strftime("%H:%M:%S %d/%m/%y",time.localtime(time.time())))


app = wx.App()
frm = Frame(None, title = "Tag Counter", size=(600,800), pos=(100,100), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
frm.Show()
frm.updateTimer.Start(1000)
app.MainLoop()