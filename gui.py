from tkinter import *

def getSelectedRow(event):
    global selectedTuple
    try:
        selectedTuple=list1.get(list1.curselection()[0])
        e1.delete(0,END)
        e1.insert(END,selectedTuple[1])
      
    except IndexError:
        pass

def deleteFunction():
   
    view()

def view():
    list1.delete(0,END)
    

def searchFunction():
    list1.delete(0,END)
    

def addItem():
    list1.delete(0,END)
    

def updateFunction():
    pass

window = Tk()
window.wm_title("CS121 Search Index")

titleLB = Label(window,text="Enter query")
titleLB.grid(row=0,column=0)




titleText = StringVar()
e1 = Entry(window,textvariable=titleText)
e1.grid(row=0,column=1)



list1 = Listbox(window, height=6,width=35)
list1.grid(row=2,column=0,rowspan=6,columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=3,column=2,rowspan=4)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind("<<ListboxSelect>>",getSelectedRow)


SearchBtn = Button(window,text="Search entry",width=12,command=searchFunction)
SearchBtn.grid(row=2,column=3)

closeBtn = Button(window,text="Close",width=12,command=window.destroy)
closeBtn.grid(row=3,column=3)

window.mainloop()
