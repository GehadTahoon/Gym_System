from tkinter import *
from PIL import Image, ImageTk
import Trainers
import ExpiredTrainers
import Supplements

def display_home():
    home_root = Tk()
    home_root.title("Home")
    home_root.geometry("1000x700+245+50")
    home_root["bg"] = "white"
    home_root.resizable(FALSE, FALSE)
    Font = ("Calibri", "15", "bold")
    img = Image.open("images/dumbbell.png")
    ico = ImageTk.PhotoImage(img)
    home_root.iconphoto(False, ico)
    padd = 5

    def center():
        w = 1000
        h = 700
        screenwidth = home_root.winfo_screenwidth()
        screenheight = home_root.winfo_screenheight()
        x = int((screenwidth - w) / 2)
        y = int((screenheight - h) / 2)
        home_root.geometry(f"{w}x{h}+{x}+{y}")
    center()
    # got to trainees page
    def naviagteToTrainer():
        home_root.destroy()
        Trainer_page = Trainers.display_Trainer()
    #go to expiration page
    def navigateToExpired():
        home_root.destroy()
        Expired_Page = ExpiredTrainers.display_Expired()
    #go to supplements page
    def navigateToSupplements():
        home_root.destroy()
        Supplement_Page = Supplements.display_Supplements()


    #frame of image
    btnframe = Frame(home_root, height=700, width=600, bg=("#588157"))
    btnframe.grid(row=0, column=1)
    btnframe.grid_propagate(FALSE)
    #frame of buttons
    imgframe = Frame(home_root, height=700, width=400, bg=("white"))
    imgframe.grid(row=0, column=0)
    imgframe.grid_propagate(FALSE)

    #trainees button
    btn1 = Button(
        btnframe,
        text="Trainees",
        width=25,
        height=2,
        fg="white",
        background="#a3b18a",
        font=Font,
        padx=padd,
        pady=padd,
        relief="groove",
        command=naviagteToTrainer,
        cursor='hand2'
    )
    btn1.place(x=175, y=150)

    #Supplement button
    btn2 = Button(
        btnframe,
        text="Supplement",
        width=25,
        height=2,
        fg="white",
        background="#a3b18a",
        font=Font,
        padx=padd,
        pady=padd,
        relief="groove",
        command=navigateToSupplements,
        cursor='hand2'
    )
    btn2.place(x=175, y=300)
    #Expired button
    btn3 = Button(
        btnframe,
        text="Expired",
        width=25,
        height=2,
        fg="white",
        background="#a3b18a",
        font=Font,
        padx=padd,
        pady=padd,
        relief="groove",
        command=navigateToExpired,
        cursor='hand2'
    )
    btn3.place(x=175, y=450)

    #image 
    image = Image.open("images/undraw_Personal_trainer_re_cnua (1).png")
    image = image.resize((400, 400), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(image)
    imgframe.bg_photo = ImageTk.PhotoImage(image)
    imglbl = Label(imgframe, image=imgframe.bg_photo, background="white")
    imglbl.place(x=0, y=0, relwidth=1, relheight=1)

    home_root.mainloop()


# this block ensures that display_home() is only called when Home.py is run directly, and not when it's imported
if __name__ == "__main__":
    display_home()
