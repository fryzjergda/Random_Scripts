#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import RawTextHelpFormatter
import os  
from textwrap import wrap


def argument_parser():

    parser = argparse.ArgumentParser(prog="db2con")
    
    parser.add_argument("-i", "--input", required=False, dest="infile",
                        help="input file")
    
    args = parser.parse_args()
    
    infile = args.infile

    return infile




def get_pair_list(ss):
#    print("get pair list")

    db_list = [['(',')'],['[',']'],['<','>'],['{','}'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
    allowed_characters = '()[]<>{}AaBbCcDdEe.'

    stack_list =[]
    pairs_list =[]


    # stack-pop for all versions of brackets form the db_list    
    for i in range(0, len(db_list)):
        for c, s in enumerate(ss):
            if s == db_list[i][0]:
                stack_list.append(c)
            elif s == db_list[i][1]:
                if len(stack_list) == 0:
                    sys.exit("There is no opening bracket for nt position "+str(c+1)+'-'+ss[c])
                elif s == db_list[i][1]:
                    pairs_list.append([stack_list.pop(), c])
        if len(stack_list) > 0:
            err = stack_list.pop()
            sys.exit("There is no closing bracket for nt position "+str(err)+'-'+ss[err])

    pairs_list_clean = [x for x in pairs_list if x != []]
    pairs_list.sort(key=lambda x: x[0])

    return pairs_list





def read_dotbracket(instring):
    
    
    with open(instring, 'r') as f:
        for line in f:
            ss_db = line.strip()
        


    return ss_db
    


def list_to_con(pairs):


    string = "Pairs:\n"
    
    for i in range(0, len(pairs)):
        string += str(pairs[i][0]+1)+" "+str(pairs[i][1]+1)+"\n"

    string+="-1 -1"
    
    return string
    
    
def write_output(string):
    
    outfile = open(name+".con", "w")
    outfile.write(string)
    outfile.close()
    

if __name__ == '__main__':


    infile = argument_parser()

    name = ''.join(infile.split(".")[:-1])

    print(name)
    
    ss_db = read_dotbracket(infile)
    
    ss_pairs = get_pair_list(ss_db)
    
    ss_con = list_to_con(ss_pairs)
    
    
    write_output(ss_con)    


    print("dotbracket converted to .con file, SUCCESS!")    