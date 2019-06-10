import http.client

from tkinter import *


import requests
import json

URL = "http://0.0.0.0:8000/store/"
URL2 = "http://0.0.0.0:3000/courses/"


master = Tk()
listbox = Listbox(master, height=30, width=50)

# Get data from server of same computer 
r = requests.get(url=URL)
data = r.json()
data2 = []


# Get data from server of another computer
server2 = 1
try:
 r2 = requests.get(url=URL2)
 data2 = r2.json()
except:
    server2 = 0


# if (len(data2) == 0):

# print(data)

# This function puts current items from database into the listbox
def appendListBox():
    r = requests.get(url=URL)
    data = r.json()
    listbox.pack()
    listbox.insert(END, "List of Courses")
    r = requests.get(url=URL)
    data = r.json()
    try:
        r2 = requests.get(url=URL2)
        global data2
        data2 = r2.json()
    except Exception as error:
        print(error)

    # print(data)
    # print(data2)
    # print(len(data2))
    for item in data:
        listbox.insert(END, item['courseCode'] + ':  ' + item['courseName'])
    for item2 in data2:
        listbox.insert(END, item2['courseCode'] + ':  ' + item2['courseName'])
        



def create():
    courseCode = e2.get()
    courseName = e.get()
    dataBody = {'courseName': courseName, 'courseCode': courseCode}
    headers = {'Content-Type': 'application/json'}
    postRequest = requests.post(URL, json.dumps(dataBody), headers=headers)
    listbox.delete(0, END)
    # print(postRequest)
    appendListBox()

# This function makes put request
def update():
    items = listbox.curselection()
    try:
        items = [data[int(item - 1)] for item in items]
        objectId = items[0]['id']
        courseName = e.get()
        putRequest = requests.put(
        URL, {'objectId': objectId, 'courseName': courseName})
        # print(putRequest)
        listbox.delete(0, END)
        appendListBox()

    except IndexError:
        try :
            items = [data2[int(item - len(data) - 1)] for item in items]
            objectId = items[0]['_id']
            courseName = e.get()
            putRequest = requests.put(
                URL2, {'_id': objectId, 'courseName': courseName})
            print(items[0]['_id'])
            listbox.delete(0, END)
            appendListBox()
        except Exception as err:
            print(err.args)
        # courseName = e.get()
        # putRequest = requests.put(
        #     URL, {'objectId': objectId, 'courseName': courseName})
    
    # appendListBox()


def delete():
    items = listbox.curselection()
    items = [data[int(item - 1)] for item in items]
    objectId = items[0]['id']
    dataBody = {'objectId': objectId}
    headers = {'Content-Type': 'application/json'}
    deleteRequest = requests.delete(
        URL, data=json.dumps(dataBody), headers=headers)
    listbox.delete(0, END)
    appendListBox()


createButton = Button(master, text="Create",
                      command=create)
updateButton = Button(master, text="Update",
                      command=update)
deleteButton = Button(master, text="Delete",
                      command=delete)


createButton.place(x=250, y=50)
updateButton.place(x=300, y=50)
deleteButton.place(x=350, y=50)


createButton2 = Button(master, text="Create2",
                      command=create)
updateButton2 = Button(master, text="Update2",
                      command=update)
deleteButton2 = Button(master, text="Delete2",
                      command=delete)

createButton2.place(x=240, y=80)
updateButton2.place(x=300, y=80)
deleteButton2.place(x=360, y=80)


# Textbox2  Its actually hhe textbox ontop
e2 = Entry(master)
e2.pack()
e2.delete(0, END)
e2.insert(0, "")



# Textbox1
e = Entry(master)
e.pack()
e.delete(0, END)
e.insert(0, "")




appendListBox()
mainloop()



