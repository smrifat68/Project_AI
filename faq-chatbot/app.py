import json
import nltk
import string
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab') # Sometimes required in newer versions
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

# Load FAQ data
with open('faqs.json', 'r') as f:
    faq_data = json.load(f)

questions = [item['question'] for item in faq_data]
answers = [item['answer'] for item in faq_data]

lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def get_bot_response(user_input):
    bot_response = ''
    # Add user input to the list of questions temporarily
    questions.append(user_input)
    
    # Create TF-IDF Vectors
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(questions)
    
    # Calculate Cosine Similarity between user input (last item) and FAQs
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    
    # Find the index of the highest similarity
    idx = vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-1]

    # Cleanup: remove user input from questions list for the next turn
    questions.pop()

    if req_tfidf == 0:
        bot_response = "I am sorry, I don't understand that. Could you rephrase?"
    else:
        bot_response = answers[idx]
        
    return bot_response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["msg"]
    response = get_bot_response(user_msg)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)