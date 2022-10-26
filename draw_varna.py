#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import argparse
import os

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




    args = parser.parse_args()

    input = args.input
    react = args.react
    alg = args.algorithm
    temperature = args.temperature
    
    return input, react, alg, temperature


def read_file(input):

    
    with open(input) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        
    
    
    
    nts = set("AUGCT")
    dbs = set("().")
    
    id = "Name"
    sequence = ""
    structure = ""
    
    for i, line in enumerate(lines):
        if line[0] == ">":
            id = line.replace(">","")
        elif any(l in line.upper() for l in nts):
            sequence = line.upper()
        elif any(c in line for c in dbs):
            structure = line.split(" ")[0]
        
        
    return id, sequence, structure
        

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
    

    return reactivities



def draw_varna(name, sequence, structure, reactivities, outfile):

    colormap = '0.0:#ffffff;0.001:#ffffcc;0.25:#fed976;0.5:#fd8d3c;0.75:#e31a1c;1:#800026'

    cmd = 'java -cp ' + VARNA_path + ' fr.orsay.lri.varna.applications.VARNAcmd -sequenceDBN ' + sequence + \
            " -structureDBN '" + structure + "' -o " + outfile +"_"+algorithm+".png  -resolution 10.0 -title '" +name +"' -titleSize 10" + \
            " -algorithm "+algorithm+" -colorMapMin '0.0' -colorMapMax '1.0' -colorMapStyle '" + colormap + "' -colorMap '" + reactivities + "'"

    os.system(cmd)


    pass



def predict_ss():
    
    
    cmd = "RNAfold -p -d2 --noLP --noDP --noPS -T %s < %s" % (temperature, in_file)
    
    ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]  

    return ss



def predict_ss_shape():

    cmd = "RNAfold -p -d2 --noLP --noDP --noPS --shape=%s --shapeMethod=D -T %s < %s" % (rfold_react, temperature, in_file)

    print(cmd)
    ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]  

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


if __name__ == '__main__':

    VARNA_path = '~/Apps/VARNAv3-93.jar'
    
    in_file, react_file, algorithm, temperature = argument_parser()

    outname = in_file.split(".")[0]

    if temperature != 37:
        outname += "_T"+str(temperature)
        
        
    id, seq, ss = read_file(in_file)

    
    
    react_profile = ""
    
    if react_file:
    
        react_profile = read_reactivity(react_file)
    
    if react_profile != "":
        rfold_react = get_rfold_react()

    if react_file and len(react_profile.split(";")) != len(seq):
        print("There is a different number of reactivity values than nucleotides in the sequence. Aborting.")
        quit()

    print("Title:\n"+ id+"\n")
    print("Sequence:\n" +seq+"\n")
    
    if ss == "":
        print("Structure:\nNot provided\n")
    else:
        print("Structure:\n" +ss+"\n")
    
    
    if ss == "" and react_profile == "":
        ss = predict_ss()
        print("Predicted structure:\n" +ss+"\n")
    elif ss == "" and react_profile != "":
        ss = predict_ss_shape()
        print("Predicted structure with SHAPE reactivities:\n" +ss+"\n")
        
        
    draw_varna(id, seq, ss, react_profile, outname)    

    