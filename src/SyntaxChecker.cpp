#include "../include/SyntaxChecker.h"
#include "../include/Stack.h"
#include <iostream>

bool SyntaxChecker::checkSyntax(const std::string& code) {
    Stack<SymbolInfo> stack;
    int line = 1;
    int column = 0;

    for (size_t i = 0; i < code.length(); ++i) {
        char ch = code[i];
        column++;

        if (ch == '\n') {
            line++;
            column = 0;
            continue;
        }

        // Si es apertura, lo apilamos
        if (ch == '(' || ch == '{' || ch == '[') {
            stack.push({ch, line, column});
        } 
        // Si es cierre, verificamos coincidencia
        else if (ch == ')' || ch == '}' || ch == ']') {
            if (stack.isEmpty()) {
                std::cout << "[Error de Sintaxis] Se encontro '" << ch 
                          << "' sin apertura correspondiente en Linea " << line 
                          << ", Columna " << column << ".\n";
                return false;
            }

            SymbolInfo topSymbol = stack.top();
            char open = topSymbol.symbol;

            if ((ch == ')' && open == '(') ||
                (ch == '}' && open == '{') ||
                (ch == ']' && open == '[')) {
                stack.pop();
            } else {
                std::cout << "[Error de Sintaxis] Delimitador '" << ch 
                          << "' en Linea " << line << ", Columna " << column 
                          << " no coincide con '" << open 
                          << "' (abierto en Linea " << topSymbol.line << ", Columna " << topSymbol.column << ").\n";
                return false;
            }
        }
    }

    if (!stack.isEmpty()) {
        SymbolInfo unclosed = stack.top();
        std::cout << "[Error de Sintaxis] Simbolo '" << unclosed.symbol 
                  << "' en Linea " << unclosed.line << ", Columna " << unclosed.column 
                  << " no fue cerrado correctamente.\n";
        return false;
    }

    std::cout << "[Éxito] El codigo activo tiene sus delimitadores ('()', '{}', '[]') balanceados correctamente.\n";
    return true;
}