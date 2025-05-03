#
# textmodel.py
#
# TextModel project!
#
# Name(s): Juhi Damley
#

import porter
import string
import math

class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        self.exclamation = {}     # For counting exclamatory words
        
        # Create another dictionary of your own
        #
        self.myparameter = {}     # For counting ___________

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'MY PARAMETER:\n{str(self.myparameter)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:42]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:42]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.
            
           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """
        sLen = 0
        for word in self.text.split():
            sLen += 1
            if word[-1] in ".!?":
                if sLen in self.sentencelengths:
                    self.sentencelengths[sLen] += 1
                else: 
                    self.sentencelengths[sLen] = 1
                sLen = 0
        return self.sentencelengths


    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        s = s.encode("ascii", "ignore")   # Ignores non-ASCII characters
        s = s.decode()         # Decodes it back to a string (with the non-ACSII characters removed)

        result = s.lower()    # Not implemented fully: this just lower-cases
                              # ..things for now
        newS = ""
        for c in result:
            if c not in string.punctuation:
                newS+= c
        result = newS
        return result
    
    def makeWordLengths(self):
        """Creates the dictionary of word lengths
        """
        for word in self.cleanedtext.split():
            if len(word) not in self.wordlengths:
                self.wordlengths[len(word)] = 1
            else:
                self.wordlengths[len(word)] += 1   
        return self.wordlengths
    
    def makeWords(self):
        """
        Creates the dictionary of words and their frequency
        """
        for word in self.cleanedtext.split():
            if word not in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1   
        return self.words
    
    def makeStems(self):
        """
        Creates the dictionary of word stems and their frequency
        """
        stemList = []
        for word in self.cleanedtext.split():
            stemList += [porter.create_stem(word)]
        
        for word in stemList:
            if word not in self.stems:
                self.stems[word] = 1
            else:
                self.stems[word] += 1
        return self.stems

    def makeExclamation(self):
        """
        Creates the dictionary of words with exclamations following them. 
        """
        for word in self.text.split():
            if word[-1] == "!":
                if word not in self.exclamation:
                    self.exclamation[word] = 1
                else:
                    self.exclamation[word] += 1   
        return self.exclamation
    
    def normalizeDictionary(self, d):
        '''
        Creates a normalized dictionary of d
        '''
        nd = {}
        sumVals = sum(d.values())
        for key in d:
            nd[key] = d[key]/sumVals
        return nd
    
    def smallestValue(self, nd1, nd2):
        """
        Finds the smallest value between nd1 and nd2
        """
        values1 = list(nd1.values()) if nd1 else []
        values2 = list(nd2.values()) if nd2 else []
        all_values = values1 + values2
        if not all_values:
            return 0.0
        return min(all_values)
    
    def checkNorm(self, d):
        sumKey = 0
        for key in d:
            sumKey += d[key]
        if round(sumKey) == 1:
            return True
        else:
            return False
    
    def compareDictionaries(self, d, nd1, nd2):
        """
        Creates a list of the log probability that d arose from nd1 and nd2
        """
        if not self.checkNorm(nd1):
            nd1 = self.normalizeDictionary(nd1)
        if not self.checkNorm(nd2):
            nd2 = self.normalizeDictionary(nd2)

        epsilon = 0.5 * self.smallestValue(nd1, nd2)

        log_prob1 = 0.0
        log_prob2 = 0.0

        for key, count in d.items():
            prob1 = nd1.get(key, epsilon)
            log_prob1 += count * math.log(prob1)

            prob2 = nd2.get(key, epsilon)
            log_prob2 += count * math.log(prob2)

        return [log_prob1, log_prob2]
    
    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makeExclamation()


    def compareTextWithTwoModels(self, model1, model2):
        """
        Compares the text with two models
        """
        nd1 = self.normalizeDictionary(model1.words)
        nd2 = self.normalizeDictionary(model2.words)
        LogProbs1 = self.compareDictionaries(self.words, nd1, nd2)

        nd3 = self.normalizeDictionary(model1.stems)
        nd4 = self.normalizeDictionary(model2.stems)
        LogProbs2 = self.compareDictionaries(self.stems, nd3, nd4)

        nd5 = self.normalizeDictionary(model1.sentencelengths)
        nd6 = self.normalizeDictionary(model2.sentencelengths)
        LogProbs3 = self.compareDictionaries(self.sentencelengths, nd5, nd6)

        nd7 = self.normalizeDictionary(model1.exclamation)
        nd8 = self.normalizeDictionary(model2.exclamation)
        LogProbs4 = self.compareDictionaries(self.exclamation, nd7, nd8)

        nd9 = self.normalizeDictionary(model1.wordlengths)
        nd10 = self.normalizeDictionary(model2.wordlengths)
        LogProbs5 = self.compareDictionaries(self.wordlengths, nd9, nd10)

        d_name = ["words", "stems", "sentencelengths", "exclamation", "wordlengths"]
        log_probs = [LogProbs1, LogProbs2, LogProbs3, LogProbs4, LogProbs5]

        print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
        print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")
        print(f"     {d_name[0]:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ")
        print(f"     {d_name[1]:>20s}   {LogProbs2[0]:>10.2f}   {LogProbs2[1]:>10.2f} ")
        print(f"     {d_name[2]:>20s}   {LogProbs3[0]:>10.2f}   {LogProbs3[1]:>10.2f} ")
        print(f"     {d_name[3]:>20s}   {LogProbs4[0]:>10.2f}   {LogProbs4[1]:>10.2f} ")
        print(f"     {d_name[4]:>20s}   {LogProbs5[0]:>10.2f}   {LogProbs5[1]:>10.2f} ")

        m1_wins = 0
        m2_wins = 0

        for lp in log_probs:
            if lp[0] > lp[1]:
                m1_wins += 1
            else:
                m2_wins +=1
        
        print(f"""-->  Model1 wins on {m1_wins} features
              -->  Model2 wins on {m2_wins} features""")
        
        win = max(m1_wins,m2_wins)

        if win == m1_wins:
            winner = "Model1"
        else:
            winner = "Model2"

        print(f"+++++      {winner} is the better match!      +++++")










# And let's test things out here...
TMintro = TextModel()


# Add a call that puts information into the model
TMintro.addRawText("""This is a small sentence. This isn't a small
sentence, because this sentence contains more than 10 words and a
number! This isn't a question, is it?""")

# Put the above triple-quoted string into a file named test.txt, then run this:
#  TMintro.addFileText("test.txt")   # "comment in" this line, once the file is created

# Print it out
print("TMintro is", TMintro)


# Add more calls - and more models - here: