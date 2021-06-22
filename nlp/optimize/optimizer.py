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
        trees = []
        sentences = []
        
        for chunk in chunks:
            trees.append( nltk.tree.Tree.fromstring(str(chunk)))
        
        for tree in trees:
            tree = Optimizer.remove_repeating_words(tree)

            tree = Optimizer.replace_invalid_words(tree)

            tree = Optimizer.replace_incomplete_words(tree)

            tree = Optimizer.translate_creole(tree)

            tree = Optimizer.remove_grammar_redundancies(tree)

            tree = Optimizer.remove_redundant_apostrophes(tree)

            tree = Optimizer.capitalize_entities(tree)

            p8_changed, p8_sentence = Optimizer.check_verb_tense(tree)
            if p8_changed:
                tree = Optimizer.regenerate_parse_tree(p8_sentence)
            
            p9_changed, p9_sentence = Optimizer.check_subject_verb_agreement(tree)
            if p9_changed:
                tree = Optimizer.regenerate_parse_tree(p9_sentence)
            
            p10_changed, p10_sentence = Optimizer.remove_pronoun_errors(tree)
            if p10_changed:
                tree = Optimizer.regenerate_parse_tree(p10_sentence)   

            p11_changed, p11_sentences = Optimizer.split_independent_clauses(tree)
            if p11_changed:
                for sentence in p11_sentences:
                    sentences.append(sentence)
            else:
                sentences.append(p11_sentences[0])
       
       
       ##LAST PROCESS - REMOVE DUPLICATE SENTENCES
        unique_sentences = Optimizer.remove_repeating_sentences(sentences)
        text =  ' '.join(['. '.join(unique_sentences)])
        print('\033[94mOPTIMIZED TEXT...\033[0m \n ', text)
        return text

    def regenerate_parse_tree(sentence):
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
        print('\033[94m #1 REMOVING REPEATING WORDS...\033[0m \n ')
        noduplist = [] #An empty list 
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())

        token_words = []
        for token in leaves:
            token_words.append(token[0])
        
        for indx,word in enumerate(token_words): #Goes through every elements in the list that contains duplicate entries 
            if((indx+1) < len(token_words)):
                iter = indx + 1
                while iter < len(token_words)  and token_words[indx+1] and token_words[indx+1].lower() == word.lower():
                    print("\033[91mRemoving ->", token_words[indx+1],'\033[0m')
                    token_words.pop(indx+1)
                    iter = iter + 1 
            noduplist.append(word) 

        sentence = TreebankWordDetokenizer().detokenize(noduplist)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree  #returns the new list                   
                
   

    def remove_repeating_sentences(sentence): #eg. He went to the gym. He went to the gym. -> He went to the gym.
        print('\033[94m #12 REMOVING REPEATING SENTENCES...\033[0m \n ')
        noduplsentence = [] #An empty list 
        
        for element in sentence: #Goes through every elements in the list that contains duplicate entries 
            lowercase_list = [word.lower() for word in noduplsentence]
            
            if element.lower() not in lowercase_list: #Add all unique elements to a newlist 
                noduplsentence.append(element)  
        return noduplsentence  #returns the new list  

        
    def replace_incomplete_words(chunk): #eg. He wen to th gym. -> He went to the gym.
        print('\033[94m #3 REPLACING INCOMPLETE WORDS...\033[0m \n ')
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
    
    def replace_invalid_words(chunk):  #eg. The tal soilder is braev -> The tall soldier is brave.
        print('\033[94m #2 REPLACING INVALID WORDS...\033[0m \n ')
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
    
       #eg. She stopped pouring water because she thought it was adequate enough.
        # -> She stopped poruing water because she thought it was enough.
    def remove_grammar_redundancies(chunk):
        print('\033[94m #5 REMOVING GRAMMAR REDUNDANCIES...\033[0m \n ')
        tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())            
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

    #     #eg. The vehicle is around the corna-> The vehicle is around the corner.
    def translate_creole(chunk):
        print('\033[94m #4 TRANSLATING CREOLE TO STANDARD ENGLISH...\033[0m \n ')
        grammar_dicti = Dictionary.Patois_Words
        translation_tokens = []
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())

        for leaf in leaves:
            if grammar_dicti.get(leaf[0]):
               new_word = grammar_dicti.get(leaf[0])
               print("\033[91m",leaf[0],'\033[0m',' ----------> ','\033[92m',new_word,'\033[0m')
               leaf[0] = new_word
            translation_tokens.append(leaf[0])
        sentence = TreebankWordDetokenizer().detokenize(translation_tokens)
        tree = Optimizer.regenerate_parse_tree(sentence)
        return tree
            
    def check_verb_tense(chunk):
        print('\033[94m #8 CHECKING VERB TENSE...\033[0m \n ')
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
                                X: {<PRP> <VBP> <TO>? <DT> <NN.*>? <PRP>? <CC> <PRP>? <VBD> <NN.*>}
                                Y: {<PRP> <VBP> <TO>? <DT> <NN.*>? <PRP>? <CC> <PRP>? <VB> <NN.*>}
                                """)
        
        output = grammar.parse(pos_sentence)

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
        print('\033[94m #9 CHECKING SUBJECT VERB AGREEMENT...\033[0m \n ')
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
        print('\033[94m #10 CHECKING FOR PRONOUN ERRORS...\033[0m \n ')
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
        print('\033[94m #11 SPLITTING INDEPENDENT CLAUSES...\033[0m \n ')
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
                if (len(subtree.leaves()) > 4):
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
        print('\033[94m #6 CHECKING FOR REDUNDANT APOSTROPHES...\033[0m \n ')
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
        print('\033[94mCAPITALIZED NAMED ENTITIES...\033[0m \n ')
        # eg. germany won the match although portugal started very well -> Germany won the match although portugal started very well.
        tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        sentence = Optimizer.reconstruct_sentence(tokens)
        pos_sentence = PosTagger.tag_pos(Tokenizer.tokenize(sentence))
        entities = Dictionary.Entities

        for indx,token in enumerate(pos_sentence):
            if token[1] == 'NN' or token[1] == 'NNS':
                if entities.get(token[0]):
                    print("\033[91m",token[0],'\033[0m',' ----------> ','\033[92m',entities.get(token[0]),'\033[0m')
                    new_token = []
                    new_token.append(entities.get(token[0]))
                    new_token.append('NNP')
                    pos_sentence[indx] = new_token
        
        sentence = Optimizer.reconstruct_sentence(pos_sentence)
        tree = Optimizer.regenerate_parse_tree(sentence)

        return tree

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

