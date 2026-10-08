"""Cleaning (attatched, existing) CSV data to processable standard"""
import pandas as pd
import re

#-------- Functions for data handling and cleaning --------

# Cleaning the data so that the column names are clear
def clean_columns(df):
    """retrieves and cleans column names so that they display correctly in the app"""
    df.columns = [re.sub(r'(_)', ' ', col).title() for col in df.columns]
    return df

#Percentage to numeric conversion
def convert_percentage_to_numeric(df, column_name):
    """Converts percentage strings to numeric values in the specified column."""

    #check if the column is of object type and contains percentage values
    if df[column_name].dtype == "object":
        if df[column_name].str.endswith('%').any():

            #Remove the percentage sign, convert to float, and divide by 100 to get the numeric value
            df[column_name] = df[column_name].str.rstrip('%').astype(float) / 100        
    return df

#function to load and clean data
def load_and_clean_data(file_path):
    """Loads a dataset from the specified file path and applies cleaning functions."""
    df = pd.read_csv(file_path)
    df = clean_columns(df)
    # Example: Convert a specific percentage column to numeric if it exists
    percentage_columns = [col for col in df.columns if 'Percentage' in col or '%' in col]
    for col in percentage_columns:
        df = convert_percentage_to_numeric(df, col)
    return df

#function to convert population strings to numeric values, removing the comma for processing
def population_to_numeric(df, column_name):
    """Converts population strings to numeric values in the specified column."""
    if df[column_name].dtype == "object":
        df[column_name] = df[column_name].str.replace(',', '').astype(float)
    return df

#function to filter and clean solely the population data
def population_cleaning(df):
   
   #filter to only include london boroughs
   df = df[df["Geography"] == "London Borough"]
   #remove all useless columns
   df = df[["Name", "Mid-2024"]]
   #rename the columns to be more user friendly
   df = df.rename(columns={
        "Name": "Borough",
        "Mid-2024": "Population"
    })
   df = population_to_numeric(df, "Population")
   return df

#function to clean the safe streets data specifically
def safe_streets_cleaning(df):
     # removing all columns that are not needed
    df = df[[
        "Borough",
        "Ltn 2024",
        "20Mph 2024",
        "Cpz 2024",
        "Protected Cycle Track 2024",
        "School Streets 2024",
        "Bus Priority 2024"
    ]]

    # Rename to match your existing dataset naming
    df = df.rename(columns={
        "Ltn 2024": "Low Traffic Neighbourhood Area As Proportion Of Total Appropriate Area",
        "20Mph 2024": "Proportion Of Borough Roads With 20Mph Speed Limit %",
        "Cpz 2024": "Cpz Area As Proportion Of Total Appropriate Area",
        "Protected Cycle Track 2024": "Protected Cycle Track (Km Per Km Of Road Length) %",
        "School Streets 2024": "School Streets As Proportion Of Total Schools %",
        "Bus Priority 2024": "Bus Route Length On Bus Lanes & Through Ltns As Proportion Of Total Bus Lane Length %"
    })

    return df

#function to merge together all data sets together, using the borough as the key
def merge_datasets(safe_streets_df, population_df, employees_and_debt_df):
    """Merges the performance, population, and safe streets datasets together on the 'Borough' column."""
    merged_df = safe_streets_df.merge(population_df, on='Borough', how='left')
    merged_df = merged_df.merge(employees_and_debt_df, on='Borough', how='left')
    #update the debt and employees to be per capita
    merged_df["Debt Per Capita"] = merged_df["Debt In Gbp"] / merged_df["Population"]
    merged_df["Percentage Of Population Employed"] = (merged_df["Number Of Employees"] / merged_df["Population"]) * 100
    
    return merged_df


#function to keep only the rows for the selected boroughs
def filter_by_boroughs(df, boroughs):
    """Returns only the rows for the named boroughs, preserving column order."""
    return df[df["Borough"].isin(list(boroughs))]
