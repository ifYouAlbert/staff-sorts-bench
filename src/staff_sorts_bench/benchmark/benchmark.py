import random
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from time import perf_counter

from staff_sorts_bench.dataset import generate_random, generate_asc, generate_desc, generate_half_sorted, generate_duplicates
from staff_sorts_bench.sorts import SortStats, bubble_sort, selection_sort, insertion_sort, quick_sort, merge_sort


class SortType(Enum):
    BUBBLE = ("bubble", bubble_sort)
    SELECTION = ("selection", selection_sort)
    INSERTION = ("insertion", insertion_sort)
    QUICK = ("quick", quick_sort)
    MERGE = ("merge", merge_sort)

    def __init__(self, label: str, function: Callable[[list[int]], SortStats]):
        self.label = label
        self.function = function


class DatasetType(Enum):
    RANDOM = ("random", generate_random)
    ASC = ("asc", generate_asc)
    DESC = ("desc", generate_desc)
    HALF_SORTED = ("half_sorted", generate_half_sorted)
    DUPLICATES = ("duplicates", generate_duplicates)

    def __init__(self, label: str, function: Callable[..., list[int]]):
        self.label = label
        self.function = function

    def generate(self, size: int, rng: random.Random | None = None) -> list[int]:
        if self in (DatasetType.ASC, DatasetType.DESC):
            return self.function(size)
        return self.function(size, rng=rng)


@dataclass
class BenchmarkConfig:
    sort_types: list[SortType]
    dataset_types: list[DatasetType]
    sizes: list[int]
    rng: random.Random | None = None


@dataclass
class BenchmarkResult:
    dataset_type: DatasetType
    size: int
    elapsed_seconds: float
    stats: SortStats


@dataclass
class BenchmarkOutput:
    total_elapsed_seconds: float
    results: dict[SortType, list[BenchmarkResult]]


def run_benchmark(conf: BenchmarkConfig) -> BenchmarkOutput:
    benchmark_start = perf_counter()
    results: dict[SortType, list[BenchmarkResult]] = {sort_type: [] for sort_type in conf.sort_types}
    rng = conf.rng or random.Random()

    for size in conf.sizes:
        for dataset_type in conf.dataset_types:
            original = dataset_type.generate(size, rng=rng)
            expected = sorted(original)

            for sort_type, bench_results in results.items():
                data = original.copy()

                start = perf_counter()
                stats = sort_type.function(data)
                elapsed_seconds = perf_counter() - start

                if data != expected:
                    raise ValueError(
                        f"{sort_type.name} produced an incorrect result "
                        f"for {dataset_type.name}, size={size}"
                    )

                bench_results.append(
                    BenchmarkResult(
                        dataset_type=dataset_type,
                        size=size,
                        elapsed_seconds=elapsed_seconds,
                        stats=stats
                    )
                )

    return BenchmarkOutput(
        total_elapsed_seconds=perf_counter() - benchmark_start,
        results=results,
    )
