from _tkinter import TclError
from tkinter import Tk, Listbox, END, Menu, LEFT, RIGHT, Scrollbar, ttk, Button, Entry, Toplevel, Label, Frame
import os
import shutil
from tkinter.messagebox import showerror, askyesno
import string
import math
import time


def newTXTFile():
    try:
        global fileCount
        if fileCount == 1:
            if f"{fileName}.txt" in os.listdir(openedFolder):
                raise FileExistsError
            else:
                open(f"{openedFolder}\\{fileName}.txt", 'a').close()
        else:
            if f"{fileName} ({fileCount}).txt" in os.listdir(openedFolder):
                raise FileExistsError
            else:
                open(f"{openedFolder}\\{fileName} ({fileCount}).txt", 'a').close()

        refresh()
    except Exception as e:
        if type(e) == FileExistsError:
            fileCount += 1
            newTXTFile()
        elif type(e) == PermissionError:
            showerror("Error!", "You don't have permission to create new text file in this directory!!!")


def show_properties():
    try:
        cur = fileList.selection()
        # col = '#1'

        # x, y, width, height = fileList.bbox(cur, col)
        # print(root.winfo_x()+fileList.winfo_x()+x, root.winfo_y()+fileList.winfo_y()+y)

        prop = Toplevel(root)
        prop.title(f"{fileList.item(cur)['values'][0]} Properties")
        # prop.geometry(f'350x480+{root.winfo_x()+fileList.winfo_x()+x}+{(root.winfo_y()+fileList.winfo_y()+y)+40}')
        prop.geometry(f"350x480+{x_root}+{y_root}")
        prop.resizable(1, 0)
        prop.focus_force()

        def on_return(event):
            widget = event.widget
            # print(os.path.join(openedFolder, fileList.item(self.iid)['values'][0]), os.path.join(openedFolder, self.get()))
            os.rename(os.path.join(openedFolder, fileList.item(cur)['values'][0]), os.path.join(openedFolder, widget.get()))
            # self.tv.item(self.iid, values=[self.get()])
            refresh()
            prop.destroy()

        ttk.Separator(prop, orient='horizontal').pack(fill='x')
        title = Entry(prop)
        title.pack(fill='x', pady=10)
        title.insert(END, f"{fileList.item(cur)['values'][0]}")
        title.bind('<Return>', on_return)

        ttk.Separator(prop, orient='horizontal').pack(fill='x')

        typeOF = Label(prop, text=f"Type:          {fileList.item(cur)['values'][2]}", anchor='w').pack(fill='x', pady=10)

        ttk.Separator(prop, orient='horizontal').pack(fill='x')

        fileSize = os.path.getsize(os.path.join(openedFolder, fileList.item(cur)['values'][0])) / 1024
        if fileSize > 1024:
            fileSize = f"{math.floor(fileSize / 1024)} MB"
        else:
            fileSize = f'{math.ceil(fileSize)} KB'

        location = Label(prop, text=f"Location:   {openedFolder}", anchor='w').pack(fill='x', pady=3)
        size = Label(prop, text=f"Size:            {fileSize}", anchor='w').pack(fill='x', pady=3)

        ttk.Separator(prop, orient='horizontal').pack(fill='x')

        created = Label(prop, text=f"Created:     {time.ctime(os.path.getctime(os.path.join(openedFolder, fileList.item(cur)['values'][0])))}", anchor='w').pack(fill='x', pady=3)
        modified = Label(prop, text=f"Modified:   {time.ctime(os.path.getmtime(os.path.join(openedFolder, fileList.item(cur)['values'][0])))}", anchor='w').pack(fill='x', pady=3)
        accessed = Label(prop, text=f"Accessed:   {time.ctime(os.path.getatime(os.path.join(openedFolder, fileList.item(cur)['values'][0])))}", anchor='w').pack(fill='x', pady=3)

        ttk.Separator(prop, orient='horizontal').pack(fill='x')

        prop.mainloop()
    except IndexError:
        prop.destroy()
        showerror("Error!", "You didn't selected any file or folder to show properties!!!")


