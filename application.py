import logging
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage
import cv2
from backend.Training import recognizer
from backend.creatingDataset import start_capture
from backend.FaceRecognition import face_recognizer
from backend.generate_database import mask_generators

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("application.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

names = set()


class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Initializing Main UI")

        global names
        try:
            with open("nameslist.txt", "r") as f:
                x = f.read()
                z = x.rstrip().split(" ")
                for i in z:
                    names.add(i)
        except FileNotFoundError:
            logger.warning(
                "nameslist.txt not found. Starting with an empty set of names."
            )
        except Exception as e:
            logger.error(f"Unexpected error while reading nameslist.txt: {e}")

        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.title(" Employee Management System - Stevens")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        logger.info(f"Switching to frame: {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            try:
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                logger.info("Saved names to nameslist.txt")
            except Exception as e:
                logger.error(f"Error while saving names to nameslist.txt: {e}")
            finally:
                self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        try:
            render = PhotoImage(file="static/imgs/applogor.png")
        except Exception as e:
            logger.error(f"Error loading applogor.png: {e}")
            render = None

        if render:
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")

        label = tk.Label(
            self,
            text="        Welcome to Stevens        ",
            font=self.controller.title_font,
            fg="#263942",
        )
        label.grid(row=0, sticky="ew")

        button1 = tk.Button(
            self,
            text="   Register a User  ",
            fg="#263942",
            bg="#ffffff",
            command=lambda: self.controller.show_frame("PageOne"),
        )
        button2 = tk.Button(
            self,
            text="   Click here to TRY!  ",
            fg="#263942",
            bg="#ffffff",
            command=lambda: self.controller.show_frame("PageTwo"),
        )
        button3 = tk.Button(
            self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing
        )
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            try:
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                logger.info("Saved names to nameslist.txt on closing StartPage.")
            except Exception as e:
                logger.error(f"Error while saving names to nameslist.txt: {e}")
            finally:
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure the grid of the frame to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create a container frame for the content
        content_frame = tk.Frame(self)
        content_frame.grid(row=1, column=1)

        tk.Label(
            content_frame, text="Enter the name", fg="#263942", font="Helvetica 12 bold"
        ).grid(row=0, column=0, pady=10, padx=5)

        self.user_name = tk.Entry(
            content_frame, borderwidth=3, bg="lightgrey", font="Helvetica 11"
        )
        self.user_name.grid(row=0, column=1, pady=10, padx=10)

        self.buttoncanc = tk.Button(
            content_frame,
            text="Cancel",
            bg="#ffffff",
            fg="#263942",
            command=lambda: controller.show_frame("StartPage"),
        )
        self.buttonext = tk.Button(
            content_frame,
            text="Next",
            fg="#263942",
            bg="#263942",
            command=self.start_training,
        )
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)

    def start_training(self):
        global names
        name = self.user_name.get().strip()

        if name.lower() == "none":
            messagebox.showerror("Error", "Name cannot be 'None'")
            logger.warning("Attempted to register user with name 'None'")
            return
        elif name in names:
            messagebox.showerror("Error", "User already exists!")
            logger.warning(f"Attempted to register an existing user: {name}")
            return
        elif len(name) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            logger.warning("Attempted to register user with empty name")
            return

        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        logger.info(f"User registered successfully: {name}")
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Select user", fg="#263942", font="Helvetica 12 bold").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.buttoncanc = tk.Button(
            self,
            text="Cancel",
            command=lambda: controller.show_frame("StartPage"),
            bg="#ffffff",
            fg="#263942",
        )
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(
            self, text="Next", command=self.nextfoo, fg="#263942", bg="#263942"
        )
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if not self.menuvar.get():
            messagebox.showerror("ERROR", "Please select a user")
            logger.warning("No user selected in PageTwo")
            return
        self.controller.active_name = self.menuvar.get()
        logger.info(f"User selected: {self.controller.active_name}")
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set("")
        self.dropdown["menu"].delete(0, "end")
        for name in names:
            self.dropdown["menu"].add_command(
                label=name, command=tk._setit(self.menuvar, name)
            )
        logger.info("User dropdown menu refreshed in PageTwo")


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure the grid of the frame to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create a container frame for the content
        content_frame = tk.Frame(self)
        content_frame.grid(row=1, column=1)

        # Add widgets to the content frame
        self.numimglabel = tk.Label(
            content_frame,
            text="Number of images captured = 0",
            font="Helvetica 12 bold",
            fg="#263942",
        )
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        self.capturebutton = tk.Button(
            content_frame,
            text="Capture Data Set",
            fg="#263942",
            bg="#263942",
            command=self.capimg,
        )
        self.trainbutton = tk.Button(
            content_frame,
            text="Train The Model",
            fg="#263942",
            bg="#263942",
            command=self.trainmodel,
        )
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        logger.info(f"Starting data capture for user: {self.controller.active_name}")
        try:
            messagebox.showinfo("INSTRUCTIONS", "We will Capture 100 pic of your Face.")
            x = start_capture(self.controller.active_name)
            mask_generators()
            self.numimglabel.config(text=f"Number of images captured = 100")
            logger.info(f"Captured 100 images for user: {self.controller.active_name}")
        except Exception as e:
            logger.error(f"Error during image capture: {e}")
            messagebox.showerror("ERROR", f"Error during image capture: {e}")

    def trainmodel(self):
        logger.info("Starting model training")
        try:
            recognizer()
            messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
            logger.info("Model training completed successfully")
            self.controller.show_frame("PageFour")
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            messagebox.showerror("ERROR", f"Error during model training: {e}")


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure the grid of the frame to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create a container frame for the content
        content_frame = tk.Frame(self)
        content_frame.grid(row=1, column=1)

        # Add widgets to the content frame
        label = tk.Label(
            content_frame, text="Face Recognition", font="Helvetica 16 bold"
        )
        label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        button1 = tk.Button(
            content_frame,
            text="Face Recognition",
            command=self.openwebcam,
            fg="#263942",
            bg="#263942",
        )
        button4 = tk.Button(
            content_frame,
            text="Go to Home Page",
            command=lambda: self.controller.show_frame("StartPage"),
            bg="#ffffff",
            fg="#263942",
        )
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        logger.info(
            f"Starting face recognition for user: {self.controller.active_name}"
        )
        try:
            cap = cv2.VideoCapture(0)  # Use laptop camera
            if not cap.isOpened():
                raise Exception("Could not open webcam.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Failed to capture frame from webcam.")

                cv2.imshow("Face Recognition", frame)

                # Break loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()
            self.face_recognizer()
            logger.info("Face recognition completed successfully")
        except Exception as e:
            logger.error(f"Error during face recognition: {e}")
            messagebox.showerror("ERROR", f"Error during face recognition: {e}")
        finally:
            if "cap" in locals() and cap.isOpened():
                cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        app = MainUI()
        app.iconphoto(False, tk.PhotoImage(file="static/imgs/applogor.png"))
        app.mainloop()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
