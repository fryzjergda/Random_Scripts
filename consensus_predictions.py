#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import argparse
import tempfile
import os


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='consensus_predictions.py', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--file", required=True, dest="file",
                        help="Input file. Containing name, sequence and secondary structure.")
    parser.add_argument("-w", "--weigth", required=False, dest="weigth", default = "0.5",
                        help="Weigth value for Consensus Finder")

    args = parser.parse_args() 

    infile = args.file
    weigth = args.weigth

    return infile, weigth


def create_tempfile(sequence):

    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, dir="./")
    temp.write(">temp\n")
    temp.write(sequence)
    temp.close()

    return temp.name


def predict_ss(predictor, sequence):

    sequencelen = len(input_rna.seq)

    if predictor == "LinearFold_C":
        cmd = "cat " + sequence + " | linearfold"
        ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]
    elif predictor == "LinearFold_V":
        cmd = "cat " + sequence + " | linearfold -V"
        ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]
    elif predictor == "RNAfold":
        cmd = "RNAfold -p -d2 --noLP --noPS --noDP < %s" % (sequence)
        ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]
    elif predictor == "ProbKnot":
        cmd = "ProbKnot --sequence " + sequence + " ProbKnot.ct"
        os.system(cmd)
        cmd = "ct2dot ProbKnot.ct 1 ProbKnot.dot"
        os.system(cmd)
        f = open("ProbKnot.dot", 'r')
        ss = f.read().splitlines()[2]
        f.close()
        cmd = 'rm ProbKnot.ct ProbKnot.dot'
        os.system(cmd)
    elif predictor == "Fold":
        cmd = "Fold " + sequence + " Fold.dot -k -q"
        os.system(cmd)
        f = open("Fold.dot", 'r')
        ss = f.read().splitlines()[2]
        cmd = 'rm Fold.dot'
        f.close()
        os.system(cmd)
    elif predictor == "CentroidFold":
        cmd = "centroid_fold " + sequence
        try:
            ss = os.popen(cmd).read().splitlines()[2].split(' ')[0]
        except:
            ss = '.'*sequencelen
    elif predictor == "CONTRAfold":
        cmd = "contrafold predict " + sequence
        ss = os.popen(cmd).read().splitlines()[2]
    elif predictor == "IPknot":
        cmd = "ipknot " + sequence
        try:
            ss = os.popen(cmd).read().splitlines()[3]
        except:
            ss = '.'*(sequencelen)
    elif predictor == "ContextFold":
        print(sequence.split("/")[-1], "kuku")
        sequence = sequence.split("/")[-1]
        cmd = "cp "+sequence+" "+PATH_TO_CONTEXTFOLD+". ; cd "+PATH_TO_CONTEXTFOLD+"; java -cp bin contextFold.app.Predict in:" +sequence
        os.system(cmd)
        cmd = "mv "+PATH_TO_CONTEXTFOLD+sequence+".pred ."        
        os.system(cmd)
        cmd = "rm "+PATH_TO_CONTEXTFOLD+"%s"%sequence
        os.system(cmd)
        ss = os.popen("cat "+sequence+".pred").read().splitlines()[2]
    elif predictor == "SPOT-RNA":
        cmd = "SPOT-RNA.py --inputs "+sequence+" --outputs './'"    
        os.system(cmd)
        cmd = "ct2dot temp.ct 1 temp.dot"
        os.system(cmd)
        ss = os.popen("cat temp.dot").read().splitlines()[2]
        
    return ss


def get_sensitivity():
    # sensitivity = TP/(TP+FN)
    
    pass

def get_PPV():
    # PPV = TP/(TP+FP)
    
    pass
    
def get_F1():
    # F1 = (2*sensitivity*PPV)/(sensitivity+PPV)

    pass
    
def get_MCC():
    # MCC = (TP*TN - FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    
    pass
    
def get_confusion(predicted_pairs):
    # TP, FP, TN, FN
    
    native_pairs = input_rna.pairs
    
    
    keys = ["TP", "TN", "FP", "FN"]
    confusion_dict = {key: None for key in keys}

    confusion_dict["TP"] = len(list(set(native_pairs).intersection(predicted_pairs)))

    TN = 


    
    print(confusion_dict)

    
    
    pass
    
    

def get_pair_list(ss):
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
                    pairs_list.append((stack_list.pop(), c))
        if len(stack_list) > 0:
            err = stack_list.pop()
            sys.exit("There is no closing bracket for nt position "+str(err)+'-'+ss[err])

    pairs_list_clean = [x for x in pairs_list if x != []]
    

    return pairs_list
    

def read_file():
    
    with open(infile) as f:
        lines = f.read().splitlines()
        
    input_rna = Input(name = lines[0])
    input_rna.add_seq(lines[1])
    input_rna.add_ss(lines[2])
    input_rna.add_pairs(lines[2])
    print(vars(input_rna))
    
    return input_rna
    
    
class Input:
    def __init__(self, name):
        self.name = name.replace(">","")
        self.seq = None
        self.ss = None
        
    def add_seq(self, seq):
        self.seq = seq
    
    def add_ss(self, ss):
        self.ss = ss

    def add_pairs(self, ss):
        self.pairs = get_pair_list(ss)


if __name__ == '__main__':

    PATH_TO_CONTEXTFOLD = "/home/fryzjer/Apps/ContextFold_1_00/"
    predictors = ["LinearFold_C","LinearFold_V","RNAfold", "ProbKnot", "Fold", "CentroidFold", "CONTRAfold", "IPknot", "ContextFold"]#,"SPOT-RNA"]

    infile, weigth = argument_parser()

    outname = '_'.join(infile.split(".")[:-1])

    input_rna = read_file()
    seqfile = create_tempfile(input_rna.seq)
    
    
    for i in range(0,len(predictors)):
        predictor = predictors[i]
        print(predictor)
        ss = predict_ss(predictor, seqfile)
        pairs = get_pair_list(ss)
        get_confusion(pairs)        
        print(ss)
    
    
    
    os.system("rm %s *.pred"%seqfile)