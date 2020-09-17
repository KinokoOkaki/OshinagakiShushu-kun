import tkinter as tk
from tkinter import ttk
import twitterOauth as ot
import tweepyProcess as tt
import datetime
import calendar
from tkinter import messagebox
import threading
import circlePostion
import os
import tkinter.filedialog

consumer_key = 'EWZEu7RBUhJ4nfy9fawZ1tTWc'
consumer_secret = 'hlyr7GPr4F1969wY5XEGutrXj00DHEbgO50ZiEKjOMFQJd7H4V'
accessToken = dict()
requestToken = dict()
isOauth = False

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,height=800,width=800)
        self.master = master
        self.master.title("お品書き取集君")
        self.master.geometry("800x800")
        self.pack()
        self.createWidgets()

#ウィジェットを配置する関数をまとめてる関数
    def createWidgets(self):
        self.oauthWidgets()
        self.listwidgets()
        self.outputOptionWidgets()
        self.searchPeriodWidgets()
        self.output()

#認証を行うウィジェットを配置する関数
    def oauthWidgets(self):
        self.oauthFrame = ttk.Frame(self, padding=10)
        self.oauthFrame.place(relheight=1/3,relwidth=3/5,relx=0,rely=0)
        self.optionLable=ttk.Label(self.oauthFrame, text="認証", font=("", 20), padding = (0,20,0,5))
        self.optionLable.pack()
        self.oauther = tk.Button(self.oauthFrame)
        self.oauther["text"] = "Twitter認証"
        self.oauther["command"] = self.oauthButton
        self.oauther.pack(side="top")
        self.warningText = tk.StringVar()
        self.warningText.set("認証されていません")
        self.warningLabel = tk.Label(self.oauthFrame, textvariable = self.warningText,fg= "red")
        self.warningLabel.pack()

#twitterのリスト一覧を表示する関数
    def listwidgets(self):
        self.listFrame = ttk.Frame(self, padding=10)
        self.listFrame.place(relheight=2/3,relwidth=3/5,relx=0,rely=1/3)
        self.optionLable=ttk.Label(self.listFrame, text="リスト", font=("", 20), padding = (0,20,0,5))
        self.optionLable.pack()
        self.listName = []
        self.listV = tk.StringVar(value = self.listName)
        self.listBox = tk.Listbox(self.listFrame, listvariable = self.listV, selectmode = 'single', height=10, width=20, font=('',15))
        self.listBox.pack()        

#出力オプションを表示するための関数
    def outputOptionWidgets(self):
        self.outputOptionFrame = ttk.Frame(self, padding=10)
        self.outputOptionFrame.place(relheight=2/3,relwidth=2/5,relx=3/5,rely=1/3)
        self.optionLable=ttk.Label(self.outputOptionFrame, text="出力オプション", font=("", 20), padding = (0,20,0,5))
        self.optionLable.pack()
        self.frame = ttk.Frame(self.outputOptionFrame, padding=10, relief='groove')
        self.csvFrame = ttk.Frame(self.outputOptionFrame, padding=10, relief='groove')

        self.dirButton = tk.Button(self.outputOptionFrame, text='保存先ディレクトリ', command=self.file_open)
        self.dirButton.pack()
        self.directory = tk.StringVar()
        self.directory.set(str(os.path.dirname(__file__)))
        self.dirEntry = tk.Entry(self.outputOptionFrame, textvariable=self.directory,width=80)
        self.dirEntry.pack()

        self.opt1=tk.BooleanVar()
        self.opt2=tk.BooleanVar()
        self.opt1.set(True)
        self.opt2.set(True)
        self.opts2=[tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()]
        for i in self.opts2:
            i.set(True)
        self.optionStr=["アカウント名", "ツイート本文", "ツイートURL", "画像名", "サークル場所"]
        self.imageOutput = ttk.Checkbutton(self.outputOptionFrame, text = "画像出力", command=self.detailsImage, variable = self.opt1)
        self.imageOutput.pack()
        self.frame.pack()
        
        self.opts = tk.BooleanVar()
        self.opts.set(True)
        self.byAuthor = tk.Radiobutton(self.frame, text="作者別でフォルダに分ける", value = True, variable = self.opts)
        self.byOneFilder = tk.Radiobutton(self.frame, text="一つのフォルダにまとめる", value = False, variable = self.opts)
        self.byAuthor.grid(row=0, column=0)
        self.byOneFilder.grid(row=0, column=1)

        self.csvOutput = ttk.Checkbutton(self.outputOptionFrame, text = "CSV出力", command=self.detailsCsv, variable = self.opt2)
        self.csvOutput.pack()
        self.csvFrame.pack()
        self.detailsCsvs = []
        for i in range(len(self.optionStr)):
            tmp = tk.Checkbutton(self.csvFrame, text = self.optionStr[i], variable = self.opts2[i])
            tmp.grid(row=int(i/2), column=i%2)
            self.detailsCsvs.append(tmp)

