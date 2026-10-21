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
  invoker.register(MoveFileCommand(ctx), aliases=("move",))

  # 2. Comandos Fase 2: Árbol Binario Clásico (Evaluador de Expresiones y Linter)
  invoker.register(EvalCommand(ctx))
  invoker.register(LintMathCommand(ctx))

  # 3. Comandos Fase 2: Árbol AVL (Autocompletado y Diccionario Rápido)
  invoker.register(AddKeywordCommand(ctx))
  invoker.register(DelKeywordCommand(ctx))
  invoker.register(SuggestCommand(ctx))
  invoker.register(AvlInfoCommand(ctx))

  # 4. Comandos Fase 2: Árbol B (Índice de Búsqueda Global)
  invoker.register(IndexAllCommand(ctx))
  invoker.register(FindGlobalCommand(ctx))
  invoker.register(BTreeInfoCommand(ctx))

  # 5. Comandos Fase 1 integrados a la CLI (Sin menú de opciones tradicional)
  invoker.register(TouchCommand(ctx), aliases=("create",))
  invoker.register(ListFilesCommand(ctx), aliases=("files",))
  invoker.register(UseFileCommand(ctx), aliases=("open",))
  invoker.register(CatCommand(ctx), aliases=("view",))
  invoker.register(EditCommand(ctx))
  invoker.register(SyntaxCommand(ctx), aliases=("check-syntax",))
  invoker.register(UndoCommand(ctx))
  invoker.register(RedoCommand(ctx))
  invoker.register(AiAskCommand(ctx))
  invoker.register(AiRunCommand(ctx))
  invoker.register(SortCommand(ctx))
  invoker.register(RemoveFileCommand(ctx), aliases=("delete",))

  # 6. Comandos de Sistema
  invoker.register(HelpCommand(invoker), aliases=("?",))
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


def main() -> None:
  ctx, invoker = build_cli()
  seed_initial_workspace(ctx)

  print("================================================================================")
  print("   SYNTHETIX STUDIO CLI — FASE 2: ESTRUCTURAS JERÁRQUICAS Y BÚSQUEDA AVANZADA   ")
  print("================================================================================")
  print("Consola interactiva basada en el Patrón de Diseño Comandos (Command Pattern).")
  print("Escribe 'help' para ver todos los comandos (mkdir, cd, tree, eval, suggest,")
  print("add-keyword, index-all, find-global, mv, touch, edit, ls, syntax, undo, exit).")
  print("--------------------------------------------------------------------------------")

  while True:
    try:
      cwd_path = ctx.workspace_tree.get_virtual_path()
      active = ctx.file_list.get_active_file()
      active_tag = f" [{active.filename}]" if active else ""
      raw_line = input(f"synthetix:{cwd_path}{active_tag}$ ")
      invoker.execute_line(raw_line)
    except (EOFError, KeyboardInterrupt):
      print("\nSaliendo de Synthetix Studio... ¡Hasta luego!")
      break


if __name__ == "__main__":
  main()
