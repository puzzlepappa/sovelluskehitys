from tkinter import *
import psycopg2
root = Tk()
##Perform connection to database, or fail. change username and password to work with your own database.
try:
    conn=psycopg2.connect(database="tuasbooker", user="do_it_yourself",password="apapap",host="localhost")
    print("connected")
    cur = conn.cursor()
except:
    print("Cant connect to db")

def insertRoom():
    var_room_name = room_name.get()

    room_name.delete(0,END)

    var_room_desc = room_desc.get()
    room_desc.delete(0,END)
##here test is tablename, num is the room number which could be replaced by id technically. data is the room description.
## Could make it so its "room id(automatic), room name(manual input) and room desc(manual input).
## We also have who uploaded the room, so some sort of log in functionality needs to be made, or the adminuser just manually inputs the name
    cur.execute("INSERT INTO test (num, data) VALUES ("+var_room_name+",'"+var_room_desc+"')")
    conn.commit()
    cur.close()
    conn.close()

myLabel = Label(root, text="Name")
myLabel.pack()
room_name = Entry(root)
room_name.pack()
myLabel = Label(root, text="Description")
myLabel.pack()
room_desc = Entry(root)
room_desc.pack()
mysubmit = Button(root,text="Submit", command=insertRoom)
mysubmit.pack()







root.mainloop()