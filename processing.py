import pandas as pd

# HAVE TO COMMENT on 1 of lates_revs

# loading data
df = pd.read_excel("C:/Users/Tuyet.Pham/Downloads/SALE_REPORT.xlsx")
# df1 = pd.read_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Historical Data.xlsx")

# list of all Rev columns from sale report
# rev_cols = [col for col in df.columns if col.startswith("Rev ")]
# print(rev_cols)
# revenue for HISTORICAL DATA (everytime when we in new month)
# latest_revs = sorted(rev_cols, reverse=True)[1]

latest_revs = "Rev 202508"
other_cols = [col for col in df.columns if not col.startswith(("Rev ", "Items ", "Total "))]
df_filtered = df[other_cols + [latest_revs]]


# Pivot the table (convert columns to rows)
df_melted = df_filtered.melt(id_vars = other_cols, 
                             value_vars = latest_revs, 
                             var_name = "Category", 
                             value_name = "Value")


# Save or display the result

df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors = "coerce")
df_melted.dropna(subset = ['Value'], inplace = True) # remove rows with NA values in Value column

print(df_melted["Value"].sum())  # Sum of revenue values for cross check with Excel file

# create current sale in python folder
df_melted.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Current Month Data.xlsx", index=False)
df_melted.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/revenue_202508.xlsx", index=False)


# append to historical data
# df1 = pd.concat([df1, df_melted], ignore_index=True)
# df1.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Historical Data.xlsx", index=False)

