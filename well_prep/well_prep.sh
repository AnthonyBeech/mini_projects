#!/usr/bin/env bash


#convert .las file to .txt containing time,vp,rho to be used for synthetic derivation
#need list of well names to loop through


#clean files
echo "remove old well txts"
rm ~/linux_training/well_txts/d_vp_rho*

echo "create new directories"
mkdir ~/linux_training/well_txts

#for each well file location in list
#convert data into time,vp,rho txt file

wlist=~/linux_training/well_file_locs.txt
welltot=`cat $wlist | wc -l`
miswell=0

cat $wlist | while read line; do

    name=`echo $line | rev | cut -d'/' -f1 | rev | cut -d'.' -f1`
    loc=~/linux_training/well_txts/d_vp_rho_${name}.txt

    cat $line | grep -A 99999999 'ASCII Log Data Section' | tr -s ' ' ',' | cut -d',' -s -f2-4 > $loc
    sed -i -e 's/Log,Data,Section//g' $loc
    sed -i '1d' $loc 


    num=`head -n1 $loc | grep -o "," | wc -l`
    if [ $num -ne 2 ]
    then
        rm $loc
        echo "missing vp or rho, deleting txt"
        (($miswell++))
    fi

    echo $name
done


echo "$miswell of $welltot wells missing vp or rho"

echo "complete" 
