import os
import shutil
from core.file_list import FileNode


class NaryNode:
  """Nodo de un Árbol N-ario implementado desde cero mediante punteros

  Hijo-Izquierdo / Hermano-Derecho (Left-Child, Right-Sibling) y puntero al
  Padre.
  Cada nodo representa una carpeta (is_dir=True) o un archivo de código
  (is_dir=False).
  """

  def __init__(
      self,
      name: str,
      is_dir: bool = True,
      parent=None,
      file_ref: FileNode = None,
  ):
    self._name = name
    self._is_dir = is_dir
    self._parent = parent
    self._first_child = None
    self._next_sibling = None
    self._file_ref = file_ref

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, value: str) -> None:
    self._name = value

  @property
  def is_dir(self) -> bool:
    return self._is_dir

  @property
  def parent(self):
    return self._parent

  @parent.setter
  def parent(self, node) -> None:
    self._parent = node

  @property
  def first_child(self):
    return self._first_child

  @first_child.setter
  def first_child(self, node) -> None:
    self._first_child = node

  @property
  def next_sibling(self):
    return self._next_sibling

  @next_sibling.setter
  def next_sibling(self, node) -> None:
    self._next_sibling = node

  @property
  def file_ref(self) -> FileNode:
    return self._file_ref

  @file_ref.setter
  def file_ref(self, ref: FileNode) -> None:
    self._file_ref = ref

  def find_child(self, child_name: str):
    """Busca un hijo directo por su nombre recorriendo la lista enlazada de hijos."""
    current = self._first_child
    while current is not None:
      if current.name == child_name:
        return current
      current = current.next_sibling
    return None

  def add_child(self, new_child) -> bool:
    """Agrega un nodo hijo al final de la lista de hijos sin usar estructuras nativas."""
    if not self._is_dir:
      return False
    if self.find_child(new_child.name) is not None:
      return False

    new_child.parent = self
    new_child.next_sibling = None

    if self._first_child is None:
      self._first_child = new_child
    else:
      current = self._first_child
      while current.next_sibling is not None:
        current = current.next_sibling
      current.next_sibling = new_child
    return True

  def detach_child(self, child_name: str):
    """Desvincula y retorna un nodo hijo directo ajustando los punteros."""
    current = self._first_child
    prev = None
    while current is not None:
      if current.name == child_name:
        if prev is None:
          self._first_child = current.next_sibling
        else:
          prev.next_sibling = current.next_sibling
        current.next_sibling = None
        current.parent = None
        return current
      prev = current
      current = current.next_sibling
    return None


