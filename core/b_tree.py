from core.file_list import FileList


class ReferenceNode:
  """Nodo de lista simplemente enlazada que almacena una referencia de aparición

  de un token (ID de archivo, nombre de archivo, línea y extracto).
  """

  def __init__(
      self,
      file_id: int,
      filename: str,
      line_number: int,
      line_preview: str = "",
  ):
    self._file_id = file_id
    self._filename = filename
    self._line_number = line_number
    self._line_preview = line_preview
    self.next = None

  @property
  def file_id(self) -> int:
    return self._file_id

  @property
  def filename(self) -> str:
    return self._filename

  @property
  def line_number(self) -> int:
    return self._line_number

  @property
  def line_preview(self) -> str:
    return self._line_preview


class BTreeEntry:
  """Representa un par (Clave, Valor) dentro de una página/nodo del Árbol B.

  - key: nombre del token (variable o función).
  - ref_head: cabeza de la lista enlazada de referencias (ID archivo y línea).
  """

  def __init__(self, key: str):
    self._key = key
    self._ref_head = None
    self._ref_tail = None
    self._ref_count = 0

  @property
  def key(self) -> str:
    return self._key

  @property
  def ref_head(self) -> ReferenceNode:
    return self._ref_head

  @property
  def ref_count(self) -> int:
    return self._ref_count

  def add_reference(
      self,
      file_id: int,
      filename: str,
      line_number: int,
      line_preview: str = "",
  ) -> None:
    """Agrega una referencia a la lista enlazada evitando duplicados (mismo archivo y línea)."""
    curr = self._ref_head
    while curr is not None:
      if curr.file_id == file_id and curr.line_number == line_number:
        return
      curr = curr.next

    new_ref = ReferenceNode(file_id, filename, line_number, line_preview)
    if self._ref_head is None:
      self._ref_head = new_ref
      self._ref_tail = new_ref
    else:
      self._ref_tail.next = new_ref
      self._ref_tail = new_ref
    self._ref_count += 1


class BTreeNode:
  """Página / Nodo de un Árbol B implementado desde cero con arreglos de capacidad fija.

  Para grado mínimo t = 2 (Orden m = 2*t = 4):
  - Máximo de claves por nodo: 2*t - 1 = 3
  - Máximo de hijos por nodo: 2*t = 4
  """

  def __init__(self, t: int, is_leaf: bool = True):
    self._t = t
    self._is_leaf = is_leaf
    self._max_keys = 2 * t - 1
    self._entries = [None] * self._max_keys
    self._children = [None] * (2 * t)
    self._num_keys = 0

  @property
  def t(self) -> int:
    return self._t

  @property
  def is_leaf(self) -> bool:
    return self._is_leaf

  @is_leaf.setter
  def is_leaf(self, value: bool) -> None:
    self._is_leaf = value

  @property
  def entries(self):
    return self._entries

  @property
  def children(self):
    return self._children

  @property
  def num_keys(self) -> int:
    return self._num_keys

  @num_keys.setter
  def num_keys(self, value: int) -> None:
    self._num_keys = value

  def is_full(self) -> bool:
    return self._num_keys == self._max_keys


