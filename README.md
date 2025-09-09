# RELION-2D-AngleDistribution

**Angular Distribution 2D Heatmap from RELION STAR File**

This Python script generates a 2D angular distribution heatmap from a RELION run_data.star file. It visualizes the distribution of particle orientations in terms of azimuth and elevation, providing a quick way to assess angular coverage in cryo-EM datasets (similar to cryoSPARC).

---

## Features

-Reads Euler angles (`rlnAngleRot`, `rlnAngleTilt`, `rlnAnglePsi`) from a RELION STAR file.
-Converts Euler angles to particle viewing vectors and then to azimuth/elevation coordinates.
-Creates a 2D histogram of particle orientations.
-Plots a **log-scaled heatmap** to emphasize both low- and high-density regions.
-Automatically computes the number of bins based on particle count (dynamic binning).
-Optional grid lines for better visual reference.
-X-axis and Y-axis labeled with **π-based notation**.
-Automatically verifies that all particles are accounted for in the histogram.
-Saves the heatmap as a PNG image.

---

## Usage
1. Install dependencies:
```bash
pip install starfile numpy matplotlib
```

2. Update the script's user parameters:
```python
star_file = r"path_to_your_run_data.star"
dynamic_bins = True        # auto-adjust bin numbers
scaling_factor_az = 5      # azimuth bin scaling (~3 for larger Cryo-EM datasets, ~5 for smaller negative stain datasets)
scaling_factor_el = 5      # elevation bin scaling (~3 for larger Cryo-EM datasets, ~5 for smaller negative stain datasets)
show_grid = True           # show grid lines
output_plot = "Angular_Distribution_2D.png"
```

3. Run the script:
```bash
python RELION-2D-Angular-Distribution.py
```

4. Check the console output to verify particle counts:
```bash
Total particles counted in histogram: XXXX
Original number of particles: XXXX
```


---

## Plot Details

-**Title:** Angular Distribution

-**X-axis (Azimuth):** -π, -3π/4, -π/2, -π/4, 0, π/4, π/2, 3π/4, π

-**Y-axis (Elevation):** π/2, π/4, 0, -π/4, -π/2

-**Colorbar:** Number of particles (log scale)


---

## Example Output

**Scaling factor for azimuth and elevation = 5**

<img width="3000" height="1800" alt="Angular_Distribution_2D" src="https://github.com/user-attachments/assets/5e99b047-d1a7-4ad0-9e06-3ebd53d9c52c" />

**Scaling factor for azimuth and elevation = 3**

<img width="3000" height="1800" alt="Angular_Distribution_2D-Cryo-EM" src="https://github.com/user-attachments/assets/b4886e92-f2b6-4bb4-a7a4-5b3837b18998" />


The heatmap shows areas of high and low particle density, helping to evaluate angular coverage and identify potential orientation biases.


---

## Notes

- Ensure your `run_data.star` or other appropriate `STAR` file contains the `particles` table and the required Euler angle columns (`rlnAngleRot`, `rlnAngleTilt`, `rlnAnglePsi`).
- **The script works best for `RELION 3.x` and onwards STAR files.**
- Dynamic binning is recommended to adjust bin numbers based on dataset size.
