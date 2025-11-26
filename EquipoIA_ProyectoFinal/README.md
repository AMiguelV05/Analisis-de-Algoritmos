# Visualizador de Algoritmos LCA con Compresión Huffman  
Aplicación en Python que permite simular, comparar y visualizar el funcionamiento de tres algoritmos para encontrar el **Lowest Common Ancestor (LCA)** en un árbol.  
Incluye gráficas de rendimiento y soporte para guardar/cargar estructuras comprimidas usando **Huffman**.

---

## Características principales

- **Algoritmos de LCA implementados:**
  - Fuerza Bruta (O(N))
  - Binary Lifting / Divide y Vencerás con programación dinámica (O(log N) por consulta)
  - Tarjan Offline con DSU (O(N + Q α(N)))

- **Visualizaciones interactivas:**
  - Recorrido DFS del preprocesamiento.
  - Construcción de tabla de saltos (Binary Lifting).
  - Paso a paso de cada algoritmo durante la consulta.

- **Medición de rendimiento:**
  - Tiempo de ejecución.
  - Uso de memoria en bytes.
  - Gráficas comparativas en tiempo real usando Matplotlib.

- **Compresión Huffman:**
  - Guardado del árbol en archivo `.huff`.
  - Carga de estructuras comprimidas.

---

## 📦 Dependencias

Instalar las dependencias necesarias:

```
pip install matplotlib
```

## Instrucciones de ejecución

- Clona o descarga el repositorio.
- Asegúrate de tener Python 3.9+.
- Ejecuta el programa:
```
python todos_los_algoritmos.py
```
- La interfaz gráfica se abrirá con opciones para:

  - Simular preprocesamientos (DFS y tabla de saltos)

  - Ejecutar y medir algoritmos LCA

  - Visualizar caminos y nodos

  - Generar gráficas de complejidad

  - Guardar y cargar estructuras comprimidas

## Breve explicación del proyecto

Este proyecto compara distintas estrategias para resolver el Ancestro Común Más Bajo (LCA) en un árbol.

**Fuerza Bruta**

Simple de implementar y de bajo consumo de memoria.
Complejidad: O(N).

**Binary Lifting**

Preprocesa una tabla que permite realizar saltos de tamaño potencia de dos.
Consulta: O(log N).
Ideal cuando se harán muchas consultas sobre un árbol estático.

**Tarjan Offline**

Utiliza Union-Find (DSU) + DFS para resolver todas las consultas conocidas de antemano.
Complejidad: O(N + Q α(N)).

**Compresión Huffman**

Permite guardar y cargar la estructura del árbol de forma comprimida mediante archivos `.huff`.

## Resultados esperados
* Binary Lifting es el más rápido para múltiples consultas.

* Fuerza Bruta es suficiente para árboles pequeños.

* Tarjan es extremadamente eficiente cuando las consultas se conocen antes.

* Huffman reduce significativamente el tamaño de la estructura serializada.