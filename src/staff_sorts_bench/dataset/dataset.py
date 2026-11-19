import random

"""
Задачи работы:
    ... ...
    
    2. Провести тестирование реализованных алгоритмов на наборах данных разного размера и структуры:
        * случайные данные; 
        * отсортированные данные (по возрастанию/убыванию); 
        * частично отсортированные данные; 
        * данные с большим количеством повторяющихся элементов
"""


def generate_random(size: int, rng: random.Random | None = None) -> list[int]:
    """Случайные данные"""
    _validate_size(size)
    rng = rng or random.Random()
    return [rng.randint(1, size) for _ in range(size)]


def generate_asc(size: int) -> list[int]:
    """По возрастанию"""
    _validate_size(size)
    return list(range(1, size + 1))


def generate_desc(size: int) -> list[int]:
    """По убыванию"""
    _validate_size(size)
    return list(range(size, 0, -1))


def generate_half_sorted(size: int, change_percent: float = 10, rng: random.Random | None = None) -> list[int]:
    """Частично отсортированный массив"""
    if not 0 <= change_percent <= 100:
        raise ValueError("Percent must be between 0 and 100")

    data = generate_asc(size)
    rng = rng or random.Random()

    pair_count = int(size * change_percent / 100 / 2)

    for pair_index in rng.sample(range(size // 2), pair_count):
        left = 2 * pair_index
        data[left], data[left + 1] = data[left + 1], data[left]
    return data


def generate_duplicates(size: int, duplicate_percent: float = 50, rng: random.Random | None = None) -> list[int]:
    """данные с большим количеством повторяющихся элементов"""
    _validate_size(size)
    if not 0 <= duplicate_percent < 100:
        raise ValueError("duplicate_percent must be between 0 and 100 but not include 100")

    rng = rng or random.Random()

    duplicate_count = int(size * duplicate_percent / 100)
    unique_count = size - duplicate_count

    data = list(range(1, unique_count + 1))

    if duplicate_count > 0:
        data.extend(rng.choices(data, k=duplicate_count))

    rng.shuffle(data)
    return data


def _validate_size(size: int) -> None:
    if size < 0:
        raise ValueError("Array size must be positive")
