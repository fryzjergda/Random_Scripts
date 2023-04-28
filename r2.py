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
from math import log


def argument_parser():


    parser = argparse.ArgumentParser(description=__doc__, prog='draw_varna', formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-r1", "--reactivity1", required=False, dest="react1",
                            help="File with reactivity profile.")
    parser.add_argument("-r2", "--reactivity2", required=False, dest="react2",
                            help="File with reactivity profile.")
    parser.add_argument("-c", "--cut", required=False, dest="cutter", default="", type=str,
                            help="Cut your input to specified range e.g.20-80. [default = no cutting]")
    parser.add_argument("-n", "--normalize", required=False, dest="norm", default='off', choices=['off','on'],
                            help="TBA")                            



    args = parser.parse_args() 

    react1 = args.react1
    react2 = args.react2

    cutter = args.cutter
    norm = args.norm

    return react1, react2, cutter, norm


def calc_r2(y_test, y_predicted, outname):

#    r2 =  r2_score(y_test, y_predicted)
#    print(r2)
    
    
#    p = pearsonr(y_test, y_predicted)[0]
#    print(p**2,"p")
    
    r2 = (pearsonr(y_test, y_predicted)[0])**2
    
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_predicted)
#    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel(r_file1)
    ax.set_ylabel(r_file2)
    ax.set_aspect('equal', adjustable='box')
    #regression line
#    y_test, y_predicted = y_test.reshape(-1,1), y_predicted.reshape(-1,1)
#    ax.annotate("r-squared = {:.3f}".format(r2_score(y_test, y_predicted)), (0, 1))
    plt.xlim([0, 2.5])
    plt.ylim([0, 2.5])
    ax.plot([y_test], LinearRegression().fit([y_test], [y_predicted]).predict([y_test]))
#    rsq = "r-squared = {:.3f}".format(r2_score(y_test, y_predicted))
    rsq = "r-squared = "+str(round(r2,3))

    print(rsq)
#    print(r2,"r2")
#    print(r2_new,"r2_new")
    plt.title(rsq)
    
    plt.savefig(outname+'_R2.png')

    
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



def cut_inputs(reactivities):

    cut_range = cutter.split("-")
    cut_from = int(cut_range[0])
    cut_to = int(cut_range[1])

    new_reactivities = reactivities[cut_from-1:cut_to]
#    react_list = reactivities.split(";")
#    new_reactivities = ";".join(reactivities[cut_from-1:cut_to])    
    
    return new_reactivities



def remove_outliers(r1, r2):

    
    list_to_remove = []
    
    for i in range(len(r1)):
        if r1[i] == -1.0:
            list_to_remove.append(i)
    
    for i in range(len(r2)):
        if r2[i] == -1.0:
            list_to_remove.append(i)

    indexes = list(set(list_to_remove))
    
    for index in sorted(indexes, reverse=True):
        del r1[index]
        del r2[index]
    
    
    return r1, r2
    

def normalize_reactivities_(react_prof):

    print(react_prof)
    
    norm_param = sum(react_prof)/len(react_prof)
    print(sum(react_prof), "sum(react)")
    
    print(norm_param)
    sum_l = 0
    
    for i in range(len(react_prof)):
        sum_l += react_prof[i]
    
    print(sum_l, "sum_lA")
    
    react_prof_new = [i / norm_param for i in react_prof]
    
    return react_prof_new


def normalize_reactivities(react_prof):
    
    print(react_prof)
    for i in range(len(react_prof)):
        #if react_prof[i] != 0:
            react_prof[i] = log(react_prof[i]+1)
    
    print(react_prof)

    return(react_prof)

if __name__ == '__main__':



    r_file1, r_file2, cutter, norm = argument_parser()
    
    react_prof1 = read_reactivity(r_file1)
    react_prof2 = read_reactivity(r_file2)
    outname = r_file1
    
    if cutter != "":
        react_prof1 = cut_inputs(react_prof1)
        react_prof2 = cut_inputs(react_prof2)
    
#    print(react_prof1)
#    print(react_prof2)
    
    react_prof1, react_prof2 = remove_outliers(react_prof1, react_prof2)
    
    if norm == "on":
        react_prof1 = normalize_reactivities(react_prof1)
        react_prof2 = normalize_reactivities(react_prof2)
    
#    print(react_prof1)
#    print(react_prof2)
    
    calc_r2(react_prof1,react_prof2, outname)
    

    