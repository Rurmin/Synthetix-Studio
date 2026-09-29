class StackNode:

  def __init__(self, data):
    self.data = data
    self.next = None


class Stack:

  def __init__(self):
    self.top_node = None
    self.size = 0

  def push(self, data) -> None:
    new_node = StackNode(data)
    new_node.next = self.top_node
    self.top_node = new_node
    self.size += 1

  def pop(self):
    if self.is_empty():
      return None
    popped_data = self.top_node.data
    self.top_node = self.top_node.next
    self.size -= 1
    return popped_data

  def top(self):
    if self.is_empty():
      return None
    return self.top_node.data

  def is_empty(self) -> bool:
    return self.top_node is None

  def clear(self) -> None:
    self.top_node = None
    self.size = 0