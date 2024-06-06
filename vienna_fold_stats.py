#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import RNA

def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='viennarna fold stats', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-i", "--input", required=True, dest="infile",
                            help="Input file. multiple fasta.")
    parser.add_argument("-o", "--outname", required=False, dest="outname", default = "",
                            help="Output file name.")

    args = parser.parse_args() 

    in_file = args.infile
    outname = args.outname

    return in_file, outname


def read_rna_file(filepath):
    """
    Read an RNA sequence file where each entry is formatted as:
    >rnaname
    sequence
    This function returns a list of lists, where each sublist contains [name, sequence].
    """
    rnas = []  # List to store result
    current_name = None  # Current RNA name
    current_seq = []  # Current RNA sequence

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()  # Remove whitespace
            if line.startswith('>'):  # RNA name line
                if current_name:  # If not the first name, save the previous RNA
                    rnas.append([current_name, ''.join(current_seq)])
                    current_seq = []  # Reset for the next RNA
                current_name = line[1:]  # Remove '>' and save the name
            else:  # Sequence line
                current_seq.append(line)  # Add line to current sequence
        # Don't forget to save the last RNA in the file
        if current_name:
            rnas.append([current_name, ''.join(current_seq)])

    return rnas


def get_stats(rna, stat_text):

    rna_name, seq = rna

    fc = RNA.fold_compound(seq)

    pf_str, pf_e = fc.pf()

    mfe_str, mfe_e = fc.mfe()

    pf_freq = fc.pr_structure(mfe_str)

    pf_div = fc.mean_bp_distance()

    stats = "RNA\n>"+ rna_name+"\n\nSequence:\n"+seq+"\n\nMFE structure:\n" + mfe_str +"\n\nMFE energy:\n" +str(round(mfe_e,3)) + \
            " kcal/mol\n\nPartrition function structure:\n" + pf_str + "\n\nPartition fucntion energy:\n" +str(round(pf_e,3)) + \
            " kcal/mol\n\nThe frequency of the MFE structure in the ensemble is: " +str(round(pf_freq*100,2))+ \
            " %\n\nThe ensemble diversity is: " + str(round(pf_div,3)) + "\n\n-------------------------\n\n\n"


    stat_text += stats


    return stat_text

def write_output(text, name):

    outfile = open(name+'.stats', "w")
    outfile.write(text)
    outfile.close

if __name__ == '__main__':

    in_file, outname = argument_parser()

    list_of_rnas = read_rna_file(in_file)


    out_text = ""

    for i in range(len(list_of_rnas)):

        
        out_text += get_stats(list_of_rnas[i], out_text)


    if outname == "":
        outname = list_of_rnas[0][0]

    write_output(out_text, outname)

    print(out_text)

