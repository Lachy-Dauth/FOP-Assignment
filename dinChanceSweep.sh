#!/bin/bash

exp_dir=dinChance_`date "+%Y-%m-%d_%H:%M:%S"`

mkdir $exp_dir
cp players.py $exp_dir
cp dinChanceSweep.sh $exp_dir
cp board.csv $exp_dir
cp game2.py $exp_dir
cp dataPro.py $exp_dir
cd $exp_dir

low=$1
hi=$2
step=$3
trials=$4

echo "Parameters are: " $low $hi $step $trials
START=$(date +%s)
for i in `seq $low $step $hi`;
do
  for t in `seq 1 8 $trials`;
    do
    echo "Experiment: " $i $t
    python3 game2.py $i & python3 game2.py $i & python3 game2.py $i & python3 game2.py $i & python3 game2.py $i & python3 game2.py $i & python3 game2.py $i & python3 game2.py $i
  done
done
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"
python3 dataPro.py
