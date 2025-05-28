# [WIP] TB-Fast-Analysis

**TB-Fast-Analysis** is a Python-based toolkit designed for rapid analysis of test beam data, particularly focusing on multilayer pixel detectors.
Designed for a quick in-testbeam sanity-check of data.

## Features

- **Data Handling**: Efficient loading and manipulation of test beam datasets.
- **Visualization Tools**: Generate plots and summaries for quick insights.
- **Extensible Design**: Modular codebase allows for easy integration of additional analysis routines.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or higher installed. The required Python packages can be installed using `pip`:

```bash
pip install pandas numpy matplotlib uproot pyarrow
```

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/michalelad1/TB-Fast-Analysis.git
cd TB-Fast-Analysis
```

## Usage

The main analysis script is `fast_testbeam_analysis.py`. To execute the analysis:

```bash
python fast_testbeam_analysis.py
```

This script utilizes functions from:

- `df_handling.py`: Functions for loading and preprocessing data.
- `io_funcs.py`: Input/output operations, including reading from and writing to files.

Ensure that the `multilayer_packages.root` data file is present in the parent directory, as it's required for the analysis.

## File Structure

- `fast_testbeam_analysis.py`: Main script orchestrating the analysis workflow.
- `df_handling.py`: Contains functions for data loading and preprocessing.
- `io_funcs.py`: Handles input/output operations.
- `multilayer_packages.root`: ROOT file example.
- `README.md`: Documentation and usage instructions.

