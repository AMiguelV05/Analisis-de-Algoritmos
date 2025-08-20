import tkinter as tk
from time import perf_counter
from tkinter import messagebox
import numpy as np
import algoritmos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Función principal
def iniciar():
    # Creacion de la ventana principal
    ventana = tk.Tk()
    ventana.geometry('650x1000')
    ventana.title('Busqueda con GUI')
    # Variables locales a utilizar
    listaDatos = []
    numElementos = tk.StringVar()
    numElementos.set('10')
    numBuscar =tk.StringVar()
    numBuscar.set('Ingresa el dato a buscar')

    # Guardar resultados
    tiemposLineal=[]
    tamanosLineal=[]
    tiemposBinaria=[]
    tamanosBinaria=[]

    # Frame para resultados + scroll
    frame_resultados = tk.Frame(ventana)

    # Cuadro de texto para mostrar resultados
    txtResultados = tk.Text(frame_resultados, wrap="word", height=10, font=("Arial", 12))

    # Barra de desplazamiento
    scrollbar = tk.Scrollbar(frame_resultados, command=txtResultados.yview)

    # Conectar el Text con la Scrollbar
    txtResultados.config(yscrollcommand=scrollbar.set, state="disabled")

    # Función para agregar resultados
    def agregar_resultado(texto):
        txtResultados.config(state="normal")  # permitir edición temporal
        txtResultados.insert("end", texto + "\n")  # añadir línea
        txtResultados.see("end")  # hacer scroll automático al final
        txtResultados.config(state="disabled")  # volver a solo lectura

    # Funciones secundarias
    # Funcion para seleccionar el texto al hacer click en el elemento Entry
    # Evita añadir el numero acompañado del texto inicial
    def seleccionar_texto(event):
        event.widget.selection_range(0, tk.END)
        lblEntrada.config(fg="black", font=("Arial", 12, 'roman'))

    # Funcion para generar num aleatorios
    def generar():
        try:
            n = int(numElementos.get())
            if n<= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Numero de elementos invalido")
            return

        datos = algoritmos.generar_datos(n)
        listaDatos.clear()
        listaDatos.extend(datos)
        messagebox.showinfo("Resultado", f"{numElementos.get()} numeros generados con exito!")

    # Lógica de los casos
    def busqueda_lineal():
        if not  listaDatos:
            messagebox.showerror("Error", "No hay datos")
            return

        try:
            x = int(numBuscar.get())
        except ValueError:
            messagebox.showerror("Error", "Numero invalido")
            return

        inicio = perf_counter()
        encontrado = algoritmos.busqueda_lineal(listaDatos, x)
        final = perf_counter()

        if encontrado:
            textoC = (f'B. Lineal: Número {x} encontrado en el índice [{listaDatos.index(x)}]  '
                      f'Tiempo: {final-inicio:.10f}s\n')
            agregar_resultado(textoC)
            tiemposLineal.append(final-inicio)
            tamanosLineal.append(len(listaDatos))
            actualizar_grafica()
            actualizar_grafica_promedio()
        else:
            agregar_resultado(f"B. Lineal: Número {x} no encontrado\n")

    def busqueda_binaria():
        if not listaDatos:
            messagebox.showerror("Error", "No hay datos")
            return
        try:
            x = int(numBuscar.get())
        except ValueError:
            messagebox.showerror("Error", "Numero invalido")
            return

        inicio = perf_counter()
        encontrado = algoritmos.busqueda_binaria(listaDatos, x)
        final = perf_counter()
        if encontrado:
            textoC = (f'B. Binaria: Número {x} encontrado en el índice [{listaDatos.index(x)}]  '
                      f'Tiempo: {final-inicio:.10f}s\n')
            agregar_resultado(textoC)
            tiemposBinaria.append(final-inicio)
            tamanosBinaria.append(len(listaDatos))
            actualizar_grafica()
        else:
            agregar_resultado(f"B. Binaria: Número {x} no encontrado\n")

    def calcular_promedios():
        tamanios = [100, 1000, 10000, 100000, 1000000]  # Tamaños de prueba
        repeticiones = 5  # Número de repeticiones por caso

        tiempos_lineal = []
        tiempos_binaria = []

        for n in tamanios:
            tiempos_l = []
            tiempos_b = []

            for _ in range(repeticiones):
                # Generar nueva lista de datos
                datos = algoritmos.generar_datos(n)

                # Elegir un número al azar de la lista
                x = np.random.choice(datos)

                # Búsqueda lineal
                inicio = perf_counter()
                algoritmos.busqueda_lineal(datos, x)
                tiempos_l.append(perf_counter() - inicio)

                # Búsqueda binaria
                inicio = perf_counter()
                algoritmos.busqueda_binaria(datos, x)
                tiempos_b.append(perf_counter() - inicio)

            # Promediar tiempos
            tiempos_lineal.append(np.mean(tiempos_l))
            tiempos_binaria.append(np.mean(tiempos_b))

        return tamanios, tiempos_lineal, tiempos_binaria

    def actualizar_grafica_promedio():
        figPromedio.clear()
        ax = figPromedio.add_subplot(111)

        tamanios, tiempos_lineal, tiempos_binaria = calcular_promedios()

        ax.plot(tamanios, tiempos_lineal, marker='o', label='Lineal')
        ax.plot(tamanios, tiempos_binaria, marker='s', label='Binaria')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Tamaño de lista')
        ax.set_ylabel('Tiempo promedio (s)')
        ax.set_title('Comparación de algoritmos (promedios)')
        ax.legend()
        canvasPromedio.draw()

    # Función para actualizar la gráfica
    def actualizar_grafica():
        fig.clear()
        ax = fig.add_subplot(111)

        if tiemposLineal:
            ax.plot(tamanosLineal, tiemposLineal, marker='o', label='Lineal')
        if tiemposBinaria:
            ax.plot(tamanosBinaria, tiemposBinaria, marker='s', label='Binaria')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Tamaño de lista')
        ax.set_ylabel('Tiempo (s)')
        ax.set_title('Comparación de algoritmos de búsqueda')
        if tiemposLineal or tiemposBinaria:
            ax.legend()
        canvas.draw()

    def reiniciar():
        tamanosLineal.clear()
        tamanosBinaria.clear()
        tiemposLineal.clear()
        tiemposBinaria.clear()
        actualizar_grafica()
        actualizar_grafica_promedio()

    # Definicion de la figura de la gráfica
    fig = Figure(figsize=(5,5))
    canvas = FigureCanvasTkAgg(fig, master=ventana)

    figPromedio = Figure(figsize=(5,5))
    canvasPromedio = FigureCanvasTkAgg(figPromedio, master=ventana)

    # Diseño de instrucciones
    lblPrincipal = tk.Label(ventana, text='Selecciona un número de datos a generar:', font=('Arial', 14))
    menuOpciones = tk.OptionMenu(ventana, numElementos,'10', '100', '1000', '10000', '100000', '1000000')
    menuOpciones.config(bg='light blue', fg='black', font=('Arial', 12), width=15)
    btnNumDatos = tk.Button(ventana, text="Generar Datos", activebackground='light gray', cursor='hand2', relief='groove',
                            command= generar)

    # Diseño de entrada de dato
    lblEntrada = tk.Entry(ventana, textvariable=numBuscar, fg='gray', font=('Arial', 12, 'italic'))
    lblEntrada.bind("<FocusIn>", seleccionar_texto)

    # Diseño botones de busqueda
    btnLineal = tk.Button(ventana, text="Busqueda Lineal", activebackground='light gray', cursor='hand2', relief='groove',
                          command= busqueda_lineal)
    btnBinario = tk.Button(ventana, text="Busqueda Binaria", activebackground='light gray', cursor='hand2', relief='groove',
                           command= busqueda_binaria)
    btnReiniciar = tk.Button(ventana, text="Reiniciar", activebackground='light gray', cursor='hand2', command= reiniciar)

    # Elementos.pack
    lblPrincipal.pack(pady = 10)
    menuOpciones.pack()
    btnNumDatos.pack(pady = 10)
    lblEntrada.pack(pady= 20)
    btnLineal.pack(pady = 10)
    btnBinario.pack(pady = 10)
    frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)
    txtResultados.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    btnReiniciar.pack(pady=50, side="right", expand=True)
    canvas.get_tk_widget().pack(pady=20, side="left")
    canvasPromedio.get_tk_widget().pack(pady=20)


    ventana.mainloop()

