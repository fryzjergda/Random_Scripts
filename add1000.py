#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
from datetime import timedelta
from multiprocessing import Pool
from multiprocessing import cpu_count
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats.stats import pearsonr 


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='draw_varna', formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-r", "--reactivity", required=False, dest="react",
                            help="File with reactivity profile.")
    parser.add_argument("-b", "--before", required=False, dest="before",type = int,
                            help="File with reactivity profile.")
    parser.add_argument("-a", "--after", required=False, dest="after",type = int,
                            help="File with reactivity profile.")

    args = parser.parse_args() 

    react = args.react
    before = args.before
    after = args.after

    return react, before, after


def read_reactivity(in_react):

    with open(in_react) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    reactivities = ""

    if len(lines) == 1:
        reactivities = lines[0].replace("\t",";").replace(" ",";").replace(":",";").replace("NaN","-1.0").replace("-999","-1.0").replace(",",".")

    elif len(lines) > 1 and "xml" not in lines[0]:
        for i in range(len(lines)):
            reac_val = lines[i].replace(" ",";").replace("\t",";").replace("NaN","-1.0").replace("-999","-1.0").replace(",",".").split(";")
            if len(reac_val) > 1:
                reac_val = reac_val[1]
            elif len(reac_val) == 1:
                reac_val = reac_val[0]
            reactivities += str(reac_val) + ";"
    elif len(lines) > 1 and "xml" in lines[0]:
        react_xml = ""
        with open(in_react) as lines:
            for line in lines:
                if "<reactivity>" in line.strip():
                    break
            for line in lines:
                if "</reactivity>" in line.strip():
                    break

                react_xml += line.strip()
        reactivities = react_xml.replace(" ",";").replace(",",";").replace("\t",";").replace("NaN","-1.0").replace("-999","-1.0").replace(",",".")

    reactivities = reactivities.rstrip(";")
    reactivities = reactivities.split(";")
    reactivities = [float(i) for i in reactivities]
    for i in range(len(reactivities)):
        if reactivities[i] < 0 and reactivities[i] != -1:
            reactivities[i] = 0.0
    #reactivities = [reactivities]

#    reactivities = [ '%.3f' % elem for elem in reactivities ]
    reactivities = list(np.around(np.array(reactivities),3))

    return reactivities
    

def add_stuff(r, b, a):
    
    print(r)

    b_l = [-1.0]*b
    a_l = [-1.0]*a
    
    
    new_r= b_l+r+a_l

    return new_r
    
    
def get_rfold_react(r):


    text = ""


#    react_list = react_profile.split(";")
    
    for i in range(len(r)):
        text += str(i+1)+"\t"+str(r[i])+"\n"
    

    rfold_react_file = react+"500"

    rnafold_file = open(rfold_react_file, 'w')
    rnafold_file.write(text)
    rnafold_file.close()

    pass    
    

if __name__ == '__main__':



    react, before, after = argument_parser()

    react_prof = read_reactivity(react)

    react1000 = add_stuff(react_prof, before, after)
    
    get_rfold_react(react1000)