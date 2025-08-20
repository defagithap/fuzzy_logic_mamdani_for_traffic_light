import pandas as pd
from fuzzy_traffic_controller import fuzzy_controller_function

rows = []
for wt in [0, 20, 40, 60, 80, 100, 120]:
    for diff in [-20, -10, 0, 10, 20, 30, 40]:  # diff = green_count - red_count
        # misal kita asumsikan green=10+diff, red=10
        red = 10
        green = max(0, red + diff)
        output = fuzzy_controller_function(
            no_vehicles_in_red_lanes=red,
            no_vehicles_in_green_lanes=green,
            max_waiting_time_in_red_lanes=wt,
            emv_waiting_time_red_lanes=0,
            emv_waiting_time_green_lanes=0,
            emv_current_lane=0,
            emv_other_lane=0
        )
        rows.append({
            'wt_red': wt,
            'green_minus_red': diff,
            'decision': output
        })

df = pd.DataFrame(rows)
# Tampilkan hanya yang decision >= 0.5
print(df[df['decision'] >= 0.5])