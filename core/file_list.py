class FileNode:

  def __init__(self, file_id: int, filename: str, initial_content: str = ""):
    self.id = file_id
    self.filename = filename
    self.content = initial_content
    self.is_active = False
    self.prev = None
    self.next = None


class FileList:

  def __init__(self):
    self.head = None
    self.tail = None
    self.active_file = None
    self.next_id = 1

  def create_file(self, filename: str, initial_content: str = "") -> bool:
    temp = self.head
    while temp is not None:
      if temp.filename == filename:
        print(f"[Error] El archivo '{filename}' ya existe.")
        return False
      temp = temp.next

    new_node = FileNode(self.next_id, filename, initial_content)
    self.next_id += 1

    if self.head is None:
      self.head = new_node
      self.tail = new_node
    else:
      self.tail.next = new_node
      new_node.prev = self.tail
      self.tail = new_node

    if self.active_file is None:
      new_node.is_active = True
      self.active_file = new_node

    print(f"[Éxito] Archivo '{filename}' creado correctamente.")
    return True

  def list_files(self) -> None:
    if self.head is None:
      print("[Info] No hay archivos abiertos en la sesión.")
      return

    print("\n=== ARCHIVOS ABIERTOS ===")
    current = self.head
    while current is not None:
      estado = "[ACTIVO]" if current.is_active else "Inactivo"
      print(f"ID: {current.id} | Nombre: {current.filename} | Estado: {estado}")
      current = current.next
    print("=========================\n")

  def switch_active_file(self, identifier: str) -> bool:
    current = self.head
    found_node = None

    while current is not None:
      if str(current.id) == identifier or current.filename == identifier:
        found_node = current
        break
      current = current.next

    if found_node is None:
      print(f"[Error] No se encontró el archivo: {identifier}")
      return False

    if self.active_file is not None:
      self.active_file.is_active = False

    found_node.is_active = True
    self.active_file = found_node
    print(f"[Éxito] Cambiado a archivo activo: {self.active_file.filename}")
    return True

  def delete_file(self, identifier: str) -> bool:
    current = self.head

    while current is not None:
      if str(current.id) == identifier or current.filename == identifier:
        if current.prev is not None:
          current.prev.next = current.next
        else:
          self.head = current.next

        if current.next is not None:
          current.next.prev = current.prev
        else:
          self.tail = current.prev

        if current == self.active_file:
          self.active_file = self.head if self.head is not None else None
          if self.active_file is not None:
            self.active_file.is_active = True

        print(
            f"[Éxito] Archivo '{current.filename}' eliminado y memoria"
            " liberada."
        )
        return True

      current = current.next

    print(f"[Error] No se encontró el archivo para eliminar: {identifier}")
    return False

  def get_active_file(self) -> FileNode:
    return self.active_file