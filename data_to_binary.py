import pyaudio, wave, sys, struct
import numpy as np
from aubio import bintofreq

# from pylab import *

# fname = raw_input("Input the name of your data file: ")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt8,
                channels=2,
                rate=48000,
                output=True,
                frames_per_buffer=20000)
# wf = wave.open(fname, 'rb')
# detect = new_aubio_pitchdetection(2000,1000,2,
#                                   48000,aubio_pitch_yin,aubio_pitchm_freq)
# buf = new_fvec(2000,2)
#
# for i in range(len(floats)):
#     fvec_write_sample(buf, floats[i], 0, i)

with open('test.txt', 'rb') as f:
    data = f.read()
    byte_data = ' '.join(format(x, 'b') for x in bytearray(data))
    byte_data = byte_data.split(' ')
    byte_data = [int(i, 2) for i in byte_data]

    # for i in range(len(byte_data)):
    #     byte_data[i] = byte_data[i].rjust(8, '0')

    # byte_data = ' '.join(byte_data)

    output = [ bintofreq(x, 48000, 96) for x in byte_data ]
    output = output[:-1]
    print output
    print byte_data
    output = struct.pack('f'*len(output), *output)
    # output = np.array
    # output = aubio.bintofreq([float(i) for i in byte_data])

# print byte_data
# print output

for i in range(5000):
    stream.write(np.array([5000, 10000, 12000]))
