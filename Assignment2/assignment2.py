import string
import re
import csv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize


PUNCT = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

#Assuming data.csv contains tweet_id,tweet,user_id info respectively in csv

data_file = "data.csv"
datasheet_file = "Datasheet.csv"
output_file = "output.csv"
input_file = "input.txt"

def get_ratios(tuples):
    data = []
    en = 0
    total = 0
    hi = 0

    for i in range(1, len(tuples)) :
        r = tuples[i].split(':')
        end = int(r[1])
        count = 1
        start = int(r[0])
        word_type = str(r[2])
        data.append((start,end,word_type))
        
        if word_type == 'HI' :
            hi+= count
        elif word_type == 'EN':
            en+=count
        #total = total + 1
    total=en+hi
    en_ratio = float(en)/float(total)
    hi_ratio = float(hi)/float(total)
    return en_ratio,hi_ratio,data 

def read_data(file):
    tweet_types = {}
    meta = {}
    with open(file,'r') as f:
        for x in f:
            tuples=x.split(',')
            t='None'
            en_ratio,hi_ratio,meta[tuples[0]] = get_ratios(tuples)            
            if en_ratio>.9:
                t='EN'
            elif en_ratio == .5:
                t='CMEQ'      
            elif en_ratio > .5:
                t='CME'          
            elif hi_ratio > .9:
                t='HI'
            elif hi_ratio > .5:
                t='CMH'
            tweet_types[tuples[0]]= t
    return (tweet_types, meta)

def get_tweet_dict(file):
    filtered={}
    with open(file,'r') as f:
        csvReader = csv.reader(f, delimiter=',')
        for t_id,tweet,_ in csvReader:
            filtered_words = []
            for s,e,t in meta[t_id]:
                word = tweet[s-1:e]

                # Heuristic Condition 1
                hi_stopword = "main"

                if t=='HI' and word.lower().startswith(hi_stopword):
                    continue

                filtered_words.append(word)
            filtered[t_id]=' '.join(filtered_words)
        return filtered  



def tokenize(text):
    punc_removed = []
    lowercased = []
    tokens = word_tokenize(re.sub('[^A-Za-z0-9]+', ' ', text))
    for t in tokens:
        lowercased.append(t.lower())
    for word in lowercased:

        processedWord = []
        for letter in word:
            if letter in PUNCT:
                continue
            processedWord.append(letter)
        punct_removed = ''.join(processedWord)

        punc_removed.append(punct_removed)
    
    stopwords_removed = []
    for w in punc_removed:
        if w in STOPWORDS:
            continue
        stopwords_removed.append(w)

    stemmed = []
    for w in stopwords_removed:
        stemmed.append(STEMMER.stem(w))

    return [w for w in stemmed if w]


def read_stemmed_words(file):
    stemmed_words = []
    key_words = []
    with open(file,'r') as f:
        csvReader = csv.reader(f)
        for key_word, in csvReader:
            key_words.append(key_word)
            stemmed_words.append(tokenize(key_word)[0])
        
        return stemmed_words,key_words


def get_required_hashes(file):
    key_hashes=set()
    with open(file,'r') as f:
        csvReader = csv.reader(f, delimiter=',')
        for t_id,tweet,u_id in csvReader:
            hash_tags = []
            words = tweet.split(" ")
            for word in words:
                if word.startswith('#'):
                    word = word.lower()
                    hash_tags.append(word)
                
            if len(hash_tags)!=0:
                words = tokenize(tweet)
                for word in words:
                    if word in stemmed_words:
                        for hash_tag in hash_tags:
                            key_hashes.add(hash_tag)
                        break
    return key_hashes



tweet_types,meta = read_data(datasheet_file)
filtered  = get_tweet_dict(data_file)
stemmed_words,key_words = read_stemmed_words(input_file)
key_hashes = get_required_hashes(data_file)

def contains_hash(tweet):
    words = tweet.split(" ")
    for word in words:
        if(word.startswith('#')) and word in key_hashes:
            return True
    return False

def get_matrices(datafile):
    word_user_data = {}
    word_tweets_data = {}
    with open(datafile, 'r') as f:
        csvReader = csv.reader(f, delimiter=',')
        for t_id,tweet,u_id in csvReader:
            tweet_type = tweet_types[t_id]

            # Heuristic Condition 2
            skip_types = ['HI', 'CMH']       
            if tweet_type not in skip_types and contains_hash(tweet) == False:
                continue
            
            words = tokenize(filtered[t_id])
            
            for word in words:
                if word in stemmed_words :
                    
                    if word not in word_user_data:
                        word_user_data[word] = {}                    
                    if tweet_type in word_user_data[word]:
                        word_user_data[word][tweet_type].add(u_id)
                    else:
                        word_user_data[word][tweet_type] = set([u_id])
                        
                    if word not in word_tweets_data:
                        word_tweets_data[word] = {}                    
                    if tweet_type in word_tweets_data[word]:
                        word_tweets_data[word][tweet_type].add(t_id)
                    else:
                        word_tweets_data[word][tweet_type] = set([t_id])

    return word_user_data, word_tweets_data

word_user_data, word_tweets_data = get_matrices(data_file)

def get_unique_ratio(counts):
    en = 1
    hi = 0
    cmh = 0

    if 'EN' in counts:
        en = len(counts['EN'])
    if 'HI' in counts:
        hi = len(counts['HI'])
    if 'CMH' in counts:
        cmh = len(counts['CMH'])

    ratio = (1.0*(hi+cmh)/en)
    return ratio

user_metric = {}
for word,type_counts in word_user_data.items():
    user_metric[word] = get_unique_ratio(type_counts)

tweet_metric = {}
for word,type_counts in word_tweets_data.items():
    tweet_metric[word] = get_unique_ratio(type_counts)

a = 0
b = 0
final_ranks = []
for key_word in key_words:
    try:
        final_metric = (user_metric[tokenize(key_word)[0]]+tweet_metric[tokenize(key_word)[0]])/2.0
        final_ranks.append((key_word,final_metric))
        a=a+1
    except:
        b=b+1


sorted_final_list = sorted(final_ranks,key=lambda l:l[1],reverse=True)
final_word_rank_list = [(s[0],s[1]) for s in sorted_final_list]

for i in final_word_rank_list:
    print i

with open(output_file,'w') as f:
    csvWriter = csv.writer(f)
    csvWriter.writerows([(data[0],i+1) for i,data in enumerate(final_word_rank_list)])