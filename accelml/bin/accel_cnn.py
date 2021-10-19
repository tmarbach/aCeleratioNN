import numpy as np


def conv_single_pos(a_slice_prev, W, b):
     """
    Args:
    a_slice_prev -- a slice of the input data, shape = (f, f, n_C_prev)
    W -- Weight parameters of the filter, shape = (f, f, n_C_prev)
    b -- Bias paramter of the filter, shape = (1, 1, 1)
    
    Returns:
    Z -- A scalar value, result of convlution.
    """
    s = np.multiply(a_slice_prev,W)
    Z = np.sum(s)
    Z = float(b)+Z
    return Z