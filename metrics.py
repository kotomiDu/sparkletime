import numpy as np
def softmax(logits):
    """ Returns softmax given logits. """

    max_logits = np.max(logits, axis=-1, keepdims=True)
    numerator = np.exp(logits - max_logits)
    denominator = np.sum(numerator, axis=-1, keepdims=True)
    return numerator / denominator