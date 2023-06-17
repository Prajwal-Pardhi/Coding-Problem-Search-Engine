import math
from flask import Flask, render_template
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField

app = Flask(__name__ , static_url_path='/static')
app.template_folder = 'templates'

def load_vocab():
    vocab = {}
    with open('TF-IDF\tf-idf-data\vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
    with open('TF-IDF\tf-idf-data\idf-values.txt', 'r') as f:
        idf_values = f.readlines()
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open('TF-IDF\tf-idf-data\documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    #print('Number of documents: ', len(documents))
    #print('Sample document: ', documents[0])
    return documents

def load_inverted_index():
    inverted_index = {}
    with open('TF-IDF\tf-idf-data\inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    #print('Size of inverted index: ', len(inverted_index))
    return inverted_index

def load_Qindex():
    q_links = []
    with open('Leetcode-Que-Scrapper\Questions-Data\Que_links.txt', 'r') as f:
        q_links = f.readlines()
    #q_links = [each_link.strip().split() for each_link in q_links]
    return q_links

def load_index():
    q_headings = []
    with open('Leetcode-Que-Scrapper\Questions-Data\Que_heading.txt', 'r') as f:
        q_headings = f.readlines()
    #q_headings = [each_head.strip().split()[1:] for each_head in q_headings]

    return q_headings


vocab_idf_values = load_vocab() #dict (word: no. of documents in which 'word' is present)
documents = load_documents() #list [['a','b',...for each document1],['a2','b2',...for docu2],[...],...]
inverted_index = load_inverted_index() #dict (word:[indexes of documents in which it present])
que_links = load_Qindex() #list of question links
que_heading = load_index() #list of question headings


def get_tf_dictionary(term):
    tf_values = {} #dict {document index : frequency of term in that document/toal no. of words in that document}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)]) #def of tf value
    
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term]) #def of idf value

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    result = []

    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        #print(term,tf_values_by_document,idf_value)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            else: potential_documents[document] += tf_values_by_document[document] * idf_value
    len(potential_documents)
    if(len(potential_documents) == 0):
        print("No matching question found, try some relevent words")
        return []
    
    #print(potential_documents)
    # divite by the length of the query terms
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))


    for document_index in potential_documents:
        #print('Document: ', documents[int(document_index)], ' Score: ', potential_documents[document_index])
        #print('Document Heading: ', que_heading[int(document_index)],
        # 'Document link: ',que_links[int(document_index)], 
        # ' Score: ', potential_documents[document_index])
        heading = que_heading[int(document_index)].split()
        new_heading = ' '.join(heading[1:])

        result.append( {"Question heading": new_heading ,
                        "Question link": que_links[int(document_index)], 
                        "Score":potential_documents[document_index] } )
        
    return result[:20:]

#query_string = input('Enter your query: ')
#query_terms = [term.lower() for term in query_string.strip().split()]

#print(query_terms)
#result = calculate_sorted_order_of_documents(query_terms)
#print(result)

app.config['SECRET_KEY'] = 'prajwal_key'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')

@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms)[:20:])
 
@app.route("/",methods = ['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query_string = form.search.data
        query_terms = [term.lower() for term in query_string.strip().split()] 
        results = calculate_sorted_order_of_documents(query_terms)[:20:]
        #print(results)
    return render_template('index.html',form = form, results = results )
