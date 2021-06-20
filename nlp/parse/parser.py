from os import name
import nltk
from nltk import RegexpParser
import fileUtil as FileUtil
from ..optimize.optimizer import Optimizer
class Parser:

        def generate_parse_trees(pos_tokens_sentences, treeFileName):
            #Extract all parts of speech from any text 
            #RegexpParser 
            grammar = RegexpParser("""
                                IC: {<PRP> <V.*> <TO>? <DT>? <NN.*>? <CC>? <NN.*>? <V.*>?}
                                PS: {<PRP> <VBP> <DT>? <IN>? <PR.*> <NN.*>}
                                VP: {<RB>? <CC>? <V.*> <P.*> <IN> <DT> <NN.*>}          #To extract Verb Phrases
                                SV1: {<NN.*> <CC> <NN.*>}
                                SV2: {<NN.*> <CC>}
                                NP: {<DT>?<JJ.*>*<NN.*>+}   #To extract Noun Phrases
                                PP: {<IN> <NP>}              #To extract Prepositional Phrases
                                FW: {<FW>}                 #To extract Foreign Words
                                CD : {<CD>}                #To extract Cardinal Digits 
                                PRP: {<PRP.*>}              #To extract all Pronouns
                                """)

            # grammar2 = nltk.CFG.fromstring("""  <--------- CFG GRAMMAR USE CASE 
            # S -> NP VP
            # NP -> Det N | Det N PP | Det Adj
            # PP -> P NP
            # P -> 'PRP' | 'PRP$'
            # Det -> 'DT'
            # N -> 'NN' | 'NNS' | 'NNP' | 'NNPS'
            # V -> 'VB' | 'VBD' | 'VBG' | 'VBP' | 'VBZ'
            # Adj -> 'JJ' | 'JJR' | 'JJS'
            # """)

            # cfg_parser = nltk.ChartParser(grammar2)

        
            # for sentence in pos_tokens_sentences:
            #     pos_tags = [pos for (token,pos) in sentence]
            #     print(pos_tags)
            #     trees = cfg_parser.parse(pos_tags)
            #     for tree in trees:
            #         print(tree)

            extractions = []
            for x in pos_tokens_sentences:  #parse sentences one by one
                output = grammar.parse(x) 
                extractions.append(output)
                print("\033[94m Extraction result for sentence \033[0m \n", output)
            FileUtil.generate_tree_pdf(extractions, treeFileName)
        
        def parse(pos_tokens_sentences):
        #Extract all parts of speech from any text 
        #RegexpParser 
            grammar = RegexpParser("""
                                IC: {<PRP> <V.*> <TO>? <DT>? <NN.*>? <CC>? <NN.*>? <V.*>?}
                                PS: {<PRP> <VBP> <DT>? <IN>? <PR.*> <NN.*>}
                                VP: {<RB>? <CC>? <V.*> <P.*> <IN> <DT> <NN.*>}          #To extract Verb Phrases
                                SV1: {<NN.*> <CC> <NN.*>}
                                SV2: {<NN.*> <CC>}
                                NP: {<DT>?<JJ.*>*<NN.*>+}   #To extract Noun Phrases
                                PP: {<IN> <NP>}              #To extract Prepositional Phrases
                                FW: {<FW>}                 #To extract Foreign Words
                                CD : {<CD>}                #To extract Cardinal Digits 
                                PRP: {<PRP.*>}              #To extract all Pronouns
                                """)
            extractions = []
            for x in pos_tokens_sentences:  #parse sentences one by one
                output = grammar.parse(x) 
                extractions.append(output)
                print("\033[94m Extraction result for sentence \033[0m \n", output)
            return Optimizer.optimize_chunks(extractions)

        # def print_named_entities(pos_sentences):
        #     named_entities = []
        #     for sentence in pos_sentences:
        #         ne_tree = nltk.ne_chunk(sentence)
        #         print("\n\033[94m============Named Entity Tree============\033[0m \n", ne_tree)

        #         for tree in ne_tree:
        #             if hasattr(tree, 'label'):
        #                named_entities.append(tree.label() + ' - ' + ' '.join(attribute[0] for attribute in tree))
        #     print("\n\033[94m============Named Entities in Text============\033[0m \n", named_entities)
           
            

                
