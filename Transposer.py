from appJar import gui
import math
import random
import music21
import numpy
import scipy

lower = 'a9'
upper = 'c9'
note = ''
noteNum = 51
octaveNum = 48

toggle = True

app = gui("Transposer", "400x200")
app.setResizable(True)
app.addLabel("title", "You Suck at Singing")
app.setLabelBg("title", "red")

counter = {0: "a", 1:"a#", 2: "b", 3: "c", 4: "c#", 5: "d", 6: "d#", 7: "e", 8: "f", 9: "f#", 10: "g", 11: "g#"}
accidential = {0: "", 1: "#"}

#the number coefficient will divide the current iterator number by 8 and subtract the remaineder
def mainPress(button):
    if button == "Bound":
        app.hide()
        app.showSubWindow("Lower Bound")
    if button == "Transpose":
        print(str(getKey()))
        score = music21.converter.parse("APie.mid")
        key = score.analyze('key')
        #key = score[0]
        print(key.tonic)
        interval = music21.interval.Interval(key.tonic,music21.pitch.Pitch(getKey()["note"]))
        print (interval)
        newScore = score.transpose(interval)
        for i in newScore.recurse().getElementsByClass('Instrument'):
            if i.midiProgram is None:
                i.midiProgram = 0  
        print(str(newScore.analyze('key'))+" Steps 1 of 2 complete")
        #newScore.write('midi',"newfilename.mid")
        newScore.write("midi", "APieTranspose.mid")
        mf = music21.midi.translate.streamToMidiFile(newScore)
        print(len(mf.tracks))
##        stream = music21.stream.Stream()
##        stream.append(score)
##        player = music21.midi.realtime.StreamPlayer(stream)
##        player.play
        #stream = music21.stream.Stream()
        #stream.append(score)
        #stream.show()
        
def lowPress(button):
    global lower, upper, note, noteNum, octaveNum
    if button == "Lower":
        noteNum = noteNum - 1
        octaveNum= octaveNum - 1
        app.playNote(halfStep(1)["note"], 1500)
    if button == "Higher":
        noteNum = noteNum + 1
        octaveNum= octaveNum + 1
        app.playNote(halfStep(-1)["note"], 1500)
    if button == "Set Lower":
        lower = note
        print(lower)
    if button == "Set Upper":
        upper = note
        print(upper)
    if button == "Back":
        app.hideSubWindow("Lower Bound")
        app.show()
    
def halfStep(num):
    global noteNum, octaveNum, toggle, octave, note,octaveNumPrev
    letter = counter[(noteNum % 12)]
    #initially set octave one time
    if(toggle):
        octave = math.floor(noteNum / 12)
        print(octave)
        toggle = False
        octaveNumPrev = 0
    octave = math.floor(octaveNum/12)
    if(octave < 0 ):
        octave = 0
    print (octaveNum)
    print("onp "+str(octaveNumPrev))
    note = {"note": letter + str(int(octave)), "number": noteNum, "octave":octave}
    
    print(note)
    return note

def getKey():
    diff = upper["number"] - lower["number"]
    if(diff <=0):
        app.warningBox("Bound Error", "Bounds are Inverted bruh")
        return
    else:
        if((diff%2) == 0):
            key = {"note": counter[(lower["number"]+(diff/2))%12], "number":lower["number"]+(diff/2)}
        else:
            qSpin = [-0.5,0.5]
            spin = random.choice(qSpin)
            key = {"note": counter[(lower["number"]+(diff/2)+spin)%12], "number":lower["number"]+(diff/2)+spin}
        print(key)
        return key
app.startSubWindow("Lower Bound", True)
app.addButtons(["Lower", "Higher"],lowPress)
app.addButtons(["Set Lower", "Set Upper"], lowPress)
app.addButtons(["Back"], lowPress)
app.stopSubWindow()
        
app.addButtons(["Upload", "Transpose"], mainPress)
app.addButtons(["Bound"], mainPress)

app.go()
