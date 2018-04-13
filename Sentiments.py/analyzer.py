import nltk 

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.posTxt = self.loadFile(positives)
        self.negTxt = self.loadFile(negatives)

    def loadFile(self, file):
        with open(file, "r") as f:
            id = []
            for ln in f:
                if not ln.startswith(";"):
                    id.append(ln.rstrip())
        return id

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tknzr = nltk.tokenize.casual.TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False)
        tknTxt = tknzr.tokenize(text)
        sentiment = 0
        
        for i in range(len(tknTxt)):
            if tknTxt[i] in self.posTxt:
                #print("POS")
                #print(tknTxt[i])
                sentiment += 1
            elif tknTxt[i] in self.negTxt:
                #print("NEG")
                #print(tknTxt[i])
                sentiment -= 1
                
        return sentiment
