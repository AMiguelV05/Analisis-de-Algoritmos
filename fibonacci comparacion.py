import tkinter as tk
from tkinter import messagebox
from time import perf_counter
import tracemalloc
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fibonacci(n) -> int:
    if n<=1:
        return n

    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_dinamico(n, dicc: dict) -> int:
    if n <= 1:
        return n
    if n not in dicc:
        dicc[n] = (fibonacci_dinamico(n-1, dicc) + fibonacci_dinamico(n-2, dicc))
    return dicc[n]

def graficar():
    try:
        n = int(entry.get())
        if n<1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Número no valido")
        return

    xs = list(range(1,n+1))
    tiempo_recursivo = []
    tiempo_dinamico = []
    memoria_recursiva = []
    memoria_dinamico = []

    for valor in xs:
        # fibonaccia normal
        tracemalloc.start()

        inicio = perf_counter()
        fibonacci(valor)
        final = perf_counter()

        actual, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tiempo_recursivo.append(final - inicio)
        memoria_recursiva.append(peak)

        # fibonacci con prog. dinamica
        diccionario_dinamico = {}

        tracemalloc.start()

        inicio = perf_counter()
        fibonacci_dinamico(valor, diccionario_dinamico)
        final = perf_counter()

        actual, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tiempo_dinamico.append(final - inicio)
        memoria_dinamico.append(peak)

    ax1.clear()
    ax1.set_title("Fibonacci recursivo/dinamico temporal")
    ax1.set_xlabel("N")
    ax1.set_ylabel("Tiempo")

    ax1.plot(xs, tiempo_recursivo, marker='o', label='Recursivo')
    ax1.plot(xs, tiempo_dinamico, marker='o', label='Dinámico')
    ax1.legend()
    ax1.grid(True, linestyle=':', alpha=0.6)

    ax2.clear()
    ax2.set_title("Fibonacci recursivo/dinamico espacial")
    ax2.set_xlabel("N")
    ax2.set_ylabel("Memoria en bytes")

    ax2.plot(xs, memoria_recursiva, marker='o', label='Recursivo')
    ax2.plot(xs, memoria_dinamico, marker='o', label='Dinamico')
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.6)

    fig.tight_layout()

    canvas.draw()

ventana = tk.Tk()
ventana.title("Análisis de Algoritmos Fibonacci")
# ventana.geometry("1000x600")

control_frame = tk.Frame(ventana)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Ingresa número de elementos:").pack(side="left", padx=5)
entry = tk.Entry(control_frame, width=8)
entry.pack(side="left", padx=5)

btn = tk.Button(control_frame, text="Graficar", command=graficar)
btn.pack(side="left", padx=10)

fig = Figure(figsize=(10, 5), dpi=100)
ax1, ax2 = fig.subplots(1, 2)

canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

ventana.mainloop()
