import pandas as pd
import os

data_dic = 'iosData'

# Get all csv files in the current directory
csv_files = [f for f in os.listdir(data_dic) if f.endswith('.csv')]

# Prepare an empty DataFrame to store the merged data
merged_data = pd.DataFrame()
watch_data_list = []

# Traverse all csv files and process phone data first
for file in csv_files:
    print(f"Processing file: {file}")
    file_path = os.path.join(data_dic, file)
    # Reading CSV Files
    data = pd.read_csv(file_path)

    # Get the prefix of the file name (the part before the second _)
    parts = file.split('_')
    if len(parts) > 2:
        prefix = parts[0] + '_' + parts[1]
    else:
        prefix = file.split('.')[0]
        # If there are not enough underscores in the file name, the file name is used as a prefix

    # Update column names, add prefix
    data.columns = [prefix + '_' + col if col != 'time' else 'time' for col in data.columns]

    # Format the time column to ensure that it can be compared
    data['time'] = pd.to_datetime(data['time'], format='%Y/%m/%d %H:%M:%S.%f')

    if 'phone' in file:
        # Processing phone data
        if merged_data.empty:
            merged_data = data
        else:
            merged_data = pd.merge(merged_data, data, on='time', how='outer')
        print(f"Phone data merged, current shape: {merged_data.shape}")
    else:
        # Temporarily save watch data
        watch_data_list.append(data)

# Process watch data and perform time alignment
for watch_data in watch_data_list:
    if not merged_data.empty:
        print("Aligning watch data")
        # Create a new DataFrame to store the aligned data
        aligned_data = pd.DataFrame(columns=merged_data.columns.tolist() + watch_data.columns.tolist()[1:])

        # Time alignment of watch data
        for i, row in merged_data.iterrows():
            time_diff = (watch_data['time'] - row['time']).abs()
            closest_idx = time_diff.idxmin()
            if time_diff[closest_idx].total_seconds() <= 1:
                combined_row = pd.concat([row, watch_data.iloc[closest_idx][1:]], axis=0)
            else:
                combined_row = pd.concat([row, pd.Series([None] * (watch_data.shape[1] - 1), index=watch_data.columns[1:])], axis=0)
            aligned_data = pd.concat([aligned_data, combined_row.to_frame().T], ignore_index=True)

        merged_data = aligned_data
        print(f"Watch data aligned, current shape: {merged_data.shape}")

# Sort timestamps
if not merged_data.empty:
    merged_data.sort_values('time', inplace=True)

    # Delete the part with empty data at the beginning
    # Find the index of the first row that has no NaN values at all
    if not merged_data.dropna().empty:
        first_full_row = merged_data.dropna().index[0]
        # Delete all rows before the index
        merged_data = merged_data.loc[first_full_row:]

    # Count the number of rows containing null values at the end of the deletion
    num_rows_before = merged_data.shape[0]
    merged_data = merged_data.dropna()
    num_rows_after = merged_data.shape[0]
    num_rows_deleted = num_rows_before - num_rows_after

    # Save the merged data to a new CSV file
    merged_data.to_csv('allData.csv', index=False)
    print("Merged data saved to allData.csv")
    print(f"Deleted {num_rows_deleted} rows containing NaN values at the end.")
else:
    print("Merged data is empty. Please check your input files.")
