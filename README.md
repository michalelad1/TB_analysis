# TB_analysis

**TB_analysis** is a Python-based toolkit designed for the rapid analysis of test beam data, particularly focusing on multilayer pixel detectors. Its primary goal is to facilitate quick, in-testbeam sanity-checking of collected data.

## Installation

To get started with the TB_analysis toolkit, follow these setup instructions:

1.  **Python Environment:** Ensure you have Python 3.6 or a newer version installed on your system.

2.  **Install Required Packages:** Install all necessary Python libraries using `pip`:

    ```bash
    pip install pandas numpy matplotlib uproot pyarrow
    ```

3.  **Clone the Repository:** Clone the TB-Fast-Analysis repository to your local machine using Git and navigate into the project directory:

    ```bash
    git clone https://github.com/michalelad1/TB_analysis.git
    ```
    
## Usage

The main analytical workflow is managed by the `main.py` script.

1.  **Data File Placement:** Ensure that your test beam data file is placed in the **same directory** as you've placed the `TB_Analysis` folder.

2.  **Execute Analysis:** Run the main analysis script from within the directory in which `TB_analysis` is.

    ```bash
    python -m TB_analysis.plot_dut_data.main -r [run_number]
    ```
If no run number is provided, the script will scan through ALL matching files in the directory.

