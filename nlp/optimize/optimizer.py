from .dictionaries import Dictionary
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

class Optimizer:

    def optimize_chunks(chunks):
        print("CHUNKS HERE:", chunks)
        
        for chunk in chunks:
            # chunk_sentence = ' '.join([w for w, t in chunk.leaves()]) 
            # print(chunk_sentence)
            tree = nltk.tree.Tree.fromstring(str(chunk))
            Optimizer.check_subject_verb_agreement(tree)
            Optimizer.remove_pronoun_errors(tree)
            Optimizer.split_independent_clauses(tree)
            

            # chunk_leaves = chunk.leaves() #this functions provides us with a list of tokens from the chunk with their POS
            # print("Chunk leaves", chunk_leaves)
            # print(chunk_leaves[0][0]) ##we can access individual tokens like this - 1st word from the 1st token



    # def remove_repeating_words(chunk):
    #     #eg. He he went to to the gym. -> He went to the gym.

    # def remove_repeating_sentences(chunk):
    #     #eg. He went to the gym. He went to the gym. -> He went to the gym.

    # def replace_incomplete_words(chunk):
    #     #eg. He wen to th gym. -> He went to the gym.
    
    # def replace_invalid_words(chunk):
    #     #eg. He ewnt to hte gim -> He went to the gym.

    # def optimize_grammar_punctuations(chunk):
    #     #eg. Afterwards he went to the gym -> Afterwards, he went to the gym.
    #     #eg. I am not angry with you, I am not happy with you, either. -> I am not angry with you. I am not happy with you, either.
    
    # def remove_grammar_redundancies(chunk):
    #     #eg. She stopped pouring water because she thought it was adequate enough.
    #     # -> She stopped poruing water because she thought it was enough.
    
    # def check_verb_tense(chunk):
    #     #eg. I walk to the store and I bought milk. ->
    #     # I walked to te store and I bought milk.
    
    def check_subject_verb_agreement(chunk):
        print('\033[94mCHECKING SUBJECT VERB AGREEMENT...\033[0m \n ')
        #eg. Anna and Mike is going skiing. -> Anna and Mike are going skiing.
        pos_tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(pos_tokens)
        sentence_updated = False
    
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
                    if token[1] == 'VBD':
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
        else:
            print("No change detected")  
        


    def remove_pronoun_errors(chunk):
        print('\033[94mCHECKING FOR PRONOUN ERRORS...\033[0m \n ')
        #eg. I fed all of her cats, then took it for a walk. ->
        # I fed all of her cats, then took them for a walk.
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(leaves)
        sentence_updated = False
        singular_pronouns = ['I','it','her','him','you']
        sentence_updated = False
        is_plural_noun = False

        for idx,i in enumerate(chunk.subtrees()):
            if i.label() == 'PS':
                for leaf in leaves:
                    if leaf[1] == 'NNS':
                        is_plural_noun = True
                    elif leaf[1] == 'NN':
                        is_plural_noun = False
            elif i.label() == 'VP':
                for x,leaf in enumerate(leaves):
                    if leaf[1] == 'PRP' and is_plural_noun and leaf[0] in singular_pronouns:
                        old_leaf = leaf
                        new_leaf = []
                        new_leaf.append('them')
                        new_leaf.append('PRP')
                        leaves[x] = new_leaf
                        sentence_updated = True
                        print("\033[91m",old_leaf,'\033[0m',' ----------> ','\033[92m',new_leaf,'\033[0m')
                    elif leaf[1] == 'PRP' and not is_plural_noun and leaf[0] not in singular_pronouns:
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
        else:
            print("No change detected")  

    def split_independent_clauses(chunk):
        print('\033[94mSPLITTING INDEPENDENT CLAUSES...\033[0m \n ')
        #eg. I went to the store I got milk and cookies  ->
        #I went to the store. I got milk and cookies.
        leaves = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(leaves)
        clauses_updated = False
        independent_clauses = []
        
        for subtree in chunk.subtrees():
            if subtree.label() == 'IC':
                pos_tokens = Optimizer.convert_leaves_to_tokens(subtree.leaves())
                sentence = Optimizer.reconstruct_sentence(pos_tokens)
                independent_clauses.append(sentence)
                clauses_updated = True
        
        if(clauses_updated):
            print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            print('\033[94m============INDEPENDENT CLAUSES============\033[0m \n ')     
            print(independent_clauses)               
        else:
            print("No change detected")  
        
    # def remove_redundant_apostrophes(chunk):
    #     redundant_apostrophes = Dictionary.Redundant_Apostrophes
    #     eg. The girls's soccer game was delayed by rain. ->
    #     The girls' soccer game was delayed by rain.

    # def capitalize_entities(chunk):
        #eg. germany won the match although portugal started very well -> Germany won the match although portugal started very well.

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

tree = nltk.tree.Tree.fromstring(""" (S
  (IC I/PRP am/VBP a/DT boy/NN)
  (IC I/PRP went/VBD to/TO the/DT shop/NN))""")

Optimizer.check_subject_verb_agreement(tree)