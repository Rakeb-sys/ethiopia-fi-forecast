import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class AdvancedInclusionEDA:
    def __init__(self, data_file: str):
        self.df = pd.read_csv(data_file)
        self.df['observation_date'] = pd.to_datetime(self.df['observation_date'], errors='coerce')
        sns.set_theme(style="whitegrid", context="talk")

    def analyze_access_slowdown(self):
        """Insight 1 & 5: Investigates the macro structural plateau vs policy shocks."""
        print("[EDA] Evaluating Access Trajectories and Policy Shocks...")
        df_acc = self.df[self.df['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot primary overall unique access line
        ax1.plot(df_acc['observation_date'], df_acc['value_numeric'], color='#1f77b4', marker='o', linewidth=3, label='Account Ownership (%)')
        ax1.set_ylabel('Unique Adult Account Ownership (%)', color='#1f77b4')
        ax1.set_ylim(0, 100)
        
        # Overlay events using vertical structural indicators
        events = self.df[self.df['record_type'] == 'event']
        for _, evt in events.dropna(subset=['observation_date']).iterrows():
            ax1.axvline(x=evt['observation_date'], color='crimson', linestyle='--', alpha=0.7)
            ax1.text(evt['observation_date'], 10, f" {evt['indicator_code']}", rotation=90, color='crimson', fontsize=10)
            
        plt.title("Ethiopia Account Ownership Trajectory and Policy/Market Milestones", pad=20)
        plt.tight_layout()
        plt.savefig('reports/figures/access_trajectory_shocks.png', dpi=300)
        plt.close()

    def evaluate_gender_gap(self):
        """Insight 3: Formal Mathematical Quantification of the Financial Inclusion Gender Disparity."""
        print("[EDA] Quantifying Gender Inclusion Gap Dynamics...")
        g_fem = self.df[self.df['indicator_code'] == 'ACC_OWNERSHIP_FEMALE']['value_numeric'].values
        g_male = self.df[self.df['indicator_code'] == 'ACC_OWNERSHIP_MALE']['value_numeric'].values
        
        if len(g_fem) > 0 and len(g_male) > 0:
            female_rate = float(g_fem[0])
            male_rate = float(g_male[0])
            absolute_gap = male_rate - female_rate
            relative_parity_index = female_rate / male_rate
            
            # Save visual distribution representation
            plt.figure(figsize=(6, 5))
            bars = plt.bar(['Female', 'Male'], [female_rate, male_rate], color=['#ff7f0e', '#1f77b4'], width=0.6)
            plt.ylim(0, 100)
            plt.ylabel('Ownership Rate (%)')
            plt.title("Financial Account Ownership Gender Disparity (2021 Baseline)")
            
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', weight='bold')
                
            plt.tight_layout()
            plt.savefig('reports/figures/gender_disparity_analysis.png', dpi=300)
            plt.close()
            print(f"Absolute Gender Inclusion Gap: {absolute_gap:.2f} percentage points. Parity Metric: {relative_parity_index:.2f}")

    def run_all_diagnostics(self):
        os.makedirs('reports/figures', exist_ok=True)
        self.analyze_access_slowdown()
        self.evaluate_gender_gap()

if __name__ == "__main__":
    analyzer = AdvancedInclusionEDA("data/processed/ethiopia_fi_unified_data_processed.csv")
    analyzer.run_all_diagnostics()