class BTree:
  """Árbol B (B-Tree) desde cero para el Índice de Búsqueda Global (Find in Files).

  Por defecto utiliza grado mínimo t = 2 (Orden m = 4).
  """

  RESERVED_IGNORED = (
      "def",
      "class",
      "return",
      "if",
      "elif",
      "else",
      "while",
      "for",
      "in",
      "import",
      "from",
      "as",
      "pass",
      "break",
      "continue",
      "True",
      "False",
      "None",
      "and",
      "or",
      "not",
      "print",
      "public",
      "private",
      "void",
      "int",
      "float",
      "bool",
      "struct",
  )

  def __init__(self, t: int = 2):
    if t < 2:
      t = 2
    self._t = t
    self._order_m = 2 * t
    self._root = BTreeNode(t, is_leaf=True)
    self._total_tokens = 0

  @property
  def root(self) -> BTreeNode:
    return self._root

  @property
  def order_m(self) -> int:
    return self._order_m

  @property
  def total_tokens(self) -> int:
    return self._total_tokens

  def clear(self) -> None:
    """Reinicia el Árbol B para reconstruir el índice global."""
    self._root = BTreeNode(self._t, is_leaf=True)
    self._total_tokens = 0

  def search(self, token: str) -> BTreeEntry:
    """Busca un token en el Árbol B en tiempo O(log n)."""
    return self._search_recursive(self._root, token.strip())

  def _search_recursive(self, node: BTreeNode, key: str) -> BTreeEntry:
    if node is None:
      return None

    i = 0
    while i < node.num_keys and key > node.entries[i].key:
      i += 1

    if i < node.num_keys and key == node.entries[i].key:
      return node.entries[i]

    if node.is_leaf:
      return None

    return self._search_recursive(node.children[i], key)

  def insert_reference(
      self,
      token: str,
      file_id: int,
      filename: str,
      line_number: int,
      line_preview: str = "",
  ) -> None:
    """Inserta un token y su referencia (archivo, línea) en el Árbol B."""
    clean_token = token.strip()
    if not clean_token:
      return

    # Si el token ya existe en el Árbol B, solo agregar la nueva referencia a su lista enlazada
    existing_entry = self.search(clean_token)
    if existing_entry is not None:
      existing_entry.add_reference(
          file_id, filename, line_number, line_preview
      )
      return

    # Crear nueva entrada para el Árbol B
    new_entry = BTreeEntry(clean_token)
    new_entry.add_reference(file_id, filename, line_number, line_preview)

    root = self._root
    if root.is_full():
      new_root = BTreeNode(self._t, is_leaf=False)
      new_root.children[0] = root
      self._split_child(new_root, 0, root)
      self._root = new_root
      self._insert_non_full(new_root, new_entry)
    else:
      self._insert_non_full(root, new_entry)

    self._total_tokens += 1

  def _split_child(
      self, parent: BTreeNode, index: int, full_child: BTreeNode
  ) -> None:
    """Divide un nodo hijo lleno (2*t - 1 claves) promoviendo su clave mediana al padre."""
    t = self._t
    new_sibling = BTreeNode(t, is_leaf=full_child.is_leaf)
    new_sibling.num_keys = t - 1

    # Copiar las últimas (t - 1) claves de full_child a new_sibling
    for j in range(t - 1):
      new_sibling.entries[j] = full_child.entries[j + t]
      full_child.entries[j + t] = None

    # Si no es hoja, copiar también los últimos t punteros a hijos
    if not full_child.is_leaf:
      for j in range(t):
        new_sibling.children[j] = full_child.children[j + t]
        full_child.children[j + t] = None

    median_entry = full_child.entries[t - 1]
    full_child.entries[t - 1] = None
    full_child.num_keys = t - 1

    # Desplazar los hijos del padre para hacer espacio a new_sibling
    for j in range(parent.num_keys, index, -1):
      parent.children[j + 1] = parent.children[j]
    parent.children[index + 1] = new_sibling

    # Desplazar las claves del padre para insertar la clave mediana
    for j in range(parent.num_keys - 1, index - 1, -1):
      parent.entries[j + 1] = parent.entries[j]
    parent.entries[index] = median_entry
    parent.num_keys += 1

  def _insert_non_full(self, node: BTreeNode, entry: BTreeEntry) -> None:
    """Inserta una nueva entrada en un nodo del Árbol B que se garantiza no está lleno."""
    i = node.num_keys - 1

    if node.is_leaf:
      while i >= 0 and entry.key < node.entries[i].key:
        node.entries[i + 1] = node.entries[i]
        i -= 1
      node.entries[i + 1] = entry
      node.num_keys += 1
    else:
      while i >= 0 and entry.key < node.entries[i].key:
        i -= 1
      i += 1
      if node.children[i].is_full():
        self._split_child(node, i, node.children[i])
        if entry.key > node.entries[i].key:
          i += 1
      self._insert_non_full(node.children[i], entry)

  @staticmethod
  def _is_ident_start(ch: str) -> bool:
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"

  @staticmethod
  def _is_ident_part(ch: str) -> bool:
    return (
        ("a" <= ch <= "z")
        or ("A" <= ch <= "Z")
        or ("0" <= ch <= "9")
        or ch == "_"
    )

  def _is_reserved(self, word: str) -> bool:
    for kw in self.RESERVED_IGNORED:
      if kw == word:
        return True
    return False

  def _extract_and_index_line(
      self, line: str, file_id: int, filename: str, line_number: int
  ) -> int:
    """Escanea carácter por carácter una línea de código extrayendo tokens de usuario

    (variables, funciones, parámetros y sus usos) sin usar expresiones regulares.
    """
    n = len(line)
    i = 0
    in_string = False
    quote_char = ""
    indexed_in_line = 0
    preview = line.strip()

    while i < n:
      ch = line[i]

      # Ignorar comentarios a partir de '#'
      if not in_string and ch == "#":
        break

      # Ignorar cadenas de texto literales '...' o "..."
      if ch in ('"', "'"):
        if not in_string:
          in_string = True
          quote_char = ch
        elif quote_char == ch:
          in_string = False
        i += 1
        continue

      if in_string:
        i += 1
        continue

      if self._is_ident_start(ch):
        token = ""
        while i < n and self._is_ident_part(line[i]):
          token += line[i]
          i += 1
        if not self._is_reserved(token):
          self.insert_reference(
              token, file_id, filename, line_number, preview
          )
          indexed_in_line += 1
      else:
        i += 1

    return indexed_in_line

  def index_all_files(self, file_list: FileList) -> None:
    """Escanea todos los archivos abiertos del Workspace y construye/actualiza el Árbol B."""
    self.clear()

    if file_list.head is None:
      print("[Árbol B] No hay archivos abiertos en el Workspace para indexar.")
      return

    files_scanned = 0
    occurrences_indexed = 0
    curr_file = file_list.head

    while curr_file is not None:
      curr_file.load_from_disk()
      files_scanned += 1
      lines = curr_file.content.splitlines()
      for line_num, line_text in enumerate(lines, start=1):
        occurrences_indexed += self._extract_and_index_line(
            line_text, curr_file.id, curr_file.filename, line_num
        )
      curr_file = curr_file.next

    print(
        f"[Éxito Árbol B (Orden m={self._order_m})] Indexación global"
        f" completada: {self._total_tokens} token(s) único(s) y"
        f" {occurrences_indexed} referencia(s) en {files_scanned} archivo(s)."
    )

  def find_global(self, token: str) -> None:
    """Busca un token en el Árbol B y muestra todos los archivos (ID y nombre) y líneas donde aparece."""
    clean_token = token.strip()
    if not clean_token:
      print("[Error] Debes especificar el token a buscar (ej. find-global contador).")
      return

    entry = self.search(clean_token)
    if entry is None:
      print(
          f"[Búsqueda Global Árbol B] El token '{clean_token}' no se encontró"
          " en el índice. (Ejecuta 'index-all' si modificaste archivos"
          " recientemente)."
      )
      return

    print(
        f"\n=== RESULTADOS EN ÁRBOL B PARA TOKEN: '{clean_token}'"
        f" ({entry.ref_count} coincidencia(s)) ==="
    )
    ref = entry.ref_head
    idx = 1
    while ref is not None:
      print(
          f"  {idx}. Archivo ID: {ref.file_id} ({ref.filename}) | Línea"
          f" {ref.line_number}:  {ref.line_preview}"
      )
      ref = ref.next
      idx += 1
    print(
        "===================================================================================\n"
    )

  def print_btree_structure(self) -> None:
    """Imprime la estructura jerárquica de páginas del Árbol B y su recorrido inorden."""
    print(
        f"\n=== ESTRUCTURA DEL ÁRBOL B (Orden m={self._order_m}, Grado mínimo"
        f" t={self._t}, Tokens={self._total_tokens}) ==="
    )
    if self._root.num_keys == 0:
      print("  (Árbol B vacío. Ejecuta 'index-all' para indexar el Workspace)")
    else:
      self._print_node_recursive(self._root, level=0)
      print(f"\n  • Recorrido Inorden: {self._inorder_keys(self._root).strip()}")
    print(
        "=====================================================================================\n"
    )

  def _print_node_recursive(self, node: BTreeNode, level: int) -> None:
    if node is None:
      return
    indent = "  " * (level + 1)
    keys_str = ""
    for i in range(node.num_keys):
      if i > 0:
        keys_str += " | "
      entry = node.entries[i]
      keys_str += f"{entry.key}({entry.ref_count} refs)"
    tipo = "Hoja" if node.is_leaf else "Interno"
    print(f"{indent}[Nivel {level} - {tipo}]: [ {keys_str} ]")
    if not node.is_leaf:
      for i in range(node.num_keys + 1):
        self._print_node_recursive(node.children[i], level + 1)

  def _inorder_keys(self, node: BTreeNode) -> str:
    if node is None:
      return ""
    res = ""
    for i in range(node.num_keys):
      if not node.is_leaf:
        res += self._inorder_keys(node.children[i])
      res += f"{node.entries[i].key} "
    if not node.is_leaf:
      res += self._inorder_keys(node.children[node.num_keys])
    return res
