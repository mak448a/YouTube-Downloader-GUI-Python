import wx
from wx import xrc
import subprocess
import threading


class MyApp(wx.App):
    frame = None
    submit = None
    combo_box = None
    link = None
    status_bar = None
    res = None
    quit_button = None

    def OnInit(self):
        self.res = xrc.XmlResource("resource.xrc")
        self.init_frame()
        return True

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, "mainFrame")
        self.submit = xrc.XRCCTRL(self.frame, "submit")
        self.combo_box = xrc.XRCCTRL(self.frame, "quality")
        self.link = xrc.XRCCTRL(self.frame, "link")
        # self.frame.SetIcon(wx.Icon("icon.ico"))
        self.status_bar = xrc.XRCCTRL(self.frame, "status")
        self.quit_button = xrc.XRCCTRL(self.frame, "quit_item")

        self.frame.Bind(wx.EVT_BUTTON, self.on_submit, id=xrc.XRCID("submit"))
        self.create_menu_bar()
        self.frame.Centre()
        self.frame.Show()

    def create_menu_bar(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = file_menu.Append(wx.ID_EXIT, "Quit", "Quit application")
        menubar.Append(file_menu, '&File')
        help_menu = wx.Menu()
        # About item
        help_menu.Append(wx.ID_ABOUT, "&About", "Information about the program")

        menubar.Append(help_menu, "&Help")
        help_menu.Bind(wx.EVT_MENU, self.on_about_box)
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.on_quit, file_item)

    @staticmethod
    def on_about_box(_):
        wx.MessageBox("This program is licensed under the MIT license.\n\nAuthor: mak448a\n"
                      "Made with: yt-dlp, Python®, pyinstaller\n"
                      "Python License: https://opensource.org/steward/python-software-foundation/" +
                      '\n"Python" is a registered trademark of the Python Software Foundation.\n' +
                      "All licenses for this project are available in the licenses folder."+
                      "\nYou can use \"ALT+H, A\" to access this menu again.",
                      "About", wx.OK | wx.ICON_INFORMATION)

    def on_quit(self, _):
        self.frame.Close()

    def on_submit(self, _):
        link = self.link.GetValue()
        quality = self.combo_box.GetValue()
        if "http" in link:
            print(f"Downloading {link} at {quality} quality")
            self.status_bar.SetStatusText(f"Downloading {link} at {quality} {'quality' if quality == 'Best' else ''}")

            threading.Thread(target=self.download, daemon=True, args=[link, quality]).start()

    def download(self, link, quality):
        print(quality[0:-1])
        process = subprocess.Popen(["yt-dlp", "--no-mtime",
                                    "-S", f"{'height:' + quality[0:-1] if quality != 'Best' else 'quality:Best'},ext"
                                          f":mp4,", "-P", "~/Downloads",
                                    f"{link}"])
        process.wait()
        self.status_bar.SetStatusText("Done downloading! Check your downloads folder.")
        wx.MessageBox("Done downloading! Check your downloads folder.", "Info",
                      wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
