#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import RawTextHelpFormatter
import os  
from textwrap import wrap


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='fake_xml_generator', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", required=True, dest="file",
                            help="Input file. One-line FASTA format.")

    args = parser.parse_args() 

    infile = args.file

    return infile



def read_fasta():
    with open(infile, 'r') as f:  # read sequence from file

        for line in f:
          if line[0] !=">" and line[0] != "\n":
            #print(f.readline())
            seq = line.strip().replace("U","T").replace("u","t").upper()

    print("kko",seq)
    return seq
    
    

def get_formatted_seq_react():
    
    seq_list = wrap(seq,60)

    seq_f = ""
    react_f = ""
    for i in range(0, len(seq_list)):
        seq_f += 24*" "+seq_list[i]+"\n"
        react_f += 24*" "+"NaN,"*len(seq_list[i])+"\n"
    
    return seq_f, react_f.rstrip(",\n")
    
    
    
def generate_fake_xml_str():


    fake_str = ""
    
    fake_str += '<?xml version="1.0" encoding="UTF-8"?>\n'
    fake_str += '<data combined="FALSE" maxmutrate="1" maxumut="0.05" norm="Box-plot" offset="1000000000" reactive="ACGT" remap="0" scoring="Siegfried" tool="rf-norm" win="1000000000">\n'
    fake_str += '        <transcript id="'+name+'" length="29903">\n'
    fake_str += '                <sequence>\n'
    fake_str += seq_formatted
    fake_str += '                </sequence>\n'
    fake_str += '                <reactivity>\n'
    fake_str += react_formatted+"\n"
    fake_str += '                </reactivity>\n'
    fake_str += '        </transcript>\n'
    fake_str += '</data>\n'


    return fake_str    


def write_output():

    outfile = open(name+'.xml', "w")
    outfile.write(result_str)
    outfile.close



if __name__ == '__main__':

    infile = argument_parser()
    
    name = ''.join(infile.split(".")[:-1])
    
    print(name)
    seq = read_fasta()
    seq_formatted, react_formatted = get_formatted_seq_react()
        
    result_str = generate_fake_xml_str()
    write_output()
    