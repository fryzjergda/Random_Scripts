#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import RawTextHelpFormatter
import os  
from textwrap import wrap
import xml.etree.ElementTree as ET
tree = ET.parse('items2.xml')
root = tree.getroot()


#print(root.attrib)

#for elem in root:
#    for subelem in elem:
#        print(subelem.attrib)

#print(root[0][0].text)

seq = root[0][0].text.replace("\t","").rstrip().replace("\n","")
print(seq)
react = root[0][1].text.replace("\t","").rstrip().replace("\n","")
print(react)

'''
def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='fake_xml_generator', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", required=True, dest="file",
                            help="Input file. One-line FASTA format.")

    args = parser.parse_args() 

    infile = args.file

    return infile
'''
