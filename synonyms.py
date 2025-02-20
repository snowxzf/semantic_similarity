import math
import re

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def dict_to_list(v):
    L=[]
    for key, value in v.items():
        L.append(value)
    return L
def common_words(v1, v2):
    com=[]
    for key, value in v1.items():
        for key1, value1 in v2.items():
            if key == key1:
                com.append(key)
    return com
def cosine_similarity(vec1, vec2):
    '''The similarity function takes in two sparse vectors stored as dictionaries and returns a float. An example of such
a function is cosine_similarity. If the semantic similarity between two words cannot be computed, it is
considered to be −1. '''
    list1=dict_to_list(vec1)
    list2=dict_to_list(vec2)
    com_words = common_words(vec1, vec2)
    cos_val = 0
    if len(com_words) == 0:
        return 0
    else:
        for i in range(len(com_words)):
            cos_val+= (vec1[com_words[i]]*vec2[com_words[i]])/((square_comp(vec1)*square_comp(vec2))**0.5)

    return cos_val

###here
    '''if len(com_words) >= 0:
        for i in range(len(com_words)):
            cos_val+= (vec1[com_words[i]]*vec2[com_words[i]])/((square_comp(vec1)*square_comp(vec2))**0.5)
        return cos_val
    else:
        return -1'''

def square_comp(v):
    sum =0
    for key, values in v.items():
        sum+=values**2
    return sum

def per_sentence_dict(sentence):
    d_main={}
    for word in sentence:
        if not word in d_main:
            d_main[word] = {}
        d_perword = {}
        for word2 in sentence:
            if word == word2:
                pass
            #setence = dog cat cat
            elif not word2 in d_perword:
                d_perword[word2]=1
            else:
                d_perword[word2]+=1
        if d_main[word] == {}:
            d_main[word] = d_perword
    return d_main
print(per_sentence_dict(["cat", "cat", "dog", "cat", "dog"]))
def build_semantic_descriptors(sentences):
    sentence_dict = {}
    words_count = {}
    for sentence in range(len(sentences)):
        sentence_dict[sentence] = per_sentence_dict(sentences[sentence])
    for sentence_num, dicts in sentence_dict.items():
        for words, sentence_count in dicts.items():
            if not words in words_count:
                words_count[words] = sentence_count
            else:
                for subwords, counts in sentence_count.items():
                    if not subwords in words_count[words]:
                        if subwords!= words:
                            words_count[words][subwords] = 1
                    else:
                        words_count[words][subwords] +=1
    return  words_count

def build_semantic_descriptors_from_files(filenames):
    '''takes a list of filenames of strings w the names of files, returns dictionary of semantic descriptors of all words in filenames
     first one can be opened using open(filenames[0], "r", encoding="latin1")), and returns  a dictionary of semantic descriptors of words in the files filenames, w  files treated as a single text.
     assume that the following punctuation always separates sentences: ".", "!", "?", and that
is the only punctuation that separates sentences.
    Assume that only the following punctuation is present in the texts: [",", "-", "--", ":", ";"]'''
    sentences=[]
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            content = file.read()
        raw_sentences = re.split(r'[.!?...]', content)

        for sentence in raw_sentences:
            cleaned_sentence = re.sub(r'[",\-–:;]', ' ', sentence).lower().strip()
            words = cleaned_sentence.split()
            if words:
                sentences.append(words)
    semantic_descriptors = build_semantic_descriptors(sentences)
    return semantic_descriptors



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''takes in a string word, a list of strings choices, and a dictionary semantic_descriptors(built according to the requirements for build_semantic_descriptors), and returns the element of choices w the largest semantic similarity to word
    the semantic similarity is computed using the data in semantic_descriptors and the similarity function similarity_fn.
    In case of a tie between several elements in choices, the one with the smallest indexin choices should be returned (e.g., if there is a tie between choices[5] and choices[7], choices[5] is
returned).'''
    dict_choices = {}
    max_sim = -10000
    word_1dicts = {}
    word_ogdicts={}
    sim=0
    same_word=[]
    print("word:", word)
    print("choices:", choices)
    for words, dicts in semantic_descriptors.items():
        if word == words:
            word_ogdicts = dicts
            print(word, "og word dicts:", word_ogdicts)
    print("semantic descriptors:", semantic_descriptors)
    for word1 in choices:
        for words, dicts in semantic_descriptors.items():
            if word1==words:
                word_1dicts = dicts
                print(word1, "dicts:", word_1dicts)
        if similarity_fn(word_1dicts, word_ogdicts) == 0:
            sim = -1
        else:
            sim = similarity_fn(word_1dicts, word_ogdicts)
        dict_choices[word1] = sim
    print(dict_choices)
    for words, sims in dict_choices.items():
        if sims>max_sim:
            max_sim = sims
    for words, sims in dict_choices.items():
        if max_sim == sims:
            same_word.append(words)
    print("same words:", same_word)
    print("max word:", same_word[0])
    return same_word[0]

some_texts = build_semantic_descriptors_from_files(["war_and_peace.txt", "swan_lake.txt", "prideandprejcopy.txt", "picdoriangray.txt", "acotar.txt", "1984.txt", "crimeandpun.txt", "frank.txt", "fourthwing.txt", "beemovie.txt", "hamlet.txt"])

def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    ans = open(filename, "r", encoding="latin1").read().split("\n")
    split_ans = []
    num = 0
    for i in range(len(ans)):
        split_ans.append(ans[i].split(" "))
    for questions in range(len(split_ans)):
        choices = []
        for words in range(len(split_ans[questions])):
            if words == 1 or words == 0:
                pass
            else:
                choices.append(split_ans[questions][words])
        comp_ans = most_similar_word(split_ans[questions][0], choices, semantic_descriptors, similarity_fn)
        if comp_ans != split_ans[questions][1]:
            num +=0
        else:
            num+=1
    denom = len(split_ans)
    return (num/denom)*100
