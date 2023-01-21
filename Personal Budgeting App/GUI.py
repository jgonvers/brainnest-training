from tkinter import *
win=Tk()
win.geometry('500x500+150+150')
win.title('budgeting app')

def func1():
    newWindow = Toplevel(win)
    newWindow.title("data entry")
    newWindow.geometry("400x280")
    
    def func2(event=None):
        typee=ent2.get()
        amount=ent3.get()
        description=ent4.get()
        datetime=ent5.get()
        print(typee,amount,description,datetime)
        
    def func3(event=None):
        ent2.delete(0,END)
        ent3.delete(0,END)
        ent4.delete(0,END)
        ent5.delete(0,END)
        
    lbl1=Label(newWindow,
               text='Please enter below data then press add',
               bg='red',
               fg='white',
               font=(4))
    lbl1.grid(row=1,column=1,columnspan=2)
    lbl2=Label(newWindow,
               text='type',
               width=10,
               bg='white',
               fg='black',
               font=(3))
    lbl2.grid(row=2,column=1)
    lbl3=Label(newWindow,
               text='amount',
               width=10,
               bg='grey',
               fg='black',
               font=(3))
    lbl3.grid(row=3,column=1)
    lbl4=Label(newWindow,
               text='description',
               width=10,
               bg='white',
               fg='black',
               font=(3))
    lbl4.grid(row=4,column=1)
    lbl5=Label(newWindow,
               text='datetime',
               width=10,
               bg='grey',
               fg='black',
               font=(3))
    lbl5.grid(row=5,column=1)
    
    ent2=Entry(newWindow,
               width=20,
               bg='white',
               fg='black',
               font=(3))
    ent2.grid(row=2,column=2)
    ent3=Entry(newWindow,
               width=20,
               bg='grey',
               fg='black',
               font=(3))
    ent3.grid(row=3,column=2)
    ent4=Entry(newWindow,
               width=20,
               fg='black',
               font=(3))
    ent4.grid(row=4,column=2)
    ent5=Entry(newWindow,
               width=20,
               bg='grey',
               fg='black',
               font=(3))
    ent5.grid(row=5,column=2)
    bn2=Button(newWindow,text='Add',
           width=10,
           font=(4),
           bg='yellow',
           fg='black',
           bd=2,
           command=func2)
    bn2.grid(row=6,column=1,columnspan=2)
    bn3=Button(newWindow,text='Clear',
           width=10,
           font=(4),
           bg='orange',
           fg='black',
           bd=2,
           command=func3)
    bn3.grid(row=7,column=1,columnspan=2)
    ent2.bind('<Return>',lambda event:ent3.focus())
    ent3.bind('<Return>',lambda event:ent4.focus())
    ent4.bind('<Return>',lambda event:ent5.focus())
    ent5.bind('<Return>',lambda event:bn2.focus())
    bn2.bind('<Return>',func2)

def func4():
    goalWindow = Toplevel(win)
    goalWindow.title("set goals")
    goalWindow.geometry("400x280")
    def func5(event=None):
        goaldatetime=ent7.get()
        goalamount=ent8.get()
        print(goaldatetime,goalamount)
        
    def func6(event=None):
        ent7.delete(0,END)
        ent8.delete(0,END)
    lbl6=Label(goalWindow,
               text='Please enter goals then press add',
               bg='red',
               fg='white',
               font=(4))
    lbl6.grid(row=1,column=1,columnspan=2)
    lbl7=Label(goalWindow,
               text='datetime',
               width=15,
               bg='white',
               fg='black',
               font=(3))
    lbl7.grid(row=2,column=1)
    lbl8=Label(goalWindow,
               text='amount of money',
               width=15,
               bg='grey',
               fg='black',
               font=(3))
    lbl8.grid(row=3,column=1)
    ent7=Entry(goalWindow,
               width=15,
               bg='white',
               fg='black',
               font=(3))
    ent7.grid(row=2,column=2)
    ent8=Entry(goalWindow,
               width=15,
               bg='grey',
               fg='black',
               font=(3))
    ent8.grid(row=3,column=2)
    bn5=Button(goalWindow,text='Add',
           width=10,
           font=(4),
           bg='yellow',
           fg='black',
           bd=2,
           command=func5)
    bn5.grid(row=4,column=1,columnspan=2)
    bn6=Button(goalWindow,text='Clear',
           width=10,
           font=(4),
           bg='orange',
           fg='black',
           bd=2,
           command=func6)
    bn6.grid(row=5,column=1,columnspan=2)
    ent7.bind('<Return>',lambda event:ent8.focus())
    ent8.bind('<Return>',lambda event:bn5.focus())
    bn5.bind('<Return>',func5)
    
bn1=Button(win,text='Insert',
           width=15,
           font=(14),
           bg='green',
           fg='white',
           bd=2,
           command=func1)
bn1.grid(row=1,column=1)
bn4=Button(win,
           text='Set goals',
           width=20,
           bg='orange',
           fg='white',
           font=(10),
           bd=2,
          command=func4)
bn4.grid(row=1,column=2)

win.mainloop()
