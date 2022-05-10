from flask import Flask, render_template, Response, request, redirect, url_for
import numpy as np
from numpy import random
import csv

app = Flask(__name__)

#import data
bigram_probabilities = {}
with open('static/bigram_probabilities.csv') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
    for row in csv_reader:
        key = (row[0],row[1])
        value = row[2]
        bigram_probabilities.update({key: value})

clubs = []
with open('static/club_titles.txt', encoding='utf-16') as f:
     for line in f:
        clubs.append(line)

#function to generate a new club name
def gen_bigram_club():
    output = ["*"]
    next_token = ""
    i = 1
    while next_token != 'STOP':
        current_history = output[i-1] #this is the previous word
        possible_bigrams = [(key, value) for key, value in bigram_probabilities.items() if key[0] == current_history] #bigrams that start with that word
        bigrams = [x[0] for x in possible_bigrams]
        bigrams = [x[1] for x in bigrams]
        probs = [x[1] for x in possible_bigrams]
        probs = [float(i) for i in probs]
        sprobs = np.sum(probs)
        probs = np.divide(probs,sprobs)
        if i == 1:
            #if it's the first word, pick it at random
            next_token = np.random.choice(np.array(bigrams), 1)[0]
        else:
            #otherwise, pick from the probability distribution of bigrams
            next_token = np.random.choice(np.array(bigrams), 1, p = np.array(probs))[0]
        output.append(next_token)
        i = i + 1
    output = output[1:-1] #remove start and stop symbols
    output = " ".join(output)
    if output in clubs:
        #if the club exactly matches an existing club, generate a new one
        output = gen_bigram_club()
    if len(output) == 1:
        output = gen_bigram_club()
    return output
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    club = gen_bigram_club()
    return render_template('index.html', forward_message=club);

if __name__ == "__main__":
    app.run(debug=True)