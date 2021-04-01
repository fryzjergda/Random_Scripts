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
                            help="Secondary structure in CT format.")
    parser.add_argument("-d", "--debug", required=False, dest="debug", default="off", choices=["off", "on"],
                                 help="Debug mode.")     

    args = parser.parse_args() 

    infile = args.file
    debug = args.debug

    return infile, debug



def bracket_to_pair(ss):


    db_list = [['(',')'],['[',']'],['<','>'],['{','}'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
    
    stack_list = []
    pairs_list = []


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

    pairs_list = sorted(pairs_list, key=lambda x: x[0]) # this sorting is super important for later, when changing pair list to brackets

    return pairs_list


def pair_to_bracket(pairs_list):

#    db_list = [['(',')'],['[',']'],['{','}'],['<','>'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
#    db_list = [['(',')'],['{','}'],['[',']'],['<','>'],['A','a'],['B','b'],['C','c'],['D','d'],['E','e']]
    db_list = [['(',')'],['[',']'], ['<','>']]
    
    if debug == True:
        seq_len = len(ss_1) #len(sequence)    
    else:
        seq_len = sequence_len
    
    array_list = []

    for i in range(0,len(db_list)):
        array_list.append(np.zeros(shape=(len(pairs_list),seq_len)))
    

    for i in range(0,len(pairs_list)):
        array_list[0][i, pairs_list[i][0]] = 1
        array_list[0][i, pairs_list[i][1]] = -1

    
    for i in range(0,len(array_list)):
        print("\n\nARRAY", i)
        current_arr = array_list[i]
        c = 0

        while len(current_arr) >1 :
            vec1 = current_arr[0]
            vec2 =  current_arr[1]
            sum_vec = vec1 + vec2
            print(c,"/",len(pairs_list))
            try:
                pos1 = np.nonzero(vec2)[0][0]
                pos2 = np.nonzero(vec2)[0][-1]
                sum_pos = sum(sum_vec[pos1:pos2+1])

                sumvec_frag_pos = list(np.nonzero(sum_vec[pos1:pos2+1])[0])
                oneone = list(itemgetter(sumvec_frag_pos)(sum_vec[pos1:pos2+1]))

                in_order = checkConsecutive(oneone)
            
            
                if (sum_pos == 0) and (in_order == True):
                    current_arr[1] = sum_vec
                    current_arr = np.delete(current_arr, (0), axis =0) 
                else:
                    array_list[i+1][c] = vec2
                    current_arr = np.delete(current_arr, (1), axis =0)

            except:
                current_arr = np.delete(current_arr, (1), axis =0)
            c+=1
            
        array_list[i] = current_arr

    print("\nFINAL\n\n")

    list_brackets = []

    for i in range(0, len(array_list)):
        positions = np.where(array_list[i] == 1)[1]
        if len(positions) != 0:
            list_brackets.append(positions.tolist())
    
#    list_brackets = sorted(list_brackets, key=len, reverse = True)

    for i in range(0, len(list_brackets)):
        print(len(list_brackets[i]))


    new_ss = list("."*seq_len)

    for i in range(0, len(list_brackets)):
        print(len(list_brackets[i]))
        print(db_list[i])
        open = db_list[i][0]
        close = db_list[i][1]
        for k in range(0, len(pairs_list)):
            for l in range(0, len(list_brackets[i])):
                if pairs_list[k][0] == list_brackets[i][l]:
                    new_ss[pairs_list[k][0]] = open
                    new_ss[pairs_list[k][1]] = close
    
    
    return ''.join(new_ss)

def checkConsecutive(x):
    return sorted(x, reverse= True) == x



def read_ct(file):

    f=open(file,"r")
    lines=f.readlines()
    result=[]
    for x in lines:
        print(x)
        if len(x.split()) < 4:
            result.append([x.split()[0]])
        else:
            result.append([x.split()[0], x.split()[4]])
    f.close()
    
    seq_len = result[0][0]
    
    result.pop(0)
    
    pairs= []
    
    print(result)
    
    for i in range(0, len(result)):
        nt1 = int(result[i][0])-1
        nt2 = int(result[i][1])-1
        if nt2 != -1:
            pairs.append([nt1,nt2])
    
    print(pairs)

    pairs_nodouble = []
    for i in range(0, len(pairs)):
        if pairs[i][0] < pairs[i][1]:
            pairs_nodouble.append(pairs[i])

    print(pairs_nodouble)
    
    return pairs_nodouble, int(seq_len)


if __name__ == '__main__':


    infile, debug = argument_parser()
    
    outname = infile.split(".")[0]
    
    if debug == "off":
        print("ct2dot_pie!")
        p_list, sequence_len = read_ct(infile)
        new_ss = pair_to_bracket(p_list)
        print(new_ss)
        
        outfile = open(outname+".db", "w")
        outfile.write(new_ss)
        outfile.close
        
        
    else:

    #infile, ss_to_map_in = argument_parser()
        sequence = "xxxxxxxxxxxxxxxx"
#    ss_1 = "(((<<.[[..)))>>...]]"
#    ss_1 = "......(..(.((((([...(((((.........................((((((.((................{................................)).))))))..((((((((....)))))))){{{...........)))))..{{{{{{{{<................))))).)[[)((...)).]]..((((]((...........}}}}.}}}}.....}}}....((((((.......))))))......[}..........((((.((..((...(((((.......)))))))..)).))))..........{...................A..........>)).))))..............(((((.............<<))))).............(...(.((.................]((([((...............BB.(((((((........C))))))).................)).)))..........}....{.....((((((((((.a...)))..)))))))..{{)){).....((((((........A>>..))))))...........<<)(..((((.....))))...D...........]((..........bb))...................[c..}..}}..............................((((}((.(((.((((....)))).....(((((((((........))))))))))))..)).)))).a.....).>>....(((((((((.(((.........((((((d..............))))))........))).)))))))))...(.{.]......................).............(((((((.(((...(((((....)))))...))).......))))))).....(([[.......))(...(......((((((.....))))))....(((((.(((.....))).)))))..................(((.(((((}(.......).))))).)))..............................(((((((.....)))))))........{{{{{....){{{)(((((....(]].((((((.((.......)).))))))...................)...)))).).}}}......}}}}}...."
#    ss_1 = ".((....[..{..<.......))......]..}...(...>..)."
#    ss_1 = "..(....[...{..<...A...B..)...(.]..}..[...>...{a....(...b...).)...].(.}..(...))."
#    ss_1 = ".((....[..{..<.......))......]..}...(...>....[...{..<...A...B..)...(.]..}..[...>...{a....(...b...).)...].(.}..(...))..(....)."
        ss_1 = "......................(((((((.((.................[[[[[..))..))))))).....................................(((....{..{..........<<<.{...((((............))))(((.(...A.(.AA.....................................((((((....))))))............]]]]][.........................BCCCC..........)[[[[[)[)))[[.[[DD))).....}}>>>}......................((((((aa..((((.a......))))...((((....))))....))))))...]].]]...](]]]]]..)...............(((((((((]...................[.[[[..b....cccc.......{.{.....)))))))))dd....((........<<<.....(((((.((((...(.A(((.((((BBB...((((((.......)))))).....(......)CCC.DD.............))))E))).......((((((((....)).)))))).............]]]..].............}[})[[[[)))).)))))...........))>>>..........................(((.a..bbb.((((.((((((....))))))))))..........ccc....dd.....(((((((e.............)))))))...]]]]((...{...)).....(((.........{...)))......<<.]}.......[[[[[...............[[[[[[[...............)))(((...AAAA....................................BB]]]]]]].......(((.(.(((((]]]]]..........>>.........)))))}).))).(((((..(((........[..))).))))).................{{{..[[[)))(<<<..........................aaaa..................)...]]]((((.......bb................................................(.(((((((((.......))))))..)))A).AAA....].((((....)))).}}}((((............>>>...)))).......))))..............................((.....[...{{..............................(((((((((((((.((((.((((....((.....(((((((((.(((......(.aaa.)<a..))).)))))..))))AAA))A))))))))...)))))))))))))...<<<B.{{.BB...CCC.........................))..(.(](..}}}}>>>....................................((.(((((..[.........))))))).......................>...a..aaa.(({{{{.......(((........((.......bb..<..b))......ccc..)))............))...[[A).)....)....((((...........]]..................B......................].....((.(((((((..((((......(...........}})}}....))))))))))).)).....[[[[[[[.[[[[[....[[>[[[[.....((((((...))))))................a.))))........]]]].]].....]]]]]...]]]]]]].......b.(...................)..................................................."    

        print("\n\nBRACKET TO PAIR\n\n")
        p_list = bracket_to_pair(ss_1)

        print("\n\nPAIR TO BREACKET \n\n")
        new_ss = pair_to_bracket(p_list)

        new_p_list = bracket_to_pair(new_ss)

        print(ss_1, "\n")
        print(new_ss)
    
        if ss_1 == new_ss:
            print("\nsuccess! both structures are the same")
        else:
            print("\nyou are a kupka, structures are not the same")
    
    
        if p_list == new_p_list:
            print("\ni tak jestes zwyciezca,  both pair lists are the same")
        else:
            print("\nnadal jestes kupkom, pair lists are different")
