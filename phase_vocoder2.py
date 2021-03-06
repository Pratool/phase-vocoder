import pyaudio
import numpy, scipy.fftpack, wave
import Tkinter
import pianoputer

'''
To Do:

Add STFT algorithm to see if it all works

'''

CHUNK = 8192*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

class PhaseVocoder:
    def __init__(self):
        self.chunk = 8192*4
        self.p = pyaudio.PyAudio()
        self.r = pyaudio.PyAudio()
        
        self.stream_input = self.p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
                    
        self.stream_output = self.r.open(format=FORMAT, 
                            channels=CHANNELS,
                            rate=RATE,
                            output=True)
                                                                  
        self.tempo = 1.
        self.pitch = 0
        
        # Creates a slider that can change the pitch and tempo
        self.control = Tkinter.Tk()
        self.control.title("Pitch and Tempo")
        self.s_pitch = Tkinter.Scale(label='Pitch', orient='horizontal', length=400, from_=-12, to=12, command=self.update_pitch)
        self.s_tempo = Tkinter.Scale(label='Tempo', orient='horizontal', length=400, from_=1, to=200, command=self.update_tempo)
        self.s_pitch.set(0)
        self.s_tempo.set(100)
        self.s_pitch.pack()
        self.s_tempo.pack()
        
        self.control.update()
                
    # Updates the pitch
    def update_pitch(self, val):
        self.pitch = int(val)
        
    # Updates the tempo
    def update_tempo(self, val):
        self.tempo = float(val) / 100.
        
    # Performs the STFT on a chunk of data and returns the new data
    def analyze_data(self, data):
        new_data = pianoputer.pitchshift(data, self.pitch, self.tempo, 2**10, 2**8)

        return new_data
        
    # Plays the specified data snippet
    def play_audio(self, data):
        out_data = data.astype(numpy.int16).tostring()
        self.stream_output.write(out_data)
            
    # Performs the phase vocoding algorithm
    def start(self):
        data = numpy.fromstring(self.stream_input.read(CHUNK), numpy.int16)
        
        while len(data) > 0:
            new_data = self.analyze_data(data)
            self.play_audio(new_data)
            self.control.update()
            data = numpy.fromstring(self.stream_input.read(CHUNK), numpy.int16)
                            
    # Closes the audio output stream
    def close_all(self):
        self.stream.close()
        self.p.terminate()
        self.control.destroy()
    
if __name__ == "__main__":
    pv = PhaseVocoder()
    pv.start()
    pv.close_all()