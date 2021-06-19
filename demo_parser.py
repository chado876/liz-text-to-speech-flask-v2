import nltk



def parse(sentence_tokens_pos):
    grammar = "NP:{<DT>?<JJ>*<NN>}" 
    Reg_parser = nltk.RegexpParser(grammar)
    for sentence in sentence_tokens_pos:
        Reg_parser.parse(sentence)
        Output = Reg_parser.parse(sentence)
        print(Output)
        Output.draw()
   

           