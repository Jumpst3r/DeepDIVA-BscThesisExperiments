#inception_v3
python template/RunMe.py --runner-class apply_model --dataset-folder /home/thomas.kolonko/datasets/ICDAR2017-CLAMM/StyleClassification \
    --load-model /home/thomas.kolonko/output_tz_classification_inception/tz_classification_inception/StyleClassification/model_name=inception_v3/epochs=50/lr=0.08231704676422484/decay_lr=20/momentum=0.6746830021238069/weight_decay=0.00689595353396544/29-12-18-23h-37m-16s/checkpoint.pth.tar \
    --output-channels 12 --ignoregit

#python util/visualization/embedding.py --results-file ./output/classify/Manuscriptdating/classify\=True/EXCUTION-DATE/results.pkl \
#    --output-file ../../results-classification-pc30/classification/ManuscriptDating/vgg11_bn_md.png --tensorboard