#ディレクトリを指定するためのウィンドウを表示する関数
    def file_open(self):
        ret = tk.filedialog.askdirectory(initialdir = os.path.dirname(__file__), title = "保存先", mustexist = True)
        self.directory.set(str(ret))

#検索期間を指定するウィジェットを配置する関数
    def searchPeriodWidgets(self):
        self.searchPeriodFrame = ttk.Frame(self, padding=10)
        self.searchPeriodFrame.place(relheight=1/3,relwidth=2/5,relx=3/5,rely=0)
        self.searchPeriodLabel=ttk.Label(self.searchPeriodFrame, text="検索期間", font=("", 20), padding = (0,20,0,5))
        self.searchPeriodLabel.pack()
        todayData = datetime.datetime.today()
        yVal = tk.StringVar()
        yVal.set(todayData.year)
        mVal = tk.StringVar()
        mVal.set(todayData.month)
        self.dVal = tk.StringVar()
        self.dVal.set(todayData.day)
        self.sframe = ttk.Frame(self.searchPeriodFrame, padding=10, relief='groove')
        self.sframe.pack()
        self.annotationLable=ttk.Label(self.sframe, text="当落発表日などが適切です。")
        self.annotationLable.pack()
        yLable=ttk.Label(self.sframe, text="年")
        mLable=ttk.Label(self.sframe, text="月")
        dLable=ttk.Label(self.sframe, text="日")
        self.ySpinBox = tk.Spinbox(self.sframe, 
                                textvariable = yVal, 
                                from_=1900, 
                                to=todayData.year, 
                                increment=1,
                                width=10, 
                                justify='center',
                                command=self.refreshDateSpinBox)
        self.mSpinBox = tk.Spinbox(self.sframe, 
                                textvariable = mVal, 
                                from_=1, 
                                to=12,
                                increment=1,
                                width=10, 
                                justify='center',
                                command=self.refreshDateSpinBox)
        self.dSpinBox = tk.Spinbox(self.sframe, 
                                textvariable = self.dVal, 
                                from_=1, 
                                to=self.getLastDate(int(self.ySpinBox.get()),int(self.mSpinBox.get())), 
                                increment=1,
                                width=10, 
                                justify='center')

        self.ySpinBox.pack(side='left')
        yLable.pack(side='left')
        self.mSpinBox.pack(side='left')
        mLable.pack(side='left')
        self.dSpinBox.pack(side='left')
        dLable.pack(side='left')
    
#出力ボタンの表示
    def output(self):
        self.outputFrame = ttk.Frame(self.outputOptionFrame, padding=10)
        self.outputFrame.pack()
        self.quit = ttk.Button(self.outputFrame, text="QUIT",
                              command = self.master.destroy)
        self.quit.pack(side="left")
        self.outputButton = ttk.Button(self.outputFrame, text="出力",
                              command = self.callSearchTwitter)
        self.outputButton.pack(side="left")

#出力処理
    def callSearchTwitter(self):
        global isOauth
        global app
        errorMsg = ''
        selectionIndex = self.listBox.curselection()

        if not isOauth:
            errorMsg += '・認証がされていません。\n'
        if not selectionIndex :
            errorMsg += '・リストが選択されていません。\n'
        if not (self.opt1.get() or self.opt2.get()):
            errorMsg += '・出力内容がありません。\n'
        if not any(self.opts2):
            errorMsg += '・CSV出力内容がありません。\n'
        if datetime.datetime.today() < datetime.datetime(int(self.ySpinBox.get()), int(self.mSpinBox.get()), int(self.dSpinBox.get())):
            errorMsg += '・検索期間を現在より先にすることはできません。\n'
        if self.directory.get() == "":
            errorMsg += '・保存先を設定してください'
        if not errorMsg == '':
            self.showError(errorMsg)
            return

        self.progress = progressWindow(self.master)

        progressThread = threading.Thread(target = lambda : [self.progress.createWidgets(selectionIndex[0])])
        searchThread = threading.Thread(target=lambda : [tt.searchTweet(consumer_key, 
                                                                            consumer_secret,
                                                                            accessToken['oauth_token'], 
                                                                            accessToken['oauth_token_secret'],
                                                                            selectionIndex[0],
                                                                            datetime.datetime(int(self.ySpinBox.get()), int(self.mSpinBox.get()), int(self.dSpinBox.get())),
                                                                            [self.opt1, self.opts],
                                                                            [self.opt2, self.opts2],
                                                                            self.progress)])
        progressThread.start()
        searchThread.start()

    def doneOutput(self):
        self.showInfo("抽出完了")
        self.progress.destroyWindow()

    def showError(self, msg):
        messagebox.showerror('Error', msg)
    
    def showInfo(self, msg):
        messagebox.showinfo('終了', msg)

