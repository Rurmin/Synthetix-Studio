import sys
from core.avl_tree import AVLTree
from core.b_tree import BTree
from core.expression_tree import ExpressionBinaryTree
from core.file_list import FileList
from core.nary_tree import WorkspaceTree
from core.request_queue import RequestQueue
from core.sorting import SortingEngine
from core.syntax_checker import SyntaxChecker
from core.undo_redo import UndoRedoManager
from services.ai_service import AIService


class IDEContext:
  """Receptor (Receiver) del Patrón Command que encapsula todas las estructuras

  de datos de Fase 1 y Fase 2 del entorno Synthetix Studio.
  """

  def __init__(self):
    self.workspace_tree = WorkspaceTree("workspace")
    self.file_list = FileList(self.workspace_tree.get_physical_path())
    self.avl_tree = AVLTree(preload_defaults=True)
    self.b_tree = BTree(t=2)  # Orden m = 4
    self.undo_redo = UndoRedoManager()
    self.request_queue = RequestQueue()
    self.ai_service = AIService()


class Command:
  """Clase base abstracta del Patrón de Diseño Comandos (Command Pattern)."""

  def __init__(self, name: str, usage: str, description: str, module: str):
    self._name = name
    self._usage = usage
    self._description = description
    self._module = module

  @property
  def name(self) -> str:
    return self._name

  @property
  def usage(self) -> str:
    return self._usage

  @property
  def description(self) -> str:
    return self._description

  @property
  def module(self) -> str:
    return self._module

  def execute(self, args: str) -> None:
    raise NotImplementedError(
        "Las subclases de Command deben implementar el método execute()."
    )


# ==============================================================================
# COMANDOS DEL MÓDULO 1: ÁRBOL N-ARIO (EXPLORADOR DE ESPACIO DE TRABAJO)
# ==============================================================================


class MkdirCommand(Command):
  """Comando CLI: mkdir <nombre_carpeta>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "mkdir",
        "mkdir <nombre_carpeta>",
        "Crea un nuevo directorio en el nivel actual del Workspace virtual y físico.",
        "Árbol N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.workspace_tree.mkdir(args)


class CdCommand(Command):
  """Comando CLI: cd <nombre_carpeta>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "cd",
        "cd <nombre_carpeta>",
        "Cambia el directorio de trabajo actual navegando por el Árbol N-ario (cd .. para subir).",
        "Árbol N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.workspace_tree.cd(args)


class TreeCommand(Command):
  """Comando CLI: tree."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "tree",
        "tree",
        "Imprime la jerarquía completa del proyecto recorriendo el Árbol N-ario en preorden.",
        "Árbol N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.workspace_tree.print_tree()


class MoveFileCommand(Command):
  """Comando CLI: mv <archivo> <carpeta_destino>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "mv",
        "mv <archivo> <carpeta_destino>",
        "Mueve un archivo (creado en Fase 1/2) dentro de las carpetas del Árbol N-ario.",
        "Árbol N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    parts = args.strip().split(None, 1)
    if len(parts) < 2:
      print("[Error] Uso correcto: mv <nombre_archivo> <carpeta_destino>")
      return
    filename, dest_folder = parts[0], parts[1].strip()
    self._ctx.workspace_tree.move_file(filename, dest_folder)


# ==============================================================================
# COMANDOS DEL MÓDULO 2: ÁRBOL BINARIO DE EXPRESIONES (EVALUADOR Y LINTER)
# ==============================================================================


class EvalCommand(Command):
  """Comando CLI: eval "<expresion>"."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "eval",
        'eval "<expresion>"',
        "Parsea una expresión, construye el Árbol Binario y la evalúa en postorden.",
        "Árbol Binario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    if not args.strip():
      print('[Error] Uso correcto: eval "<expresion>" (ej. eval "(4+8)*3")')
      return
    try:
      expr_tree = ExpressionBinaryTree()
      expr_tree.build_from_expression(args)
      result = expr_tree.evaluate_postorder()
      print("\n=== EVALUADOR DE EXPRESIONES (ÁRBOL BINARIO) ===")
      print(f"  • Expresión (Inorden) : {expr_tree.get_inorder_str()}")
      print(f"  • Recorrido Preorden  : {expr_tree.get_preorder_str()}")
      print(f"  • Recorrido Postorden : {expr_tree.get_postorder_str()}")
      print(f"  • Resultado Exacto    : {result}")
      print("================================================\n")
    except Exception as e:
      print(f"[Error en Evaluador de Expresiones] {e}")


class LintMathCommand(Command):
  """Comando CLI: lint-math."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "lint-math",
        "lint-math",
        "Ejecuta el linter de cálculos en tiempo de escritura sobre el archivo activo.",
        "Árbol Binario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return
    ExpressionBinaryTree.lint_code_expressions(active.content)


