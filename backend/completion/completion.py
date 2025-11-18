import tensorflow as tf
import numpy as np
import modelCreation
import argparse 
from fractions import Fraction
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

#this file is called on from the CLI using subprocess. in that instance, the value of __name__ is '__main__'
#it must be called using subprocess, as it expects the source to be the 'backend/completion/transformerEnv/' interpreter or venv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ocrText", default = "Provide OCRtext as a CLI argument")
    parser.add_argument("threshold", default = "1/32")
    args = parser.parse_args()

    threshold = args.threshold
    try:
        if '/' in threshold:
            threshold = float(Fraction(threshold))
        else:
            threshold = float(threshold)
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid threshold value '{threshold}'. Write the threshold value as a string either as a fraction like '1/32' or a decimal like '0.03': {e}")
        
    correctedText = textCorrection(args.ocrText, threshold)
    print(correctedText)
    #subprocess will capture this output

    