# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# _____helper Libraries_____
import csv
import json
import timeit
import random

def get_main_response(test_set_sentence, minimum_score , json_file_path):

    test_set = (test_set_sentence, "")

    tfidf_vectorizer , tfidf_matrix_train = train_bot(json_file_path)

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)

    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0
    if (max > minimum_score):
        new_max = max - 0.01
        list = np.where(cosine > new_max)
        # print ("number of responses with 0.01 from max = " + str(list[0].size))
        print("NUMBER OF POSSIBLE RESPONSES: " + str(len(list)))
        response_index = random.choice(list[0])
    else :
        return "Sorry, I didn't learn how to respond to that." , 0


    j = 0

    with open(json_file_path, "r") as sentences_file:
        reader = json.load(sentences_file)
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            if j == (response_index):
                return row["response"], max
                break


def train_bot(json_file_path):
        i = 0
        sentences = []
        sentences.append("No you. ")
        sentences.append("No you. ")

        start = timeit.default_timer()

        with open(json_file_path, "r") as sentences_file:
            reader = json.load(sentences_file)
            for row in reader:
                sentences.append(row["message"])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization

        stop = timeit.default_timer()
        # print ("Training time was: ")
        # print (stop - start)
        return tfidf_vectorizer , tfidf_matrix_train


def get_bot_response(query, datasetChoice):
    minimum_score = 0.7
    file = "human_mode_data.json"
    if(datasetChoice == 1):
        file = "movie_mode_data.json"
    else:
        file = "human_mode_data.json"
    query_response, score = get_main_response(query , minimum_score , file)
    # print("======SCORE: ", score)
    final_response = "[BOT]: "+ str(query_response)
    return final_response

datasetChoice = 2
while True:
    print("Hello there, I'm currently trained to work with two modes.")
    print("1- Movie line response, the one you choose when you\'re bored. You will be surprised!")
    print("2- Actual human mini-conversations. *screams BOOORING...*")
    datasetChoice = int(input("Choose your mode(1 OR 2): "))
    print("==========================================================")
    if(datasetChoice in [1,2]): # check if entered value is correct.
        break

while True:
    sent = input("[USER]: ")
    print(get_bot_response(sent, datasetChoice))