# ==============================================================================
# COMANDOS DEL MÓDULO 3: ÁRBOL AVL (AUTOCOMPLETADO Y DICCIONARIO RÁPIDO)
# ==============================================================================


class AddKeywordCommand(Command):
  """Comando CLI: add-keyword <palabra> [descripcion]."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "add-keyword",
        "add-keyword <palabra> [descripcion]",
        "Inserta una nueva palabra clave en el Árbol AVL aplicando rotaciones de balanceo.",
        "Árbol AVL",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    cleaned = args.strip()
    if not cleaned:
      print("[Error] Uso correcto: add-keyword <palabra> [descripcion]")
      return
    parts = cleaned.split(None, 1)
    keyword = parts[0]
    desc = (
        parts[1]
        if len(parts) > 1
        else "Palabra clave registrada por el usuario."
    )
    self._ctx.avl_tree.insert(keyword, desc)


class DelKeywordCommand(Command):
  """Comando CLI: del-keyword <palabra>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "del-keyword",
        "del-keyword <palabra>",
        "Elimina una palabra clave del Árbol AVL en O(log n) y rebalancea.",
        "Árbol AVL",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    cleaned = args.strip()
    if not cleaned:
      print("[Error] Uso correcto: del-keyword <palabra>")
      return
    self._ctx.avl_tree.delete(cleaned)


class SuggestCommand(Command):
  """Comando CLI: suggest <prefijo>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "suggest",
        "suggest <prefijo>",
        "Busca en el Árbol AVL y retorna sugerencias alfabéticas (inorden) para el prefijo.",
        "Árbol AVL",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.avl_tree.print_suggestions(args)


class AvlInfoCommand(Command):
  """Comando CLI: avl-info."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "avl-info",
        "avl-info",
        "Muestra los recorridos Inorden, Preorden y Postorden del Árbol AVL.",
        "Árbol AVL",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.avl_tree.print_traversals()


# ==============================================================================
# COMANDOS DEL MÓDULO 4: ÁRBOL B (ÍNDICE DE BÚSQUEDA GLOBAL)
# ==============================================================================


class IndexAllCommand(Command):
  """Comando CLI: index-all."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "index-all",
        "index-all",
        "Escanea todos los archivos abiertos y construye/actualiza el Árbol B con los tokens.",
        "Árbol B",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.b_tree.index_all_files(self._ctx.file_list)


class FindGlobalCommand(Command):
  """Comando CLI: find-global <token>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "find-global",
        "find-global <token>",
        "Busca un token específico en el Árbol B y muestra archivos y líneas donde aparece.",
        "Árbol B",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.b_tree.find_global(args)


class BTreeInfoCommand(Command):
  """Comando CLI: btree-info."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "btree-info",
        "btree-info",
        "Muestra las páginas/nodos internos del Árbol B y su recorrido inorden.",
        "Árbol B",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.b_tree.print_btree_structure()


# ==============================================================================
# COMANDOS DE LA FASE 1 ADAPTADOS AL PATRÓN COMMAND (SIN MENÚ DE OPCIONES)
# ==============================================================================


class TouchCommand(Command):
  """Comando CLI: touch <nombre_archivo> [contenido_inicial]."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "touch",
        "touch <archivo> [contenido]",
        "Crea un nuevo archivo físico y virtual en el directorio actual del Workspace.",
        "Fase 1 / N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    cleaned = args.strip()
    if not cleaned:
      print("[Error] Uso correcto: touch <nombre_archivo> [contenido_inicial]")
      return
    parts = cleaned.split(None, 1)
    filename = parts[0]
    content = parts[1].replace("\\n", "\n") if len(parts) > 1 else ""

    phys_dir = self._ctx.workspace_tree.get_physical_path()
    file_node = self._ctx.file_list.create_file(filename, content, phys_dir)
    if file_node is not None:
      self._ctx.workspace_tree.attach_file(
          file_node, self._ctx.workspace_tree.current_dir
      )
      ExpressionBinaryTree.lint_code_expressions(file_node.content)


