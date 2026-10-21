import os


class FileNode:
  """Nodo de la Lista Doblemente Enlazada que representa un archivo de código."""

  def __init__(
      self,
      file_id: int,
      filename: str,
      initial_content: str = "",
      physical_path: str = "",
  ):
    self._id = file_id
    self._filename = filename
    self._content = initial_content
    self._physical_path = physical_path
    self._is_active = False
    self.prev = None
    self.next = None

  @property
  def id(self) -> int:
    return self._id

  @property
  def filename(self) -> str:
    return self._filename

  @filename.setter
  def filename(self, value: str) -> None:
    self._filename = value

  @property
  def content(self) -> str:
    return self._content

  @content.setter
  def content(self, value: str) -> None:
    self._content = value
    self.save_to_disk()

  @property
  def physical_path(self) -> str:
    return self._physical_path

  @physical_path.setter
  def physical_path(self, value: str) -> None:
    self._physical_path = value

  @property
  def is_active(self) -> bool:
    return self._is_active

  @is_active.setter
  def is_active(self, value: bool) -> None:
    self._is_active = value

  def save_to_disk(self) -> None:
    """Sincroniza el contenido del nodo con el archivo físico en disco."""
    if not self._physical_path:
      return
    try:
      parent_dir = os.path.dirname(self._physical_path)
      if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
      with open(self._physical_path, "w", encoding="utf-8") as f:
        f.write(self._content)
    except OSError as e:
      print(f"[Error Disco] No se pudo guardar '{self._physical_path}': {e}")

  def load_from_disk(self) -> None:
    """Carga el contenido desde el archivo físico en disco si existe."""
    if self._physical_path and os.path.isfile(self._physical_path):
      try:
        with open(self._physical_path, "r", encoding="utf-8") as f:
          self._content = f.read()
      except OSError as e:
        print(f"[Error Disco] No se pudo leer '{self._physical_path}': {e}")


class FileList:
  """Lista Doblemente Enlazada desde cero para gestionar archivos abiertos y físicos."""

  def __init__(self, base_workspace_dir: str = "workspace"):
    self.head = None
    self.tail = None
    self.active_file = None
    self.next_id = 1
    self.base_workspace_dir = base_workspace_dir
    if not os.path.exists(self.base_workspace_dir):
      os.makedirs(self.base_workspace_dir, exist_ok=True)

  def find_file(self, identifier: str) -> FileNode:
    """Busca un archivo en la lista doblemente enlazada por ID o por nombre."""
    current = self.head
    while current is not None:
      if str(current.id) == str(identifier) or current.filename == identifier:
        return current
      current = current.next
    return None

  def create_file(
      self,
      filename: str,
      initial_content: str = "",
      physical_dir: str = None,
      silent: bool = False,
  ) -> FileNode:
    """Crea un nodo de archivo en memoria y su archivo físico correspondiente."""
    temp = self.head
    while temp is not None:
      if temp.filename == filename:
        if not silent:
          print(f"[Error] El archivo '{filename}' ya existe en el Workspace.")
        return None
      temp = temp.next

    target_dir = physical_dir if physical_dir else self.base_workspace_dir
    if not os.path.exists(target_dir):
      os.makedirs(target_dir, exist_ok=True)
    physical_path = os.path.join(target_dir, filename)

    # Si el archivo físico ya existe y no se pasó contenido inicial, leerlo de disco
    if os.path.isfile(physical_path) and initial_content == "":
      try:
        with open(physical_path, "r", encoding="utf-8") as f:
          initial_content = f.read()
      except OSError:
        pass

    new_node = FileNode(self.next_id, filename, initial_content, physical_path)
    new_node.save_to_disk()
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

    if not silent:
      print(
          f"[Éxito] Archivo físico y virtual '{filename}' (ID: {new_node.id})"
          f" creado en '{physical_path}'."
      )
    return new_node

  def list_files(self) -> None:
    if self.head is None:
      print("[Info] No hay archivos abiertos en la sesión.")
      return

    print("\n=== ARCHIVOS ABIERTOS EN MEMORIA Y DISCO ===")
    current = self.head
    while current is not None:
      estado = "[ACTIVO]" if current.is_active else "Inactivo"
      print(
          f"ID: {current.id} | Nombre: {current.filename} | Ruta:"
          f" {current.physical_path} | Estado: {estado}"
      )
      current = current.next
    print("============================================\n")

  def switch_active_file(self, identifier: str) -> bool:
    found_node = self.find_file(identifier)

    if found_node is None:
      print(f"[Error] No se encontró el archivo: {identifier}")
      return False

    if self.active_file is not None:
      self.active_file.is_active = False

    found_node.load_from_disk()
    found_node.is_active = True
    self.active_file = found_node
    print(f"[Éxito] Cambiado a archivo activo: {self.active_file.filename}")
    return True

  def delete_file(self, identifier: str) -> FileNode:
    current = self.head

    while current is not None:
      if str(current.id) == str(identifier) or current.filename == identifier:
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

        if current.physical_path and os.path.isfile(current.physical_path):
          try:
            os.remove(current.physical_path)
          except OSError:
            pass

        print(
            f"[Éxito] Archivo '{current.filename}' eliminado de memoria y"
            " disco."
        )
        return current

      current = current.next

    print(f"[Error] No se encontró el archivo para eliminar: {identifier}")
    return None

  def get_active_file(self) -> FileNode:
    return self.active_file
