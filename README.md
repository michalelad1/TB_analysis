# TB_analysis

**TB_analysis** is a Python-based toolkit designed for the rapid analysis of test beam data, particularly focusing on multilayer pixel detectors. Its primary goal is to facilitate quick, in-testbeam sanity-checking of collected data.

## Installation

To get started with the TB_analysis toolkit, follow these setup instructions:

1.  **Python Environment:** Ensure you have Python 3.6 or a newer version installed on your system.

2.  **Install Required Packages:** Install all necessary Python libraries using `pip`:

    ```bash
    pip install pandas numpy matplotlib uproot pyarrow awkward
    ```

3.  **Clone the Repository:** Clone the TB_analysis repository to your local machine using Git and navigate into the project directory:

    ```bash
    git clone https://github.com/michalelad1/TB_analysis.git
    ```

## Usage

### Merging DUT and Telescope Data

The merging workflow is managed by the `merge_sentel.py` script.

#### Input Files

Place the following files in the correct subdirectories:

- **DUT file:**  
  `./detector/Converted/ZS_Data/TB_FIRE_<run_number>_hits.root`  
  Example: `./detector/Converted/ZS_Data/TB_FIRE_1025_hits.root`

- **Telescope file:**  
  `./telescope/run_<run_number}_telescope.root`  
  Example: `./telescope/run_1025_telescope.root`

These files must contain the following trees:
- DUT: tree named `"Hits"`
- Telescope: tree named `"TrackingInfo/Tracks"`

#### Running the Script

From the project directory, run:

```bash
python -m TB_analysis.dut_tele_sync_merge.merge_sentel -r [run_number]
# Example: python -m TB_analysis.dut_tele_sync_merge.merge_sentel -r 1025
```

- The `-r` or `--runnum` argument is required and specifies the run number to process.
- The script will look for the input files in the directories as described above.

#### Output

The merged ROOT file will be created in the directory `./merged_dut_tele/` as:

```
TB25_Run_<run_number>.root
```
Example: `TB25_Run_1025.root`

This file contains the merged tree (`HitTracks`) with all synchronized branches from both input files.

#### Notes

- The script automatically handles both scalar and jagged (vector-like) branches.
- After writing, it verifies the number of entries and branches in the output file and prints the branch names.
- Make sure all dependencies (`uproot`, `awkward`, `numpy`, `matplotlib`, and your local `io_funcs.py` and `utils.py`) are installed and accessible.
- The script expects the input files to be present and named exactly as described above.

### Other Analysis

The main analytical workflow is managed by the `main.py` script.

1.  **Data File Placement:** Ensure that your test beam data file is placed in the **same directory** as you've placed the `TB_Analysis` folder.

2.  **Execute Analysis:** Run the main analysis script from within the directory in which `TB_analysis` is.

    ```bash
    python -m TB_analysis.plot_dut_data.main -r [run_number]
    ```

If no run number is provided, the script will scan through ALL matching files in the directory.

