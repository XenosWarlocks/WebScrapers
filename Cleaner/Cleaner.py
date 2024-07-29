import pandas as pd




def clean_email_column(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)
   
    # Display the initial number of rows for reference
    print(f"Initial number of rows: {len(df)}")
   
    # Remove rows where the 'Email' column is empty or NaN
    df_cleaned = df[df['Email'].notna() & (df['Email'] != '')]
   
    # Display the number of rows after cleaning
    print(f"Number of rows after cleaning: {len(df_cleaned)}")
   
    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")




# Specify the input and output file paths
input_csv = 'scraped_data.csv'  # Replace with your input CSV file path
output_csv = 'cleaned_data.csv'  # Desired output CSV file name




# Run the cleaning process
clean_email_column(input_csv, output_csv)


