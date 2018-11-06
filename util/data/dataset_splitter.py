"""
This script allows for creation of a validation set from the training set.
"""

# Utils
import argparse
import os
import shutil
import sys
import re
import numpy as np

# Torch related stuff
import torchvision.datasets as datasets
from sklearn.model_selection import train_test_split


def split_dataset(dataset_folder, split, symbolic):
    """
    Partition a dataset into train/val splits on the filesystem.

    Parameters
    ----------
    dataset_folder : str
        Path to the dataset folder (see datasets.image_folder_dataset.load_dataset for details).
    split : float
        Specifies how much of the training set should be converted into the validation set.
    symbolic : bool
        Does not make a copy of the data, but only symbolic links to the original data

    Returns
    -------
        None
    """

    # Getting the train dir
    traindir = os.path.join(dataset_folder, 'train')

    # Rename the original train dir
    shutil.move(traindir, os.path.join(dataset_folder, 'original_train'))
    traindir = os.path.join(dataset_folder, 'original_train')

    # Sanity check on the training folder
    if not os.path.isdir(traindir):
        print("Train folder not found in the args.dataset_folder={}".format(dataset_folder))
        sys.exit(-1)

    # Load the dataset file names

    train_ds = datasets.ImageFolder(traindir)

    # Extract the actual file names and labels as entries
    fileNames = np.asarray([item[0] for item in train_ds.imgs])
    labels = np.asarray([item[1] for item in train_ds.imgs])

    # Split the data into two sets
    X_train, X_val, y_train, y_val = train_test_split(fileNames, labels,
                                                      test_size=split,
                                                      random_state=42,
                                                      stratify=labels)

    # Print number of elements for each class
    for c in train_ds.classes:
        print("labels ({}) {}".format(c, np.size(np.where(y_train == train_ds.class_to_idx[c]))))
    for c in train_ds.classes:
        print("split_train ({}) {}".format(c, np.size(np.where(y_train == train_ds.class_to_idx[c]))))
    for c in train_ds.classes:
        print("split_val ({}) {}".format(c, np.size(np.where(y_val == train_ds.class_to_idx[c]))))

    # Create the folder structure to accommodate the two new splits
    split_train_dir = os.path.join(dataset_folder, "train")
    if os.path.exists(split_train_dir):
        shutil.rmtree(split_train_dir)
    os.makedirs(split_train_dir)

    for class_label in train_ds.classes:
        path = os.path.join(split_train_dir, class_label)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    split_val_dir = os.path.join(dataset_folder, "val")
    if os.path.exists(split_val_dir):
        shutil.rmtree(split_val_dir)
    os.makedirs(split_val_dir)

    for class_label in train_ds.classes:
        path = os.path.join(split_val_dir, class_label)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    # Copying the splits into their folders
    for X, y in zip(X_train, y_train):
        src = X
        file_name = os.path.basename(src)
        dest = os.path.join(split_train_dir, train_ds.classes[y], file_name)
        if symbolic:
            os.symlink(src, dest)
        else:
            shutil.copy(X, dest)

    for X, y in zip(X_val, y_val):
        src = X
        file_name = os.path.basename(src)
        dest = os.path.join(split_val_dir, train_ds.classes[y], file_name)
        if symbolic:
            os.symlink(src, dest)
        else:
            shutil.copy(X, dest)

    return


