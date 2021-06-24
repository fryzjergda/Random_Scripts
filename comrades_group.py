#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import RawTextHelpFormatter
import os  
from textwrap import wrap
import csv


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__, prog='comrades_groups', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", required=True, dest="file",
                            help="Input csv file.")

    args = parser.parse_args() 

    infile = args.file

    return infile




def read_csv_to_list():
    with open(infile, 'r') as f:  # read sequence from file
        
        reads_list = []
        for line in f:
            line_list = line.rstrip().split(",")
#            print(line_list)            
            #quit()
            left_start = int(line_list[2])
            left_end = int(line_list[3])
            right_start = int(line_list[4])
            right_end = int(line_list[5])
            no_of_reads = int(line_list[7])
            sample = line_list[8]
            seq1 = line_list[10].upper().replace("T","U")
            seq2 = line_list[11].upper().replace("T","U")
            struct = line_list[12]
            seq1new = line_list[13].upper().replace("T","U")
            seq2new = line_list[14].upper().replace("T","U")
            
            data = [left_start,left_end,right_start,right_end,no_of_reads,sample,seq1,seq2,struct,seq1new,seq2new]
            reads_list.append(data)
            
            
            
            #seq = line.strip().replace("U","T").replace("u","t").upper()

    return reads_list


def group_reads(init_list):
    
    list_size = len(init_list)
    grouped_list = []
        
    for i in range(0,len(init_list)):
    
        init_list_mod, cluster = check_range(init_list, grouped_list)
        
        if init_list_mod != []:
            init_list = init_list_mod
        
        if cluster != []:
            grouped_list.append(cluster)    


#        print(i)
    #print(grouped_list)    
    #print(init_list)

      
    
    c =0
    
    for i in range(0,len(grouped_list)):
        c+=len(grouped_list[i])
        
    print(list_size, "input")
    print(c, "output")
    print(len(grouped_list), "no_of_groups")


#    for i in range(0, len(grouped_list)):
#        print("group", i)
#        for k in range(0, len(grouped_list[i])):
#            print(grouped_list[i][k][4])
    

    return grouped_list
#    print(grouped_list)
#    print(init_list)

def check_range(main_list, grouped):
    main_list2 = []

    clust_list = []
#    print(len(main_list))
#    print(main_list)
    for i in range(0,len(main_list)):
#        print(i)
        if i == 0:
            clust_list = [main_list[0]]
    #        print(clust_list)
        l_range_clust = range(clust_list[0][0],clust_list[0][1])
        r_range_clust = range(clust_list[0][2],clust_list[0][3])
        l_range_len_clust = clust_list[0][1] - clust_list[0][0]
        r_range_len_clust = clust_list[0][3] - clust_list[0][2]
        
        l_range_curr = range(main_list[i][0],main_list[i][1])
        r_range_curr = range(main_list[i][2],main_list[i][3])

#        print(l_range_clust, r_range_clust, l_range_curr, r_range_curr)        
        
        l_common = len(set(l_range_clust).intersection(l_range_curr))
        r_common = len(set(r_range_clust).intersection(r_range_curr))
#        print(l_common, r_common, l_range_len_clust, r_range_len_clust)
        if clust_list[0] != main_list[i]:
          if l_common/l_range_len_clust > simi_cutoff and r_common/r_range_len_clust > simi_cutoff:
#            print(l_common/l_range_len_clust, "left")
#            print(r_common/r_range_len_clust, "right")
#            print("yes")
            clust_list.append(main_list[i])        
          else:
#            print("kupka")
            main_list2.append(main_list[i])

    if clust_list[0] == main_list[0] and len(main_list) == 1:
      clust_list = []

#    print(len(main_list),"len(main_list)")
#    print(len(main_list2),"len(main_list2)")

#    print(len(clust_list), "len(clust_list)")
        
    return main_list2, clust_list        
        
    
def write_output():

    outfile = open(name+'.xml', "w")
    outfile.write(result_str)
    outfile.close


def write_groups(groups_list):
    
    path = "./"+name+"/"
    for i in range(0, len(groups_list)):
        with open(path+"group_"+str(i)+".csv", 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(groups_list[i])


def get_reps(groups):
    
    reps = []
    for i in range(0, len(groups)):
        groups[i] = sorted(groups[i], key=lambda x: x[4], reverse = True)
        reps.append(groups[i][0])


    return reps    
    
        

def change_borders(chimera):
    
    old_start_5 = chimera[0]
    old_end_5 = chimera[1]
    old_start_3 = chimera[2]
    old_end_3 = chimera[3]
    
    reads = chimera[4]
    
    old_seq_5 = chimera[6]
    old_seq_3 = chimera[7]
    
    struct = chimera[8]
    
    new_seq_5 = chimera[9]
    new_seq_3 = chimera[10]
    
    
    shifted = find_borders(old_seq_5, new_seq_5)
    
    new_start_5 = old_start_5 + shifted
    new_end_5 = new_start_5 + len(new_seq_5) -1
    
    shifted = find_borders(old_seq_3, new_seq_3)

    new_start_3 = old_start_3 + shifted
    new_end_3 = new_start_3 + len(new_seq_3) -1
    
    struct_5 = struct.split("&")[0]
    struct_3 = struct.split("&")[1]
    new_chimera = [new_start_5,new_end_5,new_start_3,new_end_3,reads,new_seq_5,new_seq_3,struct_5,struct_3]    
    
    return(new_chimera)

def find_borders(old_seq,new_seq):
    temp_seq = old_seq
    c = -1
    for i in range(0,len(old_seq)):
        if new_seq in temp_seq:
            c +=1
            temp_seq = temp_seq[1:]
        else:
            pass

    return c
    

def map_to_genome(chimeras):


    for i in range(0, len(chimeras))


    pass
    
    
if __name__ == '__main__':
    
    
    simi_cutoff = 0.5
    
    infile = argument_parser()
    
    name = ''.join(infile.split(".")[:-1])
    
    print(name)

    try:
        os.mkdir(name)
    except OSError:
        print ("Creation of the directory %s failed" % name)
    else:
        print ("Successfully created the directory %s " % name)

    init_reads_list = read_csv_to_list()

    grouped_reads_list = group_reads(init_reads_list)

    write_groups(grouped_reads_list)
    
    reps_list = get_reps(grouped_reads_list)

    new_reps_list = []
    for i in range(0,len(reps_list)):
        
        new_rep = change_borders(reps_list[i])        
        new_reps_list.append(new_rep)
            
    map_to_genome(new_reps_list)
    
    
    