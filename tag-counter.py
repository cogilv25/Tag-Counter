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
# 2)Tidy up & comments
# 3)Status bar not aligned correctly
# status should be left aligned, DateTime
# should be centred and version right
# 4)Bug testing

import wx
import wx.adv
import threading
import time

version = "2.0.1b"


class StoppableThread(threading.Thread):
	def __init__(self, target):
		super(StoppableThread, self).__init__(target = target)
		self.stopEvent = threading.Event()

	def stop(self):
		self.stopEvent.set()

	def isStopped(self):
		return self.stopEvent.is_set()


class Frame(wx.Frame):
	def __init__(self, *args, **kw):
		super(Frame, self).__init__(*args, **kw)
		self.panel = wx.Panel(self)
		self.st = wx.StaticText(self.panel, label="Modifiable Parameters", pos=(25,25))
		self.st2 = wx.StaticText(self.panel, label="Information", pos =(350,25))
		self.timeLabel = wx.StaticText(self.panel, label="", pos =(350,600))
		self.status = "Running"

		font = self.st.GetFont()
		font.PointSize +=5
		font = font.Bold()
		wx.StaticText(self.panel, label="Number of tags per tray", pos = (25,60))
		self.tagsPerTray = wx.SpinCtrl(self.panel, max=1000, initial=196, pos =(25,80))
		wx.StaticText(self.panel, label="Number of tags to print", pos = (25,110))
		self.tagTarget = wx.SpinCtrl(self.panel, max=100000, initial=5000, pos =(25,130))
		wx.StaticText(self.panel, label="Tags Printed", pos = (25,160))
		self.tagsPrinted = wx.SpinCtrl(self.panel, max=100000, initial=0, pos =(25,180))
		wx.StaticText(self.panel, label="Time to Print 1 Tray", pos = (25,210))
		self.trayTime = wx.adv.TimePickerCtrl(self.panel, pos =(25,230))
		self.trayTime.SetTime(0,0,1)
		self.button = wx.Button(self.panel, label="Tray Complete", pos=(25, 600))
		self.st.SetFont(font)
		self.st2.SetFont(font)
		self.MakeMenuBar()
		self.Bind(wx.EVT_BUTTON, self.OnButtonPress, self.button)

		self.CreateStatusBar()
		self.SetStatusText(self.status +
		 "\t" + time.ctime(time.time()) + "\tVersion: " + version)

		wx.StaticText(self.panel, label="Progress", pos = (350,60))
		self.gauge = wx.Gauge(self.panel, pos = (350,80))
		wx.StaticText(self.panel, label="Time to Go", pos = (350,110))
		self.timeToGo = time.strptime((self.trayTime.GetValue()).FormatISOTime(), "%H:%M:%S")
		self.timeToGoLabel = wx.StaticText(self.panel, label=
			time.strftime("%H:%M:%S",self.timeToGo), pos = (350,130))
		
		self.Bind(wx.EVT_CLOSE, self.onExit)

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
		if(thread.isStopped()):
			event.Skip()
		thread.stop()
		self.SetStatusText("Closing...")


	def OnSave(self, event):
		wx.MessageBox("Currently not implemented... sorry!")


	def OnAbout(self, event):
		wx.MessageBox("This is a tool to help keep track of the tag printing process",
			"About Tag Counter " + version,
			wx.OK|wx.ICON_INFORMATION)

	def OnButtonPress(self, event):
		self.tagsPrinted.SetValue(self.tagsPrinted.GetValue() + self.tagsPerTray.GetValue())

	def update(self):
		while(not thread.isStopped()):
			self.SetStatusText(self.status + "\t\t" + time.ctime(time.time()) +
			 "\t\tVersion: " + version)
			traysToGo = int((self.tagTarget.GetValue() - self.tagsPrinted.GetValue()) / self.tagsPerTray.GetValue() + .99)
			self.gauge.SetValue(self.tagsPrinted.GetValue()/self.tagTarget.GetValue()*100)

			timetup = self.trayTime.GetTime()
			timespan = wx.TimeSpan(timetup[0],timetup[1],timetup[2]) * traysToGo
			self.timeToGoLabel.SetLabel(timespan.Format("%H:%M:%S"))

			time.sleep(1)

		print("update thread exiting")
		self.Close(True)



app = wx.App()
frm = Frame(None, title = "Tag Counter", size=(600,800), pos=(100,100), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
thread = StoppableThread(target=frm.update)
thread.start()
frm.Show()
app.MainLoop()