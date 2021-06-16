#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import os  
from textwrap import wrap
import xml.etree.ElementTree as ET


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='fake_xml_generator', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-x", "--xml", required=True, dest="infile1",
                            help="Input file. XML with whole genome.")
    parser.add_argument("-l", "--list", required=False, dest="infile2",
                            help="Input file. Ilst of fragments (borders).")

    args = parser.parse_args() 

    in_xml = args.infile1
    in_list = args.infile2

    return in_xml, in_list






def read_genome_xml(xml_file):
    

    tree = ET.parse(xml_file)
    root = tree.getroot()


    seq_whole = root[0][0].text.replace("\t","").rstrip().replace("\n","")
    print(seq_whole)
    react_whole = root[0][1].text.replace("\t","").rstrip().replace("\n","")
    print(react_whole)


    return list(seq_whole), react_whole.split(",")
    



def generate_fake_xml_str(seq_frag, react_frag, name):


    fake_str = ""
    
    fake_str += '<?xml version="1.0" encoding="UTF-8"?>\n'
    fake_str += '<data combined="TRUE" norm="Box-plot" offset="1000000000" reactive="AC" remap="0" scoring="Zubradt" tool="rf-norm" win="1000000000">\n'
    fake_str += '        <transcript id="'+name+'" length="'+str(len(seq_frag))+'">\n'
    fake_str += '                <sequence>\n'
    fake_str += "".join(seq_frag)+"\n"
    fake_str += '                </sequence>\n'
    fake_str += '                <reactivity>\n'
    fake_str += ",".join(react_frag)+"\n"
    fake_str += '                </reactivity>\n'
    fake_str += '        </transcript>\n'
    fake_str += '</data>\n'


    return fake_str


    
    
def write_output(string, name):

    outfile = open(name+'.xml', "w")
    outfile.write(string)
    outfile.close


def read_list(in_list):

    with open(in_list) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    
    frag_list = []

    for i in range(0, len(content)):
        start = content[i].split("-")[0]
        end = content[i].split("-")[1]
        frag_list.append([int(start),int(end)])
    
    
    return frag_list

if __name__ == '__main__':

    in_xml, in_list = argument_parser()


    seq_whole, react_whole = read_genome_xml(in_xml)

    print(seq_whole)
    print(react_whole)
    
    
    frag_list = read_list(in_list)
    print(frag_list)
        
    
    for i in range(0, len(frag_list)):
        start = frag_list[i][0]
        end = frag_list[i][1]
        print(seq_whole)
        namea = "SARS-CoV-2_"+str(start)+"-"+str(end)+"_cX"
        nameb = "SARS-CoV-2_"+str(start)+"-"+str(end)+"_cY"
        name1 = "SARS-CoV-2_"+str(start)+"-"+str(end)+"_c0"
        name2 = "SARS-CoV-2_"+str(start)+"-"+str(end)+"_c1"
        
        frag_seq = seq_whole[start:end+1]    
        frag_react = react_whole[start:end+1]
    
        xml1 = generate_fake_xml_str(frag_seq, frag_react, name1)
        xml2 = generate_fake_xml_str(frag_seq, frag_react, name2)
        
        write_output(xml1, name1)
        write_output(xml2, name2)
    
    quit()
    
    
    name = ''.join(infile.split(".")[:-1])

    print(name)
    seq = read_fasta()
    seq_formatted, react_formatted = get_formatted_seq_react()

    result_str = generate_fake_xml_str()
    write_output()
    