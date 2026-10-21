from core.stack import Stack


class ExpressionNode:
  """Nodo de un Árbol Binario de Expresiones.

  - Nodos hoja: operandos numéricos (left=None, right=None).
  - Nodos internos: operadores matemáticos (+, -, *, /).
  """

  def __init__(self, value: str, is_operator: bool = False):
    self._value = value
    self._is_operator = is_operator
    self._left = None
    self._right = None

  @property
  def value(self) -> str:
    return self._value

  @property
  def is_operator(self) -> bool:
    return self._is_operator

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

  def is_leaf(self) -> bool:
    return self._left is None and self._right is None


class TokenListNode:
  """Nodo enlazado auxiliar para almacenar tokens sin depender de listas nativas."""

  def __init__(self, token: str):
    self.token = token
    self.next = None


class ExpressionBinaryTree:
  """Árbol Binario Clásico para parsear y evaluar expresiones matemáticas en Postorden."""

  def __init__(self):
    self._root = None

  @property
  def root(self) -> ExpressionNode:
    return self._root

  @staticmethod
  def _precedence(op: str) -> int:
    if op == "+" or op == "-":
      return 1
    if op == "*" or op == "/":
      return 2
    return 0

  @staticmethod
  def _is_operator_char(ch: str) -> bool:
    return ch in ("+", "-", "*", "/")

  @staticmethod
  def _is_digit_or_dot(ch: str) -> bool:
    return ("0" <= ch <= "9") or ch == "."

  def _tokenize(self, expression: str) -> TokenListNode:
    """Analizador léxico manual (desde cero) que convierte la cadena en una lista enlazada de tokens."""
    head = None
    tail = None
    n = len(expression)
    i = 0
    prev_token = None

    while i < n:
      ch = expression[i]
      if ch in (" ", "\t", "\r", "\n"):
        i += 1
        continue

      # Manejo de signo negativo/positivo unario al inicio o después de '(' u operador
      if ch in ("-", "+") and (
          prev_token is None
          or prev_token == "("
          or self._is_operator_char(prev_token)
      ):
        # Verificar si le sigue un número
        j = i + 1
        while j < n and expression[j] == " ":
          j += 1
        if j < n and self._is_digit_or_dot(expression[j]):
          num_str = "-" if ch == "-" else ""
          i = j
          dot_count = 0
          while i < n and self._is_digit_or_dot(expression[i]):
            if expression[i] == ".":
              dot_count += 1
              if dot_count > 1:
                raise ValueError("Número decimal mal formado en la expresión.")
            num_str += expression[i]
            i += 1
          new_node = TokenListNode(num_str)
          if head is None:
            head = new_node
            tail = new_node
          else:
            tail.next = new_node
            tail = new_node
          prev_token = num_str
          continue

      if self._is_digit_or_dot(ch):
        num_str = ""
        dot_count = 0
        while i < n and self._is_digit_or_dot(expression[i]):
          if expression[i] == ".":
            dot_count += 1
            if dot_count > 1:
              raise ValueError("Número decimal mal formado en la expresión.")
          num_str += expression[i]
          i += 1
        new_node = TokenListNode(num_str)
        if head is None:
          head = new_node
          tail = new_node
        else:
          tail.next = new_node
          tail = new_node
        prev_token = num_str
      elif self._is_operator_char(ch) or ch in ("(", ")"):
        new_node = TokenListNode(ch)
        if head is None:
          head = new_node
          tail = new_node
        else:
          tail.next = new_node
          tail = new_node
        prev_token = ch
        i += 1
      else:
        raise ValueError(f"Carácter inválido en la expresión matemática: '{ch}'")

    return head

  def _build_subtree(self, op_stack: Stack, node_stack: Stack) -> None:
    """Extrae un operador y dos operandos de las pilas para enlazar un subárbol binario."""
    op = op_stack.pop()
    right_node = node_stack.pop()
    left_node = node_stack.pop()

    if op is None or right_node is None or left_node is None:
      raise ValueError("Expresión matemática incompleta o desbalanceada.")

    op_node = ExpressionNode(op, is_operator=True)
    op_node.left = left_node
    op_node.right = right_node
    node_stack.push(op_node)

  def build_from_expression(self, expression: str) -> ExpressionNode:
    """Construye el Árbol Binario de Expresiones a partir de una cadena infija."""
    cleaned = expression.strip()
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (
        cleaned.startswith("'") and cleaned.endswith("'")
    ):
      cleaned = cleaned[1:-1].strip()

    if not cleaned:
      raise ValueError("La expresión matemática está vacía.")

    tokens_head = self._tokenize(cleaned)
    if tokens_head is None:
      raise ValueError("No se encontraron tokens en la expresión.")

    op_stack = Stack()
    node_stack = Stack()

    curr = tokens_head
    while curr is not None:
      tok = curr.token
      if tok == "(":
        op_stack.push(tok)
      elif tok == ")":
        while not op_stack.is_empty() and op_stack.top() != "(":
          self._build_subtree(op_stack, node_stack)
        if op_stack.is_empty() or op_stack.top() != "(":
          raise ValueError("Paréntesis desbalanceados en la expresión.")
        op_stack.pop()  # Remueve '('
      elif self._is_operator_char(tok):
        while (
            not op_stack.is_empty()
            and op_stack.top() != "("
            and self._precedence(op_stack.top()) >= self._precedence(tok)
        ):
          self._build_subtree(op_stack, node_stack)
        op_stack.push(tok)
      else:
        # Es un operando numérico -> Nodo Hoja
        leaf = ExpressionNode(tok, is_operator=False)
        node_stack.push(leaf)

      curr = curr.next

    while not op_stack.is_empty():
      if op_stack.top() in ("(", ")"):
        raise ValueError("Paréntesis desbalanceados en la expresión.")
      self._build_subtree(op_stack, node_stack)

    root_node = node_stack.pop()
    if root_node is None or not node_stack.is_empty():
      raise ValueError("Sintaxis inválida en la expresión matemática.")

    self._root = root_node
    return self._root

  def evaluate_postorder(self) -> float:
    """Evalúa el Árbol Binario de Expresiones mediante recorrido en POSTORDEN."""
    if self._root is None:
      raise ValueError("El árbol de expresiones está vacío.")
    result = self._eval_postorder_recursive(self._root)
    if isinstance(result, float) and result.is_integer():
      return int(result)
    return result

  def _eval_postorder_recursive(self, node: ExpressionNode) -> float:
    """Recorrido en Postorden (Izquierda -> Derecha -> Raíz) para evaluar la expresión."""
    # Caso base: si es nodo hoja, retornar su valor numérico (operando)
    if node.is_leaf():
      return float(node.value)

    # 1. Recorrer subárbol izquierdo en postorden
    left_val = self._eval_postorder_recursive(node.left)
    # 2. Recorrer subárbol derecho en postorden
    right_val = self._eval_postorder_recursive(node.right)

    # 3. Procesar la raíz (operador interno)
    op = node.value
    if op == "+":
      return left_val + right_val
    elif op == "-":
      return left_val - right_val
    elif op == "*":
      return left_val * right_val
    elif op == "/":
      if right_val == 0:
        raise ZeroDivisionError("Error matemático: División por cero.")
      return left_val / right_val
    else:
      raise ValueError(f"Operador desconocido: '{op}'")

  def get_postorder_str(self) -> str:
    """Devuelve la representación en notación postfija (Postorden) del árbol."""
    return self._postorder_text(self._root).strip()

  def _postorder_text(self, node: ExpressionNode) -> str:
    if node is None:
      return ""
    left_s = self._postorder_text(node.left)
    right_s = self._postorder_text(node.right)
    return f"{left_s}{right_s}{node.value} "

  def get_preorder_str(self) -> str:
    """Devuelve la representación en notación prefija (Preorden) del árbol."""
    return self._preorder_text(self._root).strip()

  def _preorder_text(self, node: ExpressionNode) -> str:
    if node is None:
      return ""
    left_s = self._preorder_text(node.left)
    right_s = self._preorder_text(node.right)
    return f"{node.value} {left_s}{right_s}"

  def get_inorder_str(self) -> str:
    """Devuelve la representación infija (Inorden) del árbol."""
    return self._inorder_text(self._root).strip()

  def _inorder_text(self, node: ExpressionNode) -> str:
    if node is None:
      return ""
    if node.is_leaf():
      return f"{node.value}"
    left_s = self._inorder_text(node.left)
    right_s = self._inorder_text(node.right)
    return f"({left_s} {node.value} {right_s})"

  @classmethod
  def lint_code_expressions(cls, code_content: str) -> None:
    """Actúa como un 'linter' de cálculos en tiempo de escritura sobre el código activo.

    Busca expresiones matemáticas en cada línea, construye su Árbol Binario y
    muestra el resultado evaluado en postorden.
    """
    if not code_content or not code_content.strip():
      return

    lines = code_content.splitlines()
    found_any = False

    for line_idx, raw_line in enumerate(lines, start=1):
      line = raw_line.strip()
      if not line or line.startswith("#"):
        continue

      # Si hay una asignación (ej. x = (5 + 3) * 2), tomar el lado derecho
      candidate = line
      if "=" in line and not (
          "==" in line or "!=" in line or "<=" in line or ">=" in line
      ):
        parts = line.split("=", 1)
        candidate = parts[1].strip()

      # Quitar comentarios al final de la línea
      if "#" in candidate:
        candidate = candidate.split("#", 1)[0].strip()

      # Verificar si contiene al menos un operador matemático y dígitos
      has_op = False
      has_digit = False
      only_math = True
      for ch in candidate:
        if ch in ("+", "-", "*", "/"):
          has_op = True
        elif "0" <= ch <= "9":
          has_digit = True
        elif ch not in (" ", "\t", "(", ")", "."):
          only_math = False
          break

      if has_op and has_digit and only_math:
        try:
          tree = cls()
          tree.build_from_expression(candidate)
          res = tree.evaluate_postorder()
          postorder_seq = tree.get_postorder_str()
          if not found_any:
            print(
                "\n[Linter Matemático - Árbol Binario de Expresiones en"
                " Postorden]:"
            )
            found_any = True
          print(
              f"  • Línea {line_idx}: '{candidate}' | Postorden:"
              f" [{postorder_seq}] => Resultado = {res}"
          )
        except Exception as e:
          if not found_any:
            print(
                "\n[Linter Matemático - Árbol Binario de Expresiones en"
                " Postorden]:"
            )
            found_any = True
          print(f"  • Línea {line_idx}: '{candidate}' => [Alerta Linter] {e}")
