import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from config.config import db_config

# --- Config ---
TABLE_NAME = 'fortune_keys'
STEP = 3_000_000
MAX_ID = 308_915_776
GRID_SIZE = 100

if __name__ == "__main__":
    conn = mysql.connector.connect(**db_config['prod'])
    cursor = conn.cursor()

    percentages = []
    active_cells = []  # Track cells with status = 1 > 0

    print("Querying blocks...")

    total_active_keys = 0

    for start_id in range(0, MAX_ID, STEP):
        end_id = start_id + STEP
        cursor.execute(f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
            WHERE status = 1 AND id > {start_id} AND id <= {end_id}
        """)
        count_status_1 = cursor.fetchone()[0]
        total_active_keys += count_status_1
        percentage = count_status_1 / STEP
        percentages.append(percentage)
        active_cells.append(count_status_1 > 0)

    print(f"Fetched {len(percentages)} blocks.")

    print(f"Total active keys (status = 1): {total_active_keys:,}")

    cursor.close()
    conn.close()

    # Pad percentages
    total_cells = GRID_SIZE * GRID_SIZE
    if len(percentages) < total_cells:
        percentages.extend([0] * (total_cells - len(percentages)))
        active_cells.extend([False] * (total_cells - len(active_cells)))
    elif len(percentages) > total_cells:
        percentages = percentages[:total_cells]
        active_cells = active_cells[:total_cells]

    # Reshape to 100x100 grid
    grid_data = np.array(percentages).reshape((GRID_SIZE, GRID_SIZE))
    active_cells = np.array(active_cells).reshape((GRID_SIZE, GRID_SIZE))

    # --- Plot the Grid ---
    plt.figure(figsize=(10, 10))
    plt.imshow(grid_data, cmap='RdYlGn_r', vmin=0, vmax=1)
    plt.colorbar(label='Active % (status = 1)')
    plt.title('Fortune Key Activity Heatmap')

    # Overlay yellow dots on active cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if active_cells[i, j]:
                plt.plot(j, i, 'yo', markersize=1)  # yellow dot

    plt.axis('off')
    plt.show()

