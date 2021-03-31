#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import RawTextHelpFormatter
import os   
import numpy as np
from operator import itemgetter

def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='map_ss_to_ali', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", required=True, dest="file",
                            help="Input alignment file. Multiple sequence alignment in one-line FASTA format.")
    parser.add_argument("-s", "--sec_struct", required=False, dest="sec_struct", #default="linear", choices=["rnafold", "linear"],
                                 help="Structure to be mapped, should be a valid structure for first sequence in teh alignment")     

    args = parser.parse_args() 

    infile = args.file
    ss_to_map_in = args.sec_struct

    return infile, ss_to_map_in





def bracket_to_pair(ss):


    db_list = [['(',')'],['[',']'],['<','>'],['{','}'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
    
    stack_list = []
#    stack_list = [[] for i in range(0, len(db_list))]
#    pairs_list = [[] for i in range(0, len(db_list))]
    pairs_list = []
    # stack-pop for all versions of brackets form the db_list    


    for i in range(0, len(db_list)):
        for c, s in enumerate(ss):
            if s == db_list[i][0]:
                stack_list.append(c)
            elif s == db_list[i][1]:
                if len(stack_list) == 0:
                    raise IndexError("There is no opening bracket for nt position "+str(c)+'-'+ss[c])
                elif s == db_list[i][1]:
                    pairs_list.append([stack_list.pop(), c])

        if len(stack_list) > 0:
            err = stack_list.pop()
            raise IndexError("There is no closing bracket for nt position "+str(err)+'-'+ss[err])

    pairs_list = sorted(pairs_list, key=lambda x: x[0])

    return pairs_list


def pair_to_bracket(pairs_list):

#    db_list = [['(',')'],['[',']'],['{','}'],['<','>'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
    db_list = [['(',')'],['{','}'],['[',']'],['<','>'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
#    db_list = [['(',')'],['[',']'], ['<','>'],['{','}']]
#    db_list = [['(',')']]
    
    seq_len = len(ss_1) #len(sequence)    
    array_list = []

    for i in range(0,len(db_list)):
        array_list.append(np.zeros(shape=(len(pairs_list),seq_len)))
    

    for i in range(0,len(pairs_list)):
        array_list[0][i, pairs_list[i][0]] = 1
        array_list[0][i, pairs_list[i][1]] = -1

#    print(array_list)
    
    for i in range(0,len(array_list)):
        print("\n\nARRAY", i)
        current_arr = array_list[i]
        print(current_arr, "before")
        c = 0
        while len(current_arr) >1 :
            print("\nSTEP",c)
            vec1 = current_arr[0]
            print(vec1, "vec1")
            
            vec2 =  current_arr[1]
            print(vec2, "vec2")
            sum_vec = vec1 + vec2
            print(sum_vec,"sumvec")

            try:
                pos1 = np.nonzero(vec2)[0][0]
                pos2 = np.nonzero(vec2)[0][-1]
                print(np.nonzero(vec1), "tosum")
                print(pos1, pos2)
                sum_pos = sum(sum_vec[pos1:pos2+1])
                print(sum_vec[pos1:pos2+1], "sumvec portion")
                print(np.nonzero(sum_vec[pos1:pos2+1])[0], "nonzero in sumvec")
                sumvec_frag_pos = list(np.nonzero(sum_vec[pos1:pos2+1])[0])
                print(sumvec_frag_pos, "sumvec_frag_pos")
                oneone = list(itemgetter(sumvec_frag_pos)(sum_vec[pos1:pos2+1]))
                print(oneone, "oneone")
                in_order = checkConsecutive(oneone)
            
            
                if (sum_pos == 0) and (in_order == True):
                    print("merge")
                
                    current_arr[1] = sum_vec
                    current_arr = np.delete(current_arr, (0), axis =0) 
                    print(current_arr, "good")
                else:
                    print("go away")
                    array_list[i+1][c] = vec2
                    current_arr = np.delete(current_arr, (1), axis =0)
                    print(current_arr)
#                print(array_list)
            except:
                current_arr = np.delete(current_arr, (1), axis =0)
            c+=1
            
        array_list[i] = current_arr
        print(current_arr, "after") 
#    quit()           
    print("\nFINAL")
    print(array_list)

    list_brackets = []
    for i in range(0, len(array_list)):
        positions = np.where(array_list[i] == 1)[1]
        if len(positions) != 0:
            #print(positions)
            list_brackets.append(positions.tolist())
    
    print(list_brackets)
    for i in range(0, len(list_brackets)):
        print(len(list_brackets[i]))
    list_brackets = sorted(list_brackets, key=len, reverse = True)
    for i in range(0, len(list_brackets)):
        print(len(list_brackets[i]))

#    quit()
    new_ss = list("."*len(ss_1))
    print(ss_1)
    print(''.join(new_ss))    
    for i in range(0, len(list_brackets)):
        open = db_list[i][0]
        close = db_list[i][1]
        for k in range(0, len(pairs_list)):
            for l in range(0, len(list_brackets[i])):
                if pairs_list[k][0] == list_brackets[i][l]:
                    new_ss[pairs_list[k][0]] = open
                    new_ss[pairs_list[k][1]] = close
    
    print(''.join(new_ss), "here")
        
#    quit()
    
    return ''.join(new_ss)

def checkConsecutive(x):
    print("ordering!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(x)
    print(sorted(x, reverse= True) == x)
    return sorted(x, reverse= True) == x



if __name__ == '__main__':

    #infile, ss_to_map_in = argument_parser()
    sequence = "xxxxxxxxxxxxxxxx"
    ss_1 = "(((<<.[[..)))>>...]]"
    ss_1 = "......(..(.((((([...(((((.........................((((((.((................{................................)).))))))..((((((((....)))))))){{{...........)))))..{{{{{{{{<................))))).)[[)((...)).]]..((((]((...........}}}}.}}}}.....}}}....((((((.......))))))......[}..........((((.((..((...(((((.......)))))))..)).))))..........{...................A..........>)).))))..............(((((.............<<))))).............(...(.((.................]((([((...............BB.(((((((........C))))))).................)).)))..........}....{.....((((((((((.a...)))..)))))))..{{)){).....((((((........A>>..))))))...........<<)(..((((.....))))...D...........]((..........bb))...................[c..}..}}..............................((((}((.(((.((((....)))).....(((((((((........))))))))))))..)).)))).a.....).>>....(((((((((.(((.........((((((d..............))))))........))).)))))))))...(.{.]......................).............(((((((.(((...(((((....)))))...))).......))))))).....(([[.......))(...(......((((((.....))))))....(((((.(((.....))).)))))..................(((.(((((}(.......).))))).)))..............................(((((((.....)))))))........{{{{{....){{{)(((((....(]].((((((.((.......)).))))))...................)...)))).).}}}......}}}}}...."
    print(ss_1)
#    ss_1 = ".((....[..{..<.......))......]..}...(...>..)."
#    ss_1 = "..(....[...{..<...A...B..)...(.]..}..[...>...{a....(...b...).)...].(.}..(...))."
#    ss_1 = ".((....[..{..<.......))......]..}...(...>....[...{..<...A...B..)...(.]..}..[...>...{a....(...b...).)...].(.}..(...))..(....)."
    
    print(ss_1)
    print("\n\nBRACKET TO PAIR\n\n")
    p_list = bracket_to_pair(ss_1)
    #quit()
    print("\n\nPAIR TO BREACKET \n\n")
    new_ss = pair_to_bracket(p_list)

    print(p_list, "initial pairs")
    new_p_list = bracket_to_pair(new_ss)
    print(new_p_list, "new pairs")

    print(ss_1)
    print(new_ss)
    
    if ss_1 == new_ss:
        print("success!")
    else:
        print("you are a kupka")
    
    
    if p_list == new_p_list:
        print("i tak jestes zwyciezca")
    else:
        print("nadal jestes kupkom")
