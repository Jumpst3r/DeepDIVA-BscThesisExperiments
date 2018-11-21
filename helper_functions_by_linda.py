from PIL import Image
import numpy as np

from sklearn.preprocessing import OneHotEncoder


def int_to_one_hot(x, n_classes):
    """
    Read out class encoding from blue channel bit-encoding (1 to [0,0,0,1] -> length determined by the number of classes)
    :param x: integer (pixel value of Blue channel from RGB image)
    :param n_classes: number of class labels
    :return: (multi) one-hot encoded list for integer
    """
    s = '{0:0' + str(n_classes) + 'b}'
    return list(map(int, list(s.format(x))))


def multi_label_img_to_one_hot(np_array):
    """
    TODO: There must be a faster way of doing this
    Convert ground truth label image to multi-one-hot encoded matrix of size image height x image width x #classes
    :param np_array: numpy array of an RGB image
    :return: sparse one-hot encoded multi-class matrix
    """
    im_np = np_array[:, :, 2].astype(np.int8)
    nb_classes = len(int_to_one_hot(im_np.max(), ''))

    class_dict = {x: int_to_one_hot(x, nb_classes) for x in np.unique(im_np)}
    # create the one hot matrix
    one_hot_matrix = np.asanyarray(
        [[class_dict[im_np[i, j]] for j in range(im_np.shape[1])] for i in range(im_np.shape[0])])

    return np.rollaxis(one_hot_matrix.astype(np.uint8), 2, 0)


def multi_one_hot_to_output(matrix):
    """
    This function converts the multi-one-hot encoded matrix to an image like it was provided in the ground truth
    :param matrix: multi-one-hot encoded matrix
    :param RGB: RGB numpy array
    """
    # create RGB
    matrix = np.rollaxis(np.char.mod('%d', matrix), 0, 3)
    zeros = (32 - matrix.shape[2]) * '0'
    B = np.array([[int('{}{}'.format(zeros, ''.join(matrix[i][j])), 2) for j in range(matrix.shape[1])] for i in
                  range(matrix.shape[0])])

    RGB = np.dstack((np.zeros(shape=(matrix.shape[0], matrix.shape[1], 2), dtype=np.int8), B))

    return RGB


def label_img_to_one_hot(np_array):
    """
    Convert ground truth label image to one-hot encoded matrix of size image height x image width x #classes
    :param np_array: numpy array of an RGB image
    :return: sparse one-hot encoded class matrix
    """
    im_np = np_array[:, :, 2].astype(np.int8)
    
    integer_encoded = np.array([i for i in range(8)])
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded).astype(np.int8)

    replace_dict = {k:v for k,v in zip([1,2,4,6,8,10,12,14], onehot_encoded)}        
    # create the one hot matrix
    one_hot_matrix = np.asanyarray(
        [[replace_dict[im_np[i, j]] for j in range(im_np.shape[1])] for i in range(im_np.shape[0])])
        
    return np.rollaxis(one_hot_matrix.astype(np.uint8), 2, 0)


def one_hot_to_output(matrix):
    """
    This function converts the one-hot encoded matrix to an image like it was provided in the ground truth
    :param matrix: one-hot encoded matrix
    :param RGB: RGB numpy array
    """
    matrix = np.rollaxis(np.char.mod('%d', matrix), 0, 3)
    
    integer_encoded = np.array([i for i in range(8)])
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded).astype(np.int8)
    
    replace_dict = {k:v for k,v in zip([''.join(i) for i in onehot_encoded.astype(str)], [1,2,4,6,8,10,12,14])}    

    B = np.array([[replace_dict[''.join(matrix[i][j])] for j in range(matrix.shape[1])] for i in range(matrix.shape[0])])
    
    RGB = np.dstack((np.zeros(shape=(matrix.shape[0], matrix.shape[1], 2), dtype=np.int8), B))

    return RGB












