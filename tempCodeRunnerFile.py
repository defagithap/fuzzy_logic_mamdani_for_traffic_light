Plot 2: Improvement Percentage
plt.figure(figsize=(8, 5))
plt.bar(df_eval['metric'], df_eval['improvement_%'])
plt.xticks(rotation=30, ha='right')
plt.ylabel('Improvement (%)')
plt.title('Improvement Percentage by Metric')
plt.tight_layout()
plt.show()

# 2. Plot time series Average Waiting Time per step
plt.figure(figsize=(10,6))
plt.plot(waiting_base['step'], waiting_base['waiting'], label='Baseline', linewidth=1)
plt.plot(waiting_ctrl['step'], waiting_ctrl['waiting'], label='Controlled', linewidth=1)

# 3. (Opsional) Tambahkan garis rolling‐average 50‐step untuk smoothing
waiting_base['smoothed'] = waiting_base['waiting'].rolling(window=50, min_periods=1).mean()
waiting_ctrl['smoothed'] = waiting_ctrl['waiting'].rolling(window=50, min_periods=1).mean()
plt.plot(waiting_base['step'], waiting_base['smoothed'], 
         label='Baseline (rolling 50)', linestyle='--', linewidth=2)
plt.plot(waiting_ctrl['step'], waiting_ctrl['smoothed'], 
         label='Controlled (rolling 50)', linestyle='--', linewidth=2)

# 4. Formatting plot
plt.xlabel('Cycle (step)')
plt.ylabel('Average Waiting Time (s)')
plt.title('Average Waiting Time per Cycle')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()

# 5. Tampilkan
plt.show()