#各月の最終日をスピンボックスに設定する関数
    def refreshDateSpinBox(self):
        self.dSpinBox.configure(to=self.getLastDate(int(self.ySpinBox.get()),int(self.mSpinBox.get())))

#与えられた年月を用いてその月の最終日を返す関数
    def getLastDate(self, year, month):
        return calendar.monthrange(year, month)[1]

#画像出力の詳細オプションの表示・非表示を切り替える関数
    def detailsImage(self):
        if self.imageOutput.instate(['selected']):
            self.byAuthor = tk.Radiobutton(self.frame, text="作者別でフォルダに分ける", value = 0, variable = self.opts)
            self.byOneFilder = tk.Radiobutton(self.frame, text="一つのフォルダにまとめる", value = 1, variable = self.opts)
            self.byAuthor.grid(row=0, column=0)
            self.byOneFilder.grid(row=0, column=1)
        elif self.imageOutput.instate(['!selected']):
            children = self.frame.winfo_children()
            for child in children:
                child.destroy()

#CSV出力の詳細オプションの表示・非表示を切り替える関数
    def detailsCsv(self):
        if self.csvOutput.instate(['selected']):
            for i in range(4):
                tmp = tk.Checkbutton(self.csvFrame, text = self.optionStr[i], variable = self.opts2[i])
                tmp.grid(row=int(i/2), column=i%2)
                self.detailsCsvs.append(tmp)
                
        elif self.csvOutput.instate(['!selected']):
            self.detailsCsvs.clear
            children = self.csvFrame.winfo_children()
            for child in children:
                child.destroy()

#認証ボタンが押されたときの処理
    def oauthButton(self):
        global requestToken
        oauthWindow(self.master)
        requestToken = ot.getRequestToken(consumer_key, consumer_secret)

#認証完了後リストを取得するための関数
    def getLists(self):
        lists=tt.getList(consumer_key, consumer_secret, accessToken['oauth_token'], accessToken['oauth_token_secret'])
        for res in lists:
            self.listBox.insert(lists.index(res), res.name)

#twitter認証するための別ウィンドウ
class oauthWindow(tk.Frame):
    def __init__(self, master):
        self.top=tk.Toplevel(master)
        self.top.attributes('-topmost', True)
        self.frame=tk.Frame(self.top)
        labelExample = tk.Label(self.top, text = "認証が完了したらPINを入力してください")
        entryExample = tk.Entry(self.top)
        buttonExample = tk.Button(self.top)
        buttonExample["text"] = "認証"
        buttonExample["command"] = lambda : [self.windowDestory(entryExample), self.top.destroy()]
        self.top.geometry("400x200")

        self.frame.pack()
        labelExample.pack()
        entryExample.pack()
        buttonExample.pack()

#PIN入力完了後にウィンドウを閉じる処理
    def windowDestory(self, entryExample):
        global requestToken
        global accessToken
        global app
        global isOauth
        pin = entryExample.get()
        accessToken = ot.getAccessToken(pin, consumer_key, consumer_secret, requestToken)
        if 'oauth_token' in accessToken :
            app.warningText.set("認証済み")
            app.warningLabel["fg"] = 'green'
            isOauth=True
        else:
            app.showError("認証失敗")
        self.top.destroy()
        app.getLists()

#進捗をプログレスバーで表示
class progressWindow(tk.Frame):
    def __init__(self, master):
        self.top=tk.Toplevel(master)
        self.top.attributes('-topmost', True)
        self.progressFrame=tk.Frame(self.top)
        
    
    def createWidgets(self, selectionIndex):
        self.maxa = tt.getMember(consumer_key, 
                        consumer_secret,
                        accessToken['oauth_token'], 
                        accessToken['oauth_token_secret'],
                        selectionIndex)

        self.pVal = tk.IntVar(value=0)
        self.progressBar = ttk.Progressbar(self.progressFrame,
                                            orient = 'horizontal',
                                            variable = self.pVal,
                                            maximum=self.maxa,
                                            length=200,
                                            mode = 'determinate')
        self.progressBar.grid(row=0, column=0)

        self.progressText = tk.StringVar()
        self.progressText.set("0/"+str(self.maxa))
        self.progressLabel = tk.Label(self.progressFrame, textvariable=self.progressText)
        self.progressLabel.grid(row=0, column=1)

        self.loadNameText = tk.StringVar()
        self.loadNameText.set("")
        self.loadNameLabel = tk.Label(self.progressFrame, textvariable=self.loadNameText)
        self.loadNameLabel.grid(row=1, column=0)

        self.progressFrame.pack()
        self.top.geometry("400x400")
    
    def moveProgress(self, newVal, name):
        global app
        self.pVal.set(newVal)
        self.progressText.set(str(newVal)+"/"+str(self.maxa))
        self.loadNameText.set(name)
        if(newVal == self.maxa):
            app.doneOutput()
    
    def destroyWindow(self):
        self.top.destroy()

def main():
    global app
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__=="__main__":
    main()