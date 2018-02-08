class SymbolDetector():

    def __init__(self):
        symbol_list = None
        with open('data/symlist.txt', 'r') as f:
            symbol_list = f.read().split()
        self.symbol_dict = set(symbol_list)
        self.symbol_list = symbol_list

    def find_similar_symbols(self, symbol_in):
        similar_symbols = []
        size = len(symbol_in)
        for s in self.symbol_list:
            if len(s) > len(symbol_in) and s[:size] == symbol_in:
                similar_symbols.append(s)
        return similar_symbols

    def scan_sentence(self, sentence, target_symbol):
        if len(sentence) < len(target_symbol):
            return False
        for i in range(len(sentence) - len(target_symbol)):
            seg = sentence[i:i + len(target_symbol)]
            if seg == target_symbol:
                return True
        return False

    def scan_words(self, sentence, target_symbol):
        words = sentence.split()
        for word in words:
            if word == target_symbol:
                return True
        return False

    def detect_symbol(self, sentence, target_symbol):
        if self.scan_words(sentence, target_symbol):
            return True
        similar_symbols = self.find_similar_symbols(target_symbol)
        for similar_symbol in similar_symbols:
            if self.scan_sentence(sentence, similar_symbol):
                return False
        return self.scan_sentence(sentence, target_symbol)

    def detect_symbols(self, sentence, target_symbols):
        for target_symbol in target_symbols:
            if self.detect_symbol(sentence, target_symbol):
                return True
        return False
