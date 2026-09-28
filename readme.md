# 🚀 Synthetix Studio — Mini IDE & Code Analysis Tool

**Synthetix Studio** es un Entorno de Desarrollo Minimalista (Mini IDE) interactivo ejecutado desde una consola de línea de comandos (CLI). El proyecto implementa estructuras de datos dinámicas avanzadas creadas estrictamente desde cero, gestión de historial de edición, análisis estático de código mediante verificación de sintaxis, ordenamiento avanzado de diagnósticos e integración simulada con servicios de Inteligencia Artificial para métricas de complejidad algorítmica ($Big\ O$).


## 🛠️ Prerrequisitos de Software

Para compilar y ejecutar este proyecto correctamente en tu sistema operativo, asegúrate de contar con las siguientes herramientas instaladas y configuradas en tus variables de entorno:

1. **Compilador C++**: Soporte para C++17 o superior (`g++` / GCC, Clang o MSVC).
2. **Sistema de Construcción**: `CMake` (versión 3.10+) o `Make`.
3. **Control de Versiones**: `Git`.

---

## 📥 Clonación e Instalación

Sigue estos pasos en la terminal para clonar el proyecto en tu equipo local:

```bash
# 1. Clonar el repositorio desde GitHub
git clone https://github.com/Rurmin/Synthetix-Studio.git

# 2. Navegar al directorio del proyecto
cd Synthetix-Studio
```

---

## ⚙️ Compilación y Ejecución

### PowerShell 

```powershell
# Compilar con g++ en Windows
g++ -std=c++17 -Iinclude src/*.cpp -o synthetix_studio.exe

# Ejecutar la aplicación
.\synthetix_studio.exe
```

---

## 💻 Comandos CLI Disponibles

El proyecto opera exclusivamente mediante una interfaz de línea de comandos (CLI). No utiliza menús interactivos por teclado.

| Módulo | Comando | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **1. Archivos & Configuración** | `new <nombre_archivo>` | Crea un nuevo archivo en memoria asignándole nombre y contenido inicial. | `new main.cpp` |
| | `list` | Muestra la lista de todos los archivos abiertos en la sesión indicando su estado. | `list` |
| | `switch <id/nombre>` | Cambia el archivo activo actual para visualizar o editar su contenido. | `switch main.cpp` |
| | `delete <id/nombre>` | Elimina un archivo de la lista y libera correctamente sus nodos en memoria. | `delete main.cpp` |
| | `config <ruta_archivo>` | Carga el archivo de configuración externo (`config.json`) para leer rutas de respaldos/logs y endpoints. | `config config.json` |
| **2. Validación & Historial** | `check` | Valida el correcto anidamiento y balanceo de símbolos (`()`, `{}`, `[]`) en el código activo e indica línea/columna de error. | `check` |
| | `undo` | Deshace el último cambio realizado sobre el código utilizando la pila de retroceso. | `undo` |
| | `redo` | Rehace el cambio previamente deshecho utilizando la pila de avance. | `redo` |
| **3. Motor de Ordenamiento** | `<criterio> sort <algoritmo>` | Ordena los diagnósticos del código activo usando algoritmos manuales (`mergesort` o `shellsort`) por línea o gravedad. | `line sort mergesort` |
| **4. Buffer de Peticiones** | `queue-status` | Muestra el estado actual de la cola FIFO que administra las solicitudes pendientes hacia la API de IA. | `queue-status` |
| **5. Integración con IA** | `analyze` | Envía el fragmento de código activo mediante una petición HTTP al endpoint configurado para recibir métricas $Big\ O$. | `analyze` |

---

## 🏗️ Arquitectura de Software y Reglas Técnicas

El desarrollo sigue los estándares del diseño orientado a objetos (POO) y el **Patrón de Diseño Comandos (Command Pattern)**:

1. **Cero Dependencias STL para Contenedores**: No se emplean `std::list`, `std::stack`, `std::queue` ni métodos nativos de ordenamiento como `.sort()`.
2. **Estructuras Dinámicas Propias**:
   * **`FileList`**: Lista enlazada doble para administración de archivos abiertos.
   * **`Stack<T>`**: Pila genérica mediante punteros usada para validación de paréntesis y el motor Undo/Redo.
   * **`RequestQueue`**: Cola FIFO propia para buffering de solicitudes de IA.
3. **Algoritmos de Ordenamiento Manuales**: Implementaciones de **Mergesort** y **Shellsort** sobre estructuras dinámicas de diagnósticos.

---

## 👥 Autores 

* **Estudiantes**: José Pascia y Alejandra Rivero
