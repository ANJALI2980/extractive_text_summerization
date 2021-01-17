import pandas as pd 
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from rouge import FilesRouge
from nltk.stem import WordNetLemmatizer 
stopwords = stopwords.words("english")
def build_count(df):
    total = len(df)
    yes = df.apply(lambda x: True if 1 in list(x) else False, axis=1)
    total_yes = len(yes[yes == True].index)
    no = df.apply(lambda x: True if 0 in list(x) else False, axis=1)
    total_no = len(no[no == True].index)
    vocab = []
    vocabs = []
    for (sent) in df['SENTENCE']:
        vocabs=(word_tokenize(sent))
        for word in vocabs:
             word=word.lower()
             if word.isalpha():
                 if word not in stopwords:
                     if len(word)>=1:
                         vocab.append(wnl.lemmatize(word,pos="v"))
    return vocab,total,total_yes,total_no
def feauter_count(df,i):
    words=[]
    word=[]
    for (sent,j) in zip(df['SENTENCE'],df['VALUE']):
        if(j==i):
            word=(word_tokenize(sent))
            for w in word:
                w=w.lower()
                if w.isalpha():
                    if w not in stopwords:
                        if len(w)>=1:
                            words.append(wnl.lemmatize(w,pos="v"))
    return(words)
def train(vocab,yes_words,no_words):
    feauters = {}
    feauters['yesfeauter']={}
    feauters['nofeauter']={}
    for word in vocab:
        feauters['yesfeauter'][word]= (yes_words.count(word)+1)/(len(yes_words)+len(vocab))
    for word in vocab:
        feauters['nofeauter'][word]= (no_words.count(word)+1)/(len(no_words)+len(vocab))
    return feauters
def test(text,yes_prior,no_prior,feauters,total,total_yes,total_no):
    summery = []
    test_words=[]
    test_word = []
    smooth_yes = (1/(total_yes+total))
    smooth_no = (1/(total_no+total))
    sents = sent_tokenize(text)
    for s in sents:
        print(s+"\n")
        test_word = []
        test_words=(word_tokenize(s))
        #print(test_words)
        for word in test_words:
            word=word.lower()
            if word.isalpha():
                if word not in stopwords:
                    test_word.append(wnl.lemmatize(word,pos="v"))
        #print(test_word)
        yes=yes_prior
        #print(yes)
        no=no_prior
        #print(no)
        #print(feauters['yesfeauter'])
        for w in test_word:
            if w in feauters['yesfeauter']:
                yes=yes*feauters['yesfeauter'][w]
                #print(w+'yes')
                #print(yes)
            else:
                yes=yes*smooth_yes
                #print(w+'yes')
                #print(yes)
            if w in feauters['nofeauter']:
                no=no*feauters['nofeauter'][w]
                #print(w+'no')
                #print(no)
            else:
                no=no*smooth_no
                #print(w+'no')
                #print(no)
        #print('yes=',yes)
        #print('no=',no)
        if (yes>no):
            summery.append(s)
        #    print("yes")
        #else:
        #    print("m")
    return summery
if __name__=="__main__":
    df=pd.read_excel(r"C:\Users\user\Downloads\nlp_dataset.xlsx")
    outputsum=open('Downloads\outputsum.txt','w+')
    
    wnl = WordNetLemmatizer()
    vocab,total,total_yes,total_no=build_count(df)
    v=len(vocab)
    yes_words=feauter_count(df,1)
    yes_count=len(yes_words)
    no_words=feauter_count(df,0)
    no_count=len(no_words)
    yes_prior=total_yes/total
    no_prior=total_no/total
    feauters=train(vocab,yes_words,no_words)
    text_file = open(r"C:\Users\user\Downloads\samp.txt")
    text = text_file.read()
    summery=test(text,no_prior,yes_prior,feauters,total,total_yes,total_no)
    for s in summery:
        outputsum.write(s)
    outputsum.close()
    print(summery)
files_rouge = FilesRouge()   //evaluation of model
scores = files_rouge.get_scores(r"C:\Users\user\Downloads\outputsum.txt",r"C:\Users\user\Downloads\ref_sum.txt", avg=True)
scores
