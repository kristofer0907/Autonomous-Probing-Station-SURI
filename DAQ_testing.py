import numpy as np
import nidaqmx
import time
import matplotlib.pyplot as plt
import math

def create_interval(start, end, step):
    interval_list = []
    num = start
    while num <= end:
        interval_list.append(num)
        num += step
    return interval_list



print(create_interval(1,5,2))