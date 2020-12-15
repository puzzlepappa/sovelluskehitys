from tkinter import *
import psycopg2
from utils import check_password, hash_password


root = Tk()
#Perform connection to database, or fail. change username and password to work with your own database.
try:
    conn = psycopg2.connect(database="tuasbooker", user="db", password="db", host="localhost")
    print("connected")
    cur = conn.cursor()
except:
    print("Cant connect to db")


def adduser():
    hashed = hash_password(password.get())
    var_username = username.get()
    var_email = email.get()

    cur.execute('INSERT INTO "user" (username, email, password) VALUES ('"+var_username+"','"+var_email+"','"+hashed+"')')
    conn.commit()


def insertRoom():
    var_room_name = room_name.get()

    room_name.delete(0, END)

    var_room_desc = room_desc.get()
    room_desc.delete(0, END)
    var_username = username.get()
    cur.execute('SELECT password FROM "user" WHERE username="'+var_username+'"')
    hashed_pass = cur.fetchone()
    writtenpassword = password.get()
    hashed_pass_str = ''.join(hashed_pass)

    if check_password(writtenpassword, hashed_pass_str):

        cur.execute("INSERT INTO rooms (name, description) VALUES (" + var_room_name + ",'" + var_room_desc + "')")
        conn.commit()

        cur.close()
        conn.close()
        test = Label(root, text="added new room")
        test.pack()
    else:
        test2 = Label(root, text="something went wrong, room not added")
        test2.pack()


#here test is tablename, num is the room number which could be replaced by id technically. data is the room description.
# Could make it so its "room id(automatic), room name(manual input) and room desc(manual input).
# We also have who uploaded the room, so some sort of log in functionality needs to be made, or the adminuser just manually inputs the name
myLabel = Label(root, text="Name")
myLabel.pack()
room_name = Entry(root)
room_name.pack()
myLabel = Label(root, text="Description")
myLabel.pack()
room_desc = Entry(root)
room_desc.pack()
mySubmit = Button(root, text="Submit", command=insertRoom)
mySubmit.pack()

usernameLabel = Label(root, text="Username")
usernameLabel.pack()
username = Entry(root)

username.pack()
emailLabel = Label(root, text="email")
emailLabel.pack()
email = Entry(root)

email.pack()
password = Entry(root)

passwordLabel = Label(root, text="password")
passwordLabel.pack()
password.pack()

myButton = Button(root, text="adduser", command=adduser)
myButton.pack()

#root.mainloop()
