#ifndef STACK_H
#define STACK_H

#include <stdexcept>

// Estructura de Nodo para la Pila
template <typename T>
struct StackNode {
    T data;
    StackNode<T>* next;

    StackNode(const T& val) : data(val), next(nullptr) {}
};

// Clase Pila (Stack) dinámica implementada desde cero
template <typename T>
class Stack {
private:
    StackNode<T>* topNode;
    int currentSize;

public:
    Stack() : topNode(nullptr), currentSize(0) {}

    ~Stack() {
        clear();
    }

    void push(const T& value) {
        StackNode<T>* newNode = new StackNode<T>(value);
        newNode->next = topNode;
        topNode = newNode;
        currentSize++;
    }

    void pop() {
        if (isEmpty()) {
            throw std::underflow_error("La pila esta vacia (Underflow)");
        }
        StackNode<T>* temp = topNode;
        topNode = topNode->next;
        delete temp;
        currentSize--;
    }

    T top() const {
        if (isEmpty()) {
            throw std::underflow_error("La pila esta vacia");
        }
        return topNode->data;
    }

    bool isEmpty() const {
        return topNode == nullptr;
    }

    int size() const {
        return currentSize;
    }

    void clear() {
        while (!isEmpty()) {
            pop();
        }
    }
};

#endif // STACK_H