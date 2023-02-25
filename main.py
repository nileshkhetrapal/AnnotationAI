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
import argparse
import datetime

def get_article_info(url):
    # This function will get the article from the link and return a dictionary with the information
    # The code will do this by running the extrablatt program from the command line
    # The extrablatt program will return a json file with the information
    # The code will then read the json file and return the information

    info = {}
    info["link"] = url

    hurl = '"' + url + '"' # Add quotes to the url

    #Get the name of the article from the url
    aName = url.split("/")[-1]
    #Remove the .html and everything else from the name
    aName = aName.split(".")[0]

    nj = "{}.json".format(aName) # The name of the json file

    # Use the extrablatt program to get the information from the command line
    try:
     print("extrablatt article {} -o {}".format(hurl, nj))
     print(os.system("extrablatt article {} -o {}".format(hurl, nj)))
    except:
        print("Error")
    # Read the json file
    with open(nj, "r", encoding="utf-8") as json_file:
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
    #Remove the last sentence if it is empty
    if sentences[-1] == "":
        sentences.pop()
    #Remove newlines from the sentences
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace("\n", " ")
    return sentences

def get_paragraphs(info):
    #Get the paragraphs from the text, split by newlines
    paragraphs = info["text"].split("\n") 
    return paragraphs

def get_codes(sentences):
    #Use the GPT api to get the codes for the sentences
    #The codes will be stored in a dictionary along with the sentence
    #The dictionary will be returned
    #Insert your own key bruh
    openai.api_key = "sk-"
    codes = {}
    

    
    for sentence in sentences:
        #Build the prompt
        #Print the sentence
        print("Sentence: {}".format(sentence))
        prompt="(The Code for the line:\nExample: Result: 3, Explicit, Negative, KeyWords: Economic Impact, Violence\nExample: Result: 1, Implicit, Positive, Keywords: Shut Down, Critical Error\n   1:Economy/Money/Finance/Trade/GDP\n   2:Trust/Stability/Security/Peace\n   3:Violence/Conflict/Protest\n   4:Unity/Cooperation/Alliance\n   5:Change/ Reform/Revolution \n Explicit or Implicit\nPositive or Negative)\n\n{}\nThe keywords should also be extracted\nResult:"
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
 #Take the codes and get the implicit/ explicit and positive/negative and keywords
 #Create a variable with the current date and time
 now = datetime.datetime.now()
 try:
  shortName = info["title"].split(" ")[0]  #Get the first word of the title
  filename = "{}{}.csv".format(now ,shortName).strip().replace(" ", "_").replace(":", "_") #Create the filename
 except:
    filename="{}.csv".format(now).strip().replace(" ", "_").replace(":", "_")
 with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Website", "Title", "Date", "Author", "Sentence", "Code", "Implicit/Explicit" ,"Intent", "Keywords"])
    for sentence in sentences:
        #Get the code
        code = codes[sentence]
        #Fix any encoding issues
        sentence = sentence.encode("utf-8", "ignore").decode()
        writer.writerow([info["website"], info["title"], info["date"], info["author"], sentence.encode('utf-8'), codes[sentence]])



def main():
 #The input can be a link to an article or a text file with a list of links
 parser = argparse.ArgumentParser(
    description="Get the codes for the sentences in an article",
    formatter_class=argparse.RawTextHelpFormatter
 )
 parser.add_argument(
    "-i","--singleinput", help="The link to the article")
 parser.add_argument(
    "-f","--fileinput", help="The file with the links to the articles")
 args = parser.parse_args()

 if args.fileinput:
        #The file is the second argument passed to the program
    file = args.fileinput
    print(file)
    try:
        #Open the file and get the links
        with open(file, "r") as f:
            links = f.readlines()
        #Remove the newlines from the links
        links = [x.strip() for x in links]
        print(links)
    except:
        print("Error opening the file")
        #Remove the newlines from the links
    links = [x.strip() for x in links]
        #Get the information for each link
    for link in links:
        print(link)
        try:
            result = get_article_info(link)
        except:
            print("Error getting the information for {}".format(link))
        try:
            sentences = get_sentences(result)
        except:
            print("Error getting the sentences for {}".format(link))    
            #Print all the sentences
        try:
            output = get_codes(sentences)
            #output = get_paragraphs(result)
        except:
            print("Error getting the codes for {}".format(link))
        print(output)
        create_csv(result, sentences, output)
    
 elif args.singleinput:
  link = args.singleinput   
  result = get_article_info(link)
  sentences = get_sentences(result)
  #Print all the sentences
  #output = get_codes(sentences)
  print(output)
  create_csv(result, sentences, output)
 
 #print(result)

main()
