from tkinter import  *
from random import randint
from tkinter import messagebox
from datetime import *

root = Tk()

topframe = Frame(root)
topframe.grid (row = 0,  column = 0)

root.config(bg='lightblue')

level = [['Junior', 8,8,10],
         ['Middle', 6,15,20],
         ['Hard',8,20,25], 
         ['Nightmare', 8,20,35]]
             
start_time = end_time =0
def all_time():
    return end_time - start_time

var = IntVar() 

cur_lev = 0
def setlevel():
    global cur_lev
    cur_lev = int(var.get())


def startgame():
    global pole
    pole.recreate(level[cur_lev][2],level[cur_lev][1],level[cur_lev][3])
    global start_time
    start_time = datetime.now()
    
gameover = False


def randpos(h,w):
    return([randint(0,h-1), randint(0,w-1)])

class MyButton(Button):
    
    def __init__(self,frm,rr,cc,hh,ww, pole):
        super().__init__(frm,height=hh, width=ww,command = self.func)
        self.r = rr
        self.c = cc
        self.bomb = False
        self.count = 0
        self.opened = False
        self.marked = False
        self.mypole=pole
        self.bind('<B1-Motion>', self.rightclick)
        
    def setlbl(self, s):
        self.opened = not s in ['','#']
        self.config(text = s, font = 'Arial 8 bold')

        
    def func(self):
        if not self.marked:
            global gameover
            if not gameover:
                self.mypole.recover(self.r,self.c)
        else:
             self.marked =  False
             self.setlbl('')
                
            
    def rightclick(self,e):            
            if not self.opened:                
                if not self.marked:
                    self.marked = True
                    self.config(text = '#')
                

class Pole():
    
    def __init__ (self, hh, ww, nn, frm):
        self.wid = ww
        self.hig = hh
        self.bombcount = nn
        self.myframe=frm
        self.create()
        
    def create(self):
        self.pole  = []
        
        for r in range(self.hig):
            self.pole.append([])
            for c in range(self.wid):
                b = MyButton(self.myframe,r,c,1,1,self)
                self.pole[r].append(b)
                self.pole[r][c].grid (row = r+1,  column = c+1)
        
        self.lbl = Label(self.myframe, text='Починай :)')
        self.lbl.bind('<1>', self.callsettings)
        self.lbl.grid(row=self.hig+1, column =0, columnspan=self.wid+1)
        
        self.new()
        
        
    def recreate(self, hh, ww, nn):
         self.wid = ww
         self.hig = hh
         self.bombcount = nn
         for widget in self.myframe.winfo_children():
              widget.destroy()
         self.create()
    
    def new(self):
       
        global gameover
        gameover = False
        global start_time
        start_time = datetime.now()
        self.allclosed = self.wid * self.hig - self.bombcount
        self.lbl.config(text=self.allclosed)
        
        for r in range(self.hig):
            for c in range(self.wid):
               self.pole[r][c].setlbl('')
               self.pole[r][c].bomb = False
               self.pole[r][c].count = 0
               self.pole[r][c].opened = False
               self.pole[r][c].marked = False
               self.pole[r][c].config(bg = 'lightgrey')
               self.pole[r][c].config(fg='black')
                
        for b in range(self.bombcount):
            f = True
            while f:
                r, c = randpos(self.hig, self.wid)
                if not self.pole[r][c].bomb:
                    self.pole[r][c].bomb = True
                    f = False
                    for dr in range(r-1,r+2):
                        for dc in range(c-1,c+2):
                            
                            if dr >=0 and dr<self.hig and dc >=0 and dc < self.wid:
                                    
                                if not self.pole[dr][dc].bomb:
                                    self.pole[dr][dc].count += 1
 
    def recurs(self,r,c):
        if not self.pole[r][c].opened:
            if self.pole[r][c].count > 0:
                self.pole[r][c].setlbl(str(self.pole[r][c].count))
            else:
                self.pole[r][c].setlbl('-')  
            self.pole[r][c].config(bg = 'lightgreen')
            self.allclosed -= 1
            self.lbl.config(text=self.allclosed)
            
            if self.allclosed == 0:
                t = all_time().seconds
                of = open('best.txt', 'a')
                print(cur_lev, t, file=of)
                of.close()
                messagebox.showinfo("Перемога!","Ви виграли!!!\n\nЧас: "+
                ((str(t//60)+' хв ') if t//60>0 else '')+
                 str(t%60)+' с')
                self.new()
            
            elif self.pole[r][c].count == 0:
                for dr in range(r-1,r+2):
                      for dc in range(c-1,c+2):
                            if not (dr == r and dc == c):
                                if dr >=0 and dr<self.hig and dc >=0 and dc < self.wid:
                                    self.recurs(dr,dc)
                                
    def recover(self,r,c):
        global end_time
        end_time = datetime.now()
        global gameover
        if self.pole[r][c].bomb:
            
            gameover = True
            self.pole[r][c].config(fg='red')
            for r in range(self.hig):
                for c in range(self.wid):
                    if self.pole[r][c].bomb and not self.pole[r][c].marked:
                        self.pole[r][c].setlbl('b')
                    if not self.pole[r][c].bomb and self.pole[r][c].marked:
                        self.pole[r][c].config(bg='pink')
            messagebox.showinfo("Ех...","Ой!!!")
            self.new()
        else:
            if not self.pole[r][c].opened:
                    self.recurs(r,c)
        
    def callsettings(self, event):
        settings()
    
    
def settings():
    
    def usesettings():
        global pole
        
        setlevel()
        pole.recreate(level[cur_lev][2],level[cur_lev][1],level[cur_lev][3])
        startgame()
        settingswin.destroy()
        
    def exitgame():
        
        root.quit()
        
    settingswin = Toplevel(root)
    
    settingswin.transient(root)
    settingswin.title( "Налаштування" )
    for el in range(len(level)):
        r1 = Radiobutton(settingswin, text=level[el][0], value =el,variable=var, command = setlevel, padx=30, pady=30)
        r1.pack()

    bStart = Button(settingswin, text = 'Почати', command = usesettings, padx=30, pady=10)
    bStart.pack()
    bCancel = Button(settingswin, text = 'Вийти', command = exitgame, padx=30, pady=10)
    bCancel.pack() 
    settingswin.wait_visibility()
    
    x = root.winfo_x() + root.winfo_width()//2 - settingswin.winfo_width()//2
    y = root.winfo_y() + root.winfo_height()//2 - settingswin.winfo_height()//2
    settingswin.geometry(f"+{x}+{y}")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
pole = Pole(level[0][2],level[0][1],level[0][3], topframe)

settings()

root.mainloop()
