import end
import exe
import tkinter as tk
from tkinter import messagebox, Menu
import pandas as pd
import os

import normalize
import par
import glob

class UrlClassifierGUI:
    def __init__(self, master):
        pad = 3
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        self.master = master
        self.master.title("URL Classifier")
        self.master.configure(background='#F0F0F0')

        # create a menu
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        # create a "File" menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Clear History", command=self.clear_history)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # create a frame to hold the UI elements
        self.frame = tk.Frame(master, bg='#F0F0F0')
        self.frame.pack()

        self.url_label = tk.Label(self.frame, text="Enter a URL:", bg='#F0F0F0', fg='#333333',
                                  font=('Arial', 12, 'bold'))
        self.url_label.pack(pady=(20, 10))

        self.url_entry = tk.Entry(self.frame, width=40, font=('Arial', 12))
        self.url_entry.pack()

        self.classify_button = tk.Button(self.frame, text="Classify URL", command=self.classify_url, bg='#B7D1E2',
                                         activebackground='#8FC2E5', fg='#333333', activeforeground='#333333',
                                         font=('Arial', 12, 'bold'))
        self.classify_button.pack(pady=(10, 20))

        # create a table to display the classified URLs
        self.table_frame = tk.Frame(self.frame, bg='#F0F0F0')
        self.table_frame.pack()

        self.table_label = tk.Label(self.table_frame, text="History of Classified URLs", bg='#F0F0F0', fg='#333333',
                                    font=('Arial', 12, 'bold'))
        self.table_label.pack()

        self.table = tk.Label(self.table_frame, text="", bg='#F0F0F0', fg='#333333', font=('Arial', 10), justify='left')
        self.table.pack()

        self.clear_button = tk.Button(self.frame, text="Clear History", command=self.clear_history, bg='#B7D1E2',
                                      activebackground='#8FC2E5', fg='#333333', activeforeground='#333333',
                                      font=('Arial', 12, 'bold'))
        self.clear_button.pack(pady=(20, 0))


    def classify_url(self):
        url = self.url_entry.get()
        text = par.parse(url)
        text = normalize.normalize(text)
        category = exe.execute_model(text)

        # Save URL and category to CSV file
        df = pd.DataFrame({'URL': [url], 'Category': [category]})
        df.to_csv('classified_urls.csv', mode='a', header=not os.path.exists('classified_urls.csv'), index=False)

        self.url_entry.delete(0, tk.END)

        # Update the table with the classified URLs
        classified_urls = pd.read_csv('classified_urls.csv')
        self.table.configure(text=classified_urls.to_string(index=False))

        tk.messagebox.showinfo(title="Classification Result", message=f"The URL is classified as {category}.")

        # add buttons to open the classified URL or the URL's WHOIS information
        button_frame = tk.Frame(self.frame, bg=self.frame.cget('background'))
        button_frame.pack()


    def open_url(self, url):
        os.system(f'start {url}')

    def clear_history(self):
        try:
            os.remove('classified_urls.csv')
            self.table.configure(text="")
            tk.messagebox.showinfo(title="Clear History", message="The history of classified URLs has been cleared.")
        except OSError:
            tk.messagebox.showerror(title="Error", message="An error occurred while attempting to clear the history.")

if __name__ == '__main__':
    root = tk.Tk()
    app = UrlClassifierGUI(root)
    root.mainloop()
    # end.run()
