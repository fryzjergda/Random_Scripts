#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


import draw_varna_functions.RFparam as RFparam

def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='draw_varna', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-i", "--input", required=True, dest="input",
                            help="File with sequence and/or structure in FASTA format. Header id is not necessary.")
    parser.add_argument("-r", "--reactivity", required=False, dest="react",
                            help="File with reactivity profile.")
    parser.add_argument("-a", "--algorithm", required=False, dest="algorithm", default="radiate", type=str, choices=['line','circular','radiate','naview'],
                            help="Varna drawing mode.")
    parser.add_argument("-t", "--temperature", required=False, dest="temperature", default=37, type=int,
                        help="Folding temperature. [default = 37]")
    parser.add_argument("-sl", "--slope", required=False, dest="slope", default=1.9, type=float,
                        help="Slope value for SHAPE guided folding. [default = 1.9]")
    parser.add_argument("-in", "--intercept", required=False, dest="intercept", default=-0.7, type=float,
                        help="Intercept value for SHAPE guided folding. [default = -0.7]")
    parser.add_argument("-o", "--output", required=False, dest="output", default = "",
                            help="Output file name. If not provided the output will be generated basing on input file name.")
    parser.add_argument("-em", "--energymodel", required=False, dest="param", default="t", type=str, choices=['t','a'],
                            help="Energy model to use with RNAfold [t = Turner 2004, a = Andronescu 2007]")
    parser.add_argument("-p", "--predictor", required=False, dest="predictor", default="rf", type=str, choices=['rf','sk'],
                            help="Prediction method [rf = RNAfold, sk = ShapeKnots]")
    parser.add_argument("-c", "--cut", required=False, dest="cutter", default="", type=str,
                            help="Cut your input to specified range e.g.20-80. [default = no cutting]")





    args = parser.parse_args()

    input = args.input
    react = args.react
    alg = args.algorithm
    temperature = args.temperature
    slope = args.slope
    intercept = args.intercept
    output = args.output
    param = args.param
    predictor = args.predictor
    cutter = args.cutter
    
    return input, react, alg, temperature, slope, intercept, output, param, predictor, cutter


def read_file(input):

    
    with open(input) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        
    
    
    
    nts = set("AUGCT")
    dbs = set("().")
    
    id = "Name"
    sequence = ""
    structure = ""
    
    print(lines)
    for i, line in enumerate(lines):
        if line[0] == ">":
            id = line.replace(">","")
        elif any(l in line.upper() for l in nts):
            sequence = line.upper().replace("T","U")
        elif any(c in line for c in dbs):
            structure = line.split(" ")[0]
        
        
    return id, sequence, structure
        

def read_reactivity(in_react):

    with open(in_react) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    reactivities = ""
    
    if len(lines) == 1:
        reactivities = lines[0].replace("\t",";").replace(" ",";").replace(":",";").replace("NaN","-1.0").replace("-999.0","-1.0").replace("-999","-1.0").replace(",",".")

    elif len(lines) > 1 and "xml" not in lines[0]:
        for i in range(len(lines)):
            reac_val = lines[i].replace(" ",";").replace("\t",";").replace("NaN","-1.0").replace("-999.0","-1.0").replace("-999","-1.0").replace(",",".").split(";")
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
    

    return reactivities



def draw_varna(name, sequence, structure, reactivities, outfile):

    colormap = '0.0:#ffffff;0.001:#ffffcc;0.25:#fed976;0.5:#fd8d3c;0.75:#e31a1c;1:#800026'

    cmd = 'java -cp ' + VARNA_path + ' fr.orsay.lri.varna.applications.VARNAcmd -sequenceDBN ' + sequence + \
            " -structureDBN '" + structure + "' -o " + outfile +"_"+algorithm+".png  -resolution 10.0 -title '" +name +"' -titleSize 2" + \
            " -algorithm "+algorithm+" -colorMapMin '0.0' -colorMapMax '1.0' -colorMapStyle '" + colormap + "' -colorMap '" + reactivities + "'" + \
            " -bpStyle simple"

    os.system(cmd)


    pass


def check_infile(input):
    
    
    with open(input) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]


    isok =True    
    
    if len(lines) == 1 and lines[0] !=1 :
        lines.insert(0, ">RNA")
        isok = False
    

    text = ""
    
    for i in range(len(lines)):
        text += lines[i] + "\n"

    text = text.rstrip()        
    
    temp_file = open("temp.fa", 'w')
    temp_file.write(text)
    temp_file.close()
    
    
    return isok



