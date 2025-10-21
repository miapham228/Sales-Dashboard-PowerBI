import pandas as pd

# loading data
df = pd.read_excel("C:/Users/Tuyet.Pham/Downloads/SALE_REPORT.xlsx")
df1 = pd.read_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Historical Data.xlsx", dtype =str )

# list of all Rev columns from sale report
rev_cols = [col for col in df.columns if col.startswith("Rev ")]

# print(rev_cols)
latest_revs = "Rev 202509"
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
# df_melted.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Current Month Data.xlsx", index=False)
# df_melted.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/revenue_202508.xlsx", index=False)


# only run this when new month comes, remember to choose correct monthname in line 11 (latest_revs)
# df1 = pd.concat([df1, df_melted], ignore_index=True)
# df1.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Historical Data.xlsx", index=False)


# checking duplicate records in Customer No and Customer Name

# df1 = df1[['Customer No', 'Customer Name']]
# # Step 2: Group by customer number and count unique names
# name_counts = df1.groupby('Customer No')['Customer Name'].nunique()

# # Filter for customer numbers with more than one name
# filtered_counts = name_counts[name_counts > 1]

# # Convert to DataFrame and reset index
# result_df = filtered_counts.reset_index()
# result_df.columns = ['customer_number', 'name_count']

# # Step 5: Export to Excel
# result_df.to_excel('customers_with_multiple_names.xlsx', index=False)





