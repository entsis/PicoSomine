import soundfile as sf
import matplotlib.pyplot as plt
import samplerate

soundfile = 'somine.wav'
data_in, datasamplerate = sf.read(soundfile)

# This means stereo so extract one channel 0
if len(data_in.shape) > 1:
    data_in = data_in[:, 0]

converter = 'sinc_best'  # or 'sinc_fastest', ...
desired_sample_rate = 11000.0
ratio = desired_sample_rate / datasamplerate
data_out = samplerate.resample(data_in, ratio, converter)

maxValue = max(data_out)
minValue = min(data_out)
vrange = (maxValue - minValue)

m68code = "/*    File " + soundfile + "\r\n *    Sample rate " + str(int(desired_sample_rate)) + " Hz\r\n */\r\n"
m68code += "#define WAV_DATA_LENGTH " + str(len(data_out)) + " \r\n\r\n"
m68code += "uint8_t WAV_DATA[] = {\r\n    "
maxitemsperline = 16
itemsonline = maxitemsperline
firstvalue = 0
lastvalue = 0
for v in data_out:
    # scale v to between 0 and 1
    isin = (v - minValue) / vrange
    v = int((isin * 255))
    vstr = str(v)
    if firstvalue == 0:
        firstvalue = v
    lastvalue = v
    m68code += vstr
    itemsonline -= 1
    if itemsonline > 0:
        m68code += ','
    else:
        itemsonline = maxitemsperline
        m68code += ',\r\n    '

# keep track of first and last values to avoid
# blip when the loop restarts.. make the end value
# the average of the first and last.
end_value = int((firstvalue + lastvalue) / 2)
m68code += str(end_value) + '    \r\n};'

# Save the generated code to somine.h file
with open('somine.h', 'w') as file:
    file.write(m68code)