class ListFilesCommand(Command):
  """Comando CLI: ls."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "ls",
        "ls",
        "Lista todos los archivos abiertos en la Lista Doblemente Enlazada.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    self._ctx.file_list.list_files()


class UseFileCommand(Command):
  """Comando CLI: use <id_o_nombre>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "use",
        "use <id_o_nombre>",
        "Cambia el archivo activo por su ID o nombre y reinicia las pilas Undo/Redo.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    ident = args.strip()
    if not ident:
      print("[Error] Uso correcto: use <id_o_nombre_archivo>")
      return
    if self._ctx.file_list.switch_active_file(ident):
      self._ctx.undo_redo.clear()


class CatCommand(Command):
  """Comando CLI: cat."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "cat",
        "cat",
        "Muestra el contenido del archivo activo actual.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return
    active.load_from_disk()
    print(f"\n--- Archivo Activo: {active.filename} (ID: {active.id}) ---")
    for idx, line in enumerate(active.content.splitlines(), start=1):
      print(f"{idx:>3} | {line}")
    print("---------------------------------------------------\n")


class EditCommand(Command):
  """Comando CLI: edit [nuevo_contenido]."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "edit",
        "edit [nuevo_contenido]",
        "Edita el archivo activo, guarda en Pila Undo y ejecuta el Linter de Expresiones.",
        "Fase 1 / Binario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return

    if args.strip():
      new_text = args.strip().replace("\\n", "\n")
    else:
      print(f"\n--- Contenido actual de {active.filename} ---")
      print(active.content)
      print("------------------------------------------")
      new_text = input(
          "Ingresa el nuevo contenido (usa \\n para saltos de línea): "
      ).replace("\\n", "\n")

    self._ctx.undo_redo.record_state(active.content)
    active.content = new_text
    print(f"[Éxito] Contenido de '{active.filename}' actualizado en memoria y disco.")
    # Ejecutar linter de cálculos en tiempo de escritura (Árbol Binario en Postorden)
    ExpressionBinaryTree.lint_code_expressions(active.content)


class SyntaxCommand(Command):
  """Comando CLI: syntax."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "syntax",
        "syntax",
        "Valida el balanceo de delimitadores (), {}, [] en el archivo activo usando Pila.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return
    SyntaxChecker.check_syntax(active.content)


class UndoCommand(Command):
  """Comando CLI: undo."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "undo",
        "undo",
        "Deshace el último cambio en el archivo activo usando la Pila Undo.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return
    active.content = self._ctx.undo_redo.undo(active.content)


class RedoCommand(Command):
  """Comando CLI: redo."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "redo",
        "redo",
        "Rehace el último cambio deshecho en el archivo activo usando la Pila Redo.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    active = self._ctx.file_list.get_active_file()
    if active is None:
      print("[Error] No hay un archivo activo seleccionado.")
      return
    active.content = self._ctx.undo_redo.redo(active.content)


class AiAskCommand(Command):
  """Comando CLI: ai-ask <explicar|optimizar|refactorizar>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "ai-ask",
        "ai-ask <instruccion>",
        "Encola una solicitud para la IA en la Cola FIFO (explicar/optimizar/refactorizar).",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    cmd = args.strip()
    if not cmd:
      print("[Error] Uso correcto: ai-ask <explicar|optimizar|refactorizar>")
      return
    active = self._ctx.file_list.get_active_file()
    payload = active.content if active else ""
    self._ctx.request_queue.enqueue(cmd, payload)


class AiRunCommand(Command):
  """Comando CLI: ai-run."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "ai-run",
        "ai-run",
        "Desencola y procesa la siguiente solicitud pendiente en la Cola FIFO de IA.",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    req = self._ctx.request_queue.dequeue()
    if req is not None:
      res = self._ctx.ai_service.process_request(req.command, req.payload)
      print(f"\n{res}\n")


class SortCommand(Command):
  """Comando CLI: sort <name|id>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "sort",
        "sort <name|id>",
        "Ordena la lista de archivos por nombre (InsertionSort) o por ID (QuickSort).",
        "Fase 1",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    if self._ctx.file_list.head is None:
      print("[Info] No hay archivos para ordenar.")
      return

    mode = args.strip().lower() or "name"
    files_meta = []
    curr = self._ctx.file_list.head
    while curr is not None:
      files_meta.append({"id": curr.id, "filename": curr.filename})
      curr = curr.next

    if mode == "name":
      sorted_res = SortingEngine.insertion_sort_by_filename(files_meta)
      print("\n--- Archivos ordenados por Nombre (InsertionSort A-Z) ---")
      for item in sorted_res:
        print(f"ID: {item['id']} | Nombre: {item['filename']}")
    elif mode == "id":
      sorted_res = SortingEngine.quick_sort_by_id(files_meta)
      print("\n--- Archivos ordenados por ID (QuickSort Ascendente) ---")
      for item in sorted_res:
        print(f"ID: {item['id']} | Nombre: {item['filename']}")
    else:
      print("[Error] Modo inválido. Usa 'sort name' o 'sort id'.")


