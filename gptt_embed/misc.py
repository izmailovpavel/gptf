import tensorflow as tf
import numpy as np

import t3f
import t3f.kronecker as kron
from t3f import ops, TensorTrain, TensorTrainBatch

def r2(y_pred, y_true, name=None):
    """r2 score.
    """
    with tf.name_scope(name, 'r2_score', [y_pred, y_true]):
        mse_score = mse(y_pred, y_true)
        return 1. - mse_score / mse(tf.ones_like(y_true) * 
                    tf.reduce_mean(y_true), y_true)


def mse(y_pred, y_true, name=None):
    """MSE score.
    """
    with tf.name_scope(name, 'mse', [y_pred, y_true]):
        mse = tf.reduce_mean(tf.squared_difference(tf.reshape(y_pred, [-1]), 
                             tf.reshape(y_true, [-1])), name='MSE')
        return mse

        
def _kron_tril(kron_mat, name=None):
    '''Computes the lower triangular part of a kronecker-factorized matrix.

    Note, that it computes it as a product of the lower triangular parts
    of the elements of the product, which is not exactly the lower 
    triangular part.
    '''
    with tf.name_scope(name, 'Kron_tril', [kron_mat]):
        mat_l_cores = []
        for core_idx in range(kron_mat.ndims()):
            core = kron_mat.tt_cores[core_idx][0, :, :, 0]
            mat_l_cores.append(tf.matrix_band_part(core,-1, 0)
                                                [None, :, :, None])
        mat_l_shape = kron_mat.get_raw_shape()
        mat_l_ranks = kron_mat.get_tt_ranks()
        mat_l = TensorTrain(mat_l_cores, mat_l_shape, mat_l_ranks)
        return mat_l


def _kron_logdet(kron_mat, name=None):
    '''Computes the logdet of a kronecker-factorized matrix.
    '''
    with tf.name_scope(name, 'Kron_logdet', [kron_mat]):
        i_shapes = kron_mat.get_raw_shape()[0]
        pows = tf.cast(tf.reduce_prod(i_shapes), kron_mat.dtype)
        logdet = 0.
        for core_idx in range(kron_mat.ndims()):
            core = kron_mat.tt_cores[core_idx][0, :, :, 0]
            core_pow = pows / i_shapes[core_idx].value
            logdet += (core_pow * 
                tf.reduce_sum(tf.log(tf.abs(tf.diag_part(core)))))
        logdet *= 2
        return logdet