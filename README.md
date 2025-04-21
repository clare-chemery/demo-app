# The Lego Challenge

A Python-based demo application using the Preswald library.

To run the app locally, install dependencies, navigate to the app subdirectory and then use the `preswald` command:

```{bash}
$ uv sync
$ cd app
$ preswald run
```

## Project Structure

This project is configured using `uv` for managing package dependencies which results in some `uv` generated/edited top-level
files. Only this README.md and the pyproject.toml should be edited manually.

### 1. App

The structure of the `app/` subdirectory is taken from the `preswald` library. It contains:
* `preswald.toml`: project config and styling
* `main.py`: main script of the app
* `data/lego_pile_reduced.csv`: cleaned data to be used by the app 
* `images/`: image files referenced in the styling file


### 2. Preprocess

This directory contains the code used to preprocess the raw data from Rebrickable into a dataset tailored for the app's use case.

The raw data files and their documentation can be found at `preprocess/raw_data/rebrickable/`.
