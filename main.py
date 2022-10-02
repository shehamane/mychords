import autochord
from pydub import AudioSegment

AudioSegment.from_mp3('audio/test1 - test1.mp3').export('audio/test1 - test1.wav', format='wav')
print(autochord.recognize('audio/test1 - test1.wav'))