def export_data(data_import, output_file, selected_date):
    required_columns = ['amount', 'account_number', 'branch_code', 'company_name', 'reference']
    missing_columns = [col for col in required_columns if col not in data_import.columns]
    
    if missing_columns:
        raise KeyError(f"Missing columns in data_import: {', '.join(missing_columns)}")
    
    if not selected_date:
        raise ValueError("No date selected for export")
    
    try:
        formatted_date = selected_date.strftime("%Y%m%d")  # Format the date as "yyyymmdd"
        with open(output_file, 'w') as file:
            for index, entry in data_import.iterrows():
                line = f"#ZA#DD#{formatted_date}####1##{entry['amount']}##{entry['account_number']}##{entry['branch_code']}##{entry['company_name']}####0#44#0002987074#{entry['reference']}#SABRE COLLECTION##\n"
                file.write(line)
        return True
    except Exception as e:
        print(f"Error exporting data: {e}")
        return False

# Example of how to call the export_data function correctly
# Ensure you have the data_import dataframe, output_file path, and selected_date defined
# data_import = ...  # Load or create your dataframe here
# output_file = 'output_file_path.txt'
# selected_date = '2023-10-01'  # Example selected date
# export_data(data_import, output_file, selected_date)