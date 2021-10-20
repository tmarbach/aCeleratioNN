import numpy as np

# Still debating on the addition of zero padding. The 'image' data is so small that 
#   I am not sure if it is worth it. 


def zero_pad(X, pad):
    """
    Args:
    X -- a numpy array of shape (m, n_H, n_W, n_C) representing a batch of images
    pad -- an integer indicating the size of padding
    
    Returns:
    X_pad -- a padded array of shape (m, n_H + 2*pad, n_W + 2*pad, n_C)
    """
    X_pad = np.pad(X, ((0,0), (pad,pad), (pad,pad), (0,0)), 'constant')
    
    return X_pad


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


def conv_forward(A_prev, W, b, hparams):
    """
    Args:
    A_prev -- Activations from the previous layer, a numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
    W -- Weight parameters, a numpy array of shape (f, f, n_C_prev, n_C)
    b -- Bias parameters, a numpy array of shape (1, 1, 1, n_C)
    hparams -- A Python dict object containing 'stride' and 'pad'
    
    Returns:
    Z -- Output of convolution, a numpy array of shape (m, n_H, n_W, n_C)
    cache -- cache of variables needed for backward propagation
    """
    (m, n_H_prev, n_W_prev, n_C_prev) = np.shape(A_prev)
    (f, f, n_C_prev, n_C) = np.shape(W)
    stride = hparams['stride']
    pad = hparams['pad']
    n_H = int((n_H_prev-f+(2*pad))/stride)+1
    n_W = int((n_W_prev-f+(2*pad))/stride)+1
    Z = np.zeros((m,n_H,n_W,n_C))
    A_prev_pad = zero_pad(A_prev,pad)
    for i in range(m): 
        a_prev_pad = A_prev_pad[i]
        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_C):
                    vert_start = stride * h
                    vert_end = (stride * h) + f
                    horiz_start = stride * w
                    horiz_end = (stride * w) + f
                    a_prev_slice = a_prev_pad[vert_start:vert_end,horiz_start:horiz_end]
                    Z[i, h, w, c] = conv_single_pos(a_prev_slice, W[:,:,:,c], b[:,:,:,c])
    assert(Z.shape == (m, n_H, n_W, n_C))
    cache = (A_prev, W, b, hparams)
    
    return Z, cache


def pool_forward(A_prev, hparams, mode='max'):
    """
    Args:
    A_prev -- Activations from the previous layer, a numpy array of shape (m, n_H_prev, n_W_prev, n_C_prev)
    hparams -- A Python dict object containing 'stride' and 'pad'
    mode -- Pooling type, a string ('max' or 'average')
    
    Returns:
    A -- Output, a numpy array of shape (m, n_H, n_W, n_C)
    cache -- Cached variables that will be used for backward propagation 
    """
    (m, n_H_prev, n_W_prev, n_C_prev) = np.shape(A_prev)
    f = hparams['f']
    stride = hparams['stride']
    n_H = int((n_H_prev-f)/stride)+1
    n_W = int((n_W_prev-f)/stride)+1
    n_C = n_C_prev
    A = np.zeros((m, n_H, n_W, n_C))
    for i in range(m):
        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_C):
                    vert_start = stride * h
                    vert_end = (stride * h) + f
                    horiz_start = stride * w
                    horiz_end = (stride * w) + f
                    a_prev_slice = A_prev[i,vert_start:vert_end,horiz_start:horiz_end,c]
                    if mode == "max":
                        A[i, h, w, c] = np.max(a_prev_slice)
                    elif mode == "average":
                        A[i, h, w, c] = np.mean(a_prev_slice)    
    assert(A.shape == (m, n_H, n_W, n_C))
    cache = (A_prev, hparams)
    
    return A, cache
