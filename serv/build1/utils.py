# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf


def load_weights(var_list, weights_file):
    """
    Loads and converts pre-trained weights.
    :param var_list: list of network variables.
    :param weights_file: name of the binary file.
    :return: list of assign ops
    """
    with open(weights_file, "rb") as fp:
        _ = np.fromfile(fp, dtype=np.int32, count=5)

        weights = np.fromfile(fp, dtype=np.float32)

    ptr = 0
    i = 0
    assign_ops = []
    while i < len(var_list) - 1:
        #print "EEERRRRORRR"
        var1 = var_list[i]
        var2 = var_list[i + 1]
        # do something only if we process conv layer
        if 'Conv' in var1.name.split('/')[-2]:
            # check type of next layer
            if 'BatchNorm' in var2.name.split('/')[-2]:
                # load batch norm params
                gamma, beta, mean, var = var_list[i + 1:i + 5]
                batch_norm_vars = [beta, gamma, mean, var]
                for var in batch_norm_vars:
                    shape = var.shape.as_list()
                    num_params = np.prod(shape)
                    var_weights = weights[ptr:ptr + num_params].reshape(shape)
                    ptr += num_params
                    assign_ops.append(
                        tf.assign(var, var_weights, validate_shape=True))

                # we move the pointer by 4, because we loaded 4 variables
                i += 4
            elif 'Conv' in var2.name.split('/')[-2]:
                # load biases
                bias = var2
                bias_shape = bias.shape.as_list()
                bias_params = np.prod(bias_shape)
                bias_weights = weights[ptr:ptr +
                                       bias_params].reshape(bias_shape)
                ptr += bias_params
                assign_ops.append(tf.assign(bias, bias_weights, validate_shape=True))

                # we loaded 1 variable
                i += 1
            # we can load weights of conv layer
            shape = var1.shape.as_list()
            num_params = np.prod(shape)

            var_weights = weights[ptr:ptr + num_params].reshape(
                (shape[3], shape[2], shape[0], shape[1]))
            # remember to transpose to column-major
            var_weights = np.transpose(var_weights, (2, 3, 1, 0))
            ptr += num_params
            assign_ops.append(
                tf.assign(var1, var_weights, validate_shape=True))
            i += 1
    #print assign_ops[:20]
    return assign_ops


def detections_boxes(detections):
    """
    Converts center x, center y, width and height values to coordinates of top left and bottom right points.

    :param detections: outputs of YOLO v3 detector of shape (?, 10647, (num_classes + 5))
    :return: converted detections of same shape as input
    """
    center_x, center_y, width, height, attrs = tf.split(
        detections, [1, 1, 1, 1, -1], axis=-1)
    w2 = width / 2
    h2 = height / 2
    x0 = center_x - w2
    y0 = center_y - h2
    x1 = center_x + w2
    y1 = center_y + h2

    boxes = tf.concat([x0, y0, x1, y1], axis=-1)
    detections = tf.concat([boxes, attrs], axis=-1, name="output_boxes")
    #return detections
    return boxes, attrs

