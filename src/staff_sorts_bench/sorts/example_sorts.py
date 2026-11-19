from staff_sorts_bench.sorts import bubble_sort, selection_sort, insertion_sort, quick_sort, merge_sort


def main() -> None:
    original = [5, 1, 4, 2, 3, 2]

    algorithms = [bubble_sort, selection_sort, insertion_sort, quick_sort, merge_sort]

    for sort in algorithms:
        data = original.copy()

        stats = sort(data)

        print()
        print(f"* {sort.__name__}:")
        print("\t * Original:", original)
        print("\t * Sorted:", data)
        print("\t * Stats")
        print("\t\t * comparisons:", stats.comparisons)
        print("\t\t * swaps:", stats.swaps)
        print("\t\t * iterations:", stats.iterations)


if __name__ == "__main__":
    main()
