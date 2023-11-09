from textblob import TextBlob


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

1

if __name__ == '__main__':
    text = '''
        I.
        The ambience was good,food was quite good,had Saturday lunch,which was cost effective.
        Good place for a sate brunch.One can also chill with friends and or parents.
        Thnx for the service by Pradeep and Subroto,My personal recommendation is Penne Alfredo Pasta:)
        Ambiance is good, service is good- food is a Pradeecp and subro best service.
        Kebab was tasty also the service was very prompt the staff was very courteous too,Kunal catered to all our needs and saw it to it we had a good time, must visit place for all biryani lovers!!
        Nice restaurant with friendly and courteous staff and variety of options to choose from.The curry and raita are really good.There are some good options for veggies also that they can try.
        It costed 400 bucks each and receiving the same 200 bucks biryani has been my worst experience.
        '''

    # Create a TextBlob object for the entire text.
    blob = TextBlob(text)

    # Dictionary to store sentence and its sentiment score
    sentence_scores = {}
    for sentence in blob.sentences:
        sentence_text = sentence.raw
        sentence_score = calculate_sentence_score(sentence_text)
        sentence_scores[sentence_text] = sentence_score

    # Print the sentence and its sentiment score
    for sentence, score in sentence_scores.items():
        print("Sentence:", sentence)
        print("Sentiment Score:", score)
        if score == 0.0:
            print("Statement is neutral")
        elif score < 0.0:
            print("Statement is negative")
        else:
            print("Statement is positive")
        print()
