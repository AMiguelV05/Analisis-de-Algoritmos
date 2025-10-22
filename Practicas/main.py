import math
from random import randint
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showerror


def euclidiana(punto1, punto2):
    return math.sqrt((punto2[0]-punto1[0])**2+(punto2[1]-punto1[1])**2)


def visualizador():
    puntos = []
    ventana = tk.Tk()
    punto_x = tk.IntVar()
    punto_y = tk.IntVar()
    ventana.title("Distancias minimas")
    ventana.geometry('300x400')
    tk.Label(text="Ingresa el elemento X del punto: ").pack()
    tk.Entry(ventana, textvariable=punto_x).pack()
    tk.Label(text="Ingresa el elemento Y del punto: ").pack()
    tk.Entry(ventana, textvariable=punto_y).pack()

    def agregar_punto():
        if len(puntos)<5:
            x = punto_x.get()
            y = punto_y.get()
            puntos.append((x, y))
            messagebox.showinfo("Punto agregado", f"Se agregó el punto: ({x}, {y})")
        else:
            showerror("Error al añadir", "Solo se pueden agregar 5 puntos manuales")
            return
    def generar_aleatorios():
        for i in range(5):
            puntos.append((randint(0, 40), randint(0, 40)))
        messagebox.showinfo("Puntos Generados", "5 Puntos aleatorios generados con exito")

    def evaluar():
        if len(puntos) < 2:
            messagebox.showerror("Error", "Debes agregar al menos 2 puntos")
            return
        distancia_min = float("inf")
        par_cercano = None

        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                distancia = euclidiana(puntos[i], puntos[j])
                if distancia < distancia_min:
                    distancia_min = distancia
                    par_cercano = [puntos[i], puntos[j]]
        msg_final.config(text=f"Los pares más cercanos son: {par_cercano}\n"
                              f"con distancia minima de: {distancia_min:.3f}")

    tk.Button(ventana, text="Agregar", command=agregar_punto).pack(pady=10)
    tk.Button(ventana, text="Generar Aleatorios", command=generar_aleatorios).pack(pady=10)
    tk.Button(ventana, text="Ejecutar", command=evaluar).pack(pady=10)
    msg_final = tk.Label(ventana, text="")
    msg_final.pack(pady=10)

    ventana.mainloop()


if __name__ == '__main__':
    visualizador()