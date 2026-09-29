from core.stack import Stack


class SyntaxChecker:

  @staticmethod
  def check_syntax(code_content: str) -> bool:
    """Valida el anidamiento y balanceo de (), {}, [] usando la Pila dinámica.

    Reporta el error con número de línea y carácter.
    """
    if not code_content.strip():
      print("[Info] El archivo activo está vacío. No hay símbolos que validar.")
      return True

    stack = Stack()
    opening_brackets = "({["
    closing_brackets = ")}]"
    matching_pairs = {")": "(", "}": "{", "]": "["}

    lines = code_content.splitlines()

    for line_num, line_text in enumerate(lines, start=1):
      for char_num, char in enumerate(line_text, start=1):
        if char in opening_brackets:
          stack.push({
              "char": char,
              "line": line_num,
              "column": char_num,
          })
        elif char in closing_brackets:
          if stack.is_empty():
            print(
                f"[Error de Sintaxis] Se encontró '{char}' no esperado en la"
                f" Línea {line_num}, Carácter {char_num}."
            )
            return False

          top_item = stack.pop()
          if top_item["char"] != matching_pairs[char]:
            print(
                f"[Error de Sintaxis] Se esperaba el cierre para"
                f" '{top_item['char']}' (de Línea {top_item['line']}), pero se"
                f" encontró '{char}' en la Línea {line_num}, Carácter"
                f" {char_num}."
            )
            return False

    if not stack.is_empty():
      unclosed = stack.pop()
      print(
          f"[Error de Sintaxis] El símbolo '{unclosed['char']}' en la Línea"
          f" {unclosed['line']}, Carácter {unclosed['column']} no fue cerrado"
          " correctamente."
      )
      return False

    print(
        "[Éxito] Verificación de sintaxis completada: Todos los delimitadores"
        " están correctamente balanceados."
    )
    return True
  