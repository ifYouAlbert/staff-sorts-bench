from staff_sorts_bench.dataset import generate_random, generate_asc, generate_desc, generate_half_sorted, generate_duplicates


def main() -> None:
    size = 20

    generators = [generate_random, generate_asc, generate_desc, generate_half_sorted, generate_duplicates]

    for generate in generators:
        data = generate(size)

        print()
        print(f"* {generate.__name__}:")
        print("\t * Size:", size)
        print("\t * Data:", data)


if __name__ == "__main__":
    main()
