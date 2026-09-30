import json
import os
import cohere


class AIService:

  def __init__(self, config_path: str = "config/config.json"):
    self.config_path = config_path
    self.api_key = self._load_api_key()
    self.client = None

    if self.api_key and self.api_key != "demo_key":
      try:
        # Inicializa el cliente estándar de Cohere
        self.client = cohere.Client(api_key=self.api_key)
      except Exception as e:
        print(f"[Servicio IA] Error al inicializar cliente Cohere: {e}")

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
    """Envía la solicitud a la API de Cohere y muestra el error detallado si algo falla."""
    if not code_context.strip():
      return (
          "[Servicio IA] El archivo activo está vacío. Agrega contenido antes"
          " de realizar una consulta."
      )

    if not self.client:
      return (
          "[Servicio IA] Error: No se configuró una API Key válida en"
          " config/config.json."
      )

    print(
        f"[Servicio IA] Enviando petición a Cohere API ('{command}') usando"
        f" key: {self.api_key[:6]}..."
    )

    prompt = (
        f"Eres un asistente experto en análisis de código de un IDE.\n"
        f"Instrucción: {command.upper()}\n"
        f"Código a analizar:\n```python\n{code_context}\n```\n\n"
        f"Responde de forma concisa, clara y técnica en español en 2 párrafos."
    )

    try:
      # Petición utilizando el método chat estándar
      response = self.client.chat(message=prompt, model="command-r-08-2024")
      return f"\n[Respuesta Cohere IA]:\n{response.text}"

    except Exception as e:
      # Imprime el error completo para identificar el motivo
      print(f"\n[DEBUG ERROR COHERE]: {type(e).__name__} -> {e}")
      return f"[Servicio IA] Falló la llamada a la API: {type(e).__name__} - {e}"