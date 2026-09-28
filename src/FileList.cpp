#include "../include/FileList.h"
#include <iostream>

FileList::FileList() : head(nullptr), tail(nullptr), activeFile(nullptr), nextId(1) {}

FileList::~FileList() {
    clear();
}

void FileList::clear() {
    FileNode* current = head;
    while (current != nullptr) {
        FileNode* temp = current;
        current = current->next;
        delete temp;
    }
    head = nullptr;
    tail = nullptr;
    activeFile = nullptr;
}

bool FileList::createFile(const std::string& filename, const std::string& initialContent) {
    // Verificar si el archivo ya existe
    FileNode* temp = head;
    while (temp != nullptr) {
        if (temp->filename == filename) {
            std::cout << "[Error] El archivo '" << filename << "' ya existe.\n";
            return false;
        }
        temp = temp->next;
    }

    FileNode* newNode = new FileNode(nextId++, filename, initialContent);

    if (head == nullptr) {
        head = tail = newNode;
    } else {
        tail->next = newNode;
        newNode->prev = tail;
        tail = newNode;
    }

    // Si es el primer archivo creado, se establece automáticamente como activo
    if (activeFile == nullptr) {
        newNode->isActive = true;
        activeFile = newNode;
    }

    std::cout << "[Éxito] Archivo '" << filename << "' creado correctamente.\n";
    return true;
}

void FileList::listFiles() const {
    if (head == nullptr) {
        std::cout << "[Info] No hay archivos abiertos en la sesión.\n";
        return;
    }

    std::cout << "\n=== ARCHIVOS ABIERTOS ===\n";
    FileNode* current = head;
    while (current != nullptr) {
        std::cout << "ID: " << current->id 
                  << " | Nombre: " << current->filename 
                  << " | Estado: " << (current->isActive ? "[ACTIVO]" : "Inactivo") 
                  << "\n";
        current = current->next;
    }
    std::cout << "=========================\n\n";
}

bool FileList::switchActiveFile(const std::string& identifier) {
    FileNode* current = head;
    FileNode* foundNode = nullptr;

    while (current != nullptr) {
        if (std::to_string(current->id) == identifier || current->filename == identifier) {
            foundNode = current;
            break;
        }
        current = current->next;
    }

    if (foundNode == nullptr) {
        std::cout << "[Error] No se encontró el archivo: " << identifier << "\n";
        return false;
    }

    if (activeFile != nullptr) {
        activeFile->isActive = false;
    }

    foundNode->isActive = true;
    activeFile = foundNode;
    std::cout << "[Éxito] Cambiado a archivo activo: " << activeFile->filename << "\n";
    return true;
}

bool FileList::deleteFile(const std::string& identifier) {
    FileNode* current = head;

    while (current != nullptr) {
        if (std::to_string(current->id) == identifier || current->filename == identifier) {
            
            if (current->prev != nullptr) {
                current->prev->next = current->next;
            } else {
                head = current->next;
            }

            if (current->next != nullptr) {
                current->next->prev = current->prev;
            } else {
                tail = current->prev;
            }

            if (current == activeFile) {
                activeFile = (head != nullptr) ? head : nullptr;
                if (activeFile != nullptr) {
                    activeFile->isActive = true;
                }
            }

            std::cout << "[Éxito] Archivo '" << current->filename << "' eliminado y memoria liberada.\n";
            delete current;
            return true;
        }
        current = current->next;
    }

    std::cout << "[Error] No se encontró el archivo para eliminar: " << identifier << "\n";
    return false;
}

FileNode* FileList::getActiveFile() const {
    return activeFile;
}