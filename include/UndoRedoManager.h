#ifndef UNDOREDOMANAGER_H
#define UNDOREDOMANAGER_H

#include "Stack.h"
#include <string>
#include <iostream>

class UndoRedoManager {
private:
    Stack<std::string> undoStack;
    Stack<std::string> redoStack;

public:
    UndoRedoManager() {}

    // Registrar un nuevo estado del texto
    void recordState(const std::string& currentContent) {
        undoStack.push(currentContent);
        redoStack.clear(); // Al hacer un nuevo cambio, se limpia la pila de rehacer
    }

    // Comando undo
    bool undo(std::string& currentContent) {
        if (undoStack.isEmpty()) {
            std::cout << "[Info] No hay cambios para deshacer.\n";
            return false;
        }
        redoStack.push(currentContent);
        currentContent = undoStack.top();
        undoStack.pop();
        std::cout << "[Éxito] Cambio deshecho (Undo).\n";
        return true;
    }

    // Comando redo
    bool redo(std::string& currentContent) {
        if (redoStack.isEmpty()) {
            std::cout << "[Info] No hay cambios para rehacer.\n";
            return false;
        }
        undoStack.push(currentContent);
        currentContent = redoStack.top();
        redoStack.pop();
        std::cout << "[Éxito] Cambio rehecho (Redo).\n";
        return true;
    }

    void clear() {
        undoStack.clear();
        redoStack.clear();
    }
};

#endif // UNDOREDOMANAGER_H