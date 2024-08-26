import sqlite3
from Queries import update_sup
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter.ttk import Treeview
from tkinter import messagebox
import re
import Home
from PIL import Image, ImageTk


def display_Supplements():
    sups = tk.Tk() 
    sups.title("Supplements")
    img = Image.open("./images/vitamins.png")
    ico = ImageTk.PhotoImage(img)
    sups.iconphoto(False, ico)  # changing title icon
    sups.geometry("1000x700")
    sups.resizable(FALSE, FALSE)
    sups["bg"] = "#a3b18a"
    pad = 5
    def center():
        w = 1000
        h = 700
        screenwidth = sups.winfo_screenwidth()
        screenheight = sups.winfo_screenheight()
        x = int((screenwidth - w) / 2)
        y = int((screenheight - h) / 2)
        sups.geometry(f"{w}x{h}+{x}+{y}")

    center()
    #entries frame
    lbframe = Frame(sups, height=560, width=400, bg=("#588157"))
    lbframe.grid(row=0, column=0, padx=pad, pady=pad)
    lbframe.grid_propagate(FALSE)  # make frame size fixed
    # treeview frame 
    tvframe = Frame(sups, height=560, width=580, bg=("#dad7cd"))
    tvframe.grid(row=0, column=1, padx=pad, pady=pad)
    tvframe.grid_propagate(FALSE)
    #buttons frame
    btframe = Frame(sups, height=120, width=990, bg=("#344e41"))
    btframe.grid(row=1, column=0, columnspan=2, padx=pad, pady=pad)
    btframe.grid_propagate(FALSE)

    pd, wd, ft = 10, 5, 16
    # labels ##########
    #Supplements label
    lbl_1 = Label(
        lbframe,
        text="             Supplements ",
        font=("Bell MT", 20, "bold"),
        fg="white",
        bg="#588157",
        height=3,
    )
    lbl_1.grid(row=0, columnspan=2, padx=pd, pady=pd)
    #ID label
    sup_id_lb = Label(
        lbframe, text="ID", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    sup_id_lb.grid(row=1, column=0, padx=pd, pady=pd)
    #Name label
    sup_name_lb = Label(
        lbframe, text="Name", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    sup_name_lb.grid(row=2, column=0, padx=pd, pady=pd)
    #Company label
    sup_comp_lb = Label(
        lbframe, text="Company", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    sup_comp_lb.grid(row=3, column=0, padx=pd, pady=pd)
    #Quantity label
    sup_quantity_lb = Label(
        lbframe, text="Quantity", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    sup_quantity_lb.grid(row=4, column=0, padx=pd, pady=pd)
    #Price label
    sup_price_lb = Label(
        lbframe, text="Price", font=("Bell MT", ft, "bold"), fg="white", bg="#588157"
    )
    sup_price_lb.grid(row=5, column=0, padx=pd, pady=pd)
##################################
    # Entries
    #ID entry
    sup_id_ent = Entry(lbframe, width=30)
    sup_id_ent.grid(row=1, column=1, padx=pd, pady=pd)
    #Name entry
    sup_name_ent = Entry(lbframe, width=30)
    sup_name_ent.grid(row=2, column=1, padx=pd, pady=pd)
    #Company entry
    sup_comp_ent = Entry(lbframe, width=30)
    sup_comp_ent.grid(row=3, column=1, padx=pd, pady=pd)
    #Quantity entry
    sup_quantity_ent = Entry(lbframe, width=30)
    sup_quantity_ent.grid(row=4, column=1, padx=pd, pady=pd)
    #Price entry
    sup_price_ent = Entry(lbframe, width=30)
    sup_price_ent.grid(row=5, column=1, padx=pd, pady=pd)
###############################
    ###regx
    name_pattern = "^[A-Za-z\s]+$"
    company_pattern = "^[a-zA-Z0-9\s\-&.]+$"
    quantity_pattern = "^[1-9][0-9]*$"
    
    def is_valid_input(value, pattern):
        return bool(re.match(pattern, value))

    #################
    def clear_entries(frame):
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Entry, ttk.Entry)):
                widget.delete(0, tk.END)

    try:
        con = sqlite3.connect("test.db")
        cursor = con.cursor()
        cursor.execute("SELECT * from supplement")
        rows = cursor.fetchall()
    except:
        print("failed")

  
    columns = ["id", "name", "company", "quantity", "price"]
    tree = Treeview(
        tvframe, columns=columns, show="headings", selectmode="browse", height=24
    )
    tree.heading("id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("company", text="Company")
    tree.heading("quantity", text="Quantity")
    tree.heading("price", text="Price")
    for row in rows:
        tree.insert("", "end", values=row)
    tree.grid(row=1, column=0, columnspan=3, pady=(10, 0))
    tree.column("id", width=50, anchor="center")
    tree.column("name", anchor="center", width=200)
    tree.column("company", anchor="center", width=150)
    tree.column("quantity", anchor="center", width=90)
    tree.column("price", anchor="center", width=70)
    scr_bar = Scrollbar(tvframe, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scr_bar.set)
    scr_bar.grid(row=1, column=3, sticky="ns", pady=(10, 0))
    tree_style = Style()
    tree_style.configure(
        "Treeview", foreground="#000000", font=("tahoma", 10), background="#dad7cd"
    )
    tree_style.map(
        "Treeview",
        foreground=[("selected", "white")],
        background=[("selected", "#344e41")],
    )

    #Buttons' functions
    #back function
    def Back():
        sups.destroy()
        home_page = Home.display_home()

    #search function
    def search_btn():
        search = sent.get().lower()
        cursor.execute(
            "SELECT * from Supplement WHERE lower(Sup_Name) like ? ", [search + "%"]
        )
        searched_row = cursor.fetchall()
        for item in tree.get_children():
            tree.delete(item)
        for row in searched_row:
            tree.insert("", "end", values=row)
    #add function
    def ADD():
        try:
            assert sup_name_ent.get() != "", "Name is required"
            assert is_valid_input(
                sup_name_ent.get(), name_pattern
            ), "Name mustn't contain numbers"
            assert sup_comp_ent.get() != "", "Company Name is required"
            assert is_valid_input(
                sup_comp_ent.get(), company_pattern
            ), "Company mustn't contain numbers"

            assert sup_quantity_ent.get() != "", "Quantity is required"
            assert is_valid_input(
                sup_quantity_ent.get(), quantity_pattern
            ), "Quantity should contain only numbers"
            assert sup_price_ent.get() != "", "Price is required"
            assert is_valid_input(
                sup_price_ent.get(), quantity_pattern
            ), "Price should contain only numbers"
            cursor.execute(
                "insert into Supplement (Sup_Name,Sup_Company,Sup_Quantity,Sup_Price) VALUES(?,?,?,?)",
                [
                    sup_name_ent.get(),
                    sup_comp_ent.get(),
                    int(sup_quantity_ent.get()),
                    int(sup_price_ent.get()),
                ],
            )
            con.commit()
            update_tree_view()
            clear_entries(lbframe)

        except AssertionError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    #update treeview function
    def update_tree_view():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * from supplement ")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
    #buy function
    
    
    def buy():
        global selected_item_values
        if selected_item_values:
            selected_id = selected_item_values[0]
            selected_price = selected_item_values[4]
            quantity_buy = int(sup_quantity_ent.get())
            cursor.execute(
                "SELECT Sup_Quantity FROM Supplement WHERE Sup_id= ? ", (selected_id,)
            )

            current_quantity = cursor.fetchone()[0]
            if current_quantity == 0:
                messagebox.showinfo("out of stock", "this supplement out of stock ")
                return
            elif quantity_buy > current_quantity:
                messagebox.showinfo(
                    "stock error ", "the quantity exceeds available stock "
                )
                return
            elif sup_price_ent.get() != selected_price:
                messagebox.showinfo("invalid", "this price is invalid ")
                return
           

        cursor.execute(
            "UPDATE supplement SET Sup_Quantity=Sup_Quantity -? WHERE Sup_id=?",
            (quantity_buy, selected_id),
        )
        con.commit()
        update_tree_view()
        clear_entries(lbframe)
    #update function
    def update():
        selected_item_id = tree.focus()
        selected_item_values = tree.item(selected_item_id, "values")

        if not selected_item_id:
            messagebox.showerror("Error", "No item selected to update")
            return

        new_name = sup_name_ent.get()
        new_company = sup_comp_ent.get()
        new_quantity = int(sup_quantity_ent.get())
        new_price = int(sup_price_ent.get())

        if new_quantity < 0:
            messagebox.showerror("Error", "The quantity can't be below 0")
            return
        try:
            update_sup(
                new_name, new_company, new_quantity, new_price, selected_item_values[0]
            )
        except sqlite3.Error as e:
            print("Database error:", e)

        selected_item_values = tree.item(selected_item_id, "values")
        selected_item_values = (
            selected_item_values[0],
            new_name,
            new_company,
            new_quantity,
            new_price,
        )
        tree.item(selected_item_id, values=selected_item_values)
        clear_entries(lbframe)
    
    def on_row_selected(event):
        global selected_item_values
        tree = event.widget
        selected_item_id = tree.focus()
        if not selected_item_id:
            return
        selected_item_values = tree.item(selected_item_id, "values")
        # sup_quantity_ent.delete(0,'end')
        # sup_quantity_ent.insert(0, selected_item_values[0])

        # Retrieve the values of the selected row
        selected_item_values = tree.item(selected_item_id, "values")

        sup_id_ent.delete(0, "end")
        sup_id_ent.insert(0, selected_item_values[0])
        sup_name_ent.delete(0, "end")
        sup_name_ent.insert(0, selected_item_values[1])
        sup_comp_ent.delete(0, "end")
        sup_comp_ent.insert(0, selected_item_values[2])
        sup_price_ent.delete(0, "end")
        sup_price_ent.insert(0, selected_item_values[4])
        sup_quantity_ent.delete(0, "end")
        sup_quantity_ent.insert(0, selected_item_values[3])

    tree.bind("<<TreeviewSelect>>", on_row_selected)

    def buttons():
        icon_path = "images/return.png"
        icon = Image.open(icon_path)
        icon = icon.resize((50, 50), Image.LANCZOS)
        btframe.bg_photo = ImageTk.PhotoImage(icon)
        ret_Icon = Button(
            btframe,
            image=btframe.bg_photo,
            relief="flat",
            bg="#344e41",
            cursor="hand2",
            command=Back,
        )
        ret_Icon.place(x=850, y=35)

        btn_add = Button(
            btframe,
            text="ADD",
            anchor="center",
            width=10,
            font=("Calibri", 12, "bold"),
            bg="#a3b18a",
            fg="white",
            cursor="hand2",
            command=ADD,
        )
        btn_add.place(x=250, y=50)

        btn_buy = Button(
            btframe,
            text="BUY",
            anchor="center",
            width=10,
            font=("Calibri", 12, "bold"),
            bg="#a3b18a",
            fg="white",
            cursor="hand2",
            command=buy,
        )
        btn_buy.place(x=450, y=50)

        btn_update = Button(
            btframe,
            text="UPDATE",
            anchor="center",
            width=10,
            font=("Calibri", 12, "bold"),
            bg="#a3b18a",
            fg="white",
            cursor="hand2",
            command=update,
        )
        btn_update.place(x=650, y=50)

    # def search():
    # label
    slbl = Label(tvframe, text="Search", font=("Arial", 14, "bold"), bg=("#dad7cd"))
    slbl.grid(row=0, column=0, padx=1, pady=(10, 0))
    # entry
    sent = Entry(tvframe, width=35)
    sent.grid(row=0, column=1, padx=1, pady=(10, 0))
    # button
    sbtn = Button(
        tvframe,
        text="Enter",
        anchor="center",
        width=10,
        font=("Calibri", 12, "bold"),
        bg="#a3b18a",
        fg="white",
        cursor="hand2",
        command=search_btn,
    )
    sbtn.grid(row=0, column=2, padx=1, pady=(10, 0))
    """
    handle the closing database when closing the window 
    handle the problem (can't used with closed database ) 
    """
    sups.protocol("WM_DELETE_WINDOW", lambda: close_app(con))

    def close_app(con):
        con.close()
        sups.destroy()

    buttons()

    sups.mainloop()


if __name__ == "__main__":
    display_Supplements()
