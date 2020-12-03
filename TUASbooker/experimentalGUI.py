from tkinter import *
import psycopg2
root = Tk()
##probably not the right way to do this as it doesnt seem to connect
try:
    conn=psycopg2.connect(database="tuasbooker", user="do_it_yourself",password="apapap",host="localhost")
    print("connected")
    cur = conn.cursor()
except:
    print("Cant connect to db")

def insertRoom():
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
    conn.commit()
    cur.close()
    conn.close()

def openRoomSetup():
    myLabel = Label(root, text="Name")
    myLabel.pack()
    e = Entry(root)
    e.pack()
    myLabel = Label(root, text="Description")
    myLabel.pack()
    e = Entry(root)
    e.pack()
    mysubmit = Button(root,text="Submit", command=insertRoom)
    mysubmit.pack()

myButton = Button(root, text="Room creation", command=openRoomSetup)
myButton.pack()






root.mainloop()