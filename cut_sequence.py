#!/usr/bin/env python3

import argparse
import os
from Bio import SeqIO

def cut_fasta(input_fasta, fragment_length=5000, overlap=1000):
    # Read the input FASTA file
    with open(input_fasta, "r") as handle:
        record = next(SeqIO.parse(handle, "fasta"))  # Assume only one sequence in the file
    
    seq = str(record.seq)
    seq_length = len(seq)
    base_name = os.path.splitext(os.path.basename(input_fasta))[0]  # Get base name without extension
    
    # Step 1: Generate base fragment boundaries
    fragments = []
    start = 1
    while start <= seq_length:
        end = min(start + fragment_length - 1, seq_length)
        fragments.append([start, end])
        if end == seq_length:
            break
        start += fragment_length
    
    # Step 2: Adjust fragments to include overlaps
    adjusted_fragments = []
    for i, (core_start, core_end) in enumerate(fragments):
        if i == 0:
            # First fragment: Only add overlap after
            adjusted_start = core_start
            adjusted_end = min(core_end + overlap, seq_length)
        else:
            # Middle fragments: Add overlap before and after
            adjusted_start = max(core_start - overlap, 1)
            adjusted_end = min(core_end + overlap, seq_length)
        
        adjusted_fragments.append([adjusted_start, adjusted_end])
    
    # Step 3: Extract sequences and write to files
    output_files = []
    for i, (start, end) in enumerate(adjusted_fragments):
        fragment_seq = seq[start - 1:end]  # Convert to 0-based index for slicing
        output_filename = f"{base_name}_{start}_{end}.fa"
        
        with open(output_filename, "w") as out_fh:
            out_fh.write(f">{base_name}_{start}-{end}\n{fragment_seq}\n")
        
        output_files.append(output_filename)
    
    print(f"Generated files: {', '.join(output_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut an RNA sequence into overlapping fragments.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file")
    parser.add_argument("-l", "--length", type=int, default=5000, help="Fragment length (default: 5000)")
    parser.add_argument("-v", "--overlap", type=int, default=1000, help="Overlap length (default: 1000)")
    
    args = parser.parse_args()
    cut_fasta(args.input, args.length, args.overlap)