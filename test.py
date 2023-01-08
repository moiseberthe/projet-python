from tkinter import *

def search():
    query = search_entry.get()
    query = 0 if query == "" else int(query)
    liste.delete(0, END)
    if(query > 0):
        for i in range(query):
            liste.insert(i, f"Liste %d" % i)
    else:
        liste.insert(0, "Liste vide")
    liste.pack(padx=24, pady=24, fill=X)
bg="#ffffff"
font_f="Courrier"
window = Tk()
window.title("Moteur de recherche")
# window.geometry("1080x720")
window.geometry("720x480")
window.minsize(720, 500)
window.config(background=bg)

frame = Frame(window, bg=bg)

lb_welcome = Label(frame, text="Bienvenu dans l'application", font=(font_f, 40), bg=bg)
lb_welcome.pack(expand=YES)

search_entry = Entry(frame, textvariable="Rechercher", font=(font_f, 24), bg=bg)
search_entry.pack(pady=24)

search_btn = Button(frame, text="Rechercher", font=(font_f, 24), bg=bg, command=search)
search_btn.pack()

liste = Listbox(frame)
frame.pack(expand=YES)
window.mainloop()