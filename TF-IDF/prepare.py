# read the index.txt and prepare documents, vocab , idf

import chardet
import re

def find_encoding(fname):
    try:
        with open(fname, 'rb') as f:
            result = chardet.detect(f.read())
            charenc = result['encoding']
            return charenc
    except UnicodeDecodeError:
        return 'utf-8'

filename = 'Leetcode-Que-Scrapper\Questions-Data\Que_heading.txt'
my_encoding = find_encoding(filename)

with open(filename, 'r', encoding=my_encoding) as f:
    lines = f.readlines()
    print("length of lines: ",len(lines))
    #print(lines)

def preprocess(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    #terms = [term.lower() for term in document_text.strip().split()[1:] if term.isalnum()]
    #splits the document at each space and removes 1st split

    terms = []
    for term in document_text.strip().split()[1:]:
        term = re.sub(r'\W+', '', term.lower())
        if term.isalnum() and term != " ":
            terms.append(term)
    return terms

vocab = {} #dictionery of unique words(key) and their freq(value)
documents = []
for index, line in enumerate(lines):
    # read statement and add it to the line and then preprocess
    #tokens = preprocess(line)

    
    file_path = f'Leetcode-Que-Scrapper\Questions-Data\Que_description\{index+1}\{index+1}.txt'
    
    my_encoding2 = find_encoding(file_path)    
    with open(file_path,'r', encoding= my_encoding2 ) as file:
        file_contents = ''
        for line2 in file:
            if 'Example 1:' in line2:
                break
            file_contents += line2
        #print(line + file_contents)
        tokens = preprocess(line + file_contents)    
        #print(tokens)

    documents.append(tokens)
    #print("Documents :",documents)

    tokens = set(tokens) # freq added by "1 for each line" if word present once or many no. of time hence taken as set

    for token in tokens: 
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1
    print(index, 'done!!')

# reverse sort the vocab by the values
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents))
print('Size of vocab: ', len(vocab))
print('Sample document: ', documents[0])

# save the vocab in a text file
with open('G:\Algozenith\Web Dev\AZ-Hackathon\Project\TF-IDF\\tf-idf-data\\vocab.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)
        
    print("vocab file created!!")

# save the idf values in a text file
with open('G:\Algozenith\Web Dev\AZ-Hackathon\Project\TF-IDF\\tf-idf-data\idf-values.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])
    print("idf-values file created!!")

# save the documents in a text file
with open('G:\Algozenith\Web Dev\AZ-Hackathon\Project\TF-IDF\\tf-idf-data\documents.txt', 'w') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))
    print("documents file created!!")


inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
with open('G:\Algozenith\Web Dev\AZ-Hackathon\Project\TF-IDF\\tf-idf-data\inverted-index.txt', 'w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
    print("inverted index file creared!!")