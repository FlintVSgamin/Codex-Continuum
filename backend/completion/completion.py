
def encode(encodee):
    encoded = []
    for char in encodee:
        encoded.append(ord(char))
    return encoded

def decode(decodee):
    decoded = ''
    for int in decodee:
        decoded += chr(int)
    return decoded

with open('trainingData/latinCorpus.txt', 'r', encoding='utf-8') as f:
    tempText = f.read()

text = ""
#clean text data
for char in tempText:
    if not char.isnumeric():
        if char.isalpha() or char == ' ' or char == '\n':
            text += char


vocab = sorted(list(set(text)))

encoded = encode(text)
testText = decode(encoded)

if(text != testText):
    print("encode/decode failed")
else:
    print("encode/decode succeeded")
