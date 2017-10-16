import music21
score = music21.converter.parse("Lucky.mid")
stream = music21.stream.Stream()
stream.append(score)
print(score.parts)

print(score.analyze('key'))
