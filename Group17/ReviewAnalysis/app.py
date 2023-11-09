from flask import Flask, render_template, jsonify, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/text')
def text():
    return render_template('text.html')

@app.route('/file')
def file():
    return render_template('file.html')

@app.route('/file/evaluate/', methods=['POST'])
def evaluateFile():
    file = request.files['file']

    lines = file.readlines()
    count = 0
    # Strips the newline character

    result = " <div class='progress'> " \
    "   <div class='progress-bar bg-success' role='progressbar' style='width: {$$success_val$$}%' aria-valuemin='0' aria-valuemax='100'></div>" \
    "   <div class='progress-bar bg-danger' role='progressbar' style='width: {$$negative_val$$}%' aria-valuemin='0' aria-valuemax='100'></div>" \
    "   <div class='progress-bar bg-warning' role='progressbar' style='width: {$$nutral_val$$}%' aria-valuemin='0' aria-valuemax='100'></div>" \
    " </div> <br /> <br /> " \
    " <table class='table'><thead> " \
             "<tr> " \
             "<th scope='col'>#</th> " \
             "<th scope='col'>Sentence</th> " \
             "<th scope='col'>Evaluation</th>" \
             "</tr></thead><tbody>"
    positive = 0
    negative = 0
    nutral = 0
    for line in lines:
        count += 1
        strs = line.decode()
        evaltext = strs.split(',')
        #print("Line{}: {}".format(count, evaltext[3]))

        blob = TextBlob(evaltext[2])

        sentence_scores = {}
        for sentence in blob.sentences:
            sentence_text = sentence.raw
            sentence_score = calculate_sentence_score(sentence_text)
            sentence_scores[sentence_text] = sentence_score

        for sentence, score in sentence_scores.items():
            result = result + "<tr><td>" + str(count) + "</td><td>" + sentence + "</td>"
            if score == 0.0:
                result = result + "<td style='background-color:yellow;'> Neutral </td></tr>"
                nutral += 1
            elif score < 0.0:
                result = result + "<td style='background-color:red;'> Negative </td></tr>"
                negative += 1
            else:
                result = result + "<td style='background-color:green;'> Positive </td></tr>"
                positive += 1

    negPer = (negative / count) * 100
    posPer = (positive / count) * 100
    nutPer = (nutral / count) * 100
    result = result + "</tbody></table>"

    result = result.replace("{$$success_val$$}", str(posPer)).replace("{$$negative_val$$}", str(negPer)).replace("{$$nutral_val$$}", str(nutPer))

    return result


@app.route('/text/evaluate/')
def evaluate():
    usertext = request.args.get('usertext')
    print(usertext)
    blob = TextBlob(usertext)

    # Dictionary to store sentence and its sentiment score
    sentence_scores = {}
    for sentence in blob.sentences:
        sentence_text = sentence.raw
        sentence_score = calculate_sentence_score(sentence_text)
        sentence_scores[sentence_text] = sentence_score

    result = "<table class='table'><thead> " \
             "<tr> " \
             "<th scope='col'>#</th> " \
             "<th scope='col'>Sentence</th> " \
             "<th scope='col'>Evaluation</th>" \
             "</tr></thead><tbody>"
    sno = 0
    for sentence, score in sentence_scores.items():
        sno = sno + 1
        result = result + "<tr><td>"+ str(sno) +"</td><td>" + sentence + "</td>"
        if score == 0.0:
            result = result + "<td style='background-color:yellow;'> Neutral </td></tr>"
        elif score < 0.0:
            result = result + "<td style='background-color:red;'> Negative </td></tr>"
        else:
            result = result + "<td style='background-color:green;'> Positive </td></tr>"
    result = result + "</tbody></table>"
    return result

def calculate_sentence_score(sentence):
    """Calculates the sentiment score of a sentence.
    Args:
        sentence (str): The sentence to calculate the sentiment score for.
    Returns:
        float: A number between -1 and 1 that represents the sentiment of the sentence.
    """
    # Create a TextBlob object for the sentence.
    blob = TextBlob(sentence)

    # Calculate the sentiment score for the sentence.
    sentence_score = blob.sentiment.polarity
    return sentence_score

if __name__ == "__main__":
    app.run(debug=True)
