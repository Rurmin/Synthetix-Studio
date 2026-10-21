class AVLNode:
  """Nodo de un Árbol AVL (Árbol Binario de Búsqueda Auto-balanceable).

  Almacena una palabra clave (keyword), su breve descripción, referencias a
  hijos izquierdo y derecho, y su altura para el cálculo del factor de
  equilibrio.
  """

  def __init__(self, keyword: str, description: str = "Palabra clave del lenguaje"):
    self._keyword = keyword
    self._description = description
    self._left = None
    self._right = None
    self._height = 1

  @property
  def keyword(self) -> str:
    return self._keyword

  @keyword.setter
  def keyword(self, value: str) -> None:
    self._keyword = value

  @property
  def description(self) -> str:
    return self._description

  @description.setter
  def description(self, value: str) -> None:
    self._description = value

  @property
  def left(self):
    return self._left

  @left.setter
  def left(self, node) -> None:
    self._left = node

  @property
  def right(self):
    return self._right

  @right.setter
  def right(self, node) -> None:
    self._right = node

  @property
  def height(self) -> int:
    return self._height

  @height.setter
  def height(self, value: int) -> None:
    self._height = value


class SuggestionNode:
  """Nodo de lista enlazada simple para retornar sugerencias sin usar listas nativas."""

  def __init__(self, keyword: str, description: str):
    self.keyword = keyword
    self.description = description
    self.next = None


