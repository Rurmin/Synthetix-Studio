#ifndef REQUESTQUEUE_H
#define REQUESTQUEUE_H

#include <string>
#include <iostream>

struct RequestNode {
    int id;
    std::string filename;
    std::string codeSnippet;
    RequestNode* next;

    RequestNode(int id, const std::string& file, const std::string& code)
        : id(id), filename(file), codeSnippet(code), next(nullptr) {}
};

class RequestQueue {
private:
    RequestNode* frontNode;
    RequestNode* rearNode;
    int count;
    int nextRequestId;

public:
    RequestQueue() : frontNode(nullptr), rearNode(nullptr), count(0), nextRequestId(1) {}

    ~RequestQueue() {
        clear();
    }

    void enqueue(const std::string& filename, const std::string& codeSnippet) {
        RequestNode* newNode = new RequestNode(nextRequestId++, filename, codeSnippet);
        if (rearNode == nullptr) {
            frontNode = rearNode = newNode;
        } else {
            rearNode->next = newNode;
            rearNode = newNode;
        }
        count++;
        std::cout << "[Cola] Solicitud de analisis #" << newNode->id << " agregada para el archivo '" << filename << "'.\n";
    }

    bool dequeue(RequestNode& outNode) {
        if (isEmpty()) {
            return false;
        }
        RequestNode* temp = frontNode;
        outNode = *temp;
        frontNode = frontNode->next;
        if (frontNode == nullptr) {
            rearNode = nullptr;
        }
        delete temp;
        count--;
        return true;
    }

    void showStatus() const {
        std::cout << "\n=== ESTADO DE LA COLA DE PETICIONES (IA) ===\n";
        std::cout << "Peticiones pendientes en cola: " << count << "\n";
        RequestNode* curr = frontNode;
        while (curr != nullptr) {
            std::cout << "  - Solicitud #" << curr->id << " | Archivo: " << curr->filename << "\n";
            curr = curr->next;
        }
        std::cout << "===========================================\n\n";
    }

    bool isEmpty() const {
        return frontNode == nullptr;
    }

    int size() const {
        return count;
    }

    void clear() {
        while (!isEmpty()) {
            RequestNode dummy(0, "", "");
            dequeue(dummy);
        }
    }
};

#endif // REQUESTQUEUE_H