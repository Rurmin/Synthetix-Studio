import json
import os


class AIService:

  def __init__(self, config_path: str = "config/config.json"):
    self.config_path = config_path
    self.api_key = self._load_api_key()

  def _load_api_key(self) -> str:
    """Carga la clave de API desde el archivo de configuración JSON."""
    if os.path.exists(self.config_path):
      try:
        with open(self.config_path, "r", encoding="utf-8") as f:
          data = json.load(f)
          return data.get("api_key", "demo_key")
      except Exception:
        return "demo_key"
    return "demo_key"

  def process_request(self, command: str, code_context: str) -> str:
    """Procesa la petición enviada a la IA según el comando recibido."""
    if not code_context.strip():
      return (
          "[Servicio IA] El archivo activo está vacío. Agrega contenido antes"
          " de realizar una consulta."
      )

    print(
        f"[Servicio IA] Procesando comando '{command}' usando clave de API:"
        f" {self.api_key[:6]}..."
    )

    cmd = command.lower()
    if cmd == "explicar":
      total_lines = len(code_context.splitlines())
      return (
          f"[Respuesta IA] El código activo tiene {total_lines} líneas. Realiza"
          " operaciones estructuradas en memoria."
      )
    elif cmd == "optimizar":
      return (
          "[Respuesta IA] Sugerencia: Evaluar bucles anidados para reducir la"
          " complejidad temporal."
      )
    elif cmd == "refactorizar":
      return (
          "[Respuesta IA] Refactorización: Ajuste de nombres de variables a"
          " convención snake_case y limpieza de bloques."
      )
    else:
      return (
          f"[Respuesta IA] Procesamiento completado para la instrucción:"
          f" '{command}'."
      )