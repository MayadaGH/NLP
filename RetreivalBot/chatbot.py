#import nltk
import numpy as np
import random
import json
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
# Checking for greetings
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
file = "movie_mode_data.json"

questions = []
answers = []
minimum_score = 0.7
ending = re.compile(r".*bye.*")
def get_response(user_message):
    TFvectorizer= TfidfVectorizer()  
    X= TFvectorizer.fit_transform(questions)
    return response(user_message,TFvectorizer,X)
    
def train_message(test_message,TFvectorizer):
    test_vector = TFvectorizer.transform([test_message])
    return test_vector

def response(message,TFvectorizer,array):
    test_vector = train_message(message,TFvectorizer)
    j = 0
    cosine = cosine_similarity(array, test_vector)
    most_sim = cosine.max()
    if (most_sim > minimum_score):
        new_max = most_sim - 0.01
        list = np.where(cosine > new_max)
        response_index = random.choice(list[0])
    else : return "I Don't Recognize your Message"
    
    while(j != response_index):
        j+=1

    return answers[j]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "that is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    return text

def reading_data():
    with open(file, "r") as sentences_file:
        reader = json.load(sentences_file)
        for read in reader:
            questions.append(clean_text(read['message']))
            answers.append(clean_text(read['response']))
    
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def main():
    reading_data()
    flag=True
    print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
    while(flag==True):
        user_response = input()
        user_response_lower = user_response.lower()
        if(not re.search(ending,user_response_lower)):
            if(user_response_lower =='thanks' or user_response_lower=='thank you' ):
                print("ROBO: You are welcome..")
            else:
                if(greeting(user_response)!=None):
                    print("ROBO: "+greeting(user_response))
                else:
                    print("ROBO: ",end="")
                    print(get_response(clean_text(user_response)))
        else:
            flag=False
            print("ROBO: Bye! take care..") 


main()
