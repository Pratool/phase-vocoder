import pyaudio
import scipy.fftpack
import numpy
import pianoputer
from scipy.io import wavfile

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
r = pyaudio.PyAudio()

stuff = []

stream_input = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
            
stream_output = r.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)


def record_audio():
    data = stream_input.read(CHUNK)
    
    result = numpy.fromstring(data, numpy.float32)
#    result = numpy.reshape(result, (CHUNK, 1))
    
    return result
        
def analyze_audio(data):
    new_data = pianoputer.pitchshift(data, 10, CHUNK/16, CHUNK/64)
#    fps, bowl_sound = wavfile.read("bowl.wav")
#    new_data = pianoputer.pitchshift(bowl_sound, 5)
    
    out_data = new_data.astype(numpy.float32).tostring()
    
    stream_output.write(out_data)

while 1:
    data = record_audio()
    analyze_audio(data)