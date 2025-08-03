# TB_analysis

**TB_analysis** is a Python-based toolkit designed for the rapid analysis of test beam data, particularly focusing on multilayer pixel detectors. Its primary goal is to facilitate quick, in-testbeam sanity-checking of collected data.

## Installation

To get started with the TB_analysis toolkit, follow these setup instructions:

1.  **Python Environment:** Ensure you have Python 3.6 or a newer version installed on your system.

2.  **Install Required Packages:** Install all necessary Python libraries using `pip`:

    ```bash
    pip install pandas numpy matplotlib uproot pyarrow awkward
    ```

3.  **Clone the Repository:** Clone the TB-Fast-Analysis repository to your local machine using Git and navigate into the project directory:

    ```bash
    git clone https://github.com/michalelad1/TB_analysis.git
    ```

## Usage

### Merging DUT and Telescope Data

The merging workflow is managed by the `merge_sentel.py` script.

#### Input Files

Place the following files in `./TB_analysis/dut_tele_sync_merge/`:

- **DUT file:**  
  `TB_FIRE_<run_number>_hits.root`  
  Example: `TB_FIRE_1025_hits.root`

- **Telescope file:**  
  `run_<run_number>_telescope.root`  
  Example: `run_1025_telescope.root`

These files must contain the following trees:
- DUT: tree named `"Hits"`
- Telescope: tree named `"TrackingInfo/Tracks"`

#### Running the Script

From the project directory, run:

```bash
python ./TB_analysis/dut_tele_sync_merge/merge_sentel.py
```

You will be prompted to enter the run number (e.g., `1025`).

#### Output

The merged ROOT file will be created in the current directory as:

```
Merged_sentel_run_<run_number>.root
```
Example: `Merged_sentel_run_1025.root`

This file contains the merged tree (`MergedTree`) with all synchronized branches from both input files.

#### Notes

- The script automatically handles jagged arrays and scalar branches.
- After writing, it verifies the number of entries and branches in the output file and prints the branch names.
- Make sure all dependencies (`uproot`, `awkward`, `numpy`, `matplotlib`, and your local `io_funcs.py`) are installed and accessible.

### Other Analysis

The main analytical workflow is managed by the `main.py` script.

1.  **Data File Placement:** Ensure that your test beam data file is placed in the **same directory** as you've placed the `TB_Analysis` folder.

2.  **Execute Analysis:** Run the main analysis script from within the directory in which `TB_analysis` is.

    ```bash
    python -m TB_analysis.plot_dut_data.main -r [run_number]
    ```

If no run number is provided, the script will scan through ALL matching files in the directory.

