#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import RNA
from multiprocessing import Pool
import os


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='viennarna fold parallel', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-i", "--input", required=True, dest="infile",
                            help="Input file. multiple fasta.")
    parser.add_argument("-o", "--outname", required=False, dest="outname", default = "vienna_fold",
                            help="Output file name.")

    args = parser.parse_args() 

    in_file = args.infile
    outname = args.outname

    return in_file, outname


def read_fasta(filepath):
    
    with open(filepath, 'r') as file:
        entries = file.read().split('>')[1:]  
        sequences = [(entry.split('\n', 1)[0], entry.split('\n', 1)[1].replace('\n', ''))
                     for entry in entries]
    return sequences


def vienna_fold(rna):

    rna_name, seq = rna

    fc = RNA.fold_compound(seq)

    structure, mfe = fc.mfe()

    print(f"Name: {rna_name}, Sequence: {seq}, Structure: {structure}, MFE: {mfe}")

    return rna_name, seq, structure, mfe


def write_output(text, outname):

    outfile = open(outname+'.predictions', "w")
    outfile.write(text)
    outfile.close


def run_predictions(list_of_rnas, outname):

    num_processes = os.cpu_count()

    with Pool(processes=num_processes) as pool:
        results = pool.map(vienna_fold, list_of_rnas)

    results_separate = ["Name: {}, Sequence: {}, Structure: {}, MFE: {}".format(*result) for result in results]
    results_text = "\n".join(results_separate)
    
    write_output(results_text, outname)


if __name__ == '__main__':

    in_file, outname = argument_parser()

    list_of_rnas = read_fasta(in_file)

    run_predictions(list_of_rnas, outname)
    
