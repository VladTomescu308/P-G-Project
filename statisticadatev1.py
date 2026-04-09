import pandas as pd
import matplotlib.pyplot as plt
from database import engine

df_consumers = pd.read_sql("""
    SELECT cu.number_of_consumers as total, c.name as country 
    FROM ConsumerUnits cu 
    JOIN Countries c ON cu.country_name = c.name
    ORDER BY total ASC
""", engine)

flag_colors = {
    'France': ['#002395', '#FFFFFF', '#ED2939'],    
    'Germany': ['#000000', '#DD0000', '#FFCE00'],     
    'Luxembourg': ['#EA141D', '#FFFFFF', '#00A1DE'],
    'Belgium': ['#000000', '#FAE042', '#ED2939'],    
    'Netherlands': ['#AE1C28', '#FFFFFF', '#21468B'], 
    'Norway': ['#EF2B2D', '#FFFFFF', '#00205B'],      
    'Sweden': ['#006AA7', '#FECC00', '#006AA7']     
}

plt.figure(figsize=(12, 7))

for i, row in df_consumers.iterrows():
    country = row['country']
    total_val = row['total']
    segment = total_val / 3
    
    colors = flag_colors.get(country, ['#808080', '#A0A0A0', '#C0C0C0'])
    
    plt.bar(country, segment, bottom=0, color=colors[0], edgecolor='none')
    plt.bar(country, segment, bottom=segment, color=colors[1], edgecolor='none')
    plt.bar(country, segment, bottom=segment*2, color=colors[2], edgecolor='none')

plt.title('Numărul de consumatori', fontsize=15)
plt.ylabel('Nr. Consumatori')
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.show()