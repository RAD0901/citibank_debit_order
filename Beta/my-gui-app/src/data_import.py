import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

def import_data(file_path):
    """
    Imports data from a specified Excel file and processes it into a structured format.
    
    Args:
        file_path (str): The path to the file to be imported.
        
    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
    """
    required_columns = ['Customer', 'Customer Name', 'Amount', 'Debit Order', 'Bank Account Number', 'Bank Branch Code']
    try:
        df = pd.read_excel(file_path)  # Read the Excel file
        logging.debug(f"DataFrame created with {len(df)} rows")
        
        # Ensure the DataFrame has the required columns
        if not all(column in df.columns for column in required_columns):
            logging.error("The imported file does not contain all required columns.")
            return pd.DataFrame()
        
        # Select only the required columns and ensure correct order
        df = df[required_columns]
        logging.debug(f"DataFrame formatted with required columns: {required_columns}")
        
        # Rename the columns as specified
        df.rename(columns={
            'Customer': 'reference',
            'Customer Name': 'company_name',
            'Amount': 'amount',
            'Bank Account Number': 'account_number',
            'Bank Branch Code': 'branch_code'
        }, inplace=True)
        logging.debug("Columns renamed as specified")
        
        # Remove leading and trailing spaces from 'company_name'
        df['company_name'] = df['company_name'].str.strip()
        logging.debug("Leading and trailing spaces removed from 'company_name'")
        
        # Format 'amount' to have 2 decimal places
        df['amount'] = df['amount'].map(lambda x: f"{x:.2f}")
        logging.debug("Formatted 'amount' to have 2 decimal places")
        
        return df
    except Exception as e:
        logging.error(f"Error importing data: {e}")
        return pd.DataFrame()

def validate_data(data):
    """
    Validates the imported data to ensure it meets the required structure.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the imported data.
        
    Returns:
        bool: True if data is valid, False otherwise.
    """
    required_columns = ['Customer', 'Customer Name', 'Amount', 'Debit Order', 'Bank Account Number', 'Bank Branch Code']
    return data.columns.isin(required_columns).all()  # Use .isin() and .all() correctly