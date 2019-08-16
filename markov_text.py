import json
import random
class Markov:
    def __init__(self, label, word_delimiter = ' '):
        self.label = label
        self.nodes = {}
        self.word_delimiter = word_delimiter

    def process_input(self, text):
        text = text.replace('\n', ' ')
        text = text.replace('--', ' ')
        words = text.split(self.word_delimiter)
        for i in range(len(words)-2):
            if words[i] in self.nodes:
                if words[i+1] in self.nodes[words[i]]:
                    self.nodes[words[i]][words[i+1]].append(words[i+2])
                else:
                    self.nodes[words[i]][words[i+1]] = [words[i+2]]
            else:
                self.nodes[words[i]] = {words[i+1]:[words[i+2]]}

    def generate_text(self, length):
        count = 0
        sentence = False
        output = ''
        selection = self.nodes
        while count < length:
            if type(selection) == type({}):
                word = random.sample(selection.keys(),1)[0]
                output = output + word + " "
                selection = selection[word]
            elif type(selection) == type([]):
                word = random.sample(selection,1)[0]
                output = output + word + " "
                selection = self.nodes
            count += 1
        return output




markov64 = Markov("Test Markov")
markov64.process_input("""
There are also various tools for obtaining the XPath of elements such as FireBug for Firefox or the Chrome Inspector. 
If you’re using Chrome, you can right click an element, choose ‘Inspect element’, highlight the code, right click again, and choose ‘Copy XPath’.
""")
with open('pap.txt', 'r') as f:
    markov64.process_input(f.read())
sampletext = markov64.generate_text(100)
print(sampletext)
#print(json.dumps(markov64.nodes, indent=2))
demo = False
if demo:
    lookup = input()
    while lookup != 'done':
        if lookup in markov64.nodes:
            print(markov64.nodes[lookup])
        else:
            print("Not here")
        lookup = input()
