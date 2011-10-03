import os
import wx
import hashlib

from wx.lib.wordwrap import wordwrap

##########################################################################################

short_app_name = "Launcher"
long_app_name = "Brian's Spiffy Python App Launcher"

##########################################################################################
class _AppInfoPanel(wx.Panel):
    """
    Notebook AppInfo tabs
    """
    def __init__(self, parent, folder):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        # Static text with the name of the App folder.
        folderBox = wx.StaticBox(self, wx.ID_ANY)
        folderBoxSizer = wx.StaticBoxSizer(folderBox, wx.VERTICAL)
        folderBoxSizer.Add( wx.StaticText(self, wx.ID_ANY, folder), 0, wx.EXPAND | wx.ALL, 1)

        # Create a TextCtrl box containing the README file text.
        try:
            with open(os.path.join(folder, "README"), 'r') as f:
                file_data = f.read()
        except IOError:
            file_data = "[Couldn't open README.]"
        readmeText = wx.TextCtrl(self, wx.ID_ANY, file_data, size=(600,100),
                                 style=(wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_READONLY))
        readmeBox = wx.StaticBox(self, wx.ID_ANY, "README")
        readmeSizer = wx.StaticBoxSizer(readmeBox, wx.VERTICAL)
        readmeSizer.Add(readmeText, 0, wx.TOP | wx.LEFT, 10)

        # Create a list of expected files and the MD5 checksum? Validity checking here?
        # Enable/disable of the "launch" button based on this?
        # (File name in red if not found; MD5 checksum in red if not correct.)
        # File list convention - first file is the one to call.

        filesText = []

        try:
            with open(os.path.join(folder, "FILES.txt"), 'rb') as f:
                file_data = f.readlines()
                for line in file_data:
                    # Remove the trailing newline, and split the line into a list called 'record'
                    record = line.rstrip("\r\n").split(' ')
                    if len(record) == 2:
                        md5 = hashlib.md5()
                        with open(os.path.join(folder, record[0] ),'rb') as g:
                            for chunk in iter(lambda: g.read(8192), ''):
                                md5.update(chunk)
                        if md5.hexdigest() == record[1]:
                            # MD5 checksum is ok.
                            filesText.append("%s    %s\n" % (record[0], record[1]))
                        else :
                            # MD5 checksum is wrong, print both, with correct value in square brackets.
                            filesText.append("%s    %s    [%s]\n" % (record[0], record[1], md5.hexdigest()))
        except IOError:
            pass

        filesTextCtrl = wx.TextCtrl(self, wx.ID_ANY, "".join("%s" % (s) for s in filesText), size=(600,100),
                                    style=(wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_READONLY))
        filesBox = wx.StaticBox(self, wx.ID_ANY, "FILES")
        filesSizer = wx.StaticBoxSizer(filesBox, wx.VERTICAL)
        filesSizer.Add(filesTextCtrl, 0, wx.TOP | wx.LEFT, 10)

        ##############################################

        # Create a button which launches the App. Will need to remember the ID for each instance? Or can 'self' instantiation handle it?
        # May need to cd to this folder, launch, then "cd .." ?

            
        # This is the sizer which ties together the other items, vertically.
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(folderBoxSizer, 0, wx.EXPAND | wx.ALL, 1)
        border.Add(readmeSizer, 0, wx.EXPAND | wx.ALL, 0)
        border.Add(filesSizer, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(border)
    #----------------------------------------------------------------------
##########################################################################################
class _NotebookSetup(wx.Notebook):
    """
    Notebook Setup
    """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

        dirname = os.getcwd()

        # Get a list of all sub-folders in the current working directory.
        self.folder_list = [f for f in os.listdir(dirname)
                               if os.path.isdir(os.path.join(dirname, f))]

        for folder in self.folder_list:
            self.AddPage(_AppInfoPanel(self, folder), "App Info - " + folder)
##########################################################################################
class _MainWindow(wx.Frame):
    """
    Main Window
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1500, 800))

        self.CreateStatusBar()

        filemenu = wx.Menu()
        menuExit = filemenu.Append(wx.ID_EXIT, "Exit", " Terminate the Launcher")

        helpmenu = wx.Menu()
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "About", " Info about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")
        menuBar.Append(helpmenu, "Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        panel = wx.Panel(self)
        self.notebook = _NotebookSetup(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.Layout()
        self.Show(True)
    #-------------------------------------------------------------------------------------
    def OnAbout(self, e):
        info = wx.AboutDialogInfo()
        info.Name = short_app_name + " (" + long_app_name + ")"

        info.Copyright = "(C) 2011 Brian Myers"
        info.Description = wordwrap("This program blah blah blah ",
                                    350, wx.ClientDC(self))
        info.WebSite = ("https://github.com/brianmyers", "Brian's github page")
        wx.AboutBox(info)
    #-------------------------------------------------------------------------------------
    def OnExit(self, e):
        self.Close(True)
    #-------------------------------------------------------------------------------------
##########################################################################################
app = wx.App(False)
frame = _MainWindow(None, long_app_name)
app.MainLoop()
##########################################################################################
