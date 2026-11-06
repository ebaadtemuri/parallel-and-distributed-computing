# Chapter 3: Parallel Image Processor

A command-line image batch processor that converts images to grayscale, resizes them to fit within 800x800 pixels, and saves PNG results in a `processed` subfolder. Images are processed with a process pool.

## Requirement

Install Pillow with `py -m pip install Pillow`.

## Run

From this directory, run `py main.py` and enter a folder containing BMP, JPEG, or PNG images when prompted.

The included `sample_images` folder can be used for a quick test. Processing time depends on the images and computer; process startup overhead can outweigh the benefit for a small batch.
