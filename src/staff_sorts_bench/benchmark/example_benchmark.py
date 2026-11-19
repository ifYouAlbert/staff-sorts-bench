import random

from staff_sorts_bench.benchmark import DatasetType, SortType, run_benchmark, BenchmarkConfig


def main() -> None:
    output = run_benchmark(BenchmarkConfig(
        sort_types=[SortType.BUBBLE, SortType.QUICK],
        dataset_types=[DatasetType.RANDOM, DatasetType.DUPLICATES],
        sizes=[100, 1000],
        rng=random.Random(42)
    ))

    print("Total benchmark time (seconds):", output.total_elapsed_seconds)

    for sort_type, benchmark_results in output.results.items():
        print()
        print(f"* {sort_type.name}:")
        for result in benchmark_results:
            print("\t * Dataset:", result.dataset_type.name)
            print("\t\t * Size:", result.size)
            print("\t\t * Time (seconds):", result.elapsed_seconds)
            print("\t\t * Stats:")
            print("\t\t\t * comparisons:", result.stats.comparisons)
            print("\t\t\t * swaps:", result.stats.swaps)
            print("\t\t\t * iterations:", result.stats.iterations)


if __name__ == "__main__":
    main()
