import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from database import engine

query = """
    SELECT identifier_name, originator_first_name, originator_last_name, email, owner_last_name 
    FROM Ownership
"""
df_ownership = pd.read_sql(query, engine)

fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('off') 

the_table = ax.table(
    cellText=df_ownership.values, 
    colLabels=df_ownership.columns, 
    cellLoc='center', 
    loc='center'
)

n_cols = len(df_ownership.columns)

colors_plasma = cm.plasma(np.linspace(0.2, 0.8, n_cols))

for j in range(n_cols):
    cell = the_table[0, j]
    cell.set_facecolor(colors_plasma[j])
    cell.set_text_props(color='white', weight='bold') 
    cell.set_height(0.15) 

for i in range(1, len(df_ownership) + 1):
    for j in range(n_cols):
        cell = the_table[i, j]
        cell.set_height(0.12)
        if i % 2 == 0: 
            cell.set_facecolor('#f2f2f2')

the_table.auto_set_font_size(False)
the_table.set_fontsize(10)

plt.title('Tabelul de Proprietate a Identificatorilor (Ownership)', pad=20, fontsize=14)
plt.tight_layout()

plt.show()