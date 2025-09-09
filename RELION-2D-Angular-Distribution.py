import starfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --------- USER PARAMETERS ---------
star_file = r"run_data.star"
dynamic_bins = True       # auto-adjust bin numbers based on particle count
scaling_factor_az = 3     # scaling factor for elevation bins (~3 for large (>100,000 particles) cryo-EM datasets, ~5 for small (<30,000 particles) negative stain EM datasets)
scaling_factor_el = 3    # scaling factor for elevation bins (~3 for large (>100,000 particles) cryo-EM datasets, ~5 for small (<30,000 particles) negative stain EM datasets)
show_grid = True
output_plot = "Angular_Distribution_2D.png"
# ----------------------------------

# --- 1. Read STAR file ---
data_dict = starfile.read(star_file)
if isinstance(data_dict, dict):
    if 'particles' in data_dict:
        data = data_dict['particles']
    else:
        raise ValueError("No 'particles' table found in STAR file")
else:
    data = data_dict

# --- 2. Check required columns ---
required_cols = ['rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']
for col in required_cols:
    if col not in data.columns:
        raise ValueError(f"{col} not found in STAR file")

# --- 3. Convert Euler angles to unit vectors ---
def euler_to_vector(phi, theta, psi):
    """Convert ZYZ Euler angles (degrees) to particle viewing vector (x,y,z)."""
    phi = np.deg2rad(phi)
    theta = np.deg2rad(theta)
    psi = np.deg2rad(psi)

    Rz_phi = np.array([[ np.cos(phi), -np.sin(phi), 0],
                       [ np.sin(phi),  np.cos(phi), 0],
                       [          0,           0, 1]])
    
    Ry_theta = np.array([[ np.cos(theta), 0, np.sin(theta)],
                         [             0, 1,            0],
                         [-np.sin(theta), 0, np.cos(theta)]])
    
    Rz_psi = np.array([[ np.cos(psi), -np.sin(psi), 0],
                       [ np.sin(psi),  np.cos(psi), 0],
                       [          0,           0, 1]])
    
    R = Rz_phi @ Ry_theta @ Rz_psi
    vector = R @ np.array([0,0,1])
    return vector

# --- 4. Compute vectors for all particles ---
phi_vals = data['rlnAngleRot'].to_numpy(dtype=float)
theta_vals = data['rlnAngleTilt'].to_numpy(dtype=float)
psi_vals = data['rlnAnglePsi'].to_numpy(dtype=float)

vectors = np.array([euler_to_vector(phi, theta, psi)
                    for phi, theta, psi in zip(phi_vals, theta_vals, psi_vals)])

# --- 5. Convert vectors to spherical coordinates ---
x, y, z = vectors[:,0], vectors[:,1], vectors[:,2]
azimuth = np.arctan2(y, x)        # -π → π
elevation = np.arcsin(z)          # -π/2 → π/2

num_particles = len(azimuth)

# --- 6. Determine number of bins dynamically ---
if dynamic_bins:
    num_bins_az = max(10, int(np.sqrt(num_particles) / scaling_factor_az))
    num_bins_el = max(10, int(np.sqrt(num_particles) / scaling_factor_el))
else:
    num_bins_az = 90
    num_bins_el = 45

print(f"Using {num_bins_az} azimuth bins and {num_bins_el} elevation bins")

# --- 7. Compute 2D histogram (raw counts) ---
H, xedges, yedges = np.histogram2d(
    azimuth,
    elevation,
    bins=[num_bins_az, num_bins_el],
    range=[[-np.pi, np.pi], [-np.pi/2, np.pi/2]]
)

# --- 8. Plot 2D heatmap with log-scaled coloring ---
plt.figure(figsize=(10,6))
im = plt.imshow(
    H.T,
    origin='lower',
    extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    aspect='auto',
    cmap='jet',
    norm=LogNorm(vmin=1, vmax=H.max())  # Log scale, avoids log(0)
)
plt.colorbar(im, label="Number of particles")
plt.xlabel("Azimuth")
plt.ylabel("Elevation")
plt.title("Angular Distribution")  # Updated title

# --- 9. Major ticks with π labels ---
# X-axis: -π, -3π/4, -π/2, -π/4, 0, π/4, π/2, 3π/4, π
x_ticks = [-np.pi, -3*np.pi/4, -np.pi/2, -np.pi/4, 0,
           np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
x_labels = [r"$-\pi$", r"$-3\pi/4$", r"$-\pi/2$", r"$-\pi/4$", "0",
            r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"]
plt.xticks(x_ticks, x_labels)

# Y-axis: π/2, π/4, 0, -π/4, -π/2
y_ticks = [np.pi/2, np.pi/4, 0, -np.pi/4, -np.pi/2]
y_labels = [r"$\pi/2$", r"$\pi/4$", "0", r"$-\pi/4$", r"$-\pi/2$"]
plt.yticks(y_ticks, y_labels)

# Optional grid
if show_grid:
    plt.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.show()

# --- 10. Verify particle count ---
total_from_histogram = H.sum()
print(f"Total particles counted in histogram: {total_from_histogram}")
print(f"Original number of particles: {num_particles}")

# --- 11. Automatic check ---
if total_from_histogram != num_particles:
    print("WARNING: Histogram particle count does not match original number of particles!")
else:
    print("All particles accounted for in histogram.")
