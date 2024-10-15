# let's import the flask
from flask import Flask, render_template, request, redirect, url_for
import os
from collections import Counter
import string

app = Flask(__name__)
# to stop caching static files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/') # this decorator create the home route
def home ():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    name = 'Python Text Analyzer'
    return render_template('home.html', techs = techs, name = name, title = 'Home')

@app.route('/about')
def about():
    name = '30 Days of Python Programming'
    return render_template('about.html', name = name, title = 'About Us')

def analyze_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    num_of_words = len(words)
    num_of_chars = len(text)
    word_counts = Counter(words)
    most_frequent_words = word_counts.most_common(1)[0]
    unique_words = len(set(words))
    lexical_density = unique_words / num_of_words if num_of_words > 0 else 0

    all_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    return {
        "num_of_words": num_of_words,
        "num_of_chars": num_of_chars,
        "most_frequent_words": most_frequent_words,
        "lexical_density": lexical_density,
        "all_word_counts": all_word_counts
    }

@app.route('/post', methods=['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
         return render_template('post.html', name = name, title = name)
    if request.method =='POST':
        content = request.form['content']
        analysis = analyze_text(content)
        print(content)
        return render_template('result.html', analysis=analysis)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    # for deployment we use the environ
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 