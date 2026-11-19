from dataclasses import dataclass

"""
Задачи работы:
    1. Реализовать на выбранном языке программирования следующие алгоритмы сортировки:
        * пузырьковая сортировка (Bubble Sort);
        * сортировка выбором (Selection Sort); 
        * сортировка вставками (Insertion Sort); 
        * быстрая сортировка (Quick Sort); 
        * сортировка слиянием (Merge Sort).
    
    ... ...

    3. Измерить и сравнить
        * время выполнения каждого алгоритма; 
        * количество сравнений и перестановок элементов; 
        * количество итераций.
"""


@dataclass
class SortStats:
    comparisons: int = 0
    swaps: int = 0
    iterations: int = 0


def bubble_sort(data: list[int]) -> SortStats:
    stats = SortStats()
    for end in range(len(data) - 1, 0, -1):
        stats.iterations += 1
        swapped = False
        for j in range(end):
            stats.iterations += 1
            stats.comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                stats.swaps += 1
                swapped = True
        if not swapped:
            break
    return stats


def selection_sort(data: list[int]) -> SortStats:
    stats = SortStats()
    for i in range(len(data) - 1):
        stats.iterations += 1
        minimum = i
        for j in range(i + 1, len(data)):
            stats.iterations += 1
            stats.comparisons += 1
            if data[j] < data[minimum]:
                minimum = j
        if minimum != i:
            data[i], data[minimum] = data[minimum], data[i]
            stats.swaps += 1
    return stats


def insertion_sort(data: list[int]) -> SortStats:
    stats = SortStats()
    for i in range(1, len(data)):
        stats.iterations += 1
        key = data[i]
        j = i - 1
        while j >= 0:
            stats.iterations += 1
            stats.comparisons += 1
            if data[j] <= key:
                break
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return stats


def quick_sort(data: list[int]) -> SortStats:
    stats = SortStats()
    if len(data) < 2:
        return stats

    pending = [(0, len(data) - 1)]
    while pending:
        stats.iterations += 1
        low, high = pending.pop()
        pivot = data[(low + high) // 2]
        left, right = low, high

        while left <= right:
            stats.iterations += 1
            # Считаем также сравнения, остановившие поиск с каждой стороны.
            while True:
                stats.iterations += 1
                stats.comparisons += 1
                if data[left] >= pivot:
                    break
                left += 1
            while True:
                stats.iterations += 1
                stats.comparisons += 1
                if data[right] <= pivot:
                    break
                right -= 1

            if left <= right:
                if left != right:
                    data[left], data[right] = data[right], data[left]
                    stats.swaps += 1
                left += 1
                right -= 1

        if low < right:
            pending.append((low, right))
        if left < high:
            pending.append((left, high))
    return stats


def merge_sort(data: list[int]) -> SortStats:
    stats = SortStats()
    if len(data) < 2:
        return stats
    buffer = [0] * len(data)

    def sort_range(start: int, end: int) -> None:
        if end - start < 2:
            return
        middle = (start + end) // 2
        sort_range(start, middle)
        sort_range(middle, end)

        left, right, target = start, middle, start
        while left < middle and right < end:
            stats.iterations += 1
            stats.comparisons += 1
            if data[left] <= data[right]:
                buffer[target] = data[left]
                left += 1
            else:
                buffer[target] = data[right]
                right += 1
            target += 1

        while left < middle:
            stats.iterations += 1
            buffer[target] = data[left]
            left += 1
            target += 1
        while right < end:
            stats.iterations += 1
            buffer[target] = data[right]
            right += 1
            target += 1
        for i in range(start, end):
            stats.iterations += 1
            data[i] = buffer[i]

    sort_range(0, len(data))
    return stats
