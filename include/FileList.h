#ifndef FILELIST_H
#define FILELIST_H

#include <string>

// Nodo para representar un archivo abierto en la sesión
struct FileNode {
    int id;
    std::string filename;
    std::string content;
    bool isActive;
    
    FileNode* prev;
    FileNode* next;

    FileNode(int id, const std::string& name, const std::string& initialContent)
        : id(id), filename(name), content(initialContent), isActive(false), prev(nullptr), next(nullptr) {}
};

// Clase para administrar la Lista Enlazada de Archivos
class FileList {
private:
    FileNode* head;
    FileNode* tail;
    FileNode* activeFile;
    int nextId;

public:
    FileList();
    ~FileList();

    // Requerimientos del Proyecto (Punto 1):
    bool createFile(const std::string& filename, const std::string& initialContent = ""); // 1. Crear nuevo archivo
    void listFiles() const;                                                                // 2. Listar todos los archivos
    bool switchActiveFile(const std::string& identifier);                                  // 3. Cambiar de archivo activo
    bool deleteFile(const std::string& identifier);                                        // 4. Eliminar liberando memoria

    FileNode* getActiveFile() const;
    void clear();
};

#endif // FILELIST_H