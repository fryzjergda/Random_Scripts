#!/bin/bash

oldname=$1
db1=$2
db2=$3

sh1=$4
sh2=$5

method=$6

sed -s "s/$oldname/$oldname\_Rep1/" $db2 | sed -s "s/ConsensusModel/$oldname\_Rep1/" > $oldname"_Rep2.db"
sed -s "s/$oldname/$oldname\_Rep2/" $db1 | sed -s "s/ConsensusModel/$oldname\_Rep2/" > $oldname"_Rep1.db"

rf-compare -ow -r $oldname"_Rep1.db" $oldname"_Rep2.db" -g

#cp rf_compare/*svg $db1"_rf_compare_"$method.svg
cp rf_compare/*svg $oldname"_target_rf_compare_"$method.svg
rm $oldname"_Rep2.db" $oldname"_Rep1.db" 
rm -r rf_compare

r2.py -r1 $sh1 -r2 $sh2  


#rm $db1 $db2 $sh1 $sh2
