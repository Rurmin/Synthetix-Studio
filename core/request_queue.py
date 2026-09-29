class RequestNode:

  def __init__(self, request_id: int, command: str, payload: str = ""):
    self.id = request_id
    self.command = command
    self.payload = payload
    self.next = None


class RequestQueue:

  def __init__(self):
    self.front = None
    self.rear = None
    self.size = 0
    self.next_id = 1

  def enqueue(self, command: str, payload: str = "") -> int:
    """Agrega una nueva solicitud al final de la cola."""
    new_node = RequestNode(self.next_id, command, payload)
    req_id = self.next_id
    self.next_id += 1

    if self.rear is None:
      self.front = new_node
      self.rear = new_node
    else:
      self.rear.next = new_node
      self.rear = new_node

    self.size += 1
    print(
        f"[Cola] Solicitud #{req_id} ('{command}') encolada correctamente."
    )
    return req_id

  def dequeue(self) -> RequestNode:
    """Remueve y retorna la solicitud en el frente de la cola."""
    if self.is_empty():
      print("[Cola] No hay solicitudes pendientes por procesar.")
      return None

    removed_node = self.front
    self.front = self.front.next

    if self.front is None:
      self.rear = None

    self.size -= 1
    return removed_node

  def is_empty(self) -> bool:
    return self.front is None

  def list_pending(self) -> None:
    """Muestra todas las solicitudes pendientes."""
    if self.is_empty():
      print("[Info] La cola de solicitudes está vacía.")
      return

    print("\n=== SOLICITUDES EN COLA ===")
    current = self.front
    position = 1
    while current is not None:
      print(f"#{position} - ID: {current.id} | Comando: {current.command}")
      current = current.next
      position += 1
    print("===========================\n")