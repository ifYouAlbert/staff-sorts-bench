import random
from pathlib import Path

from staff_sorts_bench.benchmark import DatasetType, SortType, run_benchmark
from staff_sorts_bench.benchmark.benchmark import BenchmarkConfig
from staff_sorts_bench.show import save_results_csv, show_results


def main() -> None:
    conf = BenchmarkConfig(
        sort_types=[
            SortType.BUBBLE,
            SortType.SELECTION,
            SortType.INSERTION,
            SortType.QUICK,
            SortType.MERGE,
        ],
        dataset_types=[
            DatasetType.RANDOM,
            DatasetType.ASC,
            DatasetType.DESC,
            DatasetType.HALF_SORTED,
            DatasetType.DUPLICATES,
        ],
        sizes=[
            100,
            1_000,
            # 10_000,
            # 100_000
        ],
        rng=random.Random(42),
    )

    print("Sizes:", conf.sizes)
    print("Sorts:", ", ".join(sort_type.label for sort_type in conf.sort_types))
    print("Datasets:", ", ".join(dataset_type.label for dataset_type in conf.dataset_types))
    print("Calculation...")

    output = run_benchmark(conf)

    print()

    p_root_path: Path = Path(__file__).resolve().parents[2]
    p_csv_path: Path = p_root_path / "output" / "results.csv"

    show_results(output.results)
    print(f"Total benchmark time (seconds): {output.total_elapsed_seconds:.6f}")

    save_results_csv(output.results, p_csv_path)
    print()
    print("csv saved: ", p_csv_path)


if __name__ == "__main__":
    main()
