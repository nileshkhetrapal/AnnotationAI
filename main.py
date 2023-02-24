#The goal of this script is to create a Json for each link in the input.
#The Json will contain the following information:
#1- The link
#2- The name of the website
#3- Each line from the article
#4- The date of the article
#5- The author of the article
#6- The Code for the line:
#   0: The line does not match any code
#   1:Economy/Money/Finance/Trade/GDP
#   2:Trust/Stability/Security/Peace
#   3:Violence/Conflict/Protest
#   4:Unity/Cooperation/Alliance
#   5:Change/ Reform/Revolution
#   6:Democracy/Politics/Parliament
#   7:Human Rights/Law/Justice
#   8:Religion/Religious
#   9:Social Issues/Social Justice
#   10:Health/Environment
#   11:Education/Science/Technology
#Explicit or Implicit
#Positive or Negative
#Example: 3, Explicit, Negative
#These codes will be calculated using the GPT api
#The script will have to download the article from the link which was passed through
import requests
from bs4 import BeautifulSoup
import json
import os
import openai
import csv
import time
import sys

def get_article_info(url):
    # This function will get the article from the link and return a dictionary with the information
    # The code will do this by running the extrablatt program from the command line
    # The extrablatt program will return a json file with the information
    # The code will then read the json file and return the information

    info = {}
    info["link"] = url

    hurl = '"' + url + '"' # Add quotes to the url

    nj = "{}.json".format(url) # The name of the json file

    # Use the extrablatt program to get the information from the command line
    try:
     print(os.system("extrablatt article {} -o {}".format(hurl, nj)))
    except:
        print("Error")
    # Read the json file
    with open("article.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        # Get the information from the json file
        try:
            info["website"] = data[0]["url"].split("/")[2]
        except:
            info["website"] = ""

        try:
            info["title"] = data[0]["content"]["title"]
        except:
            info["title"] = ""

        try:
            info["date"] = data[0]["content"]["publishing_date"]["published"]["DateTime"]
        except:
            info["date"] = ""

        try:
            info["author"] = data[0]["content"]["authors"][0]
        except:
            info["author"] = ""

        try:
            info["text"] = data[0]["content"]["text"]
        except:
            info["text"] = ""

        try:
            keywords = data[0]["content"]["keywords"]
            info["keywords"] = ", ".join(keywords)
        except:
            info["keywords"] = ""

        # Copy the json file to another file with the name of the article
        os.popen("copy article.json {}.json".format(info["title"]))

    return info

def get_sentences(info):
    #Get the sentences from the text, split by periods
    sentences = info["text"].split(".")
    return sentences

def get_paragraphs(info):
    #Get the paragraphs from the text, split by newlines
    paragraphs = info["text"].split("\n") 
    return paragraphs

def get_codes(sentences):
    #Use the GPT api to get the codes for the sentences
    #The codes will be stored in a dictionary along with the sentence
    #The dictionary will be returned
    openai.api_key = "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"
    codes = {}
    

    
    for sentence in sentences:
        #Build the prompt
        #Print the sentence
        print("Sentence: {}".format(sentence))
        prompt="(The Code for the line:\nExample: Result: 3, Explicit, Negative, KeyWords: Economic Impact, Violence\nExample: Result: 1, Implicit, Positive, Keywords: Shut Down, Critical Access\n   1:Economy/Money/Finance/Trade/GDP\n   2:Trust/Stability/Security/Peace\n   3:Violence/Conflict/Protest\n   4:Unity/Cooperation/Alliance\n   5:Change/ Reform/Revolution \n Explicit or Implicit\nPositive or Negative)\n\n{}\nThe keywords should also be extracted\nResult:"
        #Remove the {} from the prompt and replace it with the sentence
        prompt = prompt.format(sentence)
        try:
         response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
        )
         codes.update({sentence: response["choices"][0]["text"]})
         print(response["choices"][0]["text"])
         #Wait for 1 second to avoid the api limit
         time.sleep(2)
        except:
         codes.update({sentence: "error"})
    return codes

def create_csv(info, sentences, codes):
    #Create a csv file with the information
    #The csv file will be named after the article title
    #The csv file will have the following columns:
    #Website, Title, Date, Author, Sentence, Code
    #The csv file will be stored in the same directory as the python file
 filename = info["title"] + ".csv"
 #Take the codes and get the implicit/ explicit and positive/negative and keywords
 IE = []
 PN = []
 KW = []

 with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Website", "Title", "Date", "Author", "Sentence", "Code", "Implicit/Explicit" ,"Intent", "Keywords"])
    for sentence in sentences:
        #Get the code
        code = codes[sentence]
        #Get the implicit/ explicit
        IE.append(code.split(",")[1])
        #Get the positive/ negative
        PN.append(code.split(",")[2])
        #Get the keywords
        KW.append(code.split(",")[3])
        #Fix any encoding issues
        sentence = sentence.encode("utf-8", "ignore").decode()
        writer.writerow([info["website"], info["title"], info["date"], info["author"], sentence, codes[sentence]])


def main():
 #The link is the first argument passed to the program
 link = sys.argv[1]
 result = get_article_info(link)
 sentences = get_sentences(result)
 paragraphs = get_paragraphs(result)
 #Print all the sentences
 output = get_codes(sentences)
 print(output)
 create_csv(result, sentences, output)
 
 #print(result)

main()
