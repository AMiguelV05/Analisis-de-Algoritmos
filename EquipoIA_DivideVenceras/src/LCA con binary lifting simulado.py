import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VisualizadorLCA:
    def __init__(self, ventana_principal):
        #Constructor de la clase. Inicializa el árbol y la GUI.
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Visualizador de LCA: Comparación de Algoritmos")
        self.ventana_principal.geometry("1100x600")

        #Definición del Árbol de Ejemplo (Estructura Estática)
        self.num_nodos = 12
        self.aristas = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7), (5, 8), (8,9), (8,10), (10,11), (11,12)]
        self.coordenadas = {
            1: (450, 50), 2: (300, 120), 3: (600, 120), 4: (225, 190),
            5: (375, 190), 6: (600, 190), 7: (325, 260), 8: (425, 260), 9: (480, 340),
            10: (405, 340), 11: (430, 420), 12: (430, 500)
        }
        self.radio_nodo = 20
        self.tabla_labels = {}  # Diccionario para guardar las etiquetas de la ventana de la tabla
        self.simulacion_activa = False  #Bandera para evitar iniciar una simulación mientras otra corre

        self.crear_componentes() #Llama a crear la ventana y todas las funciones
        self.reiniciar_estado()  #Llama al preprocesamiento inicial
        self.dibujar_arbol()

    def reiniciar_estado(self):
        #Inicializa o reinicia las estructuras de datos para los algoritmos.
        self.n_maximo = self.num_nodos + 1
        #log_max es el máximo exponente de 2 necesario para los saltos
        self.log_max = math.ceil(math.log2(self.n_maximo))
        self.lista_adyacencia = [[] for _ in range(self.n_maximo)]
        self.nivel = [0] * self.n_maximo  # Almacena la profundidad de cada nodo
        #La tabla padre[u][i] es el 2^i-ésimo ancestro de u.
        self.padre = [[0] * (self.log_max + 1) for _ in range(self.n_maximo)]
        self.construir_lista_adyacencia()

    def construir_lista_adyacencia(self):
        #Convierte la lista de aristas en una lista de adyacencia para el grafo.
        for u, v in self.aristas:
            self.lista_adyacencia[u].append(v)
            self.lista_adyacencia[v].append(u)

    #Generadores para Simulación de Preprocesamiento
    def dfs_generador(self, u, p, l, visitados):
        #Generador que simula el recorrido DFS. 'yield' pausa la función y devuelve el estado actual, permitiendo animar el recorrido paso a paso.

        visitados.add(u)
        self.nivel[u] = l  # Asigna el nivel (profundidad)
        self.padre[u][0] = p  # Asigna el padre directo (ancestro 2^0)
        yield u, p, set(visitados)  # Cede el nodo actual, su padre y el conjunto de visitados
        for v in self.lista_adyacencia[u]:
            if v != p:
                # 'yield from' permite que este generador ceda los valores de otro generador
                yield from self.dfs_generador(v, u, l + 1, visitados)

    def construir_tabla_dispersa_generador(self):
        #Generador que simula la construcción de la tabla de saltos (Binary Lifting) y calcula el ancestro 2^i basándose en los ancestros 2^(i-1) ya calculados.

        # Itera sobre las potencias de 2 (i = 1 para 2^1, i = 2 para 2^2, etc.)
        for i in range(1, self.log_max + 1):
            # Itera sobre cada nodo del árbol para encontrar sus ancestros
            for u in range(1, self.num_nodos + 1):
                ancestro_intermedio = self.padre[u][i - 1]
                if ancestro_intermedio != 0:#Se asegura que en cada salto continúa el árbol
                    #El 2^i-ésimo ancestro es el 2^(i-1)-ésimo ancestro del 2^(i-1)-ésimo ancestro.
                    ancestro_final = self.padre[ancestro_intermedio][i - 1]
                    yield u, i, ancestro_intermedio, ancestro_final  #Cede el estado para la animación
                    self.padre[u][i] = ancestro_final
                else:
                    yield u, i, 0, 0  #No hay ancestro para calcular, cede un estado nulo

    #Generadores para Simulación de Consulta LCA

    def obtener_lca(self, u, v):
        #Generador que simula la búsqueda de LCA con Binary Lifting.
        #1. Asegurar que 'v' sea el nodo más profundo para simplificar
        if self.nivel[u] > self.nivel[v]: u, v = v, u

        #2. Nivelar 'v' con 'u' usando saltos grandes
        for i in range(self.log_max, -1, -1):
            if self.nivel[v] - (1 << i) >= self.nivel[u]:
                v = self.padre[v][i]
                yield u, v

        #3. Si son iguales, 'u' era el ancestro de 'v'
        if u == v:
            yield u, v
            return u

        #4. Subir ambos nodos juntos con saltos grandes, hasta que sus padres sean iguales
        for i in range(self.log_max, -1, -1):
            if self.padre[u][i] != 0 and self.padre[u][i] != self.padre[v][i]:
                u = self.padre[u][i]
                v = self.padre[v][i]
                yield u, v

        #5. El LCA es el padre directo de 'u' (o 'v')
        yield u, v
        return self.padre[u][0]

    def obtener_lca_fuerza_bruta(self, u, v):
        #Generador que simula la búsqueda de LCA subiendo un nodo a la vez.
        #1. Nivelar los nodos subiendo el más profundo de uno en uno
        while self.nivel[u] > self.nivel[v]: u = self.padre[u][0]; yield u, v
        while self.nivel[v] > self.nivel[u]: v = self.padre[v][0]; yield u, v

        #2. Subir ambos nodos de uno en uno hasta que se encuentren
        while u != v:
            u = self.padre[u][0]
            v = self.padre[v][0]
            yield u, v

        #3. El punto de encuentro es el LCA
        yield u, v
        return u

    #Creación de la GUI
    def crear_componentes(self):#Crea y organiza todos los widgets de la interfaz gráfica.
        # Frame principal que contendrá los controles y el lienzo
        main_frame = tk.Frame(self.ventana_principal)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel de controles a la izquierda
        controles_frame = tk.Frame(main_frame, width=250, padx=10, pady=10)
        controles_frame.pack(side=tk.LEFT, fill=tk.Y)
        controles_frame.pack_propagate(False)  # Evita que el frame se encoja

        #Sección de Preprocesamiento
        prep_frame = ttk.LabelFrame(controles_frame, text="1. Simular Preprocesamiento")
        prep_frame.pack(fill=tk.X, pady=10)
        self.btn_sim_dfs = tk.Button(prep_frame, text="Simular DFS (Niveles y Padres)",
                                     command=self.iniciar_simulacion_dfs)
        self.btn_sim_dfs.pack(fill=tk.X, padx=5, pady=5)
        self.btn_sim_tabla = tk.Button(prep_frame, text="Simular Tabla de Saltos",
                                       command=self.iniciar_simulacion_tabla_dispersa)
        self.btn_sim_tabla.pack(fill=tk.X, padx=5, pady=5)

        #Sección de Consulta LCA
        query_frame = ttk.LabelFrame(controles_frame, text="2. Simular Consulta LCA")
        query_frame.pack(fill=tk.X, pady=10)

        nodos_frame = tk.Frame(query_frame)
        nodos_frame.pack(pady=5)
        tk.Label(nodos_frame, text="N1:").pack(side=tk.LEFT)
        self.entrada_nodo1 = tk.Entry(nodos_frame, width=4)
        self.entrada_nodo1.pack(side=tk.LEFT)
        self.entrada_nodo1.insert(0, "")
        tk.Label(nodos_frame, text="N2:").pack(side=tk.LEFT, padx=(10, 0))
        self.entrada_nodo2 = tk.Entry(nodos_frame, width=4)
        self.entrada_nodo2.pack(side=tk.LEFT)
        self.entrada_nodo2.insert(0, "")

        self.algoritmo_seleccionado = tk.StringVar(value="divide_y_venceras")
        self.rb_bl = tk.Radiobutton(query_frame, text="Divide y Vencerás", variable=self.algoritmo_seleccionado,
                                    value="divide_y_venceras")
        self.rb_bl.pack(anchor='w', padx=5)
        self.rb_fb = tk.Radiobutton(query_frame, text="Fuerza Bruta", variable=self.algoritmo_seleccionado,
                                    value="fuerza_bruta")
        self.rb_fb.pack(anchor='w', padx=5)
        self.btn_sim_lca = tk.Button(query_frame, text="Simular Búsqueda de LCA", command=self.iniciar_simulacion_lca)
        self.btn_sim_lca.pack(fill=tk.X, padx=5, pady=5)
        self.etiqueta_resultado = tk.Label(query_frame, text="LCA: ...", font=("Arial", 10, "bold"))
        self.etiqueta_resultado.pack(pady=5)

        #Sección de Análisis
        analysis_frame = ttk.LabelFrame(controles_frame, text="3. Análisis de Complejidad")
        analysis_frame.pack(fill=tk.X, pady=10)
        btn_comparar = tk.Button(analysis_frame, text="Comparar Complejidades",
                                 command=self.graficar_comparacion_complejidades)
        btn_comparar.pack(fill=tk.X, padx=5, pady=5)

        #Canvas a la derecha para dibujar el árbol
        self.lienzo = tk.Canvas(main_frame, bg="white")
        self.lienzo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def controlar_widgets(self, estado):
        #Habilita o deshabilita todos los controles para evitar interrupciones durante una simulación.
        state = tk.NORMAL if estado else tk.DISABLED
        self.btn_sim_dfs.config(state=state)
        self.btn_sim_tabla.config(state=state)
        self.btn_sim_lca.config(state=state)
        self.rb_bl.config(state=state)
        self.rb_fb.config(state=state)
        self.simulacion_activa = not estado

    #Lógica de Dibujo
    def dibujar_arbol(self, **kwargs): #Dibuja el árbol y todos los resaltados según los parámetros recibidos.
        self.lienzo.delete("all")
        #Extrae argumentos con los valores por defecto para no generar errores
        nodos_visitados = kwargs.get('nodos_visitados', set())
        nodo_actual_dfs = kwargs.get('nodo_actual_dfs')
        camino_tabla = kwargs.get('camino_tabla', [])
        resaltar_iniciales = kwargs.get('resaltar_iniciales')
        resaltar_actuales = kwargs.get('resaltar_actuales')
        resaltar_lca = kwargs.get('resaltar_lca')
        camino_u = kwargs.get('camino_u')
        camino_v = kwargs.get('camino_v')

        #1. Dibujar texto informativo, aristas base y caminos resaltados
        self.lienzo.create_text(10, 10, anchor='nw', text=kwargs.get('info_texto', ''))
        for u, v in self.aristas:
            self.lienzo.create_line(self.coordenadas[u], self.coordenadas[v], fill="lightgray", width=2)

        #Dibuja los caminos para la simulación de tabla y LCA en rojo
        for camino in [camino_u, camino_v, camino_tabla]:
            if camino and len(camino) > 1:
                for i in range(len(camino) - 1):
                    self.lienzo.create_line(self.coordenadas[camino[i]], self.coordenadas[camino[i + 1]], fill="red",
                                            width=3)

        #2. Dibujar nodos con colores según su estado en la simulación
        for nodo, (x, y) in self.coordenadas.items():
            color_relleno = "white"
            if nodo in nodos_visitados: color_relleno = "lightgray"  # Nodos visitados en DFS
            if resaltar_iniciales and nodo in resaltar_iniciales: color_relleno = "deepskyblue"  # Nodos de inicio LCA
            if resaltar_actuales and nodo in resaltar_actuales: color_relleno = "orange"  # Punteros actuales en LCA
            if nodo == nodo_actual_dfs: color_relleno = "violet"  # Nodo actual en DFS
            if nodo == resaltar_lca: color_relleno = "lightgreen"  # LCA encontrado

            self.lienzo.create_oval(x - self.radio_nodo, y - self.radio_nodo, x + self.radio_nodo, y + self.radio_nodo,
                                    fill=color_relleno, outline="black", width=2)
            self.lienzo.create_text(x, y, text=str(nodo), font=("Arial", 12, "bold"))

    #Lógica de Simulaciones
    def iniciar_simulacion_dfs(self): #Función de arranque para la simulación de DFS.
        if self.simulacion_activa: return
        self.controlar_widgets(False)
        self.reiniciar_estado()  #Limpia datos anteriores
        self.etiqueta_resultado.config(text="Simulando DFS...", fg="blue")
        generador = self.dfs_generador(1, 0, 1, set())  #Crea el generador
        self.paso_simulacion_dfs(generador)  #Inicia el bucle de animación

    def paso_simulacion_dfs(self, generador): #Ejecuta un paso de la animación DFS y programa el siguiente.
        try:
            u, p, visitados = next(generador)  #Avanza el generador al siguiente yield
            info = f"Visitando nodo: {u}\nPadre: {p}\nNivel: {self.nivel[u]}"
            self.dibujar_arbol(nodos_visitados=visitados, nodo_actual_dfs=u, info_texto=info)
            #Llama a esta misma función después de un retardo para el siguiente paso
            self.ventana_principal.after(400, lambda: self.paso_simulacion_dfs(generador))
        except StopIteration:
            #El generador terminó (recorrió el árbol completo)
            self.dibujar_arbol(nodos_visitados=set(range(1, self.num_nodos + 1)))
            self.etiqueta_resultado.config(text="DFS completado.", fg="black")
            self.controlar_widgets(True)  # Reactiva los botones

    def iniciar_simulacion_tabla_dispersa(self): #Función de arranque para la simulación de la tabla de saltos.
        if self.simulacion_activa: return
        self.controlar_widgets(False)
        self.reiniciar_estado()
        #Se necesita ejecutar el DFS primero para tener los padres directos (columna i=0)
        for _ in self.dfs_generador(1, 0, 1, set()): pass
        self.etiqueta_resultado.config(text="Simulando Tabla...", fg="blue")
        self.crear_ventana_tabla()  # Abre la ventana emergente para la tabla
        generador = self.construir_tabla_dispersa_generador()
        self.paso_simulacion_tabla(generador)

    def paso_simulacion_tabla(self, generador): #Ejecuta un paso de la animación de llenado de la tabla.
        try:
            u, i, p_intermedio, p_final = next(generador)
            #Resalta la celda actual en la ventana de la tabla
            for label in self.tabla_labels.values(): label.config(bg='white')
            if (u, i) in self.tabla_labels: self.tabla_labels[(u, i)].config(bg='yellow')
            if p_final != 0:
                self.tabla_labels[(u, i)].config(text=str(p_final))
                camino = self.obtener_camino_hacia_ancestro(u, p_final)
                info = f"Calculando padre[u={u}][2^{i}={1 << i}]\n" \
                       f"Salto intermedio: {u} -> {p_intermedio}\n" \
                       f"Salto final: {p_intermedio} -> {p_final}"
            else:
                camino, info = [], f"Calculando padre[u={u}][2^{i}={1 << i}]\nNo hay ancestro."
            self.dibujar_arbol(camino_tabla=camino, info_texto=info)
            self.ventana_principal.after(300, lambda: self.paso_simulacion_tabla(generador))
        except StopIteration:
            self.dibujar_arbol()
            self.etiqueta_resultado.config(text="Tabla de saltos completada.", fg="black")
            self.controlar_widgets(True)

    def iniciar_simulacion_lca(self): #Función de arranque para la simulación de búsqueda de LCA.
        if self.simulacion_activa: return
        try:
            u, v = int(self.entrada_nodo1.get()), int(self.entrada_nodo2.get())
            if u not in self.coordenadas or v not in self.coordenadas:
                self.etiqueta_resultado.config(text="Error: Nodos inválidos.", fg="red")
                return
            self.controlar_widgets(False)
            self.etiqueta_resultado.config(text="Buscando LCA...", fg="blue")
            self.dibujar_arbol(resaltar_iniciales=(u, v))

            #Asegurarse que el preprocesamiento está hecho antes de la consulta
            self.reiniciar_estado()
            for _ in self.dfs_generador(1, 0, 1, set()): pass
            for _ in self.construir_tabla_dispersa_generador(): pass

            #Elige el algoritmo según la selección del usuario
            if self.algoritmo_seleccionado.get() == "divide_y_venceras":
                generador = self.obtener_lca(u, v)
            else:
                generador = self.obtener_lca_fuerza_bruta(u, v)

            self.paso_simulacion_lca(u, v, generador)
        except ValueError:
            self.etiqueta_resultado.config(text="Error: Ingrese números.", fg="red")

    def paso_simulacion_lca(self, u_inicial, v_inicial, generador): #Ejecuta un paso de la animación de búsqueda de LCA."""
        try:
            u_actual, v_actual = next(generador)
            camino_u = self.obtener_camino_hacia_ancestro(u_inicial, u_actual)
            camino_v = self.obtener_camino_hacia_ancestro(v_inicial, v_actual)
            self.dibujar_arbol(resaltar_iniciales=(u_inicial, v_inicial), resaltar_actuales=(u_actual, v_actual),
                               camino_u=camino_u, camino_v=camino_v)
            self.ventana_principal.after(500, lambda: self.paso_simulacion_lca(u_inicial, v_inicial, generador))
        except StopIteration as e: # El generador termina y devuelve el LCA en la excepción
            lca = e.value
            self.etiqueta_resultado.config(text=f"LCA es: {lca}", fg="black")
            camino_u = self.obtener_camino_hacia_ancestro(u_inicial, lca)
            camino_v = self.obtener_camino_hacia_ancestro(v_inicial, lca)
            self.dibujar_arbol(resaltar_iniciales=(u_inicial, v_inicial), resaltar_lca=lca, camino_u=camino_u,
                               camino_v=camino_v)
            self.controlar_widgets(True)

    #Ventanas y Gráficos
    def crear_ventana_tabla(self): #Crea la ventana emergente que muestra la tabla de ancestros.
        win = tk.Toplevel(self.ventana_principal)
        win.title("Tabla de Ancestros (padre[u][i])")
        tk.Label(win, text="u \\ i", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2)
        for i in range(self.log_max + 1):
            tk.Label(win, text=f"{i}", font=("Arial", 10, "bold")).grid(row=0, column=i + 1, padx=5, pady=2)
            tk.Label(win, text=f"(2^{i})", font=("Arial", 8)).grid(row=1, column=i + 1)
        for u in range(1, self.num_nodos + 1):
            tk.Label(win, text=f"{u}", font=("Arial", 10, "bold")).grid(row=u + 1, column=0, padx=5, pady=2)
            for i in range(self.log_max + 1):
                # Inicialmente, solo se conoce la columna i=0 (padres directos)
                val = self.padre[u][i] if i == 0 else "?"
                label = tk.Label(win, text=str(val), width=4, relief="ridge")
                label.grid(row=u + 1, column=i + 1)
                self.tabla_labels[(u, i)] = label

    def obtener_camino_hacia_ancestro(self, u_start, u_end): #Devuelve una lista de nodos desde un nodo inicial hasta un ancestro.
        if u_start == 0 or u_end == 0: return []
        camino = [u_start]
        curr = u_start
        #Limita las iteraciones para evitar bucles infinitos en caso de error
        for _ in range(self.num_nodos + 1):
            if curr == u_end: break
            curr = self.padre[curr][0]  #Sube al padre directo
            if curr == 0: return []  #Si llega a la raíz virtual, el ancestro no estaba en el camino
            camino.append(curr)
        return camino

    def graficar_comparacion_complejidades(self): #Genera y muestra los gráficos de complejidad.
        if self.simulacion_activa: return
        #Crea un rango de valores para el eje X dependiendo de num_nodos
        N = np.arange(1, self.num_nodos + 2)
        #Calcula los valores del eje Y para cada curva de complejidad
        logN_time = np.log2(N)
        N_time = N
        NlogN_space = N * logN_time
        N_space = N
        #Crea el lienzo y dos ejes que son las gráficas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
        fig.suptitle('Comparación de Complejidad', fontsize=16)
        #Se configuran y dibujan las gráficas
        ax1.plot(N, logN_time, label='Divide y Vencerás (O(log N))', color='blue', marker='o')
        ax1.plot(N, N_time, label='Fuerza Bruta (O(N))', color='red', linestyle='--', marker='x')
        ax1.set_title('Complejidad Temporal (por Consulta)')
        ax1.set_xlabel('Número de Nodos (N)')
        ax1.set_ylabel('Operaciones (aprox.)')
        ax1.legend()
        ax1.grid(True)
        ax2.plot(N, NlogN_space, label='Divide y Vencerás (O(N log N))', color='blue', marker='o')
        ax2.plot(N, N_space, label='Fuerza Bruta (O(N))', color='red', linestyle='--', marker='x')
        ax2.set_title('Complejidad Espacial')
        ax2.set_xlabel('Número de Nodos (N)')
        ax2.set_ylabel('Elementos Almacenados')
        ax2.legend()
        ax2.grid(True)
        #Se muestra toda la comparación en una nueva ventana
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        win = tk.Toplevel(self.ventana_principal)
        win.title("Comparación de Complejidades (LCA)")
        win.geometry("1200x600")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


#Bloque de Ejecución Principal
if __name__ == "__main__":
    raiz = tk.Tk()
    aplicacion = VisualizadorLCA(raiz)
    raiz.mainloop()

