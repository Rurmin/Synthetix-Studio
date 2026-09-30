```markdown
# 🚀 Synthetix Studio — Mini IDE & Code Analysis Tool (Python CLI)

**Synthetix Studio** es un Entorno de Desarrollo Minimalista (Mini IDE) interactivo ejecutado desde la consola de comandos (CLI) en Python 3. El proyecto nace como una reconstrucción y migración completa de un entorno previamente diseñado en C++, manteniendo las restricciones académicas de desarrollo de bajo nivel: implementa estructuras de datos dinámicas avanzadas construidas estrictamente desde cero mediante punteros/referencias a nodos, sin depender de bibliotecas externas ni de métodos o estructuras nativas del lenguaje.

El sistema permite la administración de archivos en memoria virtual mediante una Lista Doblemente Enlazada, gestión del historial de cambios (Deshacer/Rehacer) mediante una Doble Pila, análisis sintáctico de delimitadores en tiempo real, un motor de ordenamiento interno (InsertionSort y QuickSort) y la simulación del flujo de peticiones a un servicio de Inteligencia Artificial gestionado por una Cola FIFO.

---

## 📋 Tabla de Contenidos

1. [Características Principales](#-características-principales)
2. [Prerrequisitos de Software](#-prerrequisitos-de-software)
3. [📥 Replicación e Instalación](#-replicación-e-instalación)
4. [⚙️ Guía de Ejecución y Uso](#️-guía-de-ejecución-y-uso)
5. [💻 Detalle de Opciones del Menú CLI](#-detalle-de-opciones-del-menú-cli)
6. [🏗️ Arquitectura de Software y Módulos](#️-arquitectura-de-software-y-módulos)
7. [📐 Fundamentos Técnicos y Estructuras de Datos](#-fundamentos-técnicos-y-estructuras-de-datos)
8. [👥 Autores y Créditos](#-autores-y-créditos)

---

## ✨ Características Principales

* **Administración Dinámica de Archivos Virtuales**: Creación, edición, selección y eliminación de archivos en memoria usando nodos enlazados bidireccionalmente.
* **Verificación Sintáctica (Syntax Checker)**: Algoritmo basado en Pila que analiza el balanceo de delimitadores (`()`, `{}`, `[]`), reportando la línea y columna exactas donde ocurre un error sintáctico.
* **Sistema Undo/Redo Completo**: Control del historial de ediciones por cada archivo mediante una estructura de doble pila (Pila de Deshacer y Pila de Rehacer).
* **Buffer de Peticiones a IA (Cola FIFO)**: Simulación de encolado y procesamiento de consultas analíticas (`explicar`, `optimizar`, `refactorizar`) respetando el orden estricto de llegada (*First In, First Out*).
* **Motor de Ordenamiento Interno**: Implementación manual de algoritmos de ordenamiento (**InsertionSort** para nombres de archivos y **QuickSort** para ordenamiento por identificadores numéricos).
* **Cero Dependencias Externas**: Código 100 % Python puro sin uso de paquetes de terceros ni funciones integradas como `.sort()`, `list.pop()`, etc.

---

## 🛠️ Prerrequisitos de Software

Para ejecutar este proyecto en tu entorno local, únicamente necesitas contar con el intérprete oficial de Python y Git para la gestión de versiones:

1. **Python**: Versión 3.8 o superior instalada en el sistema.
2. **Git**: Para clonar y sincronizar el repositorio.

*Nota: No se requiere la instalación de librerías mediante `pip` ya que todo el sistema corre sobre la librería estándar de Python.*

---

## 📥 Replicación e Instalación

Sigue estos pasos detallados desde tu terminal (PowerShell, CMD, Bash o la Terminal integrada de VS Code) para replicar exactamente el proyecto en tu equipo:

```bash
# 1. Clonar el repositorio desde GitHub
git clone [https://github.com/Rurmin/Synthetix-Studio.git](https://github.com/Rurmin/Synthetix-Studio.git)

# 2. Navegar al directorio raíz del proyecto
cd Synthetix-Studio

# 3. Comprobar que la estructura de carpetas y archivos esté completa
# En Windows (PowerShell/CMD):
dir
# En Linux/macOS:
ls -la

```

---

## ⚙️ Guía de Ejecución y Uso

Para iniciar el entorno CLI interactivo de Synthetix Studio, ejecuta el archivo de entrada principal `main.py`:

```bash
python main.py

```

Al ejecutarse, el programa desplegará la interfaz en consola e inicializará un archivo de demostración básico (`main.py` virtual) en la lista enlazada para permitir pruebas inmediatas.

---

## 💻 Detalle de Opciones del Menú CLI

El control del sistema se realiza ingresando el número de opción correspondiente en el menú interactivo:

| Opción | Módulo / Operación | Descripción Técnica y Funcional |
| --- | --- | --- |
| **1** | **Crear nuevo archivo** | Solicita el nombre y contenido inicial. Crea un nuevo nodo en la **Lista Doblemente Enlazada** (`FileList`). |
| **2** | **Listar archivos abiertos** | Recorre la lista bidireccional mostrando ID, nombre de archivo y marcando cuál es el archivo activo. |
| **3** | **Cambiar de archivo activo** | Cambia el puntero del archivo activo por ID o nombre y reinicia el historial Undo/Redo para el nuevo contexto. |
| **4** | **Editar contenido activo** | Muestra el código actual, almacena el estado anterior en la **Pila Undo** y actualiza el texto en el nodo activo. |
| **5** | **Validar sintaxis** | Invoca al **`SyntaxChecker`**, que recorre el código carácter por carácter apilando/desapilando apertura y cierre de símbolos. |
| **6** | **Deshacer cambio (Undo)** | Extrae el último estado de la **Pila Undo**, lo mueve a la **Pila Redo** y restaura el contenido previo del archivo. |
| **7** | **Rehacer cambio (Redo)** | Extrae el estado retenido en la **Pila Redo**, lo regresa a la **Pila Undo** y reaplica la edición. |
| **8** | **Encolar solicitud a IA** | Recibe una instrucción (`explicar`, `optimizar`, `refactorizar`) y la inserta al final de la **Cola FIFO** (`RequestQueue`). |
| **9** | **Procesar solicitud IA** | Extrae el elemento al frente de la cola y envía la petición a **`AIService`** para obtener la respuesta analítica. |
| **10** | **Ordenar y ver lista** | Ejecuta el **`SortingEngine`** aplicando **InsertionSort** (A-Z por nombre) o **QuickSort** (ascendente por ID). |
| **11** | **Eliminar archivo activo** | Remueve el nodo activo de la lista enlazada reajustando los punteros `prev` y `next`, y libera el espacio. |
| **0** | **Salir** | Finaliza la ejecución del programa de manera limpia. |

---

## 🏗️ Arquitectura de Software y Módulos

El proyecto utiliza un diseño modular para separar las estructuras de datos nucleares, los servicios de apoyo y la capa de presentación/controlador:

```text
Synthetix-Studio/
├── config/
│   └── config.json          # Archivo de configuración con parámetros y API key
├── core/
│   ├── file_list.py         # Lista Doblemente Enlazada para la gestión de archivos
│   ├── request_queue.py     # Cola FIFO para buffering de solicitudes de IA
│   ├── sorting.py           # Algoritmos manuales de ordenamiento (InsertionSort / QuickSort)
│   ├── stack.py             # Pila genérica mediante nodos y punteros
│   ├── syntax_checker.py    # Validador de delimitadores balanceados basado en Pila
│   └── undo_redo.py         # Gestor de historial con esquema de Doble Pila
├── services/
│   └── ai_service.py        # Procesador analítico de consultas y lectura de config
├── .gitignore               # Exclusiones para control de versiones Git
├── main.py                  # Controlador de la CLI y punto de entrada de la aplicación
└── readme.md                # Documentación exhaustiva del proyecto

```

---

## 📐 Fundamentos Técnicos y Estructuras de Datos

Para cumplir con los estándares académicos de la asignatura Algoritmos y Estructuras de Datos, se proscribió el uso de librerías contenedoras nativas. Todas las estructuras fueron implementadas desde cero:

### 1. Lista Doblemente Enlazada (`FileList`)

Cada archivo en memoria es representado por un objeto `FileNode` que contiene: `id`, `filename`, `content`, `prev` (referencia al nodo anterior) y `next` (referencia al nodo siguiente). Permite navegación bidireccional y eliminación de nodos arbitrarios en tiempo $O(1)$ cuando se conoce la referencia.

### 2. Pila Genérica (`Stack`)

Implementada mediante nodos enlazados donde las operaciones de apilar (`push`) y desapilar (`pop`) ocurren exclusivamente en el tope (`top`) de la pila, garantizando una complejidad temporal de $O(1)$.

* **Validación Sintáctica**: Examina caracteres `(`, `[`, `{`. Si encuentra un delimitador de apertura, lo apila junto con su posición (línea/columna). Si encuentra uno de cierre, verifica que coincida con el elemento en el tope. Si no coincide o la pila queda vacía antes de tiempo, detecta el error.
* **Motor Undo/Redo**: Utiliza dos instancias independientes de `Stack`. Cada edición apila el contenido previo en `undo_stack` y limpia `redo_stack`. Deshacer mueve el estado de `undo_stack` a `redo_stack`.

### 3. Cola FIFO (`RequestQueue`)

Estructura enlazada que mantiene dos punteros: `front` (frente de la cola) y `rear` (final de la cola). Permite la inserción de solicitudes (`enqueue`) en $O(1)$ por el final y la extracción de peticiones (`dequeue`) en $O(1)$ por el frente, garantizando el orden de atención para las llamadas a la IA.

### 4. Algoritmos de Ordenamiento Manuales (`SortingEngine`)

* **InsertionSort (por Nombre)**: Algoritmo de complejidad $O(n^2)$ idóneo para conjuntos pequeños de archivos, comparando cadenas alfabéticamente e insertándolas en su posición correcta.
* **QuickSort (por ID)**: Algoritmo de división y conquista de complejidad promedio $O(n \log n)$ que selecciona un pivote para particionar la lista de metadatos según sus identificadores enteros.

---

## 👥 Autores y Créditos

Proyecto desarrollado y migrado colaborativamente por:

* **José Pascia**
* **Alejandra Rivero**

```

```