# -*- coding: utf-8 -*-
"""
Alex Carrizo
Final Project
Grad ML 2
"""

import nltk
import random  # used to generate random responses
import string  # used to remove punctuation

with open("MovieInput.txt", 'r') as myFile1:
    data1 = myFile1.read()

input_tokens = data1.split("@")

botID = "Top 10 Movie Bot: "

initialGreeting = ("Hello.  I am a top 10 movie bot.  I can give general information about Rotten Tomatoes' top 10 movies for the year 2018,2019, and 2020.  "
                   )
AskForYear = "Please enter a the year that you would like to read about(2018,2019,2020)."
AskForMovie = ("Which movie would you like to read about?"
               " If you want to choose a different year, enter change year")

normalResponse = "Which of the top 10 movies would you like to learn more about?"

confusedResponse = "I'm sorry please enter in a placement within the top 10."

change = ["change", "change year", "year", "switch", "switch year"]
greetings = ["hello", "hi", "greetings", "sup", "what's up", "hey", "howdy"]
greetingResponses = (["Greetings. What movie would you like to see",
                      "Hello. My top 10 list of movies is online. Which would you like?",
                      "Hey there. What movie would you like?"])

thanks = ["thanks", "thank you", "cool", "awesome"]
welcomeResponse = "You are most welcome."

goodbyes = ["bye", "goodbye", "later", "lates", "cya", "cyas", "peace"]
goodbyeResponse = "Take care and stay safe."

lemmer = nltk.stem.WordNetLemmatizer()  # used to consolidate different word forms


# returns cleaned list of consolidated tokens
def lemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


# different method for removing non-alphanumeric characters
def lemNormalize(text):
    return lemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



# checks to see if the input text matches one of the greeting_inputs.  If so,
# return one of the random greeting_responses.
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greetings:
            return random.choice(greetingResponses)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def response(user_response):
    bot_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=lemNormalize)
    tfidf = TfidfVec.fit_transform(input_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    with open(outputFilename, 'r') as myFile2:
        data2 = myFile2.read()
    out_text = data2.split("@")
    if (req_tfidf == 0):
        bot_response = bot_response + confusedResponse
        return bot_response
    else:
        bot_response = bot_response + out_text[idx]
        return bot_response

def GetMovieyear():
    file = " "

    print(botID + AskForYear)
    flag = True
    while flag == True:
        user_response = input(">>> ")
        if user_response == "2020":
            file = "MoviesOutput2020.txt"
            flag = False
        elif user_response == "2019":
            file = "MoviesOutput2019.txt"
            flag = False
        elif user_response == "2018":
            file = "MoviesOutput2018.txt"
            flag = False
        elif user_response in goodbyes or user_response in thanks:
            file = user_response
            flag = False
        else:
            print(botID + "I'm sorry I only have movies for 2018, 2019, and 2020, please try again")

    return file


flag = True


print("\n\n" + botID + initialGreeting)
outputFilename = GetMovieyear()
if outputFilename not in goodbyes or outputFilename not in thanks:
    print(botID + AskForMovie)
while (flag == True):
    if outputFilename in goodbyes or outputFilename in thanks:
        user_response = outputFilename
    else:
        user_response = input(">>> ")
    user_response = user_response.lower()
    if user_response not in goodbyes:
        if user_response in thanks:
            flag = False
            print(botID + welcomeResponse)
        elif user_response in change:
            outputFilename = GetMovieyear()
            print(botID + AskForMovie)
        else:
            if (greeting(user_response) != None):
                print(botID + greeting(user_response))
            else:
                input_tokens.append(user_response)
                print(botID, end="")
                print(response(user_response))
                input_tokens.remove(user_response)
    else:
        flag = False
        print(botID + goodbyeResponse)