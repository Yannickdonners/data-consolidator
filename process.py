import pandas as pd
import numpy as np
import os

async def format_files(files):
    formatted_dfs = []
    for file in files:
        if file.filename.endswith(('.xlsx', '.xls')):
            # Read the file content
            contents = await file.read()
            filename = file.filename.split("/")[-1]
            # Save temporarily and read with pandas
            with open(f"temp_{filename}", "wb") as f:
                f.write(contents)

            # Read Excel file
            df = pd.read_excel(f"temp_{filename}")
            df = format_dataframe(df)
            formatted_dfs.append(df)
            # Clean up temp file
            os.remove(f"temp_{filename}")

    return formatted_dfs

def format_dataframe(df):
    well_row = 0
    for n in range(len(df)):
        if df.iloc[n].astype(str).str.contains('Well').any():
            well_row = n + 1
            break

    df.columns = df.iloc[well_row]
    df = df.iloc[well_row + 1:]
    df = df.reset_index(drop=True)
    return df

def process_dataframes(dfs, files):
    columns = dfs[0].columns
    output_dfs = {}

    for n in range(len(dfs[0])):  # This line assumes all dataframes have the same number of rows
        df_per_sample = [] 
        sheet_name = dfs[0].iloc[n].iloc[0]
        for file, (idx, dataframe) in zip(files, enumerate(dfs)):
            values = dataframe.iloc[n].values
            padding_length = len(columns) - len(values)

            if padding_length > 0:
                values = np.concatenate([values[:2], np.full(padding_length, np.nan), values[2:]])
            
            data = pd.DataFrame([values], columns=columns)
            data = data.drop(data.columns[0], axis = 1)
            data.iloc[0, 0] = file.strip('.xlsx')
            df_per_sample.append(data)

        output_dfs[sheet_name] = pd.concat(df_per_sample, ignore_index=True)
    
    return output_dfs



