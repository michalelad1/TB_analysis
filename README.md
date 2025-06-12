# TB-Fast-Analysis

**TB-Fast-Analysis** is a Python-based toolkit designed for the rapid analysis of test beam data, particularly focusing on multilayer pixel detectors. Its primary goal is to facilitate quick, in-testbeam sanity-checking of collected data.

## Installation

To get started with the TB-Fast-Analysis toolkit, follow these setup instructions:

1.  **Python Environment:** Ensure you have Python 3.6 or a newer version installed on your system.

2.  **Install Required Packages:** Install all necessary Python libraries using `pip`:

    ```bash
    pip install pandas numpy matplotlib uproot pyarrow
    ```

3.  **Clone the Repository:** Clone the TB-Fast-Analysis repository to your local machine using Git and navigate into the project directory:

    ```bash
    git clone [https://github.com/michalelad1/TB-Fast-Analysis.git](https://github.com/michalelad1/TB-Fast-Analysis.git)
    cd TB-Fast-Analysis
    ```

## Usage

The main analytical workflow is managed by the `main.py` script.

1.  **Data File Placement:** Before running the analysis, ensure that your test beam data file is placed in the **parent directory** of the `TB-Fast-Analysis` folder (i.e., one level up from where the `TB-Fast-Analysis` directory resides).

2.  **Execute Analysis:** Run the main analysis script from within the `TB-Fast-Analysis` directory using Python.

    ```bash
    python main.py [run_number]
    ```
If no run number is provided, the script will scan through ALL matching files in the directory.

