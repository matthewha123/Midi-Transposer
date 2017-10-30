from music21 import *
score = converter.parse("APie.mid")
key = score.analyze('key')
print(key)
f = note.Note("F5")
print(f.name)
