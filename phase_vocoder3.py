import pyaudio
import numpy, wave
import pianoputer

class PhaseVocoder:
    def __init__(self, file_name):
        self.chunk = 8192*8
        self.wf = wave.open(file_name, 'rb')
                                                          
        self.tempo = 0.5
        self.pitch = 5
                                
    # Performs the STFT on a chunk of data and returns the new data
    def analyze_data(self, data):
        new_data = pianoputer.pitchshift(data, self.pitch, self.tempo, 2**12, 2**10)

        return new_data
               
    # Writes new audio to a file
    def write_data(self, data):
        output = wave.open("output_both2.wav", 'wb')
        output.setnchannels(self.wf.getnchannels())
        output.setsampwidth(self.wf.getsampwidth())
        output.setframerate(self.wf.getframerate())
        output.writeframes(b''.join(data))
        output.close()
            
    # Performs the phase vocoding algorithm
    def start(self):
        unformatted = self.wf.readframes(self.wf.getnframes())
        data = numpy.fromstring(unformatted, numpy.int16)
        
        new_data = self.analyze_data(data).astype(numpy.int16).tostring()

        self.write_data(new_data)
        
if __name__ == "__main__":
    pv = PhaseVocoder("92002__jcveliz__violin-origional.wav")
    pv.start()