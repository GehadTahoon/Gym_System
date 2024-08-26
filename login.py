from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import Home


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.iconphoto(True, self.get_icon())
        self.root.geometry(
            f"{self.get_width()}x{self.get_height()}+{self.get_x()}+{self.get_y()}"
        )
        self.root.configure(bg="#588157")
        self.root.title("Login")

        self.frame2 = Frame(
            self.root, width=self.get_width() // 2, height=self.get_height()
        )
        self.frame2.place(x=self.get_width() // 2, y=0)
        self.set_bg_label()

        self.create_widgets()

    def get_icon(self):
        img = Image.open("images/enter.png")
        return ImageTk.PhotoImage(img)

    def get_width(self):
        return 1240

    def get_height(self):
        return 800

    def get_x(self):
        return (self.root.winfo_screenwidth() - self.get_width()) // 2

    def get_y(self):
        return (self.root.winfo_screenheight() - self.get_height()) // 2

    def set_bg_label(self):
        bg_image_path = "./images/undraw_login_re_4vu2 (1).png"
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((self.get_width(), self.get_height()), Image.LANCZOS)

        self.frame2.bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = Label(self.frame2, image=self.frame2.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_widgets(self):
        lbl_font = ("Arial", 20)

        lbl = Label(
            self.root,
            text="Username",
            font=lbl_font,
            bg="#588157",
            fg="white",
            relief="flat",
        )
        lbl2 = Label(
            self.root,
            text="Password",
            font=lbl_font,
            bg="#588157",
            fg="white",
            relief="flat",
        )

        self.ent_user = Entry(self.root, width=18, font=("Arial", 16))
        self.ent_pass = Entry(self.root, width=18, font=("Arial", 16), show="*")

        but = Button(
            self.root,
            text="Login",
            bg="#a3b18a",
            fg="white",
            font=("Bell MT", 16, "bold"),
            width=28,
            command=self.check_user,
        )

        lbl.place(x=100, y=290)
        lbl2.place(x=100, y=370)
        self.ent_user.place(x=260, y=300)
        self.ent_pass.place(x=260, y=375)
        but.place(x=120, y=480)

    def check_user(self):
        valid_username = "admin"
        valid_password = "1"
        username = self.ent_user.get()
        password = self.ent_pass.get()

        if username == valid_username and password == valid_password:
            self.root.destroy()
            home_page = (
                Home.display_home()
            )  # Create an instance of HomePage from the Home module

        elif not username or not password:
            messagebox.showerror("Error", "All fields are mandatory")

        else:
            messagebox.showerror("Error", "Invalid username or password")


if __name__ == "__main__":
    root = Tk()
    login_page = LoginPage(root)
    root.mainloop()
