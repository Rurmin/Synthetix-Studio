# 🚀 Synthetix Studio — Mini IDE: Estructuras Jerárquicas y Búsqueda Avanzada (Python CLI)

**Synthetix Studio** es un Entorno de Desarrollo Minimalista (Mini IDE) interactivo ejecutado desde la consola de línea de comandos (CLI) en Python 3 bajo el **Patrón de Diseño Comandos (Command Pattern)**. El proyecto implementa estructuras de datos lineales (Fase 1) y **no lineales jerárquicas y de búsqueda avanzada (Fase 2)** construidas **estrictamente desde cero** en Programación Orientada a Objetos (POO), encapsulando los nodos, punteros y algoritmos de recorrido y balanceo sin usar estructuras predefinidas del lenguaje, y gestionando **archivos físicos de código** en el disco.

---

## 📋 Módulos Implementados (Fase 2 + Fase 1)

### 1. Explorador de Espacio de Trabajo — Árbol N-ario (`core/nary_tree.py`)
* Representa un sistema de archivos virtual y físico (`workspace/`) mediante nodos `NaryNode` enlazados con punteros **Hijo-Izquierdo / Hermano-Derecho (`_first_child`, `_next_sibling`)** y puntero al **Padre (`_parent`)**.
* Permite la creación de carpetas infinitamente anidadas (`mkdir`), navegación jerárquica (`cd <carpeta>`, `cd ..`, `cd /`), y mover archivos creados en Fase 1/2 dentro de carpetas (`mv <archivo> <carpeta>`).
* Incluye recorrido en **Preorden** para imprimir en consola la jerarquía visual del proyecto al estilo del comando `tree` de Linux.

### 2. Evaluador de Expresiones — Árbol Binario Clásico (`core/expression_tree.py`)
* Analizador léxico y sintáctico desde cero (basado en nuestra `Stack` propia) que convierte expresiones matemáticas infijas como `(5 + 3) * 2` o `(4+8)*3` en un **Árbol Binario de Expresiones** (`ExpressionNode`).
* Los **nodos hoja** almacenan operandos numéricos y los **nodos internos** almacenan operadores (`+`, `-`, `*`, `/`).
* Recorre el árbol en **Postorden** (`Izquierda -> Derecha -> Raíz`) para evaluar matemáticamente la expresión y sirve como un **linter de cálculos en tiempo de escritura** al crear o editar archivos de código.

### 3. Autocompletado y Diccionario Rápido — Árbol AVL (`core/avl_tree.py`)
* **Árbol Binario de Búsqueda Auto-balanceable (AVL)** encapsulado en POO (`AVLNode`, `AVLTree`) con cálculo de altura, factor de equilibrio y rotaciones simples y dobles (**LL, RR, LR, RL**).
* Garantiza tiempos de **búsqueda, inserción (`add-keyword`) y eliminación (`del-keyword`) en $O(\log n)$**.
* Sugiere palabras clave completas al introducir un prefijo (`suggest <prefijo>`), combinando poda por búsqueda binaria y recorrido **Inorden** para mostrar sugerencias en orden alfabético junto con su descripción.

### 4. Índice de Búsqueda Global — Árbol B / B-Tree (`core/b_tree.py`)
* **Árbol B** de orden $m = 4$ (grado mínimo $t = 2$) implementado con páginas de capacidad fija y división de nodos llenos (`_split_child`, `_insert_non_full`).
* Escanea todos los archivos del Workspace (`index-all`) para indexar variables y funciones creadas por el usuario.
* Cada clave (`BTreeEntry`) almacena el token y una lista enlazada (`ReferenceNode`) con los **IDs de los archivos, nombres y líneas exactas** donde aparece para búsquedas globales instantáneas (`find-global <token>`).

### 5. Consola CLI con Patrón de Diseño Comandos (`core/commands.py` y `main.py`)
* Todos los comandos de la Fase 1 y Fase 2 están encapsulados como subclases de `Command` y gestionados por `CommandInvoker`, eliminando por completo los menús numéricos tradicionales.

---

## 💻 Comandos de la Consola Interactiva (CLI)

Ejecuta el entorno con:

```bash
python main.py
```

