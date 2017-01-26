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
# python src/stats.py $DATABASE

# Plot Trec Stats
# python src/trec_stats.py 'Colaborative Filtering' '/Volumes/Tyr/Projects/UFMG/Bjorn/results' 8

DATASET_PATH="/Volumes/Tyr/Projects/UFMG/Datasets/Ours/nyc"
ALGORITHMS_PATH="/Volumes/Tyr/Projects/UFMG/06Evaluation/Baselines"

ALGORITHM="ItemKNN"
RANK_NAME="ranked-items.rank.rank"

FOLD_1_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_1/ranks/"$RANK_NAME
FOLD_2_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_2/ranks/"$RANK_NAME
FOLD_3_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_3/ranks/"$RANK_NAME
FOLD_4_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_4/ranks/"$RANK_NAME
FOLD_5_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_5/ranks/"$RANK_NAME
FOLD_6_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_6/ranks/"$RANK_NAME
FOLD_7_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_7/ranks/"$RANK_NAME
FOLD_8_RANK=$ALGORITHMS_PATH"/"$ALGORITHM"/test/fold_8/ranks/"$RANK_NAME

OUTPUT_PATH="nyc/trec/"$ALGORITHM"/"

python src/trec_test.py -o $OUTPUT_PATH'fold1.result' $DATASET_PATH'/fold_1/g_test.trec' $FOLD_1_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold2.result' $DATASET_PATH'/fold_2/g_test.trec' $FOLD_2_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold3.result' $DATASET_PATH'/fold_3/g_test.trec' $FOLD_3_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold4.result' $DATASET_PATH'/fold_4/g_test.trec' $FOLD_4_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold5.result' $DATASET_PATH'/fold_5/g_test.trec' $FOLD_5_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold6.result' $DATASET_PATH'/fold_6/g_test.trec' $FOLD_6_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold7.result' $DATASET_PATH'/fold_7/g_test.trec' $FOLD_7_RANK
python src/trec_test.py -o $OUTPUT_PATH'fold8.result' $DATASET_PATH'/fold_8/g_test.trec' $FOLD_8_RANK