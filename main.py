# main.py
import tkinter as tk
from gui.app import FrescoClusterApp

def main():
    root = tk.Tk()
    app = FrescoClusterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
