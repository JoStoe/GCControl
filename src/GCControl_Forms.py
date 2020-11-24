# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

wx.ID_2 = 1000
wx.ID_1 = 1001

###########################################################################
## Class MainFrame_preset
###########################################################################

class MainFrame_preset ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"GC Control Software", pos = wx.DefaultPosition, size = wx.Size( 1200,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_load = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Load Chromatogram", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_load )

		self.m_save = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Save Chromatogram", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_save )

		self.m_menu1.AppendSeparator()

		self.m_close = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_close )

		self.m_menubar1.Append( self.m_menu1, u"Data" )

		self.m_menu2 = wx.Menu()
		self.m_about = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_about )

		self.m_menubar1.Append( self.m_menu2, u"Help" )

		self.SetMenuBar( self.m_menubar1 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.panel_graphic = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel_graphic.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		bSizer4.Add( self.panel_graphic, 1, wx.ALL|wx.EXPAND, 0 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.b_readArduino = wx.Button( self, wx.ID_ANY, u"Start Data Acquisition", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.b_readArduino.SetToolTip( u"Connect you detector and start measuring data." )

		bSizer5.Add( self.b_readArduino, 0, wx.ALL|wx.EXPAND, 5 )

		self.b_stopArduino = wx.Button( self, wx.ID_ANY, u"Stop Data Acquisition", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.b_stopArduino.SetToolTip( u"Stop measuring data." )

		bSizer5.Add( self.b_stopArduino, 0, wx.ALL|wx.EXPAND, 5 )

		self.b_saveData = wx.Button( self, wx.ID_ANY, u"Save Chromatogram", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.b_saveData.SetToolTip( u"Save the measured data." )

		bSizer5.Add( self.b_saveData, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		self.b_simulate = wx.Button( self, wx.ID_ANY, u"Simulate Chromatogram", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.b_simulate, 0, wx.ALL, 5 )


		bSizer5.Add( ( 0, 60), 0, wx.EXPAND, 5 )


		bSizer3.Add( bSizer5, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Offset correction:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.check_offset = wx.CheckBox( self, wx.ID_ANY, u"Enable Correction", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_offset.SetValue(True)
		self.check_offset.Enable( False )

		bSizer8.Add( self.check_offset, 0, wx.ALL, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer3.Add( bSizer8, 0, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Deadtime [s]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer61.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_DeadTime = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 600, 40, 0.5 )
		self.m_DeadTime.SetDigits( 1 )
		bSizer61.Add( self.m_DeadTime, 0, wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer61.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer3.Add( bSizer61, 0, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.b_evaluate = wx.Button( self, wx.ID_ANY, u"Evaluate Performance", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.b_evaluate.SetToolTip( u"Check the performance of the measurment." )

		bSizer6.Add( self.b_evaluate, 0, wx.ALL|wx.EXPAND, 5 )

		self.t_perfOutput = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer6.Add( self.t_perfOutput, 1, wx.ALL|wx.EXPAND, 5 )

		self.b_GCSettings = wx.Button( self, wx.ID_ANY, u"GC Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.b_GCSettings, 0, wx.ALIGN_RIGHT|wx.ALL|wx.SHAPED, 5 )


		bSizer3.Add( bSizer6, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer3, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()
		self.timer_simulation = wx.Timer()
		self.timer_simulation.SetOwner( self, wx.ID_2 )
		self.timer_arduinoRead = wx.Timer()
		self.timer_arduinoRead.SetOwner( self, wx.ID_1 )
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.MainWindow_OnClose )
		self.Bind( wx.EVT_SHOW, self.MainWindow_OnStartup )
		self.Bind( wx.EVT_MENU, self.m_load_click, id = self.m_load.GetId() )
		self.Bind( wx.EVT_MENU, self.m_save_click, id = self.m_save.GetId() )
		self.Bind( wx.EVT_MENU, self.m_close_click, id = self.m_close.GetId() )
		self.Bind( wx.EVT_MENU, self.m_about_click, id = self.m_about.GetId() )
		self.b_readArduino.Bind( wx.EVT_BUTTON, self.b_readArduino_click )
		self.b_stopArduino.Bind( wx.EVT_BUTTON, self.b_stopArduino_click )
		self.b_saveData.Bind( wx.EVT_BUTTON, self.b_saveData_click )
		self.b_simulate.Bind( wx.EVT_BUTTON, self.b_simulate_click )
		self.b_evaluate.Bind( wx.EVT_BUTTON, self.b_evaluate_click )
		self.b_GCSettings.Bind( wx.EVT_BUTTON, self.b_GCSettings_click )
		self.Bind( wx.EVT_TIMER, self.timer_simulation_signal, id=wx.ID_2 )
		self.Bind( wx.EVT_TIMER, self.timer_signal, id=wx.ID_1 )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def MainWindow_OnClose( self, event ):
		event.Skip()

	def MainWindow_OnStartup( self, event ):
		event.Skip()

	def m_load_click( self, event ):
		event.Skip()

	def m_save_click( self, event ):
		event.Skip()

	def m_close_click( self, event ):
		event.Skip()

	def m_about_click( self, event ):
		event.Skip()

	def b_readArduino_click( self, event ):
		event.Skip()

	def b_stopArduino_click( self, event ):
		event.Skip()

	def b_saveData_click( self, event ):
		event.Skip()

	def b_simulate_click( self, event ):
		event.Skip()

	def b_evaluate_click( self, event ):
		event.Skip()

	def b_GCSettings_click( self, event ):
		event.Skip()

	def timer_simulation_signal( self, event ):
		event.Skip()

	def timer_signal( self, event ):
		event.Skip()


###########################################################################
## Class AboutFrame_preset
###########################################################################

class AboutFrame_preset ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About GC Control Software", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/about_banner.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_bitmap1, 0, wx.ALL|wx.EXPAND, 0 )

		self.t_licenseInfo = wx.TextCtrl( self, wx.ID_ANY, u"GCControl Software Version 1.0\n2020 Johannes Stöckelmaier\n\n\nThis program uses open-source-software.\n-Python (PSF license)\n-WxPython (wxWindows Library Licence 3.1)\n-WxWidgets (wxWindows Library Licence 3.1)\n-Matplotlib (BSD compatible licenses)\n-NumPy (NumPy license)\n-SciPy (SciPy license)\n-pySerial (BSD license)\n\n\nParts of the source-code were auto-generated by wxFormBuilder.", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer2.Add( self.t_licenseInfo, 5, wx.ALL|wx.EXPAND, 5 )

		self.b_close = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.b_close, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()
		bSizer2.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.AboutFrame_OnClose )
		self.b_close.Bind( wx.EVT_BUTTON, self.b_close_click )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def AboutFrame_OnClose( self, event ):
		event.Skip()

	def b_close_click( self, event ):
		event.Skip()


###########################################################################
## Class SettingsFrame_preset
###########################################################################

class SettingsFrame_preset ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"GC Settings", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 5, 2, 0, 0 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Column length [m]:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText3.Wrap( -1 )

		gSizer1.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_columLength = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0.1, 50, 1, 0.1 )
		self.m_columLength.SetDigits( 1 )
		gSizer1.Add( self.m_columLength, 0, wx.ALL, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Column ID [mm]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		gSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_columnID = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0.1, 10, 4, 0.1 )
		self.m_columnID.SetDigits( 1 )
		gSizer1.Add( self.m_columnID, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Arduino location:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		gSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.text_ArduinoLoc = wx.TextCtrl( self, wx.ID_ANY, u"/dev/ttyACM0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.text_ArduinoLoc, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Simulate Chromatogram:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gSizer1.Add( self.m_staticText6, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.checkBox_Simulate = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.checkBox_Simulate, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


		gSizer1.Add( ( 300, 0), 0, wx.EXPAND, 5 )


		gSizer1.Add( ( 100, 0), 0, wx.EXPAND, 5 )


		bSizer7.Add( gSizer1, 0, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.b_settings_ok = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.b_settings_ok, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()
		bSizer7.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.SettingsFrame_OnClose )
		self.Bind( wx.EVT_SHOW, self.SettingsFrame_OnShow )
		self.b_settings_ok.Bind( wx.EVT_BUTTON, self.b_settings_ok_click )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def SettingsFrame_OnClose( self, event ):
		event.Skip()

	def SettingsFrame_OnShow( self, event ):
		event.Skip()

	def b_settings_ok_click( self, event ):
		event.Skip()


