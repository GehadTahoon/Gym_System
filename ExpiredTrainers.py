import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter.ttk import Treeview, Combobox
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import sqlite3
from PIL import Image, ImageTk
from datetime import date
import re
from Queries import search_Trainer
import Home


def display_Expired():
    root = Tk()
    root.title("Expired subscriptions") #root title
    
    root["bg"] = "#a3b18a" 
    img = Image.open("./images/calendar.png") 
    ico = ImageTk.PhotoImage(img)
    root.iconphoto(False, ico) #root icon
    def center():#center function
        w = 1000
        h = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        x = int((screenwidth - w) / 2)
        y = int((screenheight - h) / 2)
        root.geometry(f"{w}x{h}+{x}+{y}")  
    center()#calling function
    
    #frame 
    frame = Frame(root, height=600, width=1000, bg="#dad7cd")
    frame.grid(row=0, column=0)
    frame.grid_propagate(False)

   
    #handling user inputs !!!
    phone_pattern = "^01[0|1|2|5]\d{8}$"

    def is_valid_input(value, pattern):
        return bool(re.match(pattern, value))
    
    def handleSearch():
        try:
            assert sent.get() != "", "Please enter a phone number to search"
            assert is_valid_input(
                sent.get(), phone_pattern
            ), "Phone number is not valid"
            search_Trainer(int(sent.get()))
            populate_treeview_forSearch(int(sent.get()))
        except AssertionError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    today = date.today()

    ##back button
    #button function
    def Back():
        root.destroy()
        home_page = Home.display_home()
    #button icon
    icon_path = "images/return.png"
    icon = Image.open(icon_path)
    icon = icon.resize((50, 50), Image.LANCZOS)
    frame.bg_photo = ImageTk.PhotoImage(icon)
    ret_Icon = Button(
        frame,
        image=frame.bg_photo,
        relief="flat",
        bg="#dad7cd",
        cursor="hand2",
        command=Back,
    )
    ret_Icon.grid(row=0, columnspan=3, pady=10)
    
    
    ##search entry
    sent = Entry(
        frame,
        width=22,
        font=("Bell MT", 16, "bold"),
    )
    sent.grid(row=1, column=0, pady=10)

    ##search button
    search_btn = Button(
        frame,
        text="Search",
        font=("Bell MT", 16, "bold"),
        fg="white",
        bg="#a3b18a",
        width=10,
        cursor="hand2",
        command=handleSearch,
    )
    search_btn.grid(row=2, column=0, pady=5)

    ##Treeview

    def populate_treeview_forSearch(phoneNum):
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data from database
        con = sqlite3.connect("test.db")
        cursor = con.cursor()
        cursor.execute(
            "SELECT * from trainer WHERE Trainer_phone like ? and Trainer_EndDate < DATE('now') ",
            [int(phoneNum)],
        )
        rows = cursor.fetchall()
        con.close()

        # Populate the treeview
        for row in rows:
            tree.insert("", "end", values=row)

    
    # print(today)
    #connection
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    cursor.execute("SELECT * from trainer where Trainer_EndDate < DATE('now')")
    rows = cursor.fetchall()
    con.close()

    ## treeview ######
    tree = Treeview(
        frame,
        columns=(
            "Trainer_Id",
            "Trainer_Name",
            "Trainer_Phone",
            "Trainer_Age",
            "Trainer_Coach",
            "Trainer_StartDate",
            "Trainer_EndDate",
            "Trainer_subscription",
        ),
        show="headings",
        selectmode="browse",
        height=18,
    )

    tree.heading("Trainer_Id", text="Trainer_Id")
    tree.heading("Trainer_Name", text="Trainer_Name")
    tree.heading("Trainer_Phone", text="Trainer_Phone")
    tree.heading("Trainer_Age", text="Trainer_Age")
    tree.heading("Trainer_Coach", text="Trainer_Coach")
    tree.heading("Trainer_StartDate", text="Trainer_StartDate")
    tree.heading("Trainer_EndDate", text="Trainer_EndDate")
    tree.heading("Trainer_subscription", text="Trainer_subscription")

    tree.grid(pady=20)
    tree.column("Trainer_Id", anchor="center", width=70)
    tree.column("Trainer_Name", anchor="center", width=150)
    tree.column("Trainer_Phone", anchor="center", width=100)
    tree.column("Trainer_Age", anchor="center", width=70)
    tree.column("Trainer_Coach", anchor="center", width=150)
    tree.column("Trainer_StartDate", anchor="center", width=150)
    tree.column("Trainer_EndDate", anchor="center", width=150)
    tree.column("Trainer_subscription", anchor="center", width=133)
    vsb = Scrollbar(frame, orient="vertical", command=tree.yview)

    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=3, column=1, sticky="ns")
    tree.place(anchor="center", relx=0.5, rely=0.5)
    tree.grid(row=3, column=0, sticky="nsew")
    ##########################################

    #############################
    for row in rows:
        tree.insert("", "end", values=row)

    #########################################

    tree_style = Style()
    tree_style.configure(
        "Treeview", foreground="#000000", font=("tahoma", 10), background="#dad7cd"
    )
    tree_style.map(
        "Treeview",
        foreground=[("selected", "white")],
        background=[("selected", "#344e41")],
    )
    ############################################
    root.mainloop()

if __name__ == "__main__":
    display_Expired()
