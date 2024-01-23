import numpy as np


def calculate_percentage(positives_in_segment, width, positive=True):
    """ a function to calculate the percentage of negative/positive values in a segment """

    segment_len = len(positives_in_segment)
    if segment_len < width*720*0.9:  # width - in days, 720 points in a day, some threshold
        return np.nan

    count_positive = positives_in_segment.sum()

    if positive:
        return count_positive / segment_len
    else:
        count_negative = segment_len - count_positive
        return count_negative / segment_len
