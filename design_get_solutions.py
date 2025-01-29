#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process CSV file to extract sequences where mcc is 0.')
    parser.add_argument('-f', '--file', required=True, help='Path to the input CSV file')
    
    # Parse the arguments
    args = parser.parse_args()
    input_file_path = args.file

    # Read the CSV into a DataFrame
    df = pd.read_csv(input_file_path)

    # Filter rows where mcc is 0
    filtered_df = df[df['mcc'] == 0]

    # Get the unique sequences from the filtered DataFrame
    unique_sequences = filtered_df['sequence'].unique()

    # Extract the puzzle name from the input file name
    puzzle_name = "EteV2_"+os.path.basename(input_file_path).split('_')[1]

    # Prepare the output file name
    output_file_path = input_file_path.replace('.csv', '.solutions')

    # Write to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(f">{puzzle_name}\n")
        for sequence in unique_sequences:
            output_file.write(f"{sequence}\n")

    print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    main()
