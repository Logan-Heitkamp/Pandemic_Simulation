import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Tabbed Interface Example")
root.geometry("400x500")

# Create a Notebook widget (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

# Add frames to the notebook as tabs
notebook.add(tab1, text="   Simulation Settings   ")
notebook.add(tab2, text="    Developer Options    ")
notebook.add(tab3, text="        Extra Tab        ")

# Populate the tabs with content
label1 = tk.Label(tab1, text="This is the content of Tab 1", background='black', foreground='white')
label1.pack(padx=20, pady=20)

btn1 = tk.Button(tab1, text='Button one')
btn1.pack(padx=20, pady=20)

label2 = tk.Label(tab2, text="This is the content of Tab 2")
label2.pack(padx=20, pady=20)

label3 = tk.Label(tab3, text="This is the content of Tab 3")
label3.pack(padx=20, pady=20)


# text input testing
def text_print():
    txt = input_txt.get(1.0, 'end-1c')
    print(txt)


input_txt = tk.Text(tab1, height=5, width=30)
input_txt.pack()

btn = tk.Button(tab1, text='show result', command=text_print)
btn.pack()

# Run the application
root.mainloop()
