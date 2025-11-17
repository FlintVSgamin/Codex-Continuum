import tensorflow as tf
import numpy as np
import modelCreation
model = tf.keras.models.load_model('generator.keras')
model.compile()
sequenceLength = modelCreation.getSeqLen()

def test():
    testSeq = "s"
    testSeq = modelCreation.sequenceToInputFormat(testSeq)
    probDist = model(testSeq)[0]
    threshold = 1/32
    for i in range(0,len(probDist)):
        if probDist[i] >= threshold:
            print(f"{modelCreation.decode(i)}: {probDist[i]}")


def textCorrection(text, threshold):
    #iterate over whole text
    for i in range(1,len(text) - 1):
        sequence = modelCreation.sequenceToInputFormat('')
        if(i < sequenceLength):
            threshold = (threshold * sequenceLength) / i
            sequence = modelCreation.sequenceToInputFormat(text[:i])
        else:
            sequence = modelCreation.sequenceToInputFormat(text[i-sequenceLength:i])
        probDist = model(sequence)[0]

        charsInThreshold = []
        maxProb = 0.0
        maxChar = ' '

        for j in range(0,len(probDist)):
            probability = probDist[j]
            char = modelCreation.decode(j)
            if (probability >= threshold):
                charsInThreshold.append(char)
                if(probability > maxProb):
                    maxProb = probability
                    maxChar = char
        if text[j] not in charsInThreshold:
            text = text[:j] + maxChar + text[j+1:]
    return text

print(textCorrection("sacra, quae Cronia esse iterantur ab illis, eumque diem celebrant per agros urbesque fere omnes exercent epulas laeti famulosque procurant quisque suos", 1/32))




