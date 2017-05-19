#!/usr/bin/python3

from tkinter import *
from icomCIVUtils import *
from tkinter.filedialog import *

fields = 'CW Memory #1', \
         'CW Memory #2', \
         'CW Memory #3', \
         'CW Memory #4'
MWIN_WIDTH = 55

COMPORT = 'COM3'
BAUDRATE = '19200'
CIVADDR = '6E'


class appMain():
   def __init__(self, master = None):
      if (master == None):
         root = Tk()
         self.root = root
      ents = self.makeform(root, fields)
      self.port=COMPORT
      self.baudrate=BAUDRATE
      self.addr=CIVADDR
      root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))   
      b1 = Button(root, text='Read from Rig',
             command=(lambda e=ents: self.readrig(e)))
      b1.pack(side=LEFT, padx=5, pady=5)
      b2 = Button(root, text=' Write to Rig ', 
             command=(lambda e=ents: self.writerig(e)))
      b2.pack(side=LEFT, padx=5, pady=5)
      # create a pulldown menu, and add it to the menu bar   
      menubar = Menu()
      filemenu = Menu(menubar, tearoff=0)
      filemenu.add_command(label="Open", command=(lambda e=ents: self.readfile(e)))
      filemenu.add_command(label="Save", command=(lambda e=ents: self.writefile(e)))
      filemenu.add_separator()
      filemenu.add_command(label="Configure", command=self.configure)
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=root.quit)
      menubar.add_cascade(label="File", menu=filemenu)
      # display the menu
      root.config(menu=menubar)
      root.title("ICOM CW Memory Manager")
      
      root.mainloop()
        
   def __version__(self):
      return "0.0.3"

   def fetch(self, entries):
      for entry in entries:
         field = entry[0]
         text  = entry[1].get()
         print('%s: "%s"' % (field, text)) 

   def makeform(self, root, fields):
      entries = []
      for field in fields:
         row = Frame(root)
         lab = Label(row, width=15, text=field, anchor='w')
         ent = Entry(row, width = MWIN_WIDTH)
         row.pack(side=TOP, fill=X, padx=5, pady=5)
         lab.pack(side=LEFT)
         ent.pack(side=RIGHT, expand=YES, fill=X)
         entries.append((field, ent))
      return entries

   def readrig(self, e):
      app = icomCIVUtils(self.port, self.baudrate)
      memno = 1
      for entry in e:
      	mem1text = app.getrig_cwmemory(app.sport, self.addr, chr(memno+48) )
#      	app.hexdump(mem1text)
      	field = entry[0]
      	entry[1].delete(0,END)
      	entry[1].insert(0, mem1text)
      	memno+=1
#      self.fetch(e)

   def writerig(self, e):
#      print("Code to write rig memories goes here.")
      app = icomCIVUtils(self.port, self.baudrate)
      memno = 1
      for entry in e:
         field = entry[0]
         text  = entry[1].get()
         app.setrig_cwmemory(app.sport, self.addr, chr(memno+48), text)
#         print('%s: "%s"' % (field, text)) 
         memno+=1
#      self.fetch(e)

   def readfile(self, entries):
      print("Code to read rig memory file goes here.")
      name = askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                             title = "Choose a file."
                           )      
      if name != None:
         with open(name,'r') as UseFile:
            for entry in entries:
               text = UseFile.readline()
               entry[1].delete(0,END)
               entry[1].insert(0,text)
               print('%s' % (text)) 


   def writefile(self, entries):
      print("Code to write rig memory file goes here.")
      name=asksaveasfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                             title = "Save File As..."
                           )      
      print ("file name: %s"%(name))
      if (name != None):
         with open(name, 'a') as out:
            for entry in entries:
               field = entry[0]
               text  = entry[1].get()
               out.write(text + '\n')         
               print('%s: "%s"' % (field, text)) 


   def configure(self):
      print("Code to configure serial port goes here.")
      window = Tk()
      window.title("Serial Port Configuration")
      Label(window, width=10, text='COM PORT:').grid(row=0)
      Label(window, width=10, text='BAUD RATE:').grid(row=1)
      Label(window, width=10, text='CIV  ADDR:').grid(row=2)
      sport = Entry(window, width=10)
      baud = Entry(window, width=10)
      civ = Entry(window, width=4)
      b1 = Button(window, text='Save',
             command=(lambda: self.updateconfig(sport, baud, civ)))
      sport.grid(row=0, column=1)
      baud.grid(row=1, column=1)
      civ.grid(row=2, column=1)
      b1.grid(row=3, column=0)
      sport.insert(0,self.port)
      baud.insert(0, self.baudrate)
      civ.insert(0, self.addr)

   def updateconfig(self,sport,baud, civ):
      self.port = sport.get()
      self.baudrate = baud.get()
      self.addr = civ.get()


if __name__ == '__main__':
   app = appMain()

