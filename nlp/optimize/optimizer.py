from os import name
from typing import Dict
from nlp.lex.tokenizer import Tokenizer
from nlp.lex.pos_tagger import PosTagger
from nltk.chunk.regexp import RegexpParser
from .dictionaries import Dictionary
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import wordnet

class Optimizer:

    def optimize_chunks(chunks):
        # print("CHUNKS HERE:", chunks)
        trees = []
        sentences = []
        
        for chunk in chunks:
            # chunk_sentence = ' '.join([w for w, t in chunk.leaves()]) 
            # print(chunk_sentence)
            trees.append( nltk.tree.Tree.fromstring(str(chunk)))
        
        for tree in trees:
            tree = Optimizer.remove_repeating_words(tree)

            tree = Optimizer.replace_invalid_words(tree)

            tree = Optimizer.replace_incomplete_words(tree)

            tree = Optimizer.remove_grammar_redundancies(tree)

            tree = Optimizer.remove_redundant_apostrophes(tree)

            Optimizer.capitalize_entities(tree)

            p8_changed, p8_sentence = Optimizer.check_verb_tense(tree)
            if p8_changed:
                tree = Optimizer.regenerate_parse_tree(p8_sentence)
            
            p1_changed, p1_sentence = Optimizer.check_subject_verb_agreement(tree)
            if p1_changed:
                tree = Optimizer.regenerate_parse_tree(p1_sentence)
            
            p2_changed, p2_sentence = Optimizer.remove_pronoun_errors(tree)
            if p2_changed:
                tree = Optimizer.regenerate_parse_tree(p2_sentence)   

            p3_changed, p3_sentences = Optimizer.split_independent_clauses(tree)
            if p3_changed:
                for sentence in p3_sentences:
                    sentences.append(sentence)
            else:
                sentences.append(p3_sentences[0])
            # chunk_leaves = chunk.leaves() #this functions provides us with a list of tokens from the chunk with their POS
            # print("Chunk leaves", chunk_leaves)
            # print(chunk_leaves[0][0]) ##we can access individual tokens like this - 1st word from the 1st token
       
       
       ##LAST THING TO RUN!
        text = ' '.join(['. '.join(sentences)])        
        unique_sentences = Optimizer.remove_repeating_sentences(sentences)
        print(unique_sentences)
        text =  ' '.join(['. '.join(unique_sentences)])
        print(text)
        return text

    def regenerate_parse_tree(sentence):
        print(sentence)
        pos_sentence = PosTagger.tag_pos(Tokenizer.tokenize(sentence))

        grammar = RegexpParser("""
                                PS: {<PRP> <VBP> <DT>? <IN>? <PR.*> <NN.*>}
                                IC: {<PRP> <V.*> <TO>? <DT>? <NN.*>? <CC>? <NN.*>? <V.*>?}
                                VP: {<RB>? <CC>? <V.*> <P.*> <IN> <DT> <NN.*>}          #To extract Verb Phrases
                                SV1: {<NN.*> <CC> <NN.*>}
                                SV2: {<NN.*> <V.*>}
                                NP: {<DT>?<JJ.*>*<NN.*>+}   #To extract Noun Phrases
                                PP: {<IN> <NP>}              #To extract Prepositional Phrases
                                FW: {<FW>}                 #To extract Foreign Words
                                CD : {<CD>}                #To extract Cardinal Digits 
                                PRP: {<PRP.*>}              #To extract all Pronouns
                                """)
        output = grammar.parse(pos_sentence)
        return nltk.tree.Tree.fromstring(str(output))

    #This function removes duplicate words from sentence
    def remove_repeating_words(chunk): #eg. "He he went to to the gym." -> He went to the gym.
        noduplist = [] #An empty list 
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())

        
        for leaf in leaves: #Goes through every elements in the list that contains duplicate entries 
            lowercase_list = [word.lower() for word in noduplist]
            
            if leaf[0].lower() not in lowercase_list: #Add all unique elements to a newlist 
               noduplist.append(leaf[0])   

        sentence = TreebankWordDetokenizer().detokenize(noduplist)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree  #returns the new list                   
                
   

    def remove_repeating_sentences(sentence): #eg. He went to the gym. He went to the gym. -> He went to the gym.
        noduplsentence = [] #An empty list 
        
        for element in sentence: #Goes through every elements in the list that contains duplicate entries 
            lowercase_list = [word.lower() for word in noduplsentence]
            
            if element.lower() not in lowercase_list: #Add all unique elements to a newlist 
                noduplsentence.append(element)  
        return noduplsentence  #returns the new list  

        
    def replace_incomplete_words(chunk): #eg. He wen to th gym. -> He went to the gym.
        dicti = Dictionary.Informal_Words
        updated_tokens = []
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        
        for leaf in leaves:
            if dicti.get(leaf[0]):
               print(dicti.get(leaf[0]))
               new_word = dicti.get(leaf[0])
               print("\033[91m",leaf[0],'\033[0m',' ----------> ','\033[92m',new_word,'\033[0m')
               leaf[0] = new_word
            updated_tokens.append(leaf[0])
        sentence = TreebankWordDetokenizer().detokenize(updated_tokens)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree
    
    def replace_invalid_words(chunk):  #eg. He ewnt to hte gim -> He went to the gym.
        invalid_dicti = Dictionary.Invalid_Words
        updated_tokens = []
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())

        for leaf in leaves:
            if invalid_dicti.get(leaf[0]):
               new_word = invalid_dicti.get(leaf[0])
               print("\033[91m",leaf[0],'\033[0m',' ----------> ','\033[92m',new_word,'\033[0m')
               leaf[0] = new_word
            updated_tokens.append(leaf[0])
        sentence = TreebankWordDetokenizer().detokenize(updated_tokens)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree

         #     #eg. Afterwards he went to the gym -> Afterwards, he went to the gym.
         #     #eg. I am not angry with you, I am not happy with you, either. -> I am not angry with you. I am not happy with you, either.
    
       #eg. She stopped pouring water because she thought it was adequate enough.
        # -> She stopped poruing water because she thought it was enough.
    def remove_grammar_redundancies(chunk):
        tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())            
        # for syn in synonyms.lemma_names():
        #     print(syn)
        token_words = []
        for token in tokens:
            token_words.append(token[0])
        
        for indx,token in enumerate(token_words):
            synonyms = []
            for syn in wordnet.synsets(token): ##we use nltk's wordnet synonym library
                for lemma in syn.lemma_names():
                    synonyms.append(lemma)
            if((indx+1) < len(token_words) and token_words[indx+1] and token_words[indx+1] in synonyms):
                print("\033[91mTO BE REMOVED:\033[0m ", token_words[indx+1])
                token_words.pop(indx+1)
                break
        
        sentence = TreebankWordDetokenizer().detokenize(token_words)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree

    # def optimize_grammar_punctuations(chunk):
    #     #eg. Afterwards he went to the gym -> Afterwards, he went to the gym.
    #     #eg. I am not angry with you, I am not happy with you, either. -> I am not angry with you. I am not happy with you, either.
        
            
    def check_verb_tense(chunk):
        #eg. I walk to the store and I bought milk. ->
        # I walked to te store and I bought milk.
        pos_tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(pos_tokens)
        pos_tags = []
        words = []
        sentence_updated = False
        sentence = Optimizer.reconstruct_sentence(pos_tokens)
        pos_sentence = PosTagger.tag_pos(Tokenizer.tokenize(sentence))
        changed = False

        tense_1 = Dictionary.Tense_1

        for pos in pos_tokens:
            pos_tags.append(pos[1])
        
        for token in pos_tokens:
            words.append(token[0])

        grammar = RegexpParser("""
                                X: {<PRP> <VBP> <TO> <DT> <NN.*> <CC> <VBD> <NN.*>}
                                Y: {<PRP> <VBD> <TO>? <NN.*>? <DT>? <RB>? <VB> <NN.*>?}
                                """)
        
        output = grammar.parse(pos_sentence)
        print("PARSED OUTPUT:", output)

        for leaf in output.subtrees():
            if(leaf.label() == 'X'):
                for idx,token in enumerate(pos_tokens):
                    if token[1] == 'VBP':
                        sentence_updated = True
                        old_token = token
                        new_token = []
                        if tense_1.get(token[0]):
                            new_token.append(tense_1.get(token[0]))
                            new_token.append('VBD')
                        else:
                            new_token.append(token[0] + 'ed')
                            new_token.append('VBD')

                        pos_tokens[idx] = new_token
                        print("\033[91m",old_token,'\033[0m',' ----------> ','\033[92m',new_token,'\033[0m')
            elif(leaf.label() == 'Y'):
                for idx,token in enumerate(pos_tokens):
                    if token[1] == 'VB':
                        sentence_updated = True
                        old_token = token
                        new_token = []
                        if tense_1.get(token[0]):
                            new_token.append(tense_1.get(token[0]))
                            new_token.append('VBD')
                        else:
                            new_token.append(token[0] + 'ed')
                            new_token.append('VBD')

                        pos_tokens[idx] = new_token
                        print("\033[91m",old_token,'\033[0m',' ----------> ','\033[92m',new_token,'\033[0m')

        if(sentence_updated):
            updated_sentence = Optimizer.reconstruct_sentence(pos_tokens)    
            print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            print('\033[94m============UPDATED SENTENCE============\033[0m \n ')     
            print(updated_sentence) 
            sentence = updated_sentence
            changed = True
        else:
            print("No change detected")
            sentence = old_sentence
            changed = False
        
        return changed, sentence  
    
    def check_subject_verb_agreement(chunk):
        print('\033[94mCHECKING SUBJECT VERB AGREEMENT...\033[0m \n ')
        #eg. Anna and Mike is going skiing. -> Anna and Mike are going skiing.
        pos_tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(pos_tokens)
        sentence_updated = False
        sentence = ''
        changed = False
    
        for idx,leaf in enumerate(chunk.subtrees()):
            if leaf.label() == 'SV1':
                for idx,token in enumerate(pos_tokens):
                    if token[1] == 'VBZ':
                        sentence_updated = True
                        old_token = token
                        new_token = []
                        new_token.append('are')
                        new_token.append('VBD')
                        pos_tokens[idx] = new_token
                        print("\033[91m",old_token,'\033[0m',' ----------> ','\033[92m',new_token,'\033[0m')
            if leaf.label() == 'SV2':
                for idx,token in enumerate(pos_tokens):
                    sentence_updated = True
                    if token[1] == 'VBD' or token[0] == 'are':
                        old_token = token
                        new_token = []
                        new_token.append('is')
                        new_token.append('VBZ')
                        pos_tokens[idx] = new_token
                        print("\033[91m",old_token,'\033[0m',' ----------> ','\033[92m',new_token,'\033[0m')

        if(sentence_updated):
            updated_sentence = Optimizer.reconstruct_sentence(pos_tokens)    
            print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            print('\033[94m============UPDATED SENTENCE============\033[0m \n ')     
            print(updated_sentence) 
            sentence = updated_sentence
            changed = True
        else:
            print("No change detected")
            sentence = old_sentence
            changed = False
        
        return changed, sentence  
        


    def remove_pronoun_errors(chunk):
        print('\033[94mCHECKING FOR PRONOUN ERRORS...\033[0m \n ')
        #eg. I fed all of her cats, then took it for a walk. ->
        # I fed all of her cats, then took them for a walk.
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(leaves)
        sentence_updated = False
        singular_pronouns = ['it','her','him','you']
        sentence_updated = False
        is_plural_noun = False
        sentence = ''
        changed = False

        for idx,i in enumerate(chunk.subtrees()):
            if i.label() == 'PS':
                for leaf in leaves:
                    print(leaf)
                    if leaf[1] == 'NNS':
                        is_plural_noun = True
            elif i.label() == 'VP':
                for x,leaf in enumerate(leaves):
                    if leaf[1] == 'PRP' and x!=0 and is_plural_noun and leaf[0] in singular_pronouns:
                        old_leaf = leaf
                        new_leaf = []
                        new_leaf.append('them')
                        new_leaf.append('PRP')
                        leaves[x] = new_leaf
                        sentence_updated = True
                        print("\033[91m",old_leaf,'\033[0m',' ----------> ','\033[92m',new_leaf,'\033[0m')
                    elif leaf[1] == 'PRP' and x != 0 and not is_plural_noun and leaf[0] not in singular_pronouns:
                        old_leaf = leaf
                        new_leaf = []
                        new_leaf.append('it')
                        new_leaf.append('PRP')
                        leaves[x] = new_leaf
                        sentence_updated = True
                        print("\033[91m",old_leaf,'\033[0m',' ----------> ','\033[92m',new_leaf,'\033[0m')

        if(sentence_updated):
            updated_sentence = Optimizer.reconstruct_sentence(leaves)    
            print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            print('\033[94m============UPDATED SENTENCE============\033[0m \n ')     
            print(updated_sentence)
            sentence = updated_sentence   
            changed = True
        else:
            print("No change detected")  
            sentence = old_sentence
            changed = False
        
        return changed, sentence
        

    def split_independent_clauses(chunk):
        print('\033[94mSPLITTING INDEPENDENT CLAUSES...\033[0m \n ')
        #eg. I went to the store I got milk and cookies  ->
        #I went to the store. I got milk and cookies.
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(leaves)
        clauses_updated = False
        independent_clauses = []
        changed = False

        pos_sentence = PosTagger.tag_pos(Tokenizer.tokenize(old_sentence))
    

        grammar = RegexpParser("""
                                IC: {<PRP> <V.*> <TO>? <DT>? <NN.*>? <CC>? <NN.*>? <V.*>? <NN.*>}
                                """)
        
        chunk = nltk.tree.Tree.fromstring(str(grammar.parse(pos_sentence)))
        
        for subtree in chunk.subtrees():
            if subtree.label() == 'IC':
                if (subtree.leaves()):
                    pos_tokens = Optimizer.convert_leaves_to_tokens(subtree.leaves())
                    sentence = Optimizer.reconstruct_sentence(pos_tokens)
                    sentence = sentence.capitalize()
                    independent_clauses.append(sentence)
                    clauses_updated = True
        if(clauses_updated):
            print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            print('\033[94m============INDEPENDENT CLAUSES============\033[0m \n ')     
            print(independent_clauses)
            changed = True               
        else:
            independent_clauses.append(old_sentence)
            print("No change detected")
        
        return changed, independent_clauses
            
        

        
    def remove_redundant_apostrophes(chunk):
        print('\033[94mCHECKING FOR REDUNDANT APOSTROPHES...\033[0m \n ')
        redundant_apostrophes = Dictionary.Redundant_Apostrophes
        # eg. The girls's soccer game was delayed by rain. ->
        # The girls' soccer game was delayed by rain.
        updated_tokens = []
        tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        
        for token in tokens:
            if redundant_apostrophes.get(token[0]):
               new_word = redundant_apostrophes.get(token[0])
               print("\033[91m",token[0],'\033[0m',' ----------> ','\033[92m',new_word,'\033[0m')
               token[0] = new_word
            updated_tokens.append(token[0])
        sentence = TreebankWordDetokenizer().detokenize(updated_tokens)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree


    def capitalize_entities(chunk):
        # eg. germany won the match although portugal started very well -> Germany won the match although portugal started very well.
        tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        sentence = Optimizer.reconstruct_sentence(tokens)
        pos_sentence = PosTagger.tag_pos(Tokenizer.tokenize(sentence))
        entities = Dictionary.Entities

        for indx,token in enumerate(pos_sentence):
            if token[1] == 'NN' or token[1] == 'NNS':
                # if token[0] in entities:
                #     print("NEW WORD,:", token[0].capitalize())
                if entities.get(token[0]):
                    print("NEW WORD,:", entities.get(token[0]))
                    new_token = []
                    new_token.append('NNP')
                    new_token.append(entities.get(token[0]))
                    pos_sentence[indx] = new_token
        
        print("NEW TOKENS:", pos_sentence)




    def convert_leaves_to_tokens(leaves):
        tokens = []
        for leaf in leaves:
            leaf = leaf.split("/")
            tokens.append(leaf)
        return tokens
    
    def reconstruct_sentence(pos_tokens):
        tokens = []
        for token in pos_tokens:
            tokens.append(token[0])
        
        sentence = TreebankWordDetokenizer().detokenize(tokens)
        return sentence

# tree = nltk.tree.Tree.fromstring(""" (S
#   (IC I/PRP am/VBP a/DT boy/NN)
#   (IC I/PRP went/VBD to/TO the/DT shop/NN))""")

# # Optimizer.check_subject_verb_agreement(tree)
# teststring = ["He", "he","went", "to", "to", "the", "gym", "." ] 
# teststring2 = ["active"]
# #["Hey", "yee", "hepl", "th", "gym"]


# print(teststring)
# #print(teststring2)
# print(Optimizer.remove_repeating_words(teststring))
# print(Optimizer.remove_grammar_redundancies(teststring2))