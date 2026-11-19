import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from staff_sorts_bench.benchmark import DatasetType, SortType


SORTS: dict[SortType, tuple[str, str]] = {
    SortType.BUBBLE: ("Пузырьковая", "#0072B2"),
    SortType.SELECTION: ("Выбором", "#E69F00"),
    SortType.INSERTION: ("Вставками", "#009E73"),
    SortType.QUICK: ("Быстрая", "#CC79A7"),
    SortType.MERGE: ("Слиянием", "#687580"),
}
DATASETS: dict[DatasetType, str] = {
    DatasetType.RANDOM: "Случайный",
    DatasetType.ASC: "По возрастанию",
    DatasetType.DESC: "По убыванию",
    DatasetType.HALF_SORTED: "Наполовину отсортированный",
    DatasetType.DUPLICATES: "С повторениями",
}


def read_results_csv(path: Path) -> dict[int, dict[tuple[SortType, DatasetType], float]]:
    times: dict[int, dict[tuple[SortType, DatasetType], float]] = {}
    sort_types = {
        sort.label: sort for sort in SORTS
    }
    dataset_types: dict[str, DatasetType] = {
        dataset.label: dataset for dataset in DATASETS
    }

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    for row in csv.DictReader(lines):
        size = int(row["Size"])
        elapsed = float(row["Time (sec)"])
        sort = sort_types[row["Sort"]]
        dataset = dataset_types[row["Dataset"]]

        key = (sort, dataset)
        benchmark_results = times.setdefault(size, {})
        if key in benchmark_results:
            raise ValueError(f"Duplicate result: {key}, N={size}")
        benchmark_results[key] = elapsed
    if not times:
        raise ValueError("CSV contains no results")
    return times


def save_time_chart(
    size: int,
    benchmark_results: dict[tuple[SortType, DatasetType], float],
    path: Path,
) -> None:
    figure, axis = plt.subplots(figsize=(12, 7))
    width = 0.15
    center = (len(SORTS) - 1) / 2

    for index, (sort, (label, color)) in enumerate(SORTS.items()):
        positions = [i + (index - center) * width for i in range(len(DATASETS))]
        values = [benchmark_results[sort, dataset] for dataset in DATASETS]
        axis.bar(positions, values, width=width, color=color, label=label)

    axis.set_yscale("log")
    axis.set_ylabel("Время в секундах (логарифмическая шкала)")
    axis.set_xticks(range(len(DATASETS)), DATASETS.values())
    axis.set_title(f"Время сортировки по типам датасетов, N = {size:,}", pad=45)
    axis.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=5)
    axis.set_axisbelow(True)
    axis.grid(axis="y", alpha=0.3)
    figure.tight_layout()

    figure.savefig(path, dpi=160)
    plt.close(figure)


def save_time_charts(csv_path: Path, output_dir: Path) -> list[Path]:
    times = read_results_csv(csv_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    for size, results in sorted(times.items()):
        path = output_dir / f"sorts-bench-n{size}.png"
        save_time_chart(size, results, path)
        paths.append(path)

    return paths


def main() -> None:
    p_output_dir = Path(__file__).resolve().parents[3] / "output"
    p_csv_results = p_output_dir / "results.csv"

    for path in save_time_charts(p_csv_results, p_output_dir):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
