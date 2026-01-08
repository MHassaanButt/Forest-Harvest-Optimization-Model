import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

# 1. Load the Results
df_cp5 = pd.read_csv("results/Final_Results_CP5.csv")
df_cp15 = pd.read_csv("results/Final_Results_CP15.csv")
# df_cp25 = pd.read_csv("results/Final_Results_CP25.csv")


# 2. Helper function to parse the schedule strings back into lists
def parse_schedule(schedule_str):
    return ast.literal_eval(schedule_str)


# 3. Calculate Average Harvest per Year across the whole forest
# We stack all schedules into a big matrix and take the mean of each column (year)
schedules_cp5 = np.stack(df_cp5["Schedule"].apply(parse_schedule).values)
mean_harvest_cp5 = schedules_cp5.mean(axis=0)

schedules_cp15 = np.stack(df_cp15["Schedule"].apply(parse_schedule).values)
mean_harvest_cp15 = schedules_cp15.mean(axis=0)

# schedules_cp25 = np.stack(df_cp25["Schedule"].apply(parse_schedule).values)
# mean_harvest_cp25 = schedules_cp25.mean(axis=0)

# 4. Generate the Plot (Recreating Figure 9)
plt.figure(figsize=(10, 6))

years = range(1, 31)
plt.plot(
    years, mean_harvest_cp5, label="Carbon Price $5 (Low)", color="blue", marker="o"
)
plt.plot(
    years, mean_harvest_cp15, label="Carbon Price $15 (High)", color="red", marker="o"
)
# plt.plot(
#     years, mean_harvest_cp25, label="Carbon Price $25 (High)", color="green", marker="o"
# )

plt.title("Optimal Harvest Dynamics: Low vs. High Carbon Price")
plt.xlabel("Year")
plt.ylabel("Average Harvest (Mg/ha)")
plt.legend()
plt.grid(True, alpha=0.3)

# Save the figure
plt.savefig("results/Replication_Figure_9.png")
plt.show()

# 5. Summary Stats
print("--- Optimization Summary ---")
print(f"Total NPV (CP $5): ${df_cp5['Optimal_NPV'].sum()/1e6:.2f} Million")
print(f"Total NPV (CP $15): ${df_cp15['Optimal_NPV'].sum()/1e6:.2f} Million")
# print(f"Total NPV (CP $25): ${df_cp25['Optimal_NPV'].sum()/1e6:.2f} Million")
print(
    f"Value of Carbon Policy: ${(df_cp15['Optimal_NPV'].sum() - df_cp5['Optimal_NPV'].sum())/1e6:.2f} Million"
)
