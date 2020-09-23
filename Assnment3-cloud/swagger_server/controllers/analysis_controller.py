import connexion
import six
import json
import re

from swagger_server.models.result import Result  # noqa: E501
from swagger_server import util

def get_location(body=None):  # noqa: E501
    """Calculate

    Post text to generate array indexes # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes

    :rtype: Result
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501

    concordance_operation = ConcordanceOperation(body)
    response, code = concordance_operation.get_location()

    return response, code

class ConcordanceOperation:
    def __init__(self, body):
        self.body = body

    def get_location(self):

        try:
            concordance = []
            indexes = [] 
            store_indexes = []
            j_index = []
            counts = dict()

            #Getting input
            request_str = self.body.decode('utf-8')
  
            #Removing punctuation in string using regex
            request_str = re.sub(r'[^\w\s]', '', request_str)

            lower_str = request_str.lower()
            words = lower_str.split(" ")
            
            #This for loop loops through "words" to fine location indexes
            for i in range(0, len(words)):
                indexes.append(i)
                for j in range(i+1, len(words)):
                    if(words[i] == words[j]):
                        indexes.append(j)
                        j_index.append(j)
                       
                store_indexes.append(indexes)
                       
                indexes = []

            #Remove duplicate indexes
            for index1 in j_index:
                inte = [index1]
                print(store_indexes.remove(inte))
            
            #This is to count the number of tokens
            for word in words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            
            #Update the value pair to location arrays
            for i, item in enumerate(counts.items()):
                counts[item[0]] = store_indexes[i]
           
            #Sort alphabetically
            counts.sort()

            for pair in counts.items():
                word_counts = {"token": pair[0], "location": pair[1]}
                concordance.append(word_counts)

            #Sending response to the server
            response, code = {
                "concordance": concordance,
                "input": request_str
            }, 200

        except Exception as error:
            response, code = {
                                 "error": repr(error),
                             }, 400
        return response, code






