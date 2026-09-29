from core.stack import Stack


class UndoRedoManager:

  def __init__(self):
    self.undo_stack = Stack()
    self.redo_stack = Stack()

  def record_state(self, current_content: str) -> None:
    """Guarda el estado previo en la pila Undo y limpia la pila Redo."""
    self.undo_stack.push(current_content)
    self.redo_stack.clear()

  def undo(self, current_content: str) -> str:
    """Regresa al estado previo del código."""
    if self.undo_stack.is_empty():
      print("[Aviso] No hay acciones previas para deshacer (Undo).")
      return current_content

    self.redo_stack.push(current_content)
    previous_state = self.undo_stack.pop()
    print("[Éxito] Acción deshecha correctamente (Undo).")
    return previous_state

  def redo(self, current_content: str) -> str:
    """Avanza al estado previamente deshecho."""
    if self.redo_stack.is_empty():
      print("[Aviso] No hay acciones para rehacer (Redo).")
      return current_content

    self.undo_stack.push(current_content)
    next_state = self.redo_stack.pop()
    print("[Éxito] Acción rehecha correctamente (Redo).")
    return next_state

  def clear(self) -> None:
    """Limpia ambas pilas al cambiar de archivo activo."""
    self.undo_stack.clear()
    self.redo_stack.clear()