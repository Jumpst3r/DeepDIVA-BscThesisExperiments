#!/bin/bash

#Experiments for HisDB-55

# Unet ---------------------------------------
python ./template/RunMe.py --runner-class semantic_segmentation_hisdb --dataset-folder ../datasets/HisDB/CB55/ --model-name Unet --epochs 60 --experiment-name segmentation --output-folder ../output/ --decay-lr 28 --ignoregit \
 --batch-size 32 -j 8 --crop-size 256 --pages-in-memory 3 --crops-per-page 1000 --momentum 0.11280 --weight-decay 0.00594 --lr 0.16824 \
 --disable-databalancing --use-boundary-pixel --no-val-conf-matrix

# fcdensenet67 ---------------------------------------
python ./template/RunMe.py --runner-class semantic_segmentation_hisdb --dataset-folder ../datasets/HisDB/CB55/ --model-name fcdensenet57 --epochs 60 --experiment-name segmentation --output-folder ../output/ --decay-lr 28 \
 --batch-size 32 -j 8 --crop-size 256 --pages-in-memory 3 --crops-per-page 1000 --momentum 0.32149 --weight-decay 0.00549 --lr 0.09272 \
 --disable-databalancing --use-boundary-pixel --no-val-conf-matrix