#!/bin/bash

r1t=$1
r2t=$2
r1u=$3
r2u=$4
fasta=$5
mask=$6
name=$7
cut=$8

mkdir $name"_RF"
cd $name"_RF"

#running RNAFramework

bowtie2-build ../$fasta "reference_"$name

rf-map -p 10 -b2 -cl 15 -b5 5 -ow -bi "reference_"$name ../$r1t ../$r2t ../$r1u ../$r2u

rf-count -p 10 -r -ow -f ../$fasta -m rf_map/*.bam -mf ../$mask

rf-rctools merge rf_count/*NT*_L001_R1_001.rc rf_count/*NT*_L001_R2_001.rc -o "untreated_"$name

rf-rctools merge rf_count/*2A3*_L001_R1_001.rc rf_count/*2A3*_L001_R2_001.rc -o "treated_"$name

rf-norm -sm 3 -nm 3 -ow -o rf_norm -i rf_count/index.rci -t treated_$name.rc -u "untreated_"$name.rc

rf-fold -ow -g -nlp -sh -sl 1.0 -in -0.4 rf_norm/*.xml

#rnaming outputs

mv rf_norm/*xml rf_norm/$name"_RF".xml

mv rf_fold/images/*svg rf_fold/images/$name"_RF".svg

mv rf_fold/shannon/*wig rf_fold/shannon/$name"_RF".wig

mv rf_fold/structures/*db rf_fold/structures/$name"_RF".db


# drawing structures

draw_varna.py -i ../$fasta -r ./rf_norm/*xml -sl 1.0 -in -0.4 -o $name"_RF"

draw_varna.py -i ../$fasta -r ./rf_norm/*xml -sl 1.0 -in -0.4 -o $name"_RF" -c $cut


mkdir $name"_RF_results"

cp *.db ../.
cp *.shape ../.

mv *.png  $name"_RF_results"/.
mv *.db  $name"_RF_results"/.
mv *.shape  $name"_RF_results"/.

cp rf_fold/images/*svg $name"_RF_results"/.

rm *.log

cd ../



#runnin ShapeMapper
mkdir $name"_SM"
cd $name"_SM"

mkdir $name"_SM_results"


shapemapper --overwrite --name $name"_SM" --target ../$fasta --out $name"_SM" --amplicon --modified --R1 ../$r1t --R2 ../$r2t --untreated --R1 ../$r1u --R2 ../$r2u

cd $name"_SM"
Superfold.py *map --SHAPEslope 1.0 --SHAPEintercept -0.4

ct2dot results*/*.ct 1 $name"_SM".db
draw_varna.py -i $name"_SM".db -r $name"_SM"*.shape -sl 1.0 -in -0.4 -o $name"_SM"
cp $name"_SM"*"RNAfold"*.shape ../../.
mv $name"_SM"*"RNAfold"*.shape ../$name"_SM_results"/.
draw_varna.py -i $name"_SM".db -r $name"_SM"*.shape -sl 1.0 -in -0.4 -o $name"_SM" -c $cut
cp $name"_SM"*"RNAfold"*.shape ../../.
mv $name"_SM"*"RNAfold"*.shape ../$name"_SM_results"/.

rm *.log

cp *.db ../../.

cp results*/*.pdf ../$name"_SM_results"/.
mv *.db ../$name"_SM_results"/.
mv *.png ../$name"_SM_results"/.

cd ../


cp ./$name"_SM"/*pdf $name"_SM_results"/.



