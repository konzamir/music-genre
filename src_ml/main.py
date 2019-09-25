from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
import pydub

from utils import read_mp3

print(tf.__version__)

class_names = [
    'alternative', 'classical', 'dance',
    'easy', 'jazz', 'metal', 'other',
    'pop', 'rap', 'reggae', 'rnb',
    'rock', 'shanson', 'soundtrack'
]

sr, x = read_mp3('../dataset/pop/165.mp3')
print(sr)
print(x)

waveform = tf.contr