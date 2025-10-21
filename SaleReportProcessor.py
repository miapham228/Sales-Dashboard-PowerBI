import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(
    filename="sales_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SalesReportProcessor:
    def __init__(self, report_path):
        self.report_path = report_path
        try:
            self.df_report = pd.read_excel(self.report_path)
        except Exception as e:
            print(f"Failed to load report file: {e}")
            self.df_report = pd.DataFrame()
        

    def current_revenue(self, current_month, output_path):
        # Identify relevant columns
        try:
            rev_cols = [col for col in self.df_report.columns if col.startswith("Rev ")]
            latest_rev_col = f"Rev {current_month}"
            other_cols = [col for col in self.df_report.columns if not col.startswith(("Rev ", "Items ", "Total "))]

        # Filter and reshape
            df_filtered = self.df_report[other_cols + [latest_rev_col]]
            df_melted = df_filtered.melt(
                id_vars=other_cols,
                value_vars=latest_rev_col,
                var_name="Category",
                value_name="Value"
                )

        # Clean and process
            df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors="coerce")
            df_melted.dropna(subset=["Value"], inplace=True)

        # Output results
            print(f"Total revenue for {current_month}: {df_melted['Value'].sum():,.2f}")
            df_melted.to_excel(output_path, index=False)

            return df_melted
        except Exception as e:
            print(f"Error calculating revenue: {e}")
    

    def historical_revenue(self, pre_month, historical_data):
        # Identify relevant columns
        try:
            rev_cols = [col for col in self.df_report.columns if col.startswith("Rev ")]
            latest_rev_col = f"Rev {pre_month}"
            other_cols = [col for col in self.df_report.columns if not col.startswith(("Rev ", "Items ", "Total "))]

        # Filter and reshape
            df_filtered = self.df_report[other_cols + [latest_rev_col]]
            df_melted = df_filtered.melt(
                id_vars=other_cols,
                value_vars=latest_rev_col,
                var_name="Category",
                value_name="Value"
                )

        # Clean and process
            df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors="coerce")
            df_melted.dropna(subset=["Value"], inplace=True)

        # Output results
            print(f"Total revenue for {pre_month}: {df_melted['Value'].sum():,.2f}")
            df_old = pd.read_excel(historical_data)
            df1 = pd.concat([df_old, df_melted], ignore_index=True)
            df1.to_excel("C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Historical Data.xlsx", index=False)

        except Exception as e:
            print(f"Error calculating revenue: {e}")

processor = SalesReportProcessor(
    report_path="C:/Users/Tuyet.Pham/Downloads/SALE_REPORT.xlsx"    
)

result_df = processor.current_revenue(
    current_month = "202510",
    output_path = "C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Sale Transaction Current Month Data.xlsx"
)

# only run once per month  when new month comes
# processor.historical_revenue(pre_month="202509", historical_data= "C:/Users/Tuyet.Pham/OneDrive - FEL/Desktop/PROJECTS/Sales Dashboard/pythonwork/Test/Sale Transaction Historical Data.xlsx")

