import sys
from core.file_list import FileList
from core.request_queue import RequestQueue
from core.sorting import SortingEngine
from core.syntax_checker import SyntaxChecker
from core.undo_redo import UndoRedoManager
from services.ai_service import AIService


def print_menu():
  print("\n========================================")
  print("         SYNTHETIX STUDIO CLI           ")
  print("========================================")
  print("1. Crear nuevo archivo")
  print("2. Listar archivos abiertos")
  print("3. Cambiar de archivo activo")
  print("4. Editar contenido de archivo activo")
  print("5. Validar sintaxis (Syntax Checker)")
  print("6. Deshacer cambio (Undo)")
  print("7. Rehacer cambio (Redo)")
  print("8. Encolar solicitud a IA")
  print("9. Procesar siguiente solicitud en cola")
  print("10. Ordenar y ver lista de archivos")
  print("11. Eliminar archivo activo")
  print("0. Salir")
  print("========================================")


def main():
  file_list = FileList()
  undo_redo_manager = UndoRedoManager()
  request_queue = RequestQueue()
  ai_service = AIService()

  print("¡Bienvenido a Synthetix Studio (Python CLI)!")

  # Archivo inicial de demostración
  file_list.create_file("main.py", "def main():\n    print('Hola Mundo')\n")

  while True:
    print_menu()
    option = input("Selecciona una opción: ").strip()

    if option == "1":
      name = input("Nombre del archivo (ej. test.py): ").strip()
      content = input("Contenido inicial (opcional): ")
      file_list.create_file(name, content)

    elif option == "2":
      file_list.list_files()

    elif option == "3":
      ident = input("Ingresa ID o nombre del archivo: ").strip()
      if file_list.switch_active_file(ident):
        undo_redo_manager.clear()

    elif option == "4":
      active = file_list.get_active_file()
      if active:
        print(f"\n--- Contenido actual de {active.filename} ---")
        print(active.content)
        print("------------------------------------------")
        new_text = input("Ingresa el nuevo contenido: ")
        undo_redo_manager.record_state(active.content)
        active.content = new_text
        print("[Éxito] Contenido actualizado.")
      else:
        print("[Error] No hay un archivo activo seleccionado.")

    elif option == "5":
      active = file_list.get_active_file()
      if active:
        print(f"\nValidando sintaxis de {active.filename}...")
        SyntaxChecker.check_syntax(active.content)
      else:
        print("[Error] No hay un archivo activo seleccionado.")

    elif option == "6":
      active = file_list.get_active_file()
      if active:
        active.content = undo_redo_manager.undo(active.content)
      else:
        print("[Error] No hay un archivo activo seleccionado.")

    elif option == "7":
      active = file_list.get_active_file()
      if active:
        active.content = undo_redo_manager.redo(active.content)
      else:
        print("[Error] No hay un archivo activo seleccionado.")

    elif option == "8":
      cmd = input(
          "Ingresa comando para la IA (explicar/optimizar/refactorizar): "
      ).strip()
      active = file_list.get_active_file()
      payload = active.content if active else ""
      request_queue.enqueue(cmd, payload)

    elif option == "9":
      req = request_queue.dequeue()
      if req:
        res = ai_service.process_request(req.command, req.payload)
        print(f"\n{res}\n")

    elif option == "10":
      if file_list.head is None:
        print("[Info] No hay archivos para ordenar.")
        continue

      files_meta = []
      curr = file_list.head
      while curr:
        files_meta.append({"id": curr.id, "filename": curr.filename})
        curr = curr.next

      print("\n¿Cómo deseas ordenar los archivos?")
      print("1. Por Nombre (InsertionSort)")
      print("2. Por ID (QuickSort)")
      sub_opt = input("Opción: ").strip()

      if sub_opt == "1":
        sorted_res = SortingEngine.insertion_sort_by_filename(files_meta)
        print("\n--- Archivos ordenados por Nombre (A-Z) ---")
        for item in sorted_res:
          print(f"ID: {item['id']} | Nombre: {item['filename']}")
      elif sub_opt == "2":
        sorted_res = SortingEngine.quick_sort_by_id(files_meta)
        print("\n--- Archivos ordenados por ID (Ascendente) ---")
        for item in sorted_res:
          print(f"ID: {item['id']} | Nombre: {item['filename']}")
      else:
        print("[Error] Opción no válida.")

    elif option == "11":
      ident = input("Ingresa ID o nombre del archivo a eliminar: ").strip()
      if file_list.delete_file(ident):
        undo_redo_manager.clear()

    elif option == "0":
      print("Saliendo de Synthetix Studio... ¡Hasta luego!")
      sys.exit(0)

    else:
      print("[Error] Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
  main()