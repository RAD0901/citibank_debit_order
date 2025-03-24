from gui import GUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = GUI(master=root)
    app.run()  # Ensure this is app.run()

if __name__ == "__main__":
    main()