class AVLTree:
  """Árbol AVL implementado estrictamente desde cero en POO.

  Garantiza tiempos de búsqueda, inserción y eliminación en O(log n).
  """

  def __init__(self, preload_defaults: bool = True):
    self._root = None
    self._size = 0
    if preload_defaults:
      self._load_default_keywords()

  @property
  def root(self) -> AVLNode:
    return self._root

  @property
  def size(self) -> int:
    return self._size

  def _load_default_keywords(self) -> None:
    """Inicializa el diccionario rápido con palabras clave base del lenguaje."""
    defaults = (
        ("class", "Define una estructura de clase orientada a objetos."),
        ("public", "Modificador de acceso público para miembros y métodos."),
        ("private", "Modificador de acceso privado encapsulado en la clase."),
        ("void", "Indica que una función o método no retorna ningún valor."),
        ("int", "Tipo de dato primitivo para números enteros."),
        ("in", "Operador de pertenencia o iteración en secuencias."),
        ("import", "Importa un módulo o paquete externo al archivo actual."),
        ("interface", "Define un contrato abstracto de métodos."),
        ("if", "Estructura condicional de control de flujo."),
        ("else", "Rama alternativa de una estructura condicional."),
        ("return", "Finaliza la ejecución de una función devolviendo un valor."),
        ("while", "Ciclo condicional que se repite mientras la condición sea verdadera."),
        ("for", "Ciclo iterativo sobre un rango o colección de elementos."),
        ("def", "Define una función o método en Python."),
        ("float", "Tipo de dato numérico de coma flotante (decimales)."),
    )
    for kw, desc in defaults:
      self.insert(kw, desc, silent=True)

  def _get_height(self, node: AVLNode) -> int:
    if node is None:
      return 0
    return node.height

  def _max_int(self, a: int, b: int) -> int:
    return a if a > b else b

  def _update_height(self, node: AVLNode) -> None:
    if node is not None:
      node.height = 1 + self._max_int(
          self._get_height(node.left), self._get_height(node.right)
      )

  def _get_balance(self, node: AVLNode) -> int:
    """Factor de equilibrio = Altura( Subárbol Izquierdo ) - Altura( Subárbol Derecho )."""
    if node is None:
      return 0
    return self._get_height(node.left) - self._get_height(node.right)

  def _rotate_right(self, y: AVLNode) -> AVLNode:
    """Rotación Simple a la Derecha (Caso Izquierda-Izquierda)."""
    x = y.left
    t2 = x.right

    # Realizar rotación de punteros
    x.right = y
    y.left = t2

    # Actualizar alturas de los nodos modificados
    self._update_height(y)
    self._update_height(x)

    return x

  def _rotate_left(self, x: AVLNode) -> AVLNode:
    """Rotación Simple a la Izquierda (Caso Derecha-Derecha)."""
    y = x.right
    t2 = y.left

    # Realizar rotación de punteros
    y.left = x
    x.right = t2

    # Actualizar alturas de los nodos modificados
    self._update_height(x)
    self._update_height(y)

    return y

  def _rebalance(self, node: AVLNode) -> AVLNode:
    """Evalúa el factor de equilibrio del nodo y aplica las rotaciones AVL necesarias."""
    self._update_height(node)
    balance = self._get_balance(node)

    # Caso 1: Izquierda - Izquierda (LL)
    if balance > 1 and self._get_balance(node.left) >= 0:
      return self._rotate_right(node)

    # Caso 2: Izquierda - Derecha (LR)
    if balance > 1 and self._get_balance(node.left) < 0:
      node.left = self._rotate_left(node.left)
      return self._rotate_right(node)

    # Caso 3: Derecha - Derecha (RR)
    if balance < -1 and self._get_balance(node.right) <= 0:
      return self._rotate_left(node)

    # Caso 4: Derecha - Izquierda (RL)
    if balance < -1 and self._get_balance(node.right) > 0:
      node.right = self._rotate_right(node.right)
      return self._rotate_left(node)

    return node

  def insert(
      self,
      keyword: str,
      description: str = "Palabra clave definida por el usuario.",
      silent: bool = False,
  ) -> bool:
    """Inserta una palabra clave en O(log n) aplicando rotaciones AVL si se desbalancea."""
    clean_kw = keyword.strip()
    if not clean_kw:
      if not silent:
        print("[Error] La palabra clave no puede estar vacía.")
      return False

    existed = [False]
    self._root = self._insert_recursive(
        self._root, clean_kw, description.strip(), existed
    )

    if existed[0]:
      if not silent:
        print(
            f"[AVL] La palabra clave '{clean_kw}' ya existía; se actualizó su"
            " descripción."
        )
      return True

    self._size += 1
    if not silent:
      print(
          f"[Éxito AVL] Palabra clave '{clean_kw}' insertada y árbol"
          f" balanceado (Altura raíz: {self._get_height(self._root)})."
      )
    return True

  def _insert_recursive(
      self, node: AVLNode, keyword: str, description: str, existed: list
  ) -> AVLNode:
    if node is None:
      return AVLNode(keyword, description)

    if keyword < node.keyword:
      node.left = self._insert_recursive(
          node.left, keyword, description, existed
      )
    elif keyword > node.keyword:
      node.right = self._insert_recursive(
          node.right, keyword, description, existed
      )
    else:
      node.description = description
      existed[0] = True
      return node

    return self._rebalance(node)

  def search(self, keyword: str) -> AVLNode:
    """Búsqueda binaria en el Árbol AVL con complejidad O(log n)."""
    return self._search_recursive(self._root, keyword.strip())

  def _search_recursive(self, node: AVLNode, keyword: str) -> AVLNode:
    if node is None or node.keyword == keyword:
      return node
    if keyword < node.keyword:
      return self._search_recursive(node.left, keyword)
    return self._search_recursive(node.right, keyword)

  def _get_min_value_node(self, node: AVLNode) -> AVLNode:
    current = node
    while current.left is not None:
      current = current.left
    return current

  def delete(self, keyword: str) -> bool:
    """Elimina una palabra clave del Árbol AVL en O(log n) y rebalancea."""
    clean_kw = keyword.strip()
    if self.search(clean_kw) is None:
      print(f"[Error AVL] La palabra clave '{clean_kw}' no existe en el árbol.")
      return False

    self._root = self._delete_recursive(self._root, clean_kw)
    self._size -= 1
    print(
        f"[Éxito AVL] Palabra clave '{clean_kw}' eliminada y árbol"
        f" rebalanceado (Altura raíz: {self._get_height(self._root)})."
    )
    return True

  def _delete_recursive(self, node: AVLNode, keyword: str) -> AVLNode:
    if node is None:
      return None

    if keyword < node.keyword:
      node.left = self._delete_recursive(node.left, keyword)
    elif keyword > node.keyword:
      node.right = self._delete_recursive(node.right, keyword)
    else:
      # Nodo encontrado: caso con 0 o 1 hijo
      if node.left is None:
        return node.right
      elif node.right is None:
        return node.left

      # Nodo con 2 hijos: obtener el sucesor inorden (mínimo del subárbol derecho)
      temp = self._get_min_value_node(node.right)
      node.keyword = temp.keyword
      node.description = temp.description
      node.right = self._delete_recursive(node.right, temp.keyword)

    return self._rebalance(node)

  def suggest(self, prefix: str) -> SuggestionNode:
    """Sugiere palabras completas al introducir un prefijo.

    Aprovecha la propiedad de búsqueda binaria para podar ramas innecesarias y
    el recorrido INORDEN para devolver las sugerencias en orden alfabético.
    """
    clean_prefix = prefix.strip()
    state = {"head": None, "tail": None}
    if not clean_prefix:
      return None

    self._suggest_inorder_pruned(self._root, clean_prefix, state)
    return state["head"]

  def _suggest_inorder_pruned(
      self, node: AVLNode, prefix: str, state: dict
  ) -> None:
    """Recorrido Inorden con poda binaria por prefijo."""
    if node is None:
      return

    prefix_len = len(prefix)
    node_prefix = node.keyword[:prefix_len]

    # Si el prefijo del nodo actual es mayor o igual al buscado, puede haber coincidencias a la izquierda
    if node_prefix >= prefix:
      self._suggest_inorder_pruned(node.left, prefix, state)

    # Procesar raíz en Inorden si coincide con el prefijo
    if node_prefix == prefix:
      new_sug = SuggestionNode(node.keyword, node.description)
      if state["head"] is None:
        state["head"] = new_sug
        state["tail"] = new_sug
      else:
        state["tail"].next = new_sug
        state["tail"] = new_sug

    # Si el prefijo del nodo actual es menor o igual al buscado, puede haber coincidencias a la derecha
    if node_prefix <= prefix:
      self._suggest_inorder_pruned(node.right, prefix, state)

  def print_suggestions(self, prefix: str) -> None:
    """Ejecuta la búsqueda por prefijo y muestra los resultados alfabéticos en consola."""
    clean_prefix = prefix.strip()
    if not clean_prefix:
      print("[Error] Debes proporcionar un prefijo (ej. suggest in).")
      return

    head = self.suggest(clean_prefix)
    if head is None:
      print(
          f"[Autocompletado AVL] No se encontraron sugerencias para el prefijo"
          f" '{clean_prefix}'."
      )
      return

    print(
        f"\n=== SUGERENCIAS AVL PARA PREFIJO '{clean_prefix}' (Recorrido"
        " Inorden) ==="
    )
    curr = head
    count = 0
    while curr is not None:
      count += 1
      print(f"  {count}. {curr.keyword:<14} -> {curr.description}")
      curr = curr.next
    print("===================================================================\n")

  def print_traversals(self) -> None:
    """Imprime los recorridos Inorden, Preorden y Postorden del Árbol AVL (útil para defensa)."""
    print(
        f"\n=== DICCIONARIO ÁRBOL AVL (Total: {self._size} palabras | Altura:"
        f" {self._get_height(self._root)}) ==="
    )
    print(f"  • Inorden (Alfabético): {self._inorder_str(self._root).strip()}")
    print(f"  • Preorden (Raíz-Izq-Der): {self._preorder_str(self._root).strip()}")
    print(f"  • Postorden (Izq-Der-Raíz): {self._postorder_str(self._root).strip()}")
    print("======================================================================\n")

  def _inorder_str(self, node: AVLNode) -> str:
    if node is None:
      return ""
    return (
        f"{self._inorder_str(node.left)}{node.keyword} "
        f"{self._inorder_str(node.right)}"
    )

  def _preorder_str(self, node: AVLNode) -> str:
    if node is None:
      return ""
    return (
        f"{node.keyword}(h={node.height},fe={self._get_balance(node)}) "
        f"{self._preorder_str(node.left)}{self._preorder_str(node.right)}"
    )

  def _postorder_str(self, node: AVLNode) -> str:
    if node is None:
      return ""
    return (
        f"{self._postorder_str(node.left)}{self._postorder_str(node.right)}"
        f"{node.keyword} "
    )
