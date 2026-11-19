import csv
from pathlib import Path

from staff_sorts_bench.benchmark import BenchmarkResult, SortType


HEADERS = ["Sort", "Dataset", "Size", "Time (sec)", "Comparisons", "Swaps", "Iterations"]


def show_results(results: dict[SortType, list[BenchmarkResult]]) -> None:
    rows = []

    for sort_type, benchmark_results in results.items():
        for result in benchmark_results:
            rows.append([
                sort_type.label,
                result.dataset_type.label,
                str(result.size),
                f"{result.elapsed_seconds:.6f}",
                str(result.stats.comparisons),
                str(result.stats.swaps),
                str(result.stats.iterations),
            ])

    if not rows:
        print("No results")
        return

    widths = [max(len(cell) for cell in column) for column in zip(HEADERS, *rows)]

    print("  ".join(header.ljust(width) for header, width in zip(HEADERS, widths)))

    for row in rows:
        cells = [
            cell.ljust(width)
            for index, (cell, width) in enumerate(zip(row, widths))
        ]
        print("  ".join(cells))


def save_results_csv(results: dict[SortType, list[BenchmarkResult]], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        for sort_type, benchmark_results in results.items():
            for result in benchmark_results:
                writer.writerow([
                    sort_type.label,
                    result.dataset_type.label,
                    result.size,
                    result.elapsed_seconds,
                    result.stats.comparisons,
                    result.stats.swaps,
                    result.stats.iterations,
                ])
