import os
import subprocess
import sys

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

try:
    import customtkinter as ctk
except ImportError:
    install("customtkinter")
    import customtkinter as ctk

try:
    from pytube import YouTube
except ImportError:
    install("pytube")
    from pytube import YouTube

from tkinter import messagebox, filedialog

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "resource/config/config.txt"
ICON_PATH = "resource/ico.ico"

os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def save_path(path):
    with open(CONFIG_FILE, "w") as f:
        f.write(path)

def load_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("600x400")
        self.resizable(False, False)
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab1 = self.tabview.add("Download")
        self.tab2 = self.tabview.add("Set Path")
        self.tab3 = self.tabview.add("Exit")

        self.output_path = load_path()

        self.url_label = ctk.CTkLabel(self.tab1, text="Video URL:")
        self.url_label.pack(pady=10)
        self.url_entry = ctk.CTkEntry(self.tab1, width=400)
        self.url_entry.pack(pady=5)
        self.download_button = ctk.CTkButton(self.tab1, text="Download Video", command=self.download_video)
        self.download_button.pack(pady=20)

        self.path_label = ctk.CTkLabel(self.tab2, text="Current Path:")
        self.path_label.pack(pady=10)
        self.current_path = ctk.CTkLabel(self.tab2, text=self.output_path or "No path selected")
        self.current_path.pack(pady=5)
        self.browse_button = ctk.CTkButton(self.tab2, text="Choose Path", command=self.choose_path)
        self.browse_button.pack(pady=15)

        self.exit_label = ctk.CTkLabel(self.tab3, text="Click the button below to exit")
        self.exit_label.pack(pady=30)
        self.exit_button = ctk.CTkButton(self.tab3, text="Exit", command=self.quit)
        self.exit_button.pack(pady=10)

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.current_path.configure(text=path)
            save_path(path)
            messagebox.showinfo("Path Saved", f"Saved path: {path}")

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Enter a video URL.")
            return
        if not self.output_path:
            messagebox.showerror("Error", "Set the output path first.")
            return
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=self.output_path)
            messagebox.showinfo("Success", f"Video downloaded:\n{yt.title}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()
