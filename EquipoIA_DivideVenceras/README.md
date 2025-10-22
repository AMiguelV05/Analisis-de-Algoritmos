Visualizador de LCA: Comparación de Algoritmos

Este proyecto implementa una **aplicación visual interactiva** para comprender el funcionamiento del **algoritmo de Lowest Common Ancestor (LCA)** o **Ancestro Común Más Bajo**, utilizando Python y Tkinter.
Permite **simular, visualizar y comparar** los métodos de búsqueda de LCA mediante **Binary Lifting (Divide y Vencerás)** y **Fuerza Bruta**, mostrando su complejidad temporal y espacial.

---

Características principales

* **Visualización gráfica** del árbol y sus recorridos.
* **Simulación paso a paso** del recorrido DFS (para niveles y padres).
* **Simulación interactiva** de la construcción de la tabla de saltos (Binary Lifting).
* **Comparación visual** entre los algoritmos de:

  * 🔵 *Divide y Vencerás (Binary Lifting)*
  * 🔴 *Fuerza Bruta*
* **Gráficos de complejidad** temporal y espacial (con `matplotlib`).
* Interfaz creada con **Tkinter**.

---
Tecnologías utilizadas

* **Python 3.9+**
* **Tkinter** — para la interfaz gráfica.
* **Matplotlib** — para los gráficos comparativos.
* **NumPy** — para el manejo de datos numéricos.
* **Math** — para los cálculos logarítmicos del Binary Lifting.

---

⚙️ Instalación

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/tuusuario/Analisis-de-Algoritmos.git
   cd Analisis-de-Algoritmos
   cd EquipoIA_DivideVenceras
   ```

2. **Instala las dependencias**:

   ```bash
   pip install matplotlib numpy tracemalloc
   ```

3. **Ejecuta la aplicación**:

   ```bash
   python LCA-con-binary-lifting-simulado.py
   ```

---

Conceptos clave

DFS (Depth-First Search)

Permite recorrer el árbol para determinar los **niveles** de cada nodo y su **padre directo**, lo que es esencial para la posterior construcción de la tabla de saltos.

Binary Lifting (Divide y Vencerás)

Preprocesa una tabla `padre[u][i]` donde cada celda almacena el **2^i-ésimo ancestro** del nodo `u`.
Permite responder consultas LCA en **O(log N)** tiempo.

Fuerza Bruta

Asciende nodo por nodo hasta que ambos convergen en el mismo ancestro.
Tiene complejidad **O(N)** por consulta.

---

Complejidad de los algoritmos

| Algoritmo         | Preprocesamiento | Consulta | Espacio    |
| ----------------- | ---------------- | -------- | ---------- |
| Divide y Vencerás | O(N log N)       | O(log N) | O(N log N) |
| Fuerza Bruta      | O(N)             | O(N)     | O(N)       |

La aplicación permite visualizar gráficamente esta comparación mediante gráficos generados con `matplotlib`.

---

Uso de la aplicación

1. Ejecuta el programa (`python LCA-con-binary-lifting-simulado.py`).
2. Desde la ventana principal:

   * Pulsa **"Simular DFS"** para recorrer el árbol.
   * Pulsa **"Simular Tabla de Saltos"** para construir la tabla del Binary Lifting.
   * Ingresa dos nodos en **N1** y **N2**.
   * Elige el algoritmo (*Divide y Vencerás* o *Fuerza Bruta*).
   * Pulsa **"Simular Búsqueda de LCA"**.
   * Observa la animación paso a paso en el lienzo.
3. Pulsa **"Comparar Complejidades"** para visualizar las gráficas de rendimiento.

---
**Diseño de la visualización realizado por IsmaGC - Implementación del algoritmo por AmiguelV05**
---
