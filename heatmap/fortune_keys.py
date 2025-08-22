import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from config.config import db_config

# --- Config ---


if __name__ == "__main__":
    TABLE_NAME = 'fortune_keys'
    STEP = 3_000_000
    MAX_ID = 308_915_776

    # --- Connect to DB ---
    conn = mysql.connector.connect(**db_config['prod'])
    cursor = conn.cursor()

    percentages = []

    print("Querying blocks...")

    # --- Fetch Data ---
    for start_id in range(0, MAX_ID, STEP):
        end_id = start_id + STEP
        cursor.execute(f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
            WHERE status = 1 AND id > {start_id} AND id <= {end_id}
        """)
        count_status_1 = cursor.fetchone()[0]
        percentage = count_status_1 / STEP
        percentages.append(percentage)

    print(f"Fetched {len(percentages)} blocks.")

    cursor.close()
    conn.close()

    # --- Prepare Grid (reshape and pad if needed) ---
    grid_size = 100
    total_cells = grid_size * grid_size

    # Pad with zeros if not enough blocks
    if len(percentages) < total_cells:
        percentages.extend([0] * (total_cells - len(percentages)))
    elif len(percentages) > total_cells:
        percentages = percentages[:total_cells]

    # Reshape to 100x100
    grid_data = np.array(percentages).reshape((grid_size, grid_size))

    # --- Plot the Grid ---
    plt.figure(figsize=(10, 10))
    plt.imshow(grid_data, cmap='RdYlGn_r', vmin=0, vmax=1)  # Red to Green
    plt.colorbar(label='Active % (status = 1)')
    plt.title('Fortune Key Activity Heatmap (Red = High)')
    plt.axis('off')
    plt.show()
