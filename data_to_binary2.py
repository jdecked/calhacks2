import pyaudio, wave, sys, struct, math
import numpy as np
from aubio import bintofreq

def envelope(in_data, left=True, right=True, rate=48000):
    half = float(len(in_data)) / 2
    freq = math.pi / (len(in_data) / 2)
    out_data = []

    for x in range(len(in_data)):
        samp = in_data[x]
        if (x < half and left) or (right and x >= half):
            samp = samp * (1 + math.sin(freq*x - (math.pi / 2))) / 2
        out_data.append(int(samp))

    return out_data

def ttone(freq, datasize=4096, rate=48000, amp=12000.0, offset=0):
    sine_list = []

    for x in range(datasize):
        samp = math.sin(2*math.pi*freq*(x/float(rate)))
        sine_list.append(int(samp*amp))
    return sine_list

def pack_buffer(buffer):
    return [struct.pack('h', frame) for frame in buffer]

def make_buffer_from_bit_pattern(pattern, DATASIZE, freqs, off_freq):
    """ Takes a pattern and returns an audio buffer that encodes that pattern """
    # the key's middle value is the bit's value and the left and right bits are the bits before and after
    # the buffers are enveloped to cleanly blend into each other

    last_bit = pattern[-1]
    output_buffer = []
    offset = 0
    counter = 1

    for i in range(len(pattern)):
        bit = pattern[i]
        if i < len(pattern) - 1:
            next_bit = pattern[i+1]
        else:
            next_bit = pattern[0]

        freq = freqs[counter] if bit == '1' else off_freq
        tone = ttone(freq, DATASIZE, offset=offset)
        # output_buffer += envelope(tone, left=last_bit=='0', right=next_bit=='0')
        output_buffer.append(tone)
        # offset += DATASIZE
        last_bit = bit

        if counter == 8:
            counter = 1
        else:
            counter += 1

    output_buffer = [struct.pack('f'*len(frame), *frame) for frame in output_buffer]
    # print output_buffer

    # return struct.pack('s'*len(output_buffer), *output_buffer)
    return output_buffer

# FREQUENCIES = {
#     1: 4000,
#     2: 4150,
#     3: 4300,
#     4: 4450,
#     5: 4600,
#     6: 4750,
#     7: 4900,
#     8: 4000
# }
FREQUENCIES = {
    1: 21000,
    2: 21150,
    3: 21300,
    4: 21450,
    5: 21600,
    6: 21750,
    7: 21900,
    8: 22000
}
BITRATE = 48000
FRAMES_PER_BUFFER = 10
f = open('test.txt', 'rb')

# fname = raw_input("Input the name of your data file: ")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt8,
                channels=1,
                rate=BITRATE,
                output=True,
                frames_per_buffer=FRAMES_PER_BUFFER)

data = f.read()
byte_data = ''.join(format(x, 'b') for x in bytearray(data))
# byte_data = byte_data.split(' ')
byte_data = list(byte_data)
# byte_data = [int(i) for i in byte_data]
# WAVEDATA = ''
# FREQS = []

buffer = make_buffer_from_bit_pattern(byte_data, len(byte_data), FREQUENCIES, 0)
# print str(buffer)

# for x in xrange(len(byte_data)):
    # for bit in byte_data:
    #     # if bit == 1:
    #     FREQUENCY = FREQUENCIES[counter] if bit == 1 else 0
    #
    #     sample = tone(FREQUENCY, datasize=len(byte_data), rate=BITRATE)
    #     output_buffer += envelope(tone, left=last_bit=='0', right=next_bit=='0')
    #
    #     FREQS.append(FREQUENCY)
    #     # WAVEDATA += chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))
    #     # elif bit == 0:
    #     #     WAVEDATA += chr(128)
    #     #     FREQS.append(0)
    #
    #     if counter == 8:
    #         counter = 1
    #     else:
    #         counter += 1

# for i in range(len(byte_data)):
#     byte_data[i] = byte_data[i].rjust(8, '0')

# byte_data = ' '.join(byte_data)

# output = [ bintofreq(x, 48000, 96) for x in byte_data ]
# output = output[:-1]
# print output
# print byte_data
# output = struct.pack('f'*len(output), *output)
# output = np.array
# output = aubio.bintofreq([float(i) for i in byte_data])

# print byte_data
# print output

# print WAVEDATA
# print byte_data
# print FREQS

# for i in range(10):
stream.write(str(buffer))
