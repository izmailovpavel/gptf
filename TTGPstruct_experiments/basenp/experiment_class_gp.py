import tensorflow as tf
import os
import numpy as np
from tensorflow.contrib.layers import batch_norm

from TTGP.covariance import SE_multidim
from TTGP.projectors import FeatureTransformer, LinearProjector
from TTGP.gpc_runner import GPCRunner

with tf.Graph().as_default():
    data_dir = "data_class/"
    n_inputs = 10
    mu_ranks = 10
    C = 3
    d = 3
    D = 6438

    projector = LinearProjector(d=d, D=D)
    cov = SE_multidim(C, 0.7, 0.2, 0.1, projector)

    lr = 1e-2
    decay = (10, 0.2)
    n_epoch = 10
    batch_size = 10
    data_type = 'numpy'
    log_dir = 'log'
    save_dir = 'models/gp_4.ckpt'
    model_dir = save_dir
    load_model = False#True
    
    runner=GPCRunner(data_dir, n_inputs, mu_ranks, cov,
                lr=lr, decay=decay, n_epoch=n_epoch, batch_size=batch_size,
                data_type=data_type, log_dir=log_dir, save_dir=save_dir,
                model_dir=model_dir, load_model=load_model)
    runner.run_experiment()