class RemoveFileCommand(Command):
  """Comando CLI: rm <id_o_nombre>."""

  def __init__(self, ctx: IDEContext):
    super().__init__(
        "rm",
        "rm <id_o_nombre>",
        "Elimina un archivo de la Lista Doblemente Enlazada, del Árbol N-ario y del disco.",
        "Fase 1 / N-ario",
    )
    self._ctx = ctx

  def execute(self, args: str) -> None:
    ident = args.strip()
    if not ident:
      print("[Error] Uso correcto: rm <id_o_nombre_archivo>")
      return
    removed = self._ctx.file_list.delete_file(ident)
    if removed is not None:
      self._ctx.workspace_tree.remove_file_node(removed.filename)
      self._ctx.undo_redo.clear()


class ExitCommand(Command):
  """Comando CLI: exit."""

  def __init__(self):
    super().__init__(
        "exit",
        "exit",
        "Finaliza la sesión interactiva de Synthetix Studio CLI.",
        "Sistema",
    )

  def execute(self, args: str) -> None:
    print("Saliendo de Synthetix Studio... ¡Hasta luego!")
    sys.exit(0)


# ==============================================================================
# INVOCADOR (INVOKER) DEL PATRÓN COMMAND CON LISTA ENLAZADA DESDE CERO
# ==============================================================================


class CommandRegistryNode:
  """Nodo enlazado para registrar comandos en el Invoker sin usar diccionarios nativos."""

  def __init__(self, cmd_name: str, command_obj: Command, is_alias: bool = False):
    self.cmd_name = cmd_name
    self.command_obj = command_obj
    self.is_alias = is_alias
    self.next = None


class HelpCommand(Command):
  """Comando CLI: help."""

  def __init__(self, invoker):
    super().__init__(
        "help",
        "help",
        "Muestra la tabla de comandos disponibles integrados con el Patrón Command.",
        "Sistema",
    )
    self._invoker = invoker

  def execute(self, args: str) -> None:
    self._invoker.print_help()


class CommandInvoker:
  """Invocador (Invoker) del Patrón Command que gestiona el registro y despacho

  de comandos en la consola CLI sin menús numéricos tradicionales.
  """

  def __init__(self):
    self._head = None
    self._tail = None

  def register(self, command_obj: Command, aliases=()) -> None:
    """Registra un objeto Command y sus alias opcionales en la lista enlazada."""
    self._append_node(command_obj.name, command_obj, is_alias=False)
    for alias in aliases:
      self._append_node(alias, command_obj, is_alias=True)

  def _append_node(
      self, name: str, command_obj: Command, is_alias: bool
  ) -> None:
    new_node = CommandRegistryNode(name.lower(), command_obj, is_alias)
    if self._head is None:
      self._head = new_node
      self._tail = new_node
    else:
      self._tail.next = new_node
      self._tail = new_node

  def find_command(self, name: str) -> Command:
    target = name.lower().strip()
    curr = self._head
    while curr is not None:
      if curr.cmd_name == target:
        return curr.command_obj
      curr = curr.next
    return None

  def execute_line(self, raw_line: str) -> None:
    """Parsea la línea ingresada en el prompt y ejecuta el Command correspondiente."""
    cleaned = raw_line.strip()
    if not cleaned:
      return

    parts = cleaned.split(None, 1)
    cmd_name = parts[0]
    cmd_args = parts[1] if len(parts) > 1 else ""

    cmd_obj = self.find_command(cmd_name)
    if cmd_obj is None:
      print(
          f"[Error CLI] Comando desconocido: '{cmd_name}'. Escribe 'help' para"
          " ver los comandos disponibles."
      )
      return

    cmd_obj.execute(cmd_args)

  def print_help(self) -> None:
    print(
        "\n=========================================================================================="
    )
    print(
        "                 SYNTHETIX STUDIO CLI — REFERENCIA DE COMANDOS (FASE 1 & 2)               "
    )
    print(
        "=========================================================================================="
    )
    print(f"  {'MÓDULO':<15} | {'COMANDO / USO':<32} | {'DESCRIPCIÓN'}")
    print(
        "------------------------------------------------------------------------------------------"
    )
    curr = self._head
    while curr is not None:
      if not curr.is_alias:
        cmd = curr.command_obj
        print(f"  {cmd.module:<15} | {cmd.usage:<32} | {cmd.description}")
      curr = curr.next
    print(
        "==========================================================================================\n"
    )
