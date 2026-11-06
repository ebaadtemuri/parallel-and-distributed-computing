from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from time import perf_counter


def analyze_file(file_path, keyword):
    text = file_path.read_text(encoding="utf-8-sig", errors="replace")
    matches = text.casefold().count(keyword.casefold()) if keyword else 0

    return {
        "file": str(file_path),
        "words": len(text.split()),
        "matches": matches,
    }


def analyze_serial(file_paths, keyword):
    start_time = perf_counter()
    results = [analyze_file(path, keyword) for path in file_paths]
    elapsed_time = perf_counter() - start_time

    return results, elapsed_time


def analyze_threads(file_paths, keyword):
    start_time = perf_counter()

    with ThreadPoolExecutor() as executor:
        results = list(
            executor.map(analyze_file, file_paths, [keyword] * len(file_paths))
        )

    elapsed_time = perf_counter() - start_time
    return results, elapsed_time


def analyze_processes(file_paths, keyword):
    start_time = perf_counter()

    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(analyze_file, file_paths, [keyword] * len(file_paths))
        )

    elapsed_time = perf_counter() - start_time
    return results, elapsed_time