class WorkspaceTree:
  """Árbol N-ario para representar el sistema de archivos virtual y físico (Workspace)."""

  def __init__(self, root_name: str = "workspace"):
    self._root_physical_dir = os.path.abspath(root_name)
    if not os.path.exists(self._root_physical_dir):
      os.makedirs(self._root_physical_dir, exist_ok=True)
    self._root = NaryNode(root_name, is_dir=True, parent=None)
    self._current_dir = self._root

  @property
  def root(self) -> NaryNode:
    return self._root

  @property
  def current_dir(self) -> NaryNode:
    return self._current_dir

  def get_virtual_path(self, node: NaryNode = None) -> str:
    """Construye la ruta virtual desde la raíz hasta el nodo indicado sin listas nativas."""
    target = node if node is not None else self._current_dir
    if target == self._root:
      return f"/{self._root.name}"

    path_str = ""
    curr = target
    while curr is not None:
      path_str = "/" + curr.name + path_str
      curr = curr.parent
    return path_str

  def get_physical_path(self, node: NaryNode = None) -> str:
    """Retorna la ruta física en el sistema operativo para un nodo del árbol N-ario."""
    target = node if node is not None else self._current_dir
    if target == self._root:
      return self._root_physical_dir

    rel_parts = ""
    curr = target
    while curr is not None and curr != self._root:
      if rel_parts == "":
        rel_parts = curr.name
      else:
        rel_parts = os.path.join(curr.name, rel_parts)
      curr = curr.parent
    return os.path.join(self._root_physical_dir, rel_parts)

  def _split_path(self, raw_path: str):
    """Generador simple que separa una ruta por '/' o '\\' carácter a carácter."""
    token = ""
    for ch in raw_path:
      if ch == "/" or ch == "\\":
        if token != "":
          yield token
          token = ""
      else:
        token += ch
    if token != "":
      yield token

  def resolve_dir_node(self, path: str) -> NaryNode:
    """Resuelve una ruta (relativa o absoluta) hacia un nodo carpeta en el Árbol N-ario."""
    cleaned = path.strip()
    if cleaned == "" or cleaned == ".":
      return self._current_dir
    if cleaned == "/" or cleaned == f"/{self._root.name}":
      return self._root

    curr = self._root if cleaned.startswith("/") else self._current_dir
    for part in self._split_path(cleaned):
      if part == ".":
        continue
      elif part == "..":
        if curr.parent is not None:
          curr = curr.parent
      elif curr == self._root and part == self._root.name:
        continue
      else:
        child = curr.find_child(part)
        if child is None or not child.is_dir:
          return None
        curr = child
    return curr

  def mkdir(self, folder_path: str) -> bool:
    """Crea un nuevo directorio (o directorios anidados) en el nivel actual del Workspace."""
    cleaned = folder_path.strip()
    if not cleaned:
      print("[Error] Debes especificar un nombre de carpeta para 'mkdir'.")
      return False

    curr = self._root if cleaned.startswith("/") else self._current_dir
    created_any = False

    for part in self._split_path(cleaned):
      if part in (".", ".."):
        print(f"[Error] Nombre de carpeta inválido: '{part}'.")
        return False

      existing = curr.find_child(part)
      if existing is not None:
        if not existing.is_dir:
          print(
              f"[Error] Ya existe un archivo llamado '{part}' en este"
              " directorio."
          )
          return False
        curr = existing
      else:
        new_folder = NaryNode(part, is_dir=True, parent=curr)
        curr.add_child(new_folder)
        curr = new_folder
        created_any = True
        phys_dir = self.get_physical_path(curr)
        os.makedirs(phys_dir, exist_ok=True)

    if not created_any:
      print(f"[Error] El directorio '{folder_path}' ya existe.")
      return False

    print(f"[Éxito] Directorio '{self.get_virtual_path(curr)}' creado.")
    return True

  def cd(self, target_path: str) -> bool:
    """Cambia el directorio de trabajo actual navegando por el árbol N-ario."""
    cleaned = target_path.strip()
    if not cleaned:
      print("[Error] Especifica el directorio destino (ej. cd src o cd ..).")
      return False

    target_node = self.resolve_dir_node(cleaned)
    if target_node is None:
      print(f"[Error] No existe el directorio '{cleaned}'.")
      return False

    self._current_dir = target_node
    print(f"[Workspace] Directorio actual: {self.get_virtual_path()}")
    return True

  def attach_file(
      self,
      file_node: FileNode,
      target_dir: NaryNode = None,
      silent: bool = False,
  ) -> NaryNode:
    """Inserta un nodo hoja de archivo en el directorio indicado del Árbol N-ario."""
    dest_dir = target_dir if target_dir is not None else self._current_dir
    existing = dest_dir.find_child(file_node.filename)
    if existing is not None:
      if not silent:
        print(
            f"[Error] Ya existe un nodo '{file_node.filename}' en"
            f" {self.get_virtual_path(dest_dir)}."
        )
      return existing

    nary_file = NaryNode(
        file_node.filename,
        is_dir=False,
        parent=dest_dir,
        file_ref=file_node,
    )
    dest_dir.add_child(nary_file)
    phys_path = os.path.join(
        self.get_physical_path(dest_dir), file_node.filename
    )
    file_node.physical_path = phys_path
    file_node.save_to_disk()
    return nary_file

  def _find_node_recursive(
      self, current: NaryNode, name: str, only_files: bool = False
  ) -> NaryNode:
    """Búsqueda en preorden de un nodo por nombre dentro del Árbol N-ario."""
    if current is None:
      return None
    if current != self._root:
      if current.name == name and (not only_files or not current.is_dir):
        return current
    child = current.first_child
    while child is not None:
      found = self._find_node_recursive(child, name, only_files)
      if found is not None:
        return found
      child = child.next_sibling
    return None

  def move_file(self, filename: str, dest_folder_path: str) -> bool:
    """Mueve un archivo (creado en Fase 1/2) hacia otra carpeta del Árbol N-ario y en disco."""
    # Buscar primero en el directorio actual, y si no, en todo el árbol N-ario
    file_nary = self._current_dir.find_child(filename)
    if file_nary is None or file_nary.is_dir:
      file_nary = self._find_node_recursive(
          self._root, filename, only_files=True
      )

    if file_nary is None or file_nary.is_dir:
      print(f"[Error] No se encontró el archivo '{filename}' en el Workspace.")
      return False

    dest_dir = self.resolve_dir_node(dest_folder_path)
    if dest_dir is None:
      print(f"[Error] La carpeta destino '{dest_folder_path}' no existe.")
      return False

    if dest_dir.find_child(filename) is not None:
      print(
          f"[Error] Ya existe '{filename}' dentro de"
          f" '{self.get_virtual_path(dest_dir)}'."
      )
      return False

    old_parent = file_nary.parent
    old_phys_path = (
        file_nary.file_ref.physical_path if file_nary.file_ref else None
    )

    # Desvincular del padre actual y vincular al nuevo directorio en el Árbol N-ario
    old_parent.detach_child(filename)
    dest_dir.add_child(file_nary)

    # Actualizar ubicación física del archivo en el disco
    new_phys_dir = self.get_physical_path(dest_dir)
    os.makedirs(new_phys_dir, exist_ok=True)
    new_phys_path = os.path.join(new_phys_dir, filename)

    if file_nary.file_ref is not None:
      if old_phys_path and os.path.isfile(old_phys_path):
        try:
          shutil.move(old_phys_path, new_phys_path)
        except OSError:
          pass
      file_nary.file_ref.physical_path = new_phys_path
      file_nary.file_ref.save_to_disk()

    print(
        f"[Éxito] Archivo '{filename}' movido a"
        f" '{self.get_virtual_path(dest_dir)}'."
    )
    return True

  def remove_file_node(self, filename: str) -> bool:
    """Elimina el nodo correspondiente a un archivo del Árbol N-ario."""
    target = self._find_node_recursive(self._root, filename, only_files=True)
    if target is not None and target.parent is not None:
      target.parent.detach_child(filename)
      return True
    return False

  def print_tree(self) -> None:
    """Recorrido en PREORDEN para imprimir en consola la jerarquía visual del proyecto

    al estilo del comando 'tree' de Linux.
    """
    print(f"\n{self._root.name}/")
    counts = {"dirs": 0, "files": 0}
    self._preorder_print(self._root.first_child, "", counts)
    print(f"\n{counts['dirs']} directorio(s), {counts['files']} archivo(s)\n")

  def _preorder_print(
      self, node: NaryNode, prefix: str, counts: dict
  ) -> None:
    """Algoritmo recursivo en Preorden (Raíz -> Hijos) que formatea las ramas visuales."""
    current = node
    while current is not None:
      is_last = current.next_sibling is None
      connector = "└── " if is_last else "├── "

      if current.is_dir:
        counts["dirs"] += 1
        active_marker = "  <-- [cwd]" if current == self._current_dir else ""
        print(f"{prefix}{connector}{current.name}/{active_marker}")
        child_prefix = prefix + ("    " if is_last else "│   ")
        # Visita recursiva en preorden a los hijos del directorio
        self._preorder_print(current.first_child, child_prefix, counts)
      else:
        counts["files"] += 1
        file_info = ""
        if current.file_ref is not None:
          active_str = " [ACTIVO]" if current.file_ref.is_active else ""
          file_info = f" (ID: {current.file_ref.id}){active_str}"
        print(f"{prefix}{connector}{current.name}{file_info}")

      current = current.next_sibling
