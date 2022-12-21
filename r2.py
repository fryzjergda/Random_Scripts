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


def argument_parser():


    parser = argparse.ArgumentParser(description=__doc__, prog='draw_varna', formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-r1", "--reactivity1", required=False, dest="react1",
                            help="File with reactivity profile.")
    parser.add_argument("-r2", "--reactivity2", required=False, dest="react2",
                            help="File with reactivity profile.")




    args = parser.parse_args() 

    react1 = args.react1
    react2 = args.react2

    return react1, react2


def calc_r2(y_test, y_predicted, outname):

    r2 =  r2_score(y_test, y_predicted)
    print(r2)
    
    
    
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_predicted)
#    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Repetition 1')
    ax.set_ylabel('Repetition 2')
    #regression line
#    y_test, y_predicted = y_test.reshape(-1,1), y_predicted.reshape(-1,1)
    ax.annotate("r-squared = {:.3f}".format(r2_score(y_test, y_predicted)), (0, 1))
    ax.plot([y_test], LinearRegression().fit([y_test], [y_predicted]).predict([y_test]))

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
    #reactivities = [reactivities]



    return reactivities




if __name__ == '__main__':



    r_file1, r_file2 = argument_parser()
    
    react_prof1 = read_reactivity(r_file1)
    react_prof2 = read_reactivity(r_file2)
    outname = r_file1.split(".")[0]
    
    
    print(react_prof1)
    print(react_prof2)
    
    calc_r2(react_prof1,react_prof2, outname)
    

    