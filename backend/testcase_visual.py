"""
CUSTOM TEST CASE GENERATOR FOR FUZZY LOGIC STRESS DETECTION
============================================================
Generate visualizations dengan test case Anda sendiri!

Usage:
    1. Edit YOUR_TEST_CASES di bawah
    2. Run: python custom_test_generator.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

try:
    from logic import fuzzy_logic
    print("✅ Modul 'fuzzy_logic' berhasil diimpor.")
    SKFUZZY_AVAILABLE = True
except ImportError as e:
    print(f"❌ ERROR: Gagal impor fuzzy_logic: {e}")
    print("   Menggunakan data statis yang diekstrak dari output yang diharapkan.")
    SKFUZZY_AVAILABLE = False
except Exception as e:
    print(f"❌ ERROR saat menjalankan fuzzy_logic: {e}")
    print("   Menggunakan data statis yang diekstrak dari output yang diharapkan.")
    SKFUZZY_AVAILABLE = False


# ====================================
# ⭐ EDIT TEST CASES ANDA DI SINI ⭐
# ====================================

YOUR_TEST_CASES = [
    # Format: (screentime, temperature, humidity, air_quality, description)
    # Test cases sesuai permintaan:
    (10, 35, 85, 1.0, "T1: Screen 10h, Temp 35°C, Humid 85%, AQ 1.0"),
    (2, 25, 50, 0.8, "T2: Screen 2h, Temp 25°C, Humid 50%, AQ 0.8"),
    (2, 25, 95, 0.1, "T3: Screen 2h, Temp 25°C, Humid 95%, AQ 0.1"),
    (3, 24, 50, 0.1, "T4: Screen 3h, Temp 24°C, Humid 50%, AQ 0.1"),
    (0, 10, 0, 0.0, "T5: Screen 0h, Temp 10°C, Humid 0%, AQ 0.0"),
    (12, 40, 100, 5.0, "T6: Screen 12h, Temp 40°C, Humid 100%, AQ 5.0"),
    (1, 15, 40, 0.4, "T7: Screen 1h, Temp 15°C, Humid 40%, AQ 0.4"),
    (5, 38, 50, 0.5, "T8: Screen 5h, Temp 38°C, Humid 50%, AQ 0.5"),
]



# ====================================
# GENERATE DATASET
# ====================================

def generate_from_test_cases(test_cases):
    """Convert test cases to DataFrame"""
    data = []
    
    for idx, (screen, temp, humid, aq, desc) in enumerate(test_cases, 1):
        result = fuzzy_logic.calculate_stress(screen, temp, humid, aq)
        
        data.append({
            'id': idx,
            'screentime': screen,
            'temperature': temp,
            'humidity': humid,
            'air_quality': aq,
            'stress_value': result['stress_value'],
            'category': result['category'],
            'description': desc
        })
    
    return pd.DataFrame(data)


# ====================================
# VISUALIZATION FUNCTIONS
# ====================================

def create_visualizations(df, output_dir='case_results'):
    """Create all 5 visualization types"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    print("\n🎨 Creating Visualizations...\n")
    
    # ========================================
    # 1. MAIN DASHBOARD (2x3 grid)
    # ========================================
    fig1, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig1.suptitle('Custom Test Cases - Fuzzy Logic Analysis Dashboard', 
                  fontsize=16, fontweight='bold')
    
    # 1.1 Stress Value Distribution
    axes[0, 0].hist(df['stress_value'], bins=10, color='skyblue', 
                    edgecolor='black', alpha=0.7)
    axes[0, 0].axvline(df['stress_value'].mean(), color='red', 
                       linestyle='--', linewidth=2, 
                       label=f'Mean: {df["stress_value"].mean():.1f}')
    axes[0, 0].set_title('Distribution of Stress Values', fontweight='bold')
    axes[0, 0].set_xlabel('Stress Value')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 1.2 Category Distribution (Pie Chart)
    cat_counts = df['category'].value_counts()
    # Updated color mapping for 5 categories
    colors_map = {
        'Very Low Stress': '#00FF00',
        'Low Stress': '#90EE90',
        'Medium Stress': '#FFD700',
        'High Stress': '#FF8C00',
        'Very High Stress': '#FF0000'
    }
    axes[0, 1].pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%',
                   colors=[colors_map.get(cat, 'gray') for cat in cat_counts.index],
                   startangle=90, textprops={'fontsize': 9, 'fontweight': 'bold'})
    axes[0, 1].set_title('Category Distribution', fontweight='bold')
    
    # 1.3 Screen Time vs Stress
    scatter1 = axes[0, 2].scatter(df['screentime'], df['stress_value'], 
                                  c=df['stress_value'], cmap='RdYlGn_r', 
                                  s=100, alpha=0.7, edgecolors='black')
    axes[0, 2].set_title('Screen Time vs Stress', fontweight='bold')
    axes[0, 2].set_xlabel('Screen Time (hours)')
    axes[0, 2].set_ylabel('Stress Value')
    plt.colorbar(scatter1, ax=axes[0, 2], label='Stress')
    axes[0, 2].grid(alpha=0.3)
    
    # 1.4 Temperature vs Stress
    scatter2 = axes[1, 0].scatter(df['temperature'], df['stress_value'], 
                                  c=df['stress_value'], cmap='RdYlGn_r', 
                                  s=100, alpha=0.7, edgecolors='black')
    axes[1, 0].set_title('Temperature vs Stress', fontweight='bold')
    axes[1, 0].set_xlabel('Temperature (°C)')
    axes[1, 0].set_ylabel('Stress Value')
    plt.colorbar(scatter2, ax=axes[1, 0], label='Stress')
    axes[1, 0].grid(alpha=0.3)
    
    # 1.5 Humidity vs Stress
    scatter3 = axes[1, 1].scatter(df['humidity'], df['stress_value'], 
                                  c=df['stress_value'], cmap='RdYlGn_r', 
                                  s=100, alpha=0.7, edgecolors='black')
    axes[1, 1].set_title('Humidity vs Stress', fontweight='bold')
    axes[1, 1].set_xlabel('Humidity (%)')
    axes[1, 1].set_ylabel('Stress Value')
    plt.colorbar(scatter3, ax=axes[1, 1], label='Stress')
    axes[1, 1].grid(alpha=0.3)
    
    # 1.6 Air Quality vs Stress
    scatter4 = axes[1, 2].scatter(df['air_quality'], df['stress_value'], 
                                  c=df['stress_value'], cmap='RdYlGn_r', 
                                  s=100, alpha=0.7, edgecolors='black')
    axes[1, 2].set_title('Air Quality vs Stress', fontweight='bold')
    axes[1, 2].set_xlabel('Air Quality (PPM)')
    axes[1, 2].set_ylabel('Stress Value')
    plt.colorbar(scatter4, ax=axes[1, 2], label='Stress')
    axes[1, 2].grid(alpha=0.3)
    
    plt.tight_layout()
    fig1.savefig(f'{output_dir}/01_main_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ [1/5] Main Dashboard (2x3 grid)")
    plt.close(fig1)
    
    # ========================================
    # 2. CORRELATION HEATMAP
    # ========================================
    fig2, ax = plt.subplots(figsize=(10, 8))
    numeric_cols = ['screentime', 'temperature', 'humidity', 'air_quality', 'stress_value']
    corr_matrix = df[numeric_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
                center=0, square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1, ax=ax)
    ax.set_title('Correlation Matrix - Variables vs Stress', 
                 fontsize=14, fontweight='bold', pad=20)
    
    fig2.tight_layout()
    fig2.savefig(f'{output_dir}/02_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ [2/5] Correlation Heatmap")
    plt.close(fig2)
    
    # ========================================
    # 3. BOX PLOTS BY CATEGORY
    # ========================================
    fig3, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig3.suptitle('Input Variables Distribution by Stress Category', 
                  fontsize=14, fontweight='bold')
    
    for idx, var in enumerate(['screentime', 'temperature', 'air_quality']):
        df.boxplot(column=var, by='category', ax=axes[idx], 
                   patch_artist=True, grid=True)
        axes[idx].set_title(f'{var.capitalize()} by Category')
        axes[idx].set_xlabel('Stress Category')
        axes[idx].set_ylabel(var.capitalize())
        plt.sca(axes[idx])
        plt.xticks(rotation=15, ha='right', fontsize=8)
    
    plt.tight_layout()
    fig3.savefig(f'{output_dir}/03_boxplots_by_category.png', dpi=300, bbox_inches='tight')
    print("✅ [3/5] Box Plots by Category")
    plt.close(fig3)
    
    # ========================================
    # 4. VALIDATION TABLE
    # ========================================
    fig4, ax = plt.subplots(figsize=(16, len(df)*0.5 + 2))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = []
    for _, row in df.iterrows():
        # Color coding based on 5 categories
        if 'Very Low' in row['category']:
            emoji = '🟢🟢'
        elif 'Low' in row['category'] and 'Very' not in row['category']:
            emoji = '🟢'
        elif 'Medium' in row['category']:
            emoji = '🟡'
        elif 'High' in row['category'] and 'Very' not in row['category']:
            emoji = '🟠'
        else:
            emoji = '🔴'
        
        table_data.append([
            row['id'],
            f"{row['screentime']:.1f}h",
            f"{row['temperature']:.1f}°C",
            f"{row['humidity']:.0f}%",
            f"{row['air_quality']:.2f}",
            f"{row['stress_value']:.1f}",
            f"{emoji} {row['category']}",
            row['description']
        ])
    
    table = ax.table(cellText=table_data,
                     colLabels=['ID', 'Screen', 'Temp', 'Humid', 'AQ(PPM)', 
                               'Stress', 'Category', 'Description'],
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.05, 0.08, 0.08, 0.08, 0.08, 0.08, 0.15, 0.40])
    
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2.5)
    
    # Color code stress values with 5 levels
    for i in range(len(table_data)):
        stress_val = df.iloc[i]['stress_value']
        if stress_val < 20:
            table[(i+1, 5)].set_facecolor('#00FF00')
        elif stress_val < 40:
            table[(i+1, 5)].set_facecolor('#90EE90')
        elif stress_val < 60:
            table[(i+1, 5)].set_facecolor('#FFD700')
        elif stress_val < 80:
            table[(i+1, 5)].set_facecolor('#FF8C00')
        else:
            table[(i+1, 5)].set_facecolor('#FF0000')
    
    plt.title(f'Test Cases Results Table ({len(df)} cases)', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.savefig(f'{output_dir}/04_validation_table.png', dpi=300, bbox_inches='tight')
    print("✅ [4/5] Validation Table")
    plt.close(fig4)
    
    # ========================================
    # 5. LINE PLOT PROGRESSION
    # ========================================
    fig5, ax = plt.subplots(figsize=(14, 6))
    
    # Sort by stress value for better visualization
    df_sorted = df.sort_values('stress_value').reset_index(drop=True)
    
    # Plot line
    ax.plot(range(len(df_sorted)), df_sorted['stress_value'], 
            marker='o', linewidth=2, markersize=8, color='purple',
            label='Stress Value')
    
    # Add boundaries for 5 categories
    ax.axhline(y=20, color='green', linestyle=':', linewidth=1.5, 
               label='Very Low/Low Boundary', alpha=0.7)
    ax.axhline(y=40, color='lightgreen', linestyle=':', linewidth=1.5, 
               label='Low/Medium Boundary', alpha=0.7)
    ax.axhline(y=60, color='orange', linestyle=':', linewidth=1.5, 
               label='Medium/High Boundary', alpha=0.7)
    ax.axhline(y=80, color='red', linestyle=':', linewidth=1.5, 
               label='High/Very High Boundary', alpha=0.7)
    
    # Shade regions for 5 categories
    ax.fill_between(range(len(df_sorted)), 0, 20, alpha=0.2, color='green', label='Very Low')
    ax.fill_between(range(len(df_sorted)), 20, 40, alpha=0.2, color='lightgreen', label='Low')
    ax.fill_between(range(len(df_sorted)), 40, 60, alpha=0.2, color='yellow', label='Medium')
    ax.fill_between(range(len(df_sorted)), 60, 80, alpha=0.2, color='orange', label='High')
    ax.fill_between(range(len(df_sorted)), 80, 100, alpha=0.2, color='red', label='Very High')
    
    # Add value labels
    for i, row in df_sorted.iterrows():
        ax.text(i, row['stress_value'] + 3, f"{row['stress_value']:.1f}", 
                ha='center', fontsize=7, bbox=dict(facecolor='white', 
                alpha=0.7, boxstyle='round,pad=0.3'))
    
    ax.set_title('Stress Value Progression (Sorted)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Test Case Index (sorted by stress)')
    ax.set_ylabel('Stress Value (0-100)')
    ax.set_ylim(-5, 105)
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    fig5.savefig(f'{output_dir}/05_line_plot_progression.png', dpi=300, bbox_inches='tight')
    print("✅ [5/5] Line Plot Progression")
    plt.close(fig5)
    
    print(f"\n✅ All visualizations saved to: {output_dir}/\n")


# ====================================
# EXPORT FUNCTIONS
# ====================================

def export_results(df, output_dir='case_results'):
    """Export results to CSV and TXT"""
    
    # CSV export
    df.to_csv(f'{output_dir}/test_results.csv', index=False)
    print(f"✅ Exported: test_results.csv")
    
    # Summary report
    with open(f'{output_dir}/summary_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("CUSTOM TEST CASES - FUZZY LOGIC STRESS DETECTION\n")
        f.write("="*70 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Test Cases: {len(df)}\n\n")
        
        f.write("STRESS STATISTICS:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Mean      : {df['stress_value'].mean():.2f}\n")
        f.write(f"Median    : {df['stress_value'].median():.2f}\n")
        f.write(f"Std Dev   : {df['stress_value'].std():.2f}\n")
        f.write(f"Min       : {df['stress_value'].min():.2f}\n")
        f.write(f"Max       : {df['stress_value'].max():.2f}\n\n")
        
        f.write("CATEGORY DISTRIBUTION:\n")
        f.write("-" * 70 + "\n")
        cat_dist = df['category'].value_counts()
        for cat in ['Very Low Stress', 'Low Stress', 'Medium Stress', 'High Stress', 'Very High Stress']:
            count = cat_dist.get(cat, 0)
            pct = (count / len(df)) * 100 if len(df) > 0 else 0
            f.write(f"{cat:20s}: {count:3d} cases ({pct:5.1f}%)\n")
        
        f.write("\nCORRELATION WITH STRESS:\n")
        f.write("-" * 70 + "\n")
        corr = df[['screentime', 'temperature', 'humidity', 'air_quality', 'stress_value']].corr()
        for var in ['screentime', 'temperature', 'humidity', 'air_quality']:
            f.write(f"{var:15s}: {corr.loc[var, 'stress_value']:+.4f}\n")
        
        f.write("\nDETAILED RESULTS:\n")
        f.write("-" * 70 + "\n")
        for _, row in df.iterrows():
            f.write(f"\n[{row['id']}] {row['description']}\n")
            f.write(f"    Input: Screen={row['screentime']}h, Temp={row['temperature']}°C, ")
            f.write(f"Humid={row['humidity']}%, AQ={row['air_quality']} PPM\n")
            f.write(f"    Output: Stress={row['stress_value']:.2f} ({row['category']})\n")
    
    print(f"✅ Exported: summary_report.txt\n")


# ====================================
# MAIN
# ====================================

def main():
    print("\n" + "="*70)
    print(" CUSTOM TEST CASE GENERATOR - FUZZY LOGIC STRESS DETECTION")
    print("="*70)
    print(f" Total Test Cases: {len(YOUR_TEST_CASES)}")
    print("="*70 + "\n")
    
    # Generate dataset
    df = generate_from_test_cases(YOUR_TEST_CASES)
    
    # Show preview
    print("📊 Test Cases Preview:")
    print(df[['id', 'description', 'stress_value', 'category']].to_string(index=False))
    
    # Create visualizations
    create_visualizations(df)
    
    # Export results
    export_results(df)
    
    print("="*70)
    print("✅ ALL DONE!")
    print("="*70)
    print("\n📂 Check folder: case_results/")
    print("   - 01_main_dashboard.png (2x3 comprehensive view)")
    print("   - 02_correlation_heatmap.png (variable correlations)")
    print("   - 03_boxplots_by_category.png (distribution by category)")
    print("   - 04_validation_table.png (detailed results table)")
    print("   - 05_line_plot_progression.png (stress progression)")
    print("   - test_results.csv (raw data)")
    print("   - summary_report.txt (text summary)")


if __name__ == '__main__':
    main()