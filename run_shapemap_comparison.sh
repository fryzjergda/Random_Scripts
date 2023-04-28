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
cp rf_compare/*svg $oldname"_rf_compare_"$method.svg
rm $oldname"_Rep2.db" $oldname"_Rep1.db" 
rm -r rf_compare

r2.py -r1 $sh1 -r2 $sh2  

#echo cat $oldname"500.fa" | linearfold -V --shape $sh1"500" > $db1"500.db"

#cat $oldname"500.fa" | linearfold -V --shape $sh1"500" > $db1"500.db"
#cat $oldname"500.fa" | linearfold -V > $db1"500.db"



cat $oldname"500.fa" | linearfold -V --shape $sh2"500" > $db2"500.db"

RNAfold -p -d2 --noLP --shape=$sh1"500" --shapeMethod=Dm1.0b-0.4 < $oldname"500.fa" | head -3 > $db1"500.db"
RNAfold -p -d2 --noLP --shape=$sh2"500" --shapeMethod=Dm1.0b-0.4 < $oldname"500.fa" | head -3> $db2"500.db"


oldname500=$oldname"500"

echo sed -s "s/$oldname500/$oldname500\_Rep2/" $db1"500.db" | sed -s "s/ConsensusModel/$oldname500\_Rep2/" > $oldname"500_Rep1.db"
sed -s "s/$oldname500/$oldname500\_Rep2/" $db1"500.db" | sed -s "s/ConsensusModel/$oldname500\_Rep2/" > $oldname"500_Rep1.db"
sed -s "s/$oldname500/$oldname500\_Rep1/" $db2"500.db" | sed -s "s/ConsensusModel/$oldname500\_Rep1/" > $oldname"500_Rep2.db"

echo rf-compare -ow -r $oldname"500_Rep1.db" $oldname"500_Rep2.db"
rf-compare -ow -r $oldname"500_Rep1.db" $oldname"500_Rep2.db" -g

#cp rf_compare/*svg $db1"_rf_compare_"$method.svg
cp rf_compare/*svg $oldname"500_rf_compare_"$method.svg
rm $oldname"500_Rep2.db" $oldname"500_Rep1.db" 
rm -r rf_compare





#rm $db1 $db2 $sh1 $sh2
