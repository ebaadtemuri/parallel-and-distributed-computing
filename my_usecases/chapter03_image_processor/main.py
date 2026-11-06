import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from time import perf_counter

from PIL import Image, ImageOps


SUPPORTED_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png"}
MAX_IMAGE_SIZE = (800, 800)


def process_image(input_path, output_folder):
    source_path = Path(input_path)
    output_name = (
        f"{source_path.stem}_{source_path.suffix[1:].lower()}_grayscale.png"
    )
    output_path = Path(output_folder) / output_name

    try:
        with Image.open(source_path) as original:
            processed = ImageOps.grayscale(original)
            processed.thumbnail(MAX_IMAGE_SIZE)
            processed.save(output_path, format="PNG")
            processed.close()

        return f"Processed: {source_path.name} -> {output_path.name}"
    except OSError as error:
        return f"Skipped: {source_path.name} ({error})"


def main():
    folder_text = input("Enter the image folder path: ").strip().strip('"')
    input_folder = Path(folder_text)

    if not input_folder.is_dir():
        print("That folder does not exist.")
        return

    image_paths = sorted(
        path
        for path in input_folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_paths:
        print("No supported images found.")
        return

    output_folder = input_folder / "processed"
    output_folder.mkdir(exist_ok=True)

    worker_count = min(len(image_paths), os.cpu_count() or 1)
    print(f"Processing {len(image_paths)} image(s) with {worker_count} process(es).")

    start_time = perf_counter()

    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        results = executor.map(
            process_image,
            [str(path) for path in image_paths],
            [str(output_folder)] * len(image_paths),
        )

        for result in results:
            print(result)

    elapsed_time = perf_counter() - start_time
    print(f"Finished in {elapsed_time:.3f} seconds.")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()
