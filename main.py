from flask import Flask, render_template, Response, request, redirect, url_for
import numpy as np
from numpy import random
import csv

app = Flask(__name__)

nums = []
with open('static/nums.csv') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
    for row in csv_reader:
        row = "".join(row)
        nums.append(row)

bigram_probabilities = {}
with open('static/bigram_probabilities.csv') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
    for row in csv_reader:
        key = (row[0],row[1])
        value = row[2]
        bigram_probabilities.update({key: value})

tokenized_courses = []
with open('static/tokenizedcourses.csv') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
    for row in csv_reader:
        tokenized_courses.append(row)

def gen_bigram_course():
    output = ["*"]
    next_token = ""
    i = 1
    while next_token != 'STOP':
        current_history = output[i-1]
        possible_bigrams = [(key, value) for key, value in bigram_probabilities.items() if key[0] == current_history]
        bigrams = [x[0] for x in possible_bigrams]
        bigrams = [x[1] for x in bigrams]
        probs = [x[1] for x in possible_bigrams]
        sprobs = np.sum(probs)
        probs = np.divide(probs,sprobs)
        if i == 1:
            next_token = choice(np.array(bigrams), 1)[0]
        else:
            #next_token = choice(np.array(bigrams), 1)[0]
            next_token = choice(np.array(bigrams), 1, p = np.array(probs))[0]
        #look back 2, choose bigram based on distribution of bigrams with those first two words in common
        output.append(next_token)
        i = i + 1
    output = output[1:-1] #remove stop
    if output in tokenized_courses:
        #print("dupe:", output)
        output = gen_bigram_course()
    return output
        
def put_course_name_together(output):
    new_name = " ".join(output)
    new_name = new_name.replace(" ,",",")
    new_name = new_name.replace(" :",":")
    new_name = new_name.replace(" ?","?")
    num = choice(nums,1)[0]
    new_name = "MGT " + num + " " + new_name 
    return new_name

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    output = gen_bigram_course()
    course = put_course_name_together(output)
    return render_template('index.html', forward_message=forward_message);

if __name__ == "__main__":
    app.run(debug=True)