import pyaudio
import numpy, wave
#import scipy.fftpack
import Tkinter
import pianoputer

'''
To Do:

Add STFT algorithm to see if it all works

'''

class PhaseVocoder:
    def __init__(self, file_name):
        self.chunk = 8192*8
        self.wf = wave.open(file_name, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()),
                             channels = self.wf.getnchannels(),
                             rate = self.wf.getframerate(),
                             output = True)
                                                          
        self.tempo = 1.
        self.pitch = 0
        
        # Creates a slider that can change the pitch and tempo
        self.control = Tkinter.Tk()
        self.control.title("Pitch and Tempo")
        self.s_pitch = Tkinter.Scale(label='Pitch', orient='horizontal', length=400, from_=-12, to=12, command=self.update_pitch)
        self.s_tempo = Tkinter.Scale(label='Tempo', orient='horizontal', length=400, from_=0, to=200, command=self.update_tempo)
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
        pitch_shifted = pianoputer.pitchshift(data, self.pitch, 2**12, 2**10)
        tempo_shifted = pianoputer.stretch(pitch_shifted, self.tempo, 2**12, 2**10)
        return pitch_shifted
        
    # Plays the specified data snippet
    def play_audio(self, data):
        out_data = data.astype(numpy.int16).tostring()
        self.stream.write(out_data)
            
    # Performs the phase vocoding algorithm
    def start(self):
        data = numpy.fromstring(self.wf.readframes(self.chunk), numpy.int16)
        
        while len(data) > 0:
            new_data = self.analyze_data(data)
            self.play_audio(new_data)
            self.control.update()
            data = numpy.fromstring(self.wf.readframes(self.chunk), numpy.int16)
                            
    # Closes the audio output stream
    def close_all(self):
        self.stream.close()
        self.p.terminate()
        self.control.destroy()
    
if __name__ == "__main__":
    pv = PhaseVocoder("firework.wav")
    pv.start()
    pv.close_all()
