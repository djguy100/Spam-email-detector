import tkinter as tk
from Scripts.model import Model


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path from the relative path of the file
    :param relative_path: The relative path of the file
    :return: Absolute path of the file
    """
    import sys
    import os

    try:
        base_path: str = sys._MEIPASS

    except AttributeError:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)


class SpamEmailDetector:
    """
    This is the main class for the app
    """
    def __init__(self) -> None:
        """
        Here we create the basic UI for the app and load the model
        """
        self.window: tk.Tk = tk.Tk()
        self.window.title("Spam Email Detector")
        self.window.resizable(width=False, height=False)
        self.window.iconphoto(True, tk.PhotoImage(file=resource_path("Assets/icon.png")))

        self.model: Model = Model.load()
        self.instructions()

    def instructions(self) -> None:
        """
        Here we display the instructions & details of the app
        :return: This doesn't return anything
        """
        toplevel: tk.Toplevel = tk.Toplevel(self.window)
        toplevel.title("Instructions & Details")
        toplevel.resizable(False, False)

        frame: tk.Frame = tk.Frame(toplevel)
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Welcome to Spam Email Detector!", font=("Arial", 35, "bold")).grid(row=0, column=0)
        tk.Label(frame, text="This app is there to tell you\n"
                                "if your mails are a spam or not.", font=("Arial", 20)).grid(row=1, column=0)
        tk.Label(frame, text="Note: The longer your text the better the results!", font=("Arial", 20, "bold")).grid(row=2, column=0, pady=10)
        tk.Label(frame, text="To use this app, all you have to do is enter your text\n"
                             "and press evaluate. That's how simple it is!", font=("Arial", 20)).grid(row=3, column=0)

    def run(self) -> None:
        """
        This is the main function for the app
        :return: This doesn't return anything
        """
        tk.Label(self.window, text="Spam email detector", font=("Arial", 35, "bold")).pack(padx=10)
        tk.Label(self.window, text="Enter your text here:", font=("Arial", 20, )).pack(pady=10)

        e_text: tk.Text = tk.Text(self.window, height=20, width=48, bg="#333333")
        e_text.pack()

        def result() -> None:
            from tkinter import messagebox as mbox

            text: str = e_text.get("1.0", tk.END)
            spam: str = self.model.evaluate(text)

            mbox.showinfo(title="Email evaluation", message=spam)

        frame: tk.Frame = tk.Frame(self.window)
        frame.pack(pady=10)

        evaluate: tk.Button = tk.Button(frame, text="evaluate", command=result)
        evaluate.grid(row=0, column=0)

        info: tk.Button = tk.Button(frame, text="info", command=self.instructions)
        info.grid(row=0, column=1)

        self.window.mainloop()


def main() -> None:
    """
    Here we run the app
    :return: This doesn't return anything
    """
    sed: SpamEmailDetector = SpamEmailDetector()
    sed.run()


if __name__ == "__main__":
    main()