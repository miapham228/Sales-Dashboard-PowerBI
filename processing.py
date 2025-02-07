import pandas as pd


# loading data
df = pd.read_excel("C:/Users/Tuyet.Pham/Downloads/SALE REPORT.xlsx")

# remove columns
rev_cols = [col for col in df.columns if col.startswith("Rev ")]
latest_revs = sorted(rev_cols, reverse=True)[:1]
other_cols = [col for col in df.columns if not col.startswith(("Rev ", "Items ", "Total "))]
df_filtered = df[other_cols + latest_revs]

# Pivot the table (convert columns to rows)
df_melted = df_filtered.melt(id_vars=other_cols, 
                             value_vars=latest_revs, 
                             var_name="Category", 
                             value_name="Value")

# Save or display the result
# df_melted.to_excel("pivoted_file.xlsx", index=False)

#print(df_melted.head())  # Display first few rows
df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors="coerce")
print(df_melted["Value"].sum())  # Sum of revenue values
df_melted.to_excel("C:/Users/Tuyet.Pham/Downloads/revenue.xlsx", index=False)