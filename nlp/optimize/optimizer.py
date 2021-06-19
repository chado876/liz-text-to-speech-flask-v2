
class Optimizer:

    def optimize_chunks(chunks):
        print("Chunks:", chunks)
        for chunk in chunks:
            # chunk_sentence = ' '.join([w for w, t in chunk.leaves()]) convert chunk back to original string
            # print("Chunk Sentence:", chunk_sentence)

            chunk_leaves = chunk.leaves() #this functions provides us with a list of tokens from the chunk with their POS
            print("Chunk leaves", chunk_leaves)
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
    
    # def check_subject_verb_agreement(chunk):
    #     #eg. Anna and Mike is going skiing. -> Anna and Mike are going skiing.
    
    # def remove_pronoun_errors(chunk):
    #     #eg. I fed all of her cats, then took it for a walk. ->
    #     # I fed all of her cats, then took them for a walk.

    # def split_run_on_sentences(chunk):
    #     #eg. I went to the store I got milk and cookies ->
    #     #I went to the store. I got milk and cookies.
        
    # def remove_redundant_apostrophes(chunk):
    #     #eg. The girls's soccer game was delayed by rain. ->
    #     #The girls' soccer game was delayed by rain.

    # def capitalize_entities(chunk):
    #     #eg. germany won the match although portugal started very well -> Germany won the match although portugal started very well.