class EntryPopUp(Entry):
    def __init__(self, parent, iid, text, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self['bd'] = 2
        self.iid = iid
        self.insert('end', text[0])
        self['exportselection'] = False
        self.focus_force()
        self.bind("<Return>", self.on_return)
        # self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda e: self.destroy())

    def on_return(self, event):
        # print(os.path.join(openedFolder, fileList.item(self.iid)['values'][0]), os.path.join(openedFolder, self.get()))
        os.rename(os.path.join(openedFolder, fileList.item(self.iid)['values'][0]), os.path.join(openedFolder, self.get()))
        # self.tv.item(self.iid, values=[self.get()])
        refresh()
        self.destroy()


def rename_from_menu():
    rowid = fileList.selection()
    column_id = "#1"

    x, y, width, height = fileList.bbox(rowid, column_id)

    text = fileList.item(rowid, 'values')
    entryPopUp = EntryPopUp(fileList, rowid, text)
    entryPopUp.place(x=0, y=y, width=width, height=height)


def newFolder(event=""):
    try:
        global folderCount
        if folderCount == 1:
            os.mkdir(f"{openedFolder}\\{folderName}")
        else:
            os.mkdir(f"{openedFolder}\\{folderName} ({folderCount})")

        refresh()
    except Exception as e:
        if type(e) == FileExistsError:
            folderCount += 1
            newFolder()
        elif type(e) == PermissionError:
            showerror("Error!", "You don't have permission to create new folder in this directory!!!")


def delete():
    cur = fileList.selection()
    ans = askyesno("Delete!", "Do you really want to delete?")
    if ans:
        try:
            if os.path.isfile(os.path.join(openedFolder, fileList.item(cur)['values'][0])):
                os.remove(os.path.join(openedFolder, fileList.item(cur)['values'][0]))
            elif os.path.isdir(os.path.join(openedFolder, fileList.item(cur)['values'][0])):
                shutil.rmtree(os.path.join(openedFolder, fileList.item(cur)['values'][0]))
            refresh()
        except TclError:
            showerror("Error!", "Select a file or folder to delete!!")
        except WindowsError:
            showerror("Error!", "You Can't delete this file!!")


def cut():
    cur = fileList.selection()
    try:
        global file, fileName, copy_or_cut
        copy_or_cut = "cut"
        file = os.path.join(openedFolder, fileList.item(cur)['values'][0])
        fileName = fileList.item(cur)['values'][0]
        # print(file)
        # print(fileName)
    except:
        showerror("Error!", "You need to select a file to cut!!")


def refresh(e=None):
    try:
        # fileInfo = []
        pathVar = lambda file_name: os.path.join(openedFolder, file_name)

        fileList.delete(*fileList.get_children())

        for fName in os.listdir(openedFolder):
            try:
                if os.path.isfile(pathVar(fName)):
                    fileList.insert('', END, values=[fName, time.ctime(os.path.getmtime(pathVar(fName))), f"{os.path.splitext(pathVar(fName))[1].split('.')[1].upper()} File", f"{math.ceil(os.path.getsize(pathVar(fName)) / 1024)} KB"])

                elif os.path.isdir(pathVar(fName)):
                    fileList.insert('', END, values=[fName, time.ctime(os.path.getmtime(pathVar(fName))), 'File Directory', ''])
            except IndexError:
                if os.path.isfile(pathVar(fName)):
                    if len(fName.split('.')) == 1:
                        fileList.insert('', END, values=[fName, time.ctime(os.path.getmtime(pathVar(fName))), f"File", f"{math.ceil(os.path.getsize(pathVar(fName)) / 1024)} KB"])
                    elif len(fName.split('.')) == 2:
                        fileList.insert('', END, values=[fName, time.ctime(os.path.getmtime(pathVar(fName))), f"{fName.split('.')[1].upper()} File", f"{math.ceil(os.path.getsize(pathVar(fName)) / 1024)} KB"])

                elif os.path.isdir(pathVar(fName)):
                    fileList.insert('', END, values=[fName, time.ctime(os.path.getmtime(pathVar(fName))), 'File Directory', ''])

        # fileList.delete(*fileList.get_children())

        # for i in fileInfo:
        #     fileList.insert('', END, values=i)

        global disks
        lengthDisk = len(disks)
        disks = [i for i in driveLetters if os.path.exists(i)]
        if len(disks) != lengthDisk:
            directories.delete(0, END)
            for i in disks:
                directories.insert(END, i)
    except WindowsError as e:
        showerror("Error!", e)
    except NameError:
        pass


def paste():
    try:
        global file, fileName
        if copy_or_cut == 'copy':
            if os.path.isdir(file):
                # It returns where the file paste
                shutil.copytree(file, os.path.join(openedFolder, fileName))
            elif os.path.isfile(file):
                shutil.copyfile(file, os.path.join(openedFolder, fileName))

        elif copy_or_cut == "cut":
            if os.path.isdir(file):
                # It returns where the file paste
                shutil.move(file, os.path.join(openedFolder, fileName))
                # shutil.rmtree(file)

            elif os.path.isfile(file):
                shutil.move(file, os.path.join(openedFolder, fileName))
                # os.remove(file)

            file = None
            fileName = None

        refresh()
    except NameError:
        showerror("Error!", "You didn't copy or cut any file!!")
    except FileExistsError:
        showerror("Error!", "File or Folder already exists!!")


def copy():
    cur = fileList.selection()
    try:
        global file, fileName, copy_or_cut
        copy_or_cut = "copy"
        file = os.path.join(openedFolder, fileList.item(cur)['values'][0])
        fileName = fileList.item(cur)['values'][0]
    except:
        showerror("Error!", "You need to select a file to copy!!")


def rightClicked(e):
    try:
        rowid = fileList.identify_row(e.y)
        fileList.selection_set(rowid)

        global x_root, y_root
        x_root = e.x_root
        y_root = e.y_root
        rightClickMenu.tk_popup(x=e.x_root, y=e.y_root)
    finally:
        rightClickMenu.grab_release()


def openD(e):
    cur = directories.curselection()
    global disk, openedFolder
    disk = directories.get(cur) + "\\"
    openedFolder = disk

    refresh()


def fileOpen(e=None):
    cur = fileList.selection()
    global openedFolder
    try:
        if e == "^":
            if len(openedFolder.split("\\")[:-1]) == 0:
                temp = [disk]
            else:
                temp = openedFolder.split("\\")[:-1]

            currentDir = ''
            for i in temp:
                currentDir += i + '\\'

            if currentDir[-1] == '\\' and currentDir != disk:
                openedFolder = currentDir[:-1]

            elif currentDir == disk:
                openedFolder = currentDir

        elif os.path.isdir(os.path.join(openedFolder, fileList.item(cur)['values'][0])):
            openedFolder = os.path.join(openedFolder, fileList.item(cur)['values'][0])

        elif os.path.isfile(os.path.join(openedFolder, fileList.item(cur)['values'][0])):
            os.startfile(os.path.join(openedFolder, fileList.item(cur)['values'][0]))

        refresh()

    except WindowsError:
        showerror("Error!", "This file can't be opened")
    except IndexError:
        pass
    except NameError:
        pass


folderCount = 1
folderName = "New Folder"
fileCount = 1
fileName = "New Text File"
driveLetters = [f'{i}:' for i in string.ascii_uppercase]
disks = [i for i in driveLetters if os.path.exists(i)]

root = Tk()
root.geometry("1350x600")
root.title("File Explorer Developed By Imran")

treeViewFrame = Frame(root)

scrollY = Scrollbar(treeViewFrame, orient='vertical')
scrollY.pack(fill='y', side='right')

upBtn = Button(treeViewFrame, text="^", bd=0, command=lambda: fileOpen('^'))
upBtn.pack(anchor='nw')

fileList = ttk.Treeview(treeViewFrame, yscrollcommand=scrollY.set, columns=["name", 'date modified', 'type', 'size'])

fileList.heading("name", text="Name")
fileList.heading("date modified", text="Date Modified")
fileList.heading("type", text="Type")
fileList.heading("size", text="Size")

fileList['show'] = 'headings'

fileList.column("name", width=200)
fileList.column("date modified", width=50)
fileList.column("type", width=20)
fileList.column("size", width=150)

fileList.bind("<Double-1>", fileOpen)
fileList.bind("<Return>", fileOpen)
fileList.bind("<ButtonRelease-3>", rightClicked)
# fileList.bind("<ButtonRelease-1>")
fileList.bind("<Control-Shift-N>", newFolder)
fileList.bind("<F5>", refresh)

fileList.pack(fill='both', expand=1, side=RIGHT)

scrollY.configure(command=fileList.yview)

directories = Listbox(root, font="{times new roman} 13", bd=5, relief="ridge")
directories.pack(fill="y", expand=0, side=LEFT)
for item in disks:
    directories.insert(END, item)
directories.bind("<ButtonRelease-1>", openD)

rightClickMenu = Menu(root, tearoff=0)
rightClickMenu.add_command(label="Open", command=fileOpen)
rightClickMenu.add_separator()
rightClickMenu.add_command(label="Refresh", command=refresh, accelerator='F5')
rightClickMenu.add_separator()
rightClickMenu.add_command(label="Copy", command=copy)
rightClickMenu.add_command(label="Cut", command=cut)
rightClickMenu.add_command(label="Paste", command=paste)
rightClickMenu.add_separator()
rightClickMenu.add_command(label="Rename", command=rename_from_menu)
rightClickMenu.add_command(label="Delete", command=delete)
rightClickMenu.add_separator()

newMenu = Menu(rightClickMenu, tearoff=0)
newMenu.add_command(label="Folder", accelerator="Ctrl+Shift+N", command=newFolder)
newMenu.add_command(label="Text Document", command=newTXTFile)

rightClickMenu.add_cascade(label="New", menu=newMenu)
rightClickMenu.add_command(label="Properties", command=show_properties)

treeViewFrame.pack(fill="both", expand=1, side=RIGHT)

root.mainloop()
