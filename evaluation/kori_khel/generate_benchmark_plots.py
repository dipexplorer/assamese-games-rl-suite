import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

PLOTS_DIR = os.path.join(PROJECT_ROOT, "evaluation", "kori_khel", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Set clean matplotlib styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 1.2,
    'grid.color': '#eeeeee',
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
})

def generate_head_to_head_chart():
    """Generates 3-metric comparison chart over 1,000 games."""
    metrics = {
        'Win Rate (%)': {'Standard PPO': 28.30, 'Maskable PPO': 36.20, 'Unit': '%'},
        'Rule Adherence (%)': {'Standard PPO': 72.80, 'Maskable PPO': 100.00, 'Unit': '%'},
        'Avg Episode Reward': {'Standard PPO': 80.93, 'Maskable PPO': 108.90, 'Unit': 'pts'}
    }

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Head-to-Head Benchmark: Standard PPO vs Maskable PPO (1,000 Games)', 
                 fontsize=15, fontweight='bold', y=1.02)

    colors = {'Standard PPO': '#e74c3c', 'Maskable PPO': '#2ecc71'}

    for idx, (metric_name, values) in enumerate(metrics.items()):
        ax = axes[idx]
        models = ['Standard PPO', 'Maskable PPO']
        vals = [values[m] for m in models]
        bar_colors = [colors[m] for m in models]
        
        bars = ax.bar(models, vals, color=bar_colors, width=0.45, edgecolor='black', linewidth=0.8, alpha=0.9)
        
        for bar, val in zip(bars, vals):
            yval = bar.get_height()
            unit = values['Unit']
            text_str = f"{val:.1f}{unit}" if unit == '%' else f"{val:+.1f}"
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + (max(vals)*0.03), 
                    text_str, ha='center', va='bottom', fontsize=11, fontweight='bold')
            
        ax.set_title(metric_name, fontsize=13, fontweight='bold', pad=12)
        ax.set_ylim(0, max(vals) * 1.22)
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    output_path = os.path.join(PLOTS_DIR, "ppo_vs_maskable_comparison.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: {output_path}")


def generate_training_curves():
    """Generates 2-panel learning curve comparison from monitor logs."""
    ppo_log_path = os.path.join(PROJECT_ROOT, "training", "kori_khel", "logs", "monitor.csv")
    maskable_log_path = os.path.join(PROJECT_ROOT, "training", "kori_khel", "logs_maskable", "monitor.csv")

    if not os.path.exists(ppo_log_path) or not os.path.exists(maskable_log_path):
        print("Skipping training curves: monitor logs not found.")
        return

    df_ppo = pd.read_csv(ppo_log_path, skiprows=1)
    df_maskable = pd.read_csv(maskable_log_path, skiprows=1)

    df_ppo['cum_timesteps'] = df_ppo['l'].cumsum()
    df_maskable['cum_timesteps'] = df_maskable['l'].cumsum()

    window = 50
    df_ppo['r_smooth'] = df_ppo['r'].rolling(window=window, min_periods=5).mean()
    df_maskable['r_smooth'] = df_maskable['r'].rolling(window=window, min_periods=5).mean()

    df_ppo['l_smooth'] = df_ppo['l'].rolling(window=window, min_periods=5).mean()
    df_maskable['l_smooth'] = df_maskable['l'].rolling(window=window, min_periods=5).mean()

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle('Training Trajectory Comparison (2.0 Million Timesteps)', 
                 fontsize=15, fontweight='bold', y=1.02)

    # Panel 1: Smoothed Reward
    ax1 = axes[0]
    ax1.plot(df_ppo['cum_timesteps'], df_ppo['r_smooth'], color='#e74c3c', label='Standard PPO', linewidth=2.0)
    ax1.plot(df_maskable['cum_timesteps'], df_maskable['r_smooth'], color='#2ecc71', label='Maskable PPO (Action Masked)', linewidth=2.2)
    ax1.set_title('Moving Average Episode Reward (Window=50)', fontsize=13, fontweight='bold', pad=10)
    ax1.set_xlabel('Total Timesteps', fontsize=11)
    ax1.set_ylabel('Episode Reward', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(fontsize=11, loc='upper left')

    # Panel 2: Episode Length
    ax2 = axes[1]
    ax2.plot(df_ppo['cum_timesteps'], df_ppo['l_smooth'], color='#e74c3c', label='Standard PPO', linewidth=2.0)
    ax2.plot(df_maskable['cum_timesteps'], df_maskable['l_smooth'], color='#2ecc71', label='Maskable PPO (Action Masked)', linewidth=2.2)
    ax2.set_title('Moving Average Episode Length (Turns)', fontsize=13, fontweight='bold', pad=10)
    ax2.set_xlabel('Total Timesteps', fontsize=11)
    ax2.set_ylabel('Episode Length (Turns)', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(fontsize=11, loc='upper right')

    plt.tight_layout()
    output_path = os.path.join(PLOTS_DIR, "training_curves_comparison.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: {output_path}")


if __name__ == "__main__":
    generate_head_to_head_chart()
    generate_training_curves()
