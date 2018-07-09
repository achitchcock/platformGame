from tkinter import *
from functools import partial


class App(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.canvas = Canvas(self.master, width=600, height=600, bg='white' )
        self.canvas.grid(row=0, column=0)
        self.images = [PhotoImage(file="stop.gif"),
                       PhotoImage(file="jump.gif"),
                       PhotoImage(file="left.gif"),
                       PhotoImage(file="right.gif")]

        self.master.bind("<KeyPress>",self.start)
        self.master.bind("<KeyRelease>",self.stop)

        self.player = self.canvas.create_image(50,400,anchor=S,image=self.images[0])
        
        self.canvas.create_rectangle(0,400,600,440, fill='green')
        self.canvas.create_rectangle(150,340,300,350, fill='green')
        self.canvas.create_rectangle(300,280,500,290, fill='green')
        self.canvas.create_rectangle(500,220,800,230, fill='green')
        
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = -24
        self.onSurface = True
        self.speed = 15
        self.screenUpdate()

    def start(self, event):
        key = event.keysym
        if key == 'a':
            self.left = True
        if key == 'd':
            self.right = True
        if key =='space':
            self.onsurface = False
            self.up = True

    def delayStop(self, key):
        if self.up or self.down:
            self.master.after(10, self.delayStop,(key))
            return
        if self.speed > 1:
            self.speed /= 1.5
            self.master.after(100, self.delayStop,(key))
            return
        if key == 'a' and self.speed < 1:
            self.left = False
        if key == 'd' and self.speed < 1:
            self.right = False
        self.speed = 15

    def stop(self, event):
        key = event.keysym
        if key == 'a':
            self.left = False
            #self.master.after(100, self.delayStop,(key))
        if key == 'd':
            self.right = False
            #self.master.after(100,self.delayStop, (key))
        if key == 'space':
            self.up = True


    def screenUpdate(self):
        loc = self.canvas.coords(self.player)
        #print(loc)
        x1 = loc[0] - 18
        x2 = loc[0] + 18
        y1 = loc[1] -10
        y2 = loc[1] + 10
        '''try:
            self.canvas.delete(self.bbox)
        except:
            pass
        self.bbox = self.canvas.create_rectangle(x1, y1, x2, y2)'''
        over = list(self.canvas.find_overlapping(x1, y1, x2, y2))
        #over.remove(self.bbox)
        over.remove(self.player)
        if len(over) == 0 and self.onSurface and not self.up:
            print('falling')
            self.down = True
            self.onSurface = False
            self.jump = 2
            self.master.after(100,self.screenUpdate)
            return
        if self.left:
            self.canvas.itemconfig(self.player, image=self.images[2])
            self.canvas.move(self.player,-self.speed,0)
            #self.canvas.move(self.bbox,-self.speed,0)
        if self.right:
            self.canvas.itemconfig(self.player, image=self.images[3])
            self.canvas.move(self.player,self.speed,0)
            #self.canvas.move(self.bbox,self.speed,0)
        if self.up:
            self.canvas.itemconfig(self.player, image=self.images[1])
            self.canvas.move(self.player,0,self.jump)
            #self.canvas.move(self.bbox,0,self.jump)
            self.jump += 4
            if self.jump >= 0:
                self.up = False
                self.down = True
        if self.down:
            self.canvas.itemconfig(self.player, image=self.images[1])
            self.canvas.move(self.player,0,self.jump)
            #self.canvas.move(self.bbox,0,self.jump)
            if self.jump <= 16:
                self.jump += 4
            print(over)
            if len(over) > 0:
                self.down = False
                self.onSurface = True
                self.jump = -24
                print(self.canvas.coords(self.player,loc[0],self.canvas.coords(over[0])[1]))
            #if 
            #if self.jump > 16:
                #self.down = False
                #self.jump = -16
        #print(self.jump)
            
        if not (self.left or self.right or self.up or self.down):
            self.canvas.itemconfig(self.player, image=self.images[0])

            
        self.master.after(100,self.screenUpdate)
        
            

myApp = App(Tk())
myApp.mainloop()