def split_dataset_segmentation(dataset_folder, split, symbolic):
    """
    Partitions a segmentation dataset into train/val splits on the filesystem.

    The data set has to have two sub-folders in train 'gt' (pixel-wise labelled ground truth and 'imgs'
    (RGB images to be segmented). The file name for corresponding images has to be the same in the imgs and gt folder.
    The data set structure has to be in the following format
    train/gt/datas-subset1/image1.JPG, train/imgs/data-subset2/image1.JPG etc.

    The split will be performed according to the split argument within each data-subset.

    Parameters
    ----------
    dataset_folder : str
        Path to the dataset folder (see datasets.image_folder_segmentation.load_dataset for details).
    split : float
        Specifies how much of the training set should be converted into the validation set.
    symbolic : bool
        Does not make a copy of the data, but only symbolic links to the original data

    Returns
    -------
        None
    """

    # Getting the train dir
    traindir = os.path.join(dataset_folder, 'train')

    # Rename the original train dir
    shutil.move(traindir, os.path.join(dataset_folder, 'original_train'))
    traindir = os.path.join(dataset_folder, 'original_train')

    # Sanity check on the training folder
    if not os.path.isdir(traindir):
        print("Train folder not found in the args.dataset_folder={}".format(dataset_folder))
        sys.exit(-1)
    if not os.path.isdir(os.path.join(traindir, 'imgs')):
        print("gt folder not found in the args.dataset_folder={} train folder".format(dataset_folder))
        sys.exit(-1)
    if not os.path.isdir(os.path.join(traindir, 'gt')):
        print("imgs folder not found in the args.dataset_folder={} train folder".format(dataset_folder))
        sys.exit(-1)

    # Load the dataset file names
    train_ds = datasets.ImageFolder(traindir)

    # Extract the actual file names and labels as entries
    file_names_all = np.asarray([item[0] for item in train_ds.imgs])
    fileNames = [f for f in file_names_all if 'imgs' in f]
    labels = np.asanyarray([os.path.basename(os.path.dirname(file_name)) for file_name in
                            fileNames])  # use folder names as lables -> name of data-subset

    # Split the data into two sets
    X_train, X_val, y_train_subset, y_val_subset = train_test_split(fileNames, labels,
                                                                    test_size=split,
                                                                    random_state=42,
                                                                    stratify=labels)
    # Create y_train and y_test from X_train and X_test file names that maps the path to the img to the path of the gt
    # (substitute 'imgs' for 'gt' and '.jpg' for '.png' in folder path)
    y_train = {p: re.sub('.jpg', '.png', re.sub(r'/imgs/', '/gt/', p)) for p in X_train}
    y_val = {p: re.sub('.jpg', '.png', re.sub(r'/imgs/', '/gt/', p)) for p in X_val}

    # Print number of elements for each sub-set
    for subset in list(set(labels)):
        print("data sub-sets ({}) {}".format(subset, np.size(np.where(labels == subset))))
    for subset in list(set(labels)):
        print("split_train ({}) {}".format(subset, np.size(np.where(y_train_subset == subset))))
    for subset in list(set(labels)):
        print("split_val ({}) {}".format(subset, np.size(np.where(y_val_subset == subset))))

    # Create the folder structure to accommodate the two new splits
    split_train_dir = os.path.join(dataset_folder, "train")
    if os.path.exists(split_train_dir):
        shutil.rmtree(split_train_dir)
    os.makedirs(split_train_dir)

    for subfolder in ["imgs", "gt"]:
        split_train_dir_sub = os.path.join(split_train_dir, subfolder)
        if os.path.exists(split_train_dir_sub):
            shutil.rmtree(split_train_dir_sub)
        os.makedirs(split_train_dir_sub)

        for subset in list(set(labels)):
            path = os.path.join(split_train_dir_sub, subset)
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

    split_val_dir = os.path.join(dataset_folder, "val")
    if os.path.exists(split_val_dir):
        shutil.rmtree(split_val_dir)
    os.makedirs(split_val_dir)

    for subfolder in ["imgs", "gt"]:
        split_val_dir_sub = os.path.join(split_val_dir, subfolder)
        if os.path.exists(split_val_dir_sub):
            shutil.rmtree(split_val_dir_sub)
        os.makedirs(split_val_dir_sub)

        for subset in list(set(labels)):
            path = os.path.join(split_val_dir_sub, subset)
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

    # Copying the splits into their folders
    for X, y in y_train.items():
        file_name_X = _get_file_with_parents(X, 2)
        file_name_y = _get_file_with_parents(y, 2)
        dest_X = os.path.join(split_train_dir, file_name_X)
        dest_y = os.path.join(split_train_dir, file_name_y)

        if symbolic:
            os.symlink(X, dest_X)
            os.symlink(y, dest_y)
        else:
            shutil.copy(X, dest_X)
            shutil.copy(y, dest_y)

    for X, y in y_val.items():
        file_name_X = _get_file_with_parents(X, 2)
        file_name_y = _get_file_with_parents(y, 2)
        dest_X = os.path.join(split_val_dir, file_name_X)
        dest_y = os.path.join(split_val_dir, file_name_y)

        if symbolic:
            os.symlink(X, dest_X)
            os.symlink(y, dest_y)
        else:
            shutil.copy(X, dest_X)
            shutil.copy(y, dest_y)

    return


def _get_file_with_parents(filepath, levels=1):
    common = filepath
    for i in range(levels + 1):
        common = os.path.dirname(common)
    return os.path.relpath(filepath, common)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='This script creates train/val splits '
                                                 'from a specified dataset folder.')

    parser.add_argument('--dataset-folder',
                        help='path to root of the dataset.',
                        required=True,
                        type=str,
                        default=None)

    parser.add_argument('--split',
                        help='Ratio of the split for validation set.'
                             'Example: if 0.2 the training set will be 80% and val 20%.',
                        type=float,
                        default=0.2)

    parser.add_argument('--symbolic',
                        help='Make symbolic links instead of copies.',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    split_dataset(dataset_folder=args.dataset_folder, split=args.split, symbolic=args.symbolic)
