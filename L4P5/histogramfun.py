import pylab

# You may have to change this path
WORDLIST_FILENAME = "/home/simon/Source/mit_600.2/L4P5/words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    vowelList = []
    vowels =  ['a','e','i','o','u','A','E','I','O','U']
    
    for word in wordList:
        vowelsTot = 0
        for l in word:
            if l in vowels:
                vowelsTot += 1
        vowelList.append(vowelsTot / float(len(word)))
    
    pylab.figure(1)
    pylab.title('Histogram of vowels in words')
    pylab.xlabel('proportion of vowels')
    pylab.ylabel('number of words')
    pylab.hist(vowelList, numBins)
    pylab.show()

if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
