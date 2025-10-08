import tkinter as tk

def saludar():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    root.geometry("360x620")
    lbl.config(text=f"Hola Compa, {nombre} 👋")
    lblimg.pack()

root = tk.Tk()
root.title("Saludador de Compas")
root.geometry("360x220")

lbl = tk.Label(root, text="Eh compa, Escribe tu nombre y presiona el botón",
               foreground="blue", font="Helvetica", justify="center", background="light green")
lbl.pack(pady=10)

img = tk.PhotoImage(file="good-morning-images-good-morning-sunshine.gif")
lblimg = tk.Label(root, image=img)

entrada = tk.Entry(root)
entrada.pack(pady=5)

btn = tk.Button(root, text="Saludar", command=saludar)
btn.pack(pady=10)


root.mainloop()
