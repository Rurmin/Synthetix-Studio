class SortingEngine:

  @staticmethod
  def insertion_sort_by_filename(files_data: list) -> list:
    """Ordena una lista de diccionarios con información de archivos por nombre (A-Z)

    utilizando el algoritmo Insertion Sort.
    """
    sorted_list = files_data.copy()
    for i in range(1, len(sorted_list)):
      key_item = sorted_list[i]
      j = i - 1
      while j >= 0 and sorted_list[j]["filename"].lower() > key_item[
          "filename"
      ].lower():
        sorted_list[j + 1] = sorted_list[j]
        j -= 1
      sorted_list[j + 1] = key_item
    return sorted_list

  @staticmethod
  def quick_sort_by_id(files_data: list) -> list:
    """Ordena una lista de archivos por su ID numérico de menor a mayor

    utilizando el algoritmo QuickSort.
    """
    if len(files_data) <= 1:
      return files_data

    pivot = files_data[len(files_data) // 2]["id"]
    left = [x for x in files_data if x["id"] < pivot]
    middle = [x for x in files_data if x["id"] == pivot]
    right = [x for x in files_data if x["id"] > pivot]

    return (
        SortingEngine.quick_sort_by_id(left)
        + middle
        + SortingEngine.quick_sort_by_id(right)
    )