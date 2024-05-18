import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter.ttk import Treeview, Combobox
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import sqlite3
from PIL import Image, ImageTk
from Queries import addTrainer, updateTrainer, deleteTrainer, search_Trainer
import re
import Home


###regx
name_pattern = "^[A-Za-z\s]+$"
age_pattern = "^(1[8-9]|[2-9][0-9])$" 
phone_pattern = "^01[0|1|2|5]\d{8}$"
subscription_pattern = "300"


def is_valid_input(value, pattern):
    return bool(re.match(pattern, value))

def month_difference(date1, date2):
    return (date1.year - date2.year) * 12 + date1.month - date2.month


# Connect to the database
con = sqlite3.connect("test.db")
cursor = con.cursor()
cursor.execute("SELECT * from trainer")
rows = cursor.fetchall()
con.close()

# Create the main window


def display_Trainer():
    root = tk.Tk()
    img = Image.open("./images/workout.png")

    ico = ImageTk.PhotoImage(img)
    root.iconphoto(False, ico)

    def Back():
        root.destroy()
        home_page = Home.display_home()

    def center():
        w = 1000
        h = 800
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        x = int((screenwidth - w) / 2)
        y = int((screenheight - h) / 2)
        root.geometry(f"{w}x{h}+{x}+{y}")

    root.title("Trainee")

    # root.geometry("1400x1000")

    center()
    icon_path = "./images/return.png"
    icon = Image.open(icon_path)
    icon = icon.resize((50, 50), Image.LANCZOS)
    root["bg"] = "#a3b18a"
    frame = Frame(
        root, height=600, width=1000, bg="#dad7cd"
    )  # Adjust height and width as needed
    frame2 = Frame(root, height=350, width=490, bg="#588157")
    frame3 = Frame(root, height=350, width=490, bg="#344e41")
    frame3.grid(row=0, column=1, padx=3, pady=5)
    frame2.grid(row=0, column=0, padx=3, pady=5)
    frame3.bg_photo = ImageTk.PhotoImage(icon)

    frame3.grid_propagate(False)
    frame2.grid_propagate(False)
    frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    # frame.grid_propagate(False)

    def populate_treeview_forSearch(phoneNum):
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data from database
        con = sqlite3.connect("test.db")
        cursor = con.cursor()
        cursor.execute(
            "SELECT * from trainer WHERE Trainer_phone like ?", [int(phoneNum)]
        )
        rows = cursor.fetchall()
        con.close()

        # Populate the treeview
        for row in rows:
            tree.insert("", "end", values=row)

    def populate_treeview():
        # Clear existing records
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data from database
        con = sqlite3.connect("test.db")
        cursor = con.cursor()
        cursor.execute("SELECT * from trainer")
        rows = cursor.fetchall()
        con.close()

        # Populate the treeview
        for row in rows:
            tree.insert("", "end", values=row)

    # Treeview setup
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
        height=16,
    )

    # Add column headings
    tree.heading("Trainer_Id", text="Trainer_Id")
    tree.heading("Trainer_Name", text="Trainer_Name")
    tree.heading("Trainer_Phone", text="Trainer_Phone")
    tree.heading("Trainer_Age", text="Trainer_Age")
    tree.heading("Trainer_Coach", text="Trainer_Coach")
    tree.heading("Trainer_StartDate", text="Trainer_StartDate")
    tree.heading("Trainer_EndDate", text="Trainer_EndDate")
    tree.heading("Trainer_subscription", text="Trainer_subscription")

    # Insert data into the treeview
    for row in rows:
        tree.insert("", "end", values=row)

        ############################

    def on_row_selected(event):
        # Get the Treeview widget from the event
        tree = event.widget

        # Get the ID of the selected row
        selected_item_id = tree.focus()
        if not selected_item_id:
            return
        # Retrieve the values of the selected row
        selected_item_values = tree.item(selected_item_id, "values")
        entry_Id.delete(0, "end")
        entry_Id.insert(0, selected_item_values[0])
        entry_name.delete(0, "end")
        entry_name.insert(0, selected_item_values[1])
        entry_Age.delete(0, "end")
        entry_Age.insert(0, selected_item_values[3])
        entry_phone.delete(0, "end")
        entry_phone.insert(0, "0" + selected_item_values[2])
        combo_coach.delete(0, "end")
        coaches_var.set(selected_item_values[4])
        entry_start_date.delete(0, "end")
        entry_start_date.insert(0, selected_item_values[5])
        entry_end_date.delete(0, "end")
        entry_end_date.insert(0, selected_item_values[6])
        entry_subscription.delete(0, "end")
        entry_subscription.insert(0, selected_item_values[7])

    tree.bind("<<TreeviewSelect>>", on_row_selected)

    # Populate Treeview
    populate_treeview()
    #####################################

    # Pack the treeview
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
    hsb = Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.grid(row=0, column=1, sticky="ns")
    tree.grid(row=0, column=0, sticky="nsew")

    tree_style = Style()
    tree_style.configure(
        "Treeview", foreground="#000000", font=("tahoma", 10), background="#dad7cd"
    )
    tree_style.map(
        "Treeview",
        foreground=[("selected", "white")],
        background=[("selected", "#344e41")],
    )

    ###

    frame.place(anchor="center", relx=0.5, rely=0.70)
    #############setup Coaches
    coaches = ["Mohamed salah", "Big ramy", "Hesham magroushy", "mahmoud Eldora"]
    coaches_var = StringVar()
    coaches_var.set(coaches[0])

    ################################

    def coachesName():
        return coaches_var.get()

    def checkMonth():
        start_date = entry_start_date.get_date()
        end_date = entry_end_date.get_date()

        difference = month_difference(end_date, start_date)
        if difference <= 0:
            return 0
        return difference * 300

    def handleAdd():
        try:
            assert entry_name.get() != "", "Name is required"
            assert is_valid_input(
                entry_name.get(), name_pattern
            ), "Name mustn't contain numbers"
            assert entry_Age.get() != "", "Age is required"

            assert is_valid_input(
                entry_Age.get(), age_pattern
            ), "age must be between 18 to 99"
            assert entry_phone.get() != "", "Phone is required"
            assert is_valid_input(
                entry_phone.get(), phone_pattern
            ), "phone number is not valid"
            assert checkMonth(), "Date is invalid"
            assert entry_subscription.get() != "", "Subscription is required"
            assert is_valid_input(
                entry_subscription.get(), subscription_pattern
            ), "Subscription is invalid"
            addTrainer(
                entry_name.get(),
                int(entry_phone.get()),
                int(entry_Age.get()),
                coachesName(),
                str(entry_start_date.get_date()),
                str(entry_end_date.get_date()),
                int(checkMonth()),
            )
            # Update the treeview after adding
            populate_treeview()
            clear_entries(frame2)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid input. Please ensure that phone, age, and subscription are numbers.",
            )

        except AssertionError as e:
            # You can show a generic error message or be more specific based on the type of exception
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handleUpdate():
        try:
            assert checkMonth(), "Date is invalid"
            assert entry_name.get() != "", "Name is required"
            assert is_valid_input(
                entry_name.get(), name_pattern
            ), "Name mustn't contain numbers"
            assert entry_Age.get() != "", "Age is required"
            assert is_valid_input(
                entry_Age.get(), age_pattern
            ), "Age must be between 18 to 99"
            assert entry_phone.get() != "", "Phone is required"
            assert is_valid_input(
                entry_phone.get(), phone_pattern
            ), "Phone number is not valid"
            assert entry_subscription.get() != "", "Subscription is required"
            assert is_valid_input(
                entry_subscription.get(), subscription_pattern
            ), "Subscription is invalid"

            updateTrainer(
                entry_name.get(),
                int(entry_phone.get()),
                int(entry_Age.get()),
                coachesName(),
                str(entry_start_date.get_date()),
                str(entry_end_date.get_date()),
                int(entry_subscription.get()),
                int(entry_Id.get()),
            )
            populate_treeview()
            clear_entries(frame2)
        except AssertionError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handleDelete():
        try:
            deleteTrainer(int(entry_Id.get()))
            populate_treeview()
            clear_entries(frame2)
        except ValueError as e:
            messagebox.showerror(
                "Error", f"An error occurred: Please select a row to delete"
            )

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

    ##################
    padx = 10
    pady = 5
    ft = 16
    label_Name = Label(
        frame2, text="Name", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    label_Age = Label(
        frame2, text="Age", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    label_phone = Label(
        frame2, text="Phone", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    label_coach = Label(
        frame2, text="Coach", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    label_start_date = Label(
        frame2,
        text="Start Date",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#588157",
    )
    label_end_date = Label(
        frame2, text="End Date", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    label_subscription = Label(
        frame2,
        text="Subscription",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#588157",
    )

    #####buttons
    add_btn = Button(
        frame3,
        text="Add",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#a3b18a",
        width=36,
        command=handleAdd,
        cursor='hand2'
    )
    update_btn = Button(
        frame3,
        text="Update",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#a3b18a",
        width=36,
        command=handleUpdate,
        cursor='hand2'
    )
    delete_btn = Button(
        frame3,
        text="Delete",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#a3b18a",
        width=36,
        command=handleDelete,
        cursor='hand2'
    )
    search_btn = Button(
        frame3,
        text="Search",
        font=("Bell MT", ft, "bold"),
        fg="white",
        bg="#a3b18a",
        width=10,
        command=handleSearch,
        cursor='hand2'
    )
    entry_start_date = DateEntry(frame2, width=25, state="readonly")
    entry_end_date = DateEntry(frame2, width=25, state="readonly")
    entry_subscription = Entry(frame2, width=28)

    ret_Icon = Button(
        frame3, image=frame3.bg_photo, relief="flat", bg="#344e41", command=Back,cursor='hand2'
    )
    #################################3
    entry_Id = Entry(frame2, width=28)
    sent = Entry(
        frame3,
        width=22,
        font=("Bell MT", ft, "bold"),
    )
    entry_name = Entry(frame2, width=28)
    entry_Age = Entry(frame2, width=28)
    entry_phone = Entry(frame2, width=28)
    combo_coach = tk.ttk.Combobox(
        frame2, values=coaches, state="readonly", textvariable=coaches_var, width=25
    )

    combo_coach.bind("<<ComboboxSelected>>", lambda event=None: coachesName())

    #######################################
    def clear_entries(frame):
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Entry, ttk.Entry)):
                widget.delete(0, tk.END)

    ########################################
    label_Name.grid(row=0, column=0, pady=(pady + 25, pady))
    entry_name.grid(row=0, column=1, padx=padx, pady=(pady + 25, pady))
    label_Age.grid(row=1, column=0, padx=padx,pady=pady)
    entry_Age.grid(row=1, column=1, padx=padx, pady=pady)
    label_phone.grid(row=2, column=0, padx=padx,pady=pady)
    entry_phone.grid(row=2, column=1, padx=padx, pady=pady)
    label_coach.grid(row=3, column=0, padx=padx)
    combo_coach.grid(row=3, column=1, padx=padx, pady=pady)
    label_start_date.grid(row=4, column=0, padx=padx, pady=pady)
    entry_start_date.grid(row=4, column=1, padx=padx, pady=pady)
    label_end_date.grid(row=5, column=0, padx=padx, pady=pady)
    entry_end_date.grid(row=5, column=1, padx=padx, pady=pady)
    label_subscription.grid(row=6, column=0, padx=padx, pady=pady)
    entry_subscription.grid(row=6, column=1, padx=padx, pady=pady)
    add_btn.grid(row=1, padx=padx, pady=pady, columnspan=3)
    update_btn.grid(row=2, padx=padx, pady=pady, columnspan=3)
    delete_btn.grid(row=3, padx=padx, pady=pady, columnspan=3)
    ret_Icon.grid(row=4, columnspan=3)
    search_btn.grid(row=6, column=1, pady=pady)
    sent.grid(row=6, pady=pady + 20)

    ##############################

    ##############################

    root.mainloop()

if __name__ == "__main__":
    display_Trainer()
