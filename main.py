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
    DemoCommand,
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

  # 0. Comando Todo-en-Uno para probar todos los módulos de una sola vez
  invoker.register(DemoCommand(invoker), aliases=("test-all", "probar"))

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


def print_welcome_banner() -> None:
  print("\n======================================================================================")
  print("     🚀 SYNTHETIX STUDIO CLI — FASE 2: ESTRUCTURAS JERÁRQUICAS Y BÚSQUEDA AVANZADA     ")
  print("======================================================================================")
  print("  ✨ MODO RÁPIDO (UN SOLO PASO):")
  print("     • Escribe  demo      -> Ejecuta y demuestra los 4 ÁRBOLES automáticamente.")
  print("     • Usa ';' entre comandos para aplicar varios de una sola vez:")
  print('       mkdir src ; mv main.py src ; tree ; eval "(4+8)*3" ; suggest in ; find-global contador')
  print("--------------------------------------------------------------------------------------")
  print("  🌳 COMANDOS POR ÁRBOL (Puedes escribirlos directos o solos para que el asistente te guíe):")
  print("     [1. Árbol N-ario]   mkdir src       | cd src (o cd ..) | mv main.py src | tree")
  print('     [2. Árbol Binario]  eval "(4+8)*3"  | lint-math')
  print("     [3. Árbol AVL]      add-keyword struct | suggest in    | del-keyword struct | avl-info")
  print("     [4. Árbol B]        index-all       | find-global contador | btree-info")
  print("     [Archivos Fase 1]   touch test.py   | ls | cat | edit  | syntax | undo | redo | sort")
  print("     [Ayuda / Salir]     help (o ayuda)  | exit (o salir)")
  print("======================================================================================\n")


def main() -> None:
  ctx, invoker = build_cli()
  seed_initial_workspace(ctx)

  # Si se pasan comandos por argumento al ejecutar (ej: python main.py demo)
  if len(sys.argv) > 1:
    arg_cmd = " ".join(sys.argv[1:])
    invoker.execute_line(arg_cmd)
    return

  print_welcome_banner()

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
