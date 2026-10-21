import sys
from core.commands import (
    AddKeywordCommand,
    AiAskCommand,
    AiRunCommand,
    AvlInfoCommand,
    BTreeInfoCommand,
    CatCommand,
    CdCommand,
    CommandInvoker,
    DelKeywordCommand,
    EditCommand,
    EvalCommand,
    ExitCommand,
    FindGlobalCommand,
    HelpCommand,
    IDEContext,
    IndexAllCommand,
    LintMathCommand,
    ListFilesCommand,
    MkdirCommand,
    MoveFileCommand,
    RedoCommand,
    RemoveFileCommand,
    SortCommand,
    SuggestCommand,
    SyntaxCommand,
    TouchCommand,
    TreeCommand,
    UndoCommand,
    UseFileCommand,
)

# Configurar salida estándar en UTF-8 para soportar caracteres de árbol (├──, └──) en Windows
if hasattr(sys.stdout, "reconfigure"):
  try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  except Exception:
    pass


def build_cli() -> tuple:
  """Construye el contexto del IDE y registra todos los comandos del Patrón Command."""
  ctx = IDEContext()
  invoker = CommandInvoker()

  # 1. Comandos Fase 2: Árbol N-ario (Workspace Virtual y Físico)
  invoker.register(MkdirCommand(ctx))
  invoker.register(CdCommand(ctx))
  invoker.register(TreeCommand(ctx))
  invoker.register(MoveFileCommand(ctx), aliases=("move", "mover"))

  # 2. Comandos Fase 2: Árbol Binario Clásico (Evaluador de Expresiones y Linter)
  invoker.register(EvalCommand(ctx), aliases=("calcular",))
  invoker.register(LintMathCommand(ctx), aliases=("linter",))

  # 3. Comandos Fase 2: Árbol AVL (Autocompletado y Diccionario Rápido)
  invoker.register(AddKeywordCommand(ctx), aliases=("add-kw",))
  invoker.register(DelKeywordCommand(ctx), aliases=("del-kw",))
  invoker.register(SuggestCommand(ctx), aliases=("autocompletar",))
  invoker.register(AvlInfoCommand(ctx), aliases=("avl",))

  # 4. Comandos Fase 2: Árbol B (Índice de Búsqueda Global)
  invoker.register(IndexAllCommand(ctx), aliases=("indexar",))
  invoker.register(FindGlobalCommand(ctx), aliases=("buscar", "find"))
  invoker.register(BTreeInfoCommand(ctx), aliases=("btree",))

  # 5. Comandos Fase 1 integrados a la CLI (Sin menú de opciones tradicional)
  invoker.register(TouchCommand(ctx), aliases=("create", "crear"))
  invoker.register(ListFilesCommand(ctx), aliases=("files", "archivos"))
  invoker.register(UseFileCommand(ctx), aliases=("open", "abrir"))
  invoker.register(CatCommand(ctx), aliases=("view", "ver"))
  invoker.register(EditCommand(ctx), aliases=("editar",))
  invoker.register(SyntaxCommand(ctx), aliases=("check-syntax", "sintaxis"))
  invoker.register(UndoCommand(ctx))
  invoker.register(RedoCommand(ctx))
  invoker.register(AiAskCommand(ctx))
  invoker.register(AiRunCommand(ctx))
  invoker.register(SortCommand(ctx), aliases=("ordenar",))
  invoker.register(RemoveFileCommand(ctx), aliases=("delete", "eliminar"))

  # 6. Comandos de Sistema
  invoker.register(HelpCommand(invoker), aliases=("?", "ayuda"))
  invoker.register(ExitCommand(), aliases=("quit", "salir"))

  return ctx, invoker


def seed_initial_workspace(ctx: IDEContext) -> None:
  """Inicializa un archivo físico de demostración en el Workspace e indexa el Árbol B."""
  demo_code = (
      "def calcular_puntaje():\n"
      "    contador = (5 + 3) * 2\n"
      "    bono = (4 + 8) * 3\n"
      "    contador = contador + bono\n"
      "    return contador\n"
  )
  phys_dir = ctx.workspace_tree.get_physical_path()
  node = ctx.file_list.create_file(
      "main.py", demo_code, phys_dir, silent=True
  )
  if node is not None:
    ctx.workspace_tree.attach_file(
        node, ctx.workspace_tree.current_dir, silent=True
    )
  ctx.b_tree.index_all_files(ctx.file_list)


def print_commands_panel() -> None:
  print("\n======================================================================================")
  print("     🚀 SYNTHETIX STUDIO CLI — COMANDOS INDIVIDUALES (PATRÓN COMMAND)                 ")
  print("======================================================================================")
  print("  📁 1. ÁRBOL N-ARIO (Carpetas y Archivos del Workspace):")
  print("     • mkdir <carpeta>        -> Crea una carpeta nueva         (Ej: mkdir src)")
  print("     • cd <carpeta>           -> Entra a carpeta o sube al padre(Ej: cd src  |  cd ..)")
  print("     • mv <archivo> <carpeta> -> Mueve un archivo a una carpeta (Ej: mv main.py src)")
  print("     • tree                   -> Dibuja el árbol de carpetas    (Recorrido Preorden)")
  print("--------------------------------------------------------------------------------------")
  print("  ➗ 2. ÁRBOL BINARIO (Evaluador de Expresiones Matemáticas):")
  print('     • eval "<expresion>"     -> Resuelve operación en Postorden(Ej: eval "(4+8)*3")')
  print("     • lint-math              -> Calcula las operaciones del archivo activo")
  print("--------------------------------------------------------------------------------------")
  print("  📖 3. ÁRBOL AVL (Autocompletado y Diccionario Auto-balanceable):")
  print("     • add-keyword <palabra>  -> Inserta palabra y balancea AVL (Ej: add-keyword struct)")
  print("     • suggest <prefijo>      -> Autocompleta en orden A-Z      (Ej: suggest in)")
  print("     • del-keyword <palabra>  -> Elimina palabra y rebalancea   (Ej: del-keyword struct)")
  print("     • avl-info               -> Muestra recorridos Inorden, Preorden y Postorden")
  print("--------------------------------------------------------------------------------------")
  print("  🔍 4. ÁRBOL B (Índice de Búsqueda Global en Archivos):")
  print("     • index-all              -> Escanea e indexa todas las variables en el Árbol B")
  print("     • find-global <token>    -> Busca en qué archivo y línea está una variable (Ej: find-global contador)")
  print("     • btree-info             -> Muestra las páginas internas del Árbol B")
  print("--------------------------------------------------------------------------------------")
  print("  📄 ARCHIVOS (Fase 1): touch | ls | cat | edit | use | syntax | undo | redo | sort | rm")
  print("  ⚙️  SISTEMA          : help (tabla completa) | exit (salir)")
  print("  💡 Tip: También puedes escribir solo el nombre del comando (ej: mkdir, eval, mv) y te pedirá los datos paso a paso.")
  print("======================================================================================")


def main() -> None:
  ctx, invoker = build_cli()
  seed_initial_workspace(ctx)

  while True:
    try:
      print_commands_panel()
      cwd_path = ctx.workspace_tree.get_virtual_path()
      active = ctx.file_list.get_active_file()
      active_tag = f" [{active.filename}]" if active else ""
      raw_line = input(f"\nsynthetix:{cwd_path}{active_tag}$ ")
      invoker.execute_line(raw_line)
    except (EOFError, KeyboardInterrupt):
      print("\nSaliendo de Synthetix Studio... ¡Hasta luego!")
      break


if __name__ == "__main__":
  main()