| Módulo | Comando CLI / Acción | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **Árbol N-ario** | `mkdir <nombre_carpeta>` | Crea un nuevo directorio (o ruta anidada) en el nivel actual del Workspace virtual y físico. | `mkdir src` |
| **Árbol N-ario** | `cd <nombre_carpeta>` | Cambia el directorio de trabajo actual navegando por los hijos del nodo (`cd ..` para subir al padre). | `cd src` / `cd ..` |
| **Árbol N-ario** | `tree` | Imprime la estructura jerárquica completa del proyecto recorriendo el Árbol N-ario en **preorden**. | `tree` |
| **Árbol N-ario** | `mv <archivo> <carpeta>` | Mueve un archivo (creado en Fase 1/2) dentro de las carpetas del Árbol N-ario y en disco. | `mv main.py src` |
| **Árbol Binario** | `eval "<expresion>"` | Parsea una expresión, construye el Árbol Binario de Expresión y devuelve el resultado en **postorden**. | `eval "(4+8)*3"` |
| **Árbol Binario** | `lint-math` | Ejecuta el linter de cálculos matemáticos en tiempo de escritura sobre el archivo activo. | `lint-math` |
| **Árbol AVL** | `add-keyword <palabra> [desc]` | Inserta una nueva palabra clave en el Árbol AVL, balanceando mediante rotaciones si es necesario. | `add-keyword struct` |
| **Árbol AVL** | `del-keyword <palabra>` | Elimina una palabra clave del Árbol AVL en $O(\log n)$ y rebalancea la estructura. | `del-keyword struct` |
| **Árbol AVL** | `suggest <prefijo>` | Busca en el Árbol AVL y retorna alfabéticamente (inorden) las palabras clave que coincidan con el prefijo. | `suggest in` |
| **Árbol AVL** | `avl-info` | Muestra los recorridos **Inorden, Preorden y Postorden** y factores de equilibrio del Árbol AVL. | `avl-info` |
| **Árbol B** | `index-all` | Escanea todos los archivos abiertos y construye/actualiza el Árbol B con los tokens encontrados. | `index-all` |
| **Árbol B** | `find-global <token>` | Busca un token específico en el Árbol B y muestra en qué archivos (ID) y líneas se encuentra. | `find-global contador` |
| **Árbol B** | `btree-info` | Muestra la estructura interna de páginas/niveles del Árbol B y su recorrido inorden. | `btree-info` |
| **Fase 1** | `touch <archivo> [contenido]` | Crea un archivo físico y virtual en el directorio actual y lo añade a la Lista Doblemente Enlazada. | `touch utils.py x = (5+3)*2` |
| **Fase 1** | `ls` / `use <id>` / `cat` | Lista archivos abiertos (`ls`), cambia archivo activo (`use`), o muestra su código numerado (`cat`). | `ls` / `use main.py` |
| **Fase 1** | `edit [nuevo_contenido]` | Edita el archivo activo, registra en la Pila Undo y ejecuta el Linter de Expresiones en vivo. | `edit total = (10+2)*4` |
| **Fase 1** | `syntax` / `undo` / `redo` | Valida paréntesis/llaves con Pila (`syntax`), deshace (`undo`) o rehace (`redo`) cambios. | `syntax` / `undo` |
| **Fase 1** | `sort <name\|id>` / `rm <id>` | Ordena archivos con InsertionSort/QuickSort (`sort`) o elimina un archivo (`rm`). | `sort name` |
| **Sistema** | `help` / `exit` | Muestra la tabla de comandos (`help`) o cierra la consola interactiva (`exit`). | `help` |

---

## 🏗️ Arquitectura del Proyecto

```text
Synthetix-Studio/
├── config/
│   └── config.json            # Configuración de servicios y API Key
├── core/
│   ├── avl_tree.py            # Módulo 3: Árbol AVL auto-balanceable y autocompletado por prefijo
│   ├── b_tree.py              # Módulo 4: Árbol B (Orden m=4) para indexación y búsqueda global
│   ├── commands.py            # Patrón Command (Command, Invoker y comandos CLI de Fase 1 y 2)
│   ├── expression_tree.py     # Módulo 2: Árbol Binario de Expresiones y evaluador en Postorden
│   ├── file_list.py           # Lista Doblemente Enlazada sincronizada con archivos físicos
│   ├── nary_tree.py           # Módulo 1: Árbol N-ario para el Explorador de Workspace y 'tree'
│   ├── request_queue.py       # Cola FIFO para solicitudes a IA
│   ├── sorting.py             # Algoritmos de ordenamiento InsertionSort y QuickSort
│   ├── stack.py               # Pila dinámica desde cero
│   ├── syntax_checker.py      # Validador de sintaxis de delimitadores basado en Pila
│   └── undo_redo.py           # Gestor Undo/Redo con Doble Pila
├── services/
│   └── ai_service.py          # Integración de análisis de código con IA
├── main.py                    # Punto de entrada CLI con Patrón Command
└── readme.md                  # Documentación técnica del proyecto
```

---

## 👥 Autores

* **José Pascia**
* **Alejandra Rivero**
