#!/bin/bash -l
#$ -S /bin/bash
#$ -N $2
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "./sven.sh <database>"
    exit 1
fi

DATABASE=$1

echo 'Sven'
echo 'Database: ' $DATABASE
echo '#############'

# Discriminate places' categories in big groups
python src/stats.py $DATABASE

# Plot Trec Stats
# python src/trec_stats.py 'Colaborative Filtering' '/Volumes/Tyr/Projects/UFMG/Bjorn/results' 8