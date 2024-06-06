#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(description='Parse PQR files to extract coordinates and pocket numbers.')
parser.add_argument('-i', '--input', required=True, help='Path to the input PQR file.')

# Parse arguments
args = parser.parse_args()

# Extract the base filename without '.pqr'
base_filename = args.input.replace('.pqr', '')

# Output CSV file path
csv_path = f'{base_filename}_coords.csv'
middle_csv_path = f'{base_filename}_middle.csv'

# Initialize a list to store the data
data = []

# Open and read the PQR file
with open(args.input, 'r') as file:
    for line in file:
        if line.startswith('ATOM'):
            # Split each line into parts
            parts = line.split()
            # Extract x, y, z coordinates and pocket number
            x, y, z = float(parts[5]), float(parts[6]), float(parts[7])
            pocket_number = int(parts[4])
            # Append the extracted data to the list
            data.append([x, y, z, pocket_number])

# Convert the list of data to a DataFrame
df = pd.DataFrame(data, columns=['x', 'y', 'z', 'pocket_number'])

# Save the DataFrame to a CSV file
df.to_csv(csv_path, index=False)

# Group data by pocket number and calculate the median or mean
median_df = df.groupby('pocket_number').median().reset_index()
mean_df = df.groupby('pocket_number').mean().reset_index()

# Save the median/mean DataFrame to CSV files
median_df.to_csv(f'{base_filename}_median.csv', index=False)
mean_df.to_csv(middle_csv_path, index=False)
