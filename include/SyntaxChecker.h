#ifndef SYNTAXCHECKER_H
#define SYNTAXCHECKER_H

#include <string>

// Estructura para registrar la posición del delimitador
struct SymbolInfo {
    char symbol;
    int line;
    int column;
};

class SyntaxChecker {
public:
    // Requerimiento 2: Pila de Verificación de Sintaxis
    static bool checkSyntax(const std::string& code);
};

#endif // SYNTAXCHECKER_H