def predict_ss():
    
    
    isok = check_infile(in_file)
    
    if isok == True:    
        input = in_file
    else:
        input = "temp.fa"

    if param == "a":
        em = "-P and.param "
    else:
        em = ""

    
    
    cmd = "RNAfold -p -d2 --noLP --noDP --noPS -T %s %s < %s" % (temperature, em, input)

    print(cmd, "\n")
        
    ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]  

    
    if isok == False:
        cmd = "rm temp.fa"
        os.popen(cmd)




    return ss



def predict_ss_shape():

    isok = check_infile(in_file)
    
    if isok == True:    
        input = in_file
    else:
        input = "temp.fa"
    
    if param == "a":
        em = "-P and.param "
    else:
        em = ""
        
    cmd = "RNAfold -p -d2 --noLP --noDP --noPS --shape=%s --shapeMethod=Dm%sb%s -T %s %s < %s" % (rfold_react,slope, intercept, temperature, em, input)

    print(cmd, "\n")
    ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]  


    if isok == False:
        cmd = "rm temp.fa"
        os.popen(cmd)

    return ss


def predict_ss_sk():

    cmd = "ShapeKnots-smp " + in_file + " tmp.ct -ph 100 -sm " + str(slope) + " -si " + str(intercept)
    os.system(cmd)

    cmd = "ct2dot tmp.ct 1 tmp.sk" 
    os.system(cmd)

    with open("tmp.sk") as file:
        lines = file.readlines()
        ss = lines[2]

    cmd = "rm tmp.ct"
    os.popen(cmd)


    return ss

    
def predict_ss_sk_shape():

    cmd = "ShapeKnots-smp " + in_file + " tmp.ct -ph 100 -sm " + str(slope) + " -si " + str(intercept) + " -sh " + rfold_react 
    os.system(cmd)

    cmd = "ct2dot tmp.ct 1 tmp.sk" 
    os.system(cmd)
    
    with open("tmp.sk") as file:
        lines = file.readlines()
        ss = lines[2]

    cmd = "rm tmp.ct"
    os.popen(cmd)

    
    return ss


def get_rfold_react():
    
    
    text = ""
    
    
    react_list = react_profile.split(";")
    
    for i in range(len(react_list)):
        text += str(i+1)+"\t"+react_list[i]+"\n"
    

    rfold_react_file = outname+"_RNAfold_reactivities.shape"    

    rnafold_file = open(rfold_react_file, 'w')
    rnafold_file.write(text)
    rnafold_file.close()
    
    return rfold_react_file


def write_out(id, seq, ss, outname):
    
    text = ">"+id + "\n" + seq + "\n" + ss 
    
    out_file = open(outname+"_DVout.db", "w")
    out_file.write(text)
    out_file.close()

    print("Output file: " + outname+"_DVout.db\n")    


def get_outname(outname):
    
    if outname == "":
        outname = in_file.split(".")[0]

    if temperature != 37:
        outname += "_T"+str(temperature)

    if slope != 1.9:
        outname += "_sl"+str(slope)

    if intercept != -0.7:
        outname += "_in"+str(intercept)

    if ss == "" and predictor == "sk":
        outname += "_SK"
    elif ss == "" and predictor == "rf":
        outname += "_Rfold"

    if react_profile != "":
        outname += "_shape"

    if param == "a":
        outname += "_AndronescuEM"

    if cutter != "":
        cut_range = cutter.split("-")
        cut_from = cut_range[0]
        cut_to = cut_range[1]
        outname += "_cut"+cut_from+"-"+cut_to
        
        
    return outname
    
def cut_inputs(sequence, structure, reactivities):

    cut_range = cutter.split("-")
    cut_from = int(cut_range[0])
    cut_to = int(cut_range[1])

    new_sequence = sequence[cut_from-1:cut_to]
    new_structure = structure[cut_from-1:cut_to]
    
    react_list = reactivities.split(";")
    new_reactivities = ";".join(react_list[cut_from-1:cut_to])    
    
    return new_sequence, new_structure, new_reactivities

def generate_temp_cut_fasta(seq):



    text = ">RNA\n"+seq

    text = text.rstrip()

    temp_file = open("temp_cut.fa", 'w')
    temp_file.write(text)
    temp_file.close()



def draw_heatmap(seq, react):


    result_heatmap = outname + '_heatmap.png'

    vmin = 0.0

    react_l = react.split(";")
    react_l = [float(i) for i in react_l]
    
    
    sns.set(font_scale=1)  # ticks font size

    if len(seq) > 600:
        size_fig_x = len(seq)*0.3
    elif len(seq) > 300:
        size_fig_x = len(seq)*0.6
    else:
        size_fig_x = len(seq)*1.2

    fig, ax = plt.subplots(figsize=(size_fig_x, 5))

    seq_split = list(seq)


    seqnum = []

    color_cmap = 'YlOrRd'

    
    c=0
    for i in seq_split:
        c+=1
        if c == 0:
            c=1
        seqnum.append(str(c) + '\n' + i)
     
    df2 = pd.DataFrame(react_l, columns=['ave2'])    
#    df4 =[['2', '3', '4', '5','2', '3', '4', '5']] 
    df4 = df2[["ave2"]].copy()
    df4 = df4.transpose()

#    print(df4)

    ax = sns.heatmap(df4, annot= False, cbar=True, xticklabels=seqnum, \
                     square=True, linewidths=1, linecolor= 'black', cmap=color_cmap, vmin=vmin, vmax=1.0)  # xticklabels=kok, takes labels from list


    if len(seq) > 600:
        xfontsize = 2
    elif len(seq) > 300:
        xfontsize = 12
    else:
        xfontsize = 25

    ax = sns.heatmap(df4.mask(df4 >= 0), cmap='Greys',xticklabels=seqnum, vmin=-999.0, vmax=-1.01, cbar=False,square=True, linewidths=2, linecolor= 'black')

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=xfontsize)
    plt.tight_layout(h_pad=0.1)
    plt.xticks(size=xfontsize, fontweight="bold")
    plt.yticks(size=xfontsize, fontweight="bold")
    ax.set(yticklabels=[])
    plt.savefig(result_heatmap,bbox_inches='tight')
    plt.clf()
    plt.close()

    pass




if __name__ == '__main__':

    VARNA_path = '~/Apps/VARNAv3-93.jar'
#    PARAM_path = 
    
    SCRIPT_path =os.path.abspath(__file__) 
    PARAM_path = SCRIPT_path.replace(".py", "_functions/")
    
    in_file, react_file, algorithm, temperature, slope, intercept, outfile, param, predictor, cutter = argument_parser()

    
    if param == "a":
        cmd = "cp "+ PARAM_path+"and.param ."
        os.system(cmd)

    id, seq, ss = read_file(in_file)
    

    react_profile = ""

    if react_file:

        react_profile = read_reactivity(react_file)


    if cutter != "":
        seq, ss, react_profile = cut_inputs(seq, ss, react_profile)
    
        generate_temp_cut_fasta(seq)
        
        
    outname = get_outname(outfile)


    with open(outname+'.log', 'w') as f:
        f.write("draw_varna.py "+'\n'.join(sys.argv[1:]).replace('\n',' ')+"\n")
        

    
    if react_profile != "":
        rfold_react = get_rfold_react()

    if react_file and len(react_profile.split(";")) != len(seq):
        print("There is a different number of reactivity values than nucleotides in the sequence. Aborting.")
        quit()

    print("Title:\n"+ id+"\n")
    print("Outfile:\n" + outname+ "\n")
    print("Sequence:\n" +seq+"\n")
    
    if cutter != "":
        in_file = "temp_cut.fa"
    pred_used = ""
    if predictor == "sk":
        pred_used = " with Shapeknots"
    elif predictor == "rf":
        pred_used = " with RNAfold"
        
    if ss == "":
        print("Structure:\nNot provided\n")
        print("Predicting structure"+pred_used+".\n")
    else:
        print("Structure"+pred_used+":\n" +ss+"\n")
    
    
    if ss == "" and react_profile == "":
        
        if predictor == "rf":
            ss = predict_ss()
        elif predictor == "sk":
        
            ss = predict_ss_sk()
        print("Predicted structure:"+pred_used+"\n" +ss+"\n")
        
    elif ss == "" and react_profile != "":
        
        if predictor == "rf":
            ss = predict_ss_shape()
        elif predictor == "sk":
            ss = predict_ss_sk_shape()

        print("Predicted structure with SHAPE reactivities"+pred_used+":\n" +ss+"\n")
        
    draw_varna(id, seq, ss, react_profile, outname)    


    write_out(id, seq, ss, outname)

    draw_heatmap(seq, react_profile)


    
    if param == "a":
        cmd = "rm and.param"
        os.system(cmd)

    if cutter != "":
        os.system("rm temp_cut.fa")