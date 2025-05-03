#
# textmodel.py
#
# TextModel project!
#
# Name(s): Juhi Damley
#

import porter
import string

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
        self.exclamation = {}     # For counting cat references
        
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