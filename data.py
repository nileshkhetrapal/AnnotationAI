#The goal of this script is to clean the data and create a csv file with all the information
#All the data is stored in the same folder as the script
#It is all stored in CSV format
#These are the headers for the output csv file:
#Sentence, Annotation, Explicit/Implicit, Intent, Keywords1, Keywords2, Keywords3, Keywords4, Keywords5
#The data is stored in the following format:
#Website,Title,Date,Author,Sentence,Code
#Where Code Number, Implicit/Explicit, Intent , Keywords are stored in the same cell under code
#Code number needs to be translated to the annotation using this dictionary:
#codes = {
#    1: "Economy/Money/Finance/Trade/GDP",
#    2: "Trust/Stability/Security/Peace",
#    3: "Violence/Conflict/Protest",
#    4: "Unity/Cooperation/Alliance",
#    5: "Change/ Reform/Revolution",
#This is what the data looks like:
#knowledge.wharton.upenn.edu,"To Stave Off Arab Spring Revolts, Saudi Arabia and Fellow Gulf Countries Spend $150 Billion",,,"b'Possessing 20% of the world\xe2\x80\x99s proven petroleum reserves, Saudi Arabia has long played the expected role of benefactor among its fellow Arab and Muslim countries'"," 4, Explicit, Positive, Keywords: Petroleum Reserves, Benefactor"

import csv
import os
import json
import re
import pandas as pd
import chardet



def get_data():
    # This function will read the data from the csv files and return a list of dictionaries
    # Each dictionary will contain the information for one sentence
    # The data is stored in the following format:
    # Website,Title,Date,Author,Sentence,Code
    # Where Code Number, Implicit/Explicit, Intent , Keywords are stored in the same cell under code
    # Code number needs to be translated to the annotation using this dictionary:
    # codes = {
    #    1: "Economy/Money/Finance/Trade/GDP",
    #    2: "Trust/Stability/Security/Peace",
    #    3: "Violence/Conflict/Protest",
    #    4: "Unity/Cooperation/Alliance",
    #    5: "Change/ Reform/Revolution",

    data = [] # This is the list that will contain all the dictionaries

    # Get the list of all the files in the current directory
    files = os.listdir(os.getcwd())

    # Loop through all the files
    for file in files:
        # Check if the file is a csv file
        if file.endswith(".csv"):
            #Get the encoding of the file
            with open(file, "rb") as f:
                result = chardet.detect(f.read())
                encoding = result["encoding"]
            # Open the csv file
            with open(file, "r", encoding=encoding) as csv_file:
                # Read the csv file
                csv_reader = csv.reader(csv_file, delimiter=",")
                # Loop through all the rows in the csv file
                for row in csv_reader:
                    #Skip the row if it does not have 6 columns
                    if len(row) != 6:
                        continue
                    # Get the information from the row
                    website = row[0]
                    title = row[1]
                    date = row[2]
                    author = row[3]
                    sentence = row[4]
                    code = row[5]

                    # Create the list of information
                    info = [website, title, date, author, sentence, code]

                    # Add the dictionary to the list
                    data.append(info)

    # Return the list of dictionaries
    return data

def remove_unnecessary(data):
    #This function will remove all the unnecessary information from the data
    #It will also translate the code number to the annotation
    #It will also remove the b' from the beginning of the sentence
    #It will also remove the ' from the end of the sentence
    #It will also remove any byte characters from the sentence
    #It will remove the line that contain the following words:
    #Website,Title,Date,Author,Sentence,Code,Implicit/Explicit,Intent,Keywords
    #It will also remove the column headers
    #It will also remove the columns that contain the following words:
    #Website,Title,Author

    #This is the list that will contain the cleaned sentences
    AllSentences = []

    #This is the list that will contain the cleaned annotations
    AllAnnotations = []

    #This is the list that will contain the cleaned Explicit/Implicit
    AllIE = []

    #This is the list that will contain the cleaned Intent
    AllIntent = []

    #This is the list that will contain the cleaned Keyword1
    AllKeyword1 = []

    #This is the list that will contain the cleaned Keyword2
    AllKeyword2 = []

    #This is the list that will contain the cleaned Keyword3
    AllKeyword3 = []

    #This is the list that will contain the cleaned Keyword4
    AllKeyword4 = []

    #This is the list that will contain the cleaned Keyword5
    AllKeyword5 = []

    #Loop through all the dictionaries in the data
    for dictionary in data:
        #print(dictionary)
        #Remove the line that contain the following words:
        #Website,Title,Date,Author,Sentence,Code,Implicit/Explicit,Intent,Keywords
        if "Website" in dictionary:
            continue
        #Get the code number
        codeCell = dictionary[5]
        #print(codeCell)
        #This is the format for code: 1, Explicit, Positive, Keywords: Petroleum Reserves, Benefactor
        #The code field may have the following formats:
        #0
        #error
        #In which case we are skipping the row
        if codeCell == "0" or codeCell == "error":
            continue
        #Extract the code number for all the code numbers
        code = int(codeCell.split(",")[0].strip())
        print(code)
        # This is the dictionary that will be used to translate the code number to the annotation
        codes = {
    1: "Economy/Money/Finance/Trade/GDP",
    2: "Trust/Stability/Security/Peace",
    3: "Violence/Conflict/Protest",
    4: "Unity/Cooperation/Alliance",
    5: "Change/ Reform/Revolution",
}
        
        #Check if the code number is in the dictionary
        if int(code) in codes:
            print("Code is in dictionary")
            #Get the annotation
            annotation = codes[code]
            AllAnnotations.append(annotation)
            #Get the IE
        else:
            print("Code is not in dictionary")
            AllAnnotations.append("None")
        try:
            AllSentences.append(dictionary[4].replace("b'", "").replace("'", "").encode("ascii", "ignore").decode("ascii"))
        except:
            AllSentences.append("None")
        try:
            IE = codeCell.split(",")[1] #Index 1 is Implicit/Explicit
            AllIE.append(IE) #Add the IE to the list
        except:
            AllIE.append("None")
        try:
            intent = codeCell.split(",")[2] #Index 2 is Intent
            AllIntent.append(intent) #Add the intent to the list
        except:
            AllIntent.append("None")
        #Get the keywords and create a list of keywords that should be 5 keywords long, if there are less than 5 keywords, the rest of the list will have a string "None"
        try:
            keywords = codeCell.split(",")[3:]
        
        #Remove the "Keywords: " from the first keyword
        
            keywords[0] = keywords[0].replace("Keywords: ", "")
        #Create a list to store the keywords that are seperated by , and remove the "Keywords: " from the first keyword
            keywordList = keywords[0].split(", ")
        #Check if there are more than 5 keywords in the list
            if len(keywordList) > 5:
            #Remove the last keyword from the list
                keywordList.pop()
        except:
            keywordList = ["None", "None", "None", "None", "None"]
        try:
            #Get the first keyword
            keyword1 = keywordList[0]
        except:
            keyword1 = "None"
        try:
            keyword2 = keywordList[1]
        except:
            keyword2 = "None"
        try:
            keyword3 = keywordList[2]
        except:
            keyword3 = "None"
        try:
            keyword4 = keywordList[3]
        except:
            keyword4 = "None"
        try:
            keyword5 = keywordList[4]
        except:
            keyword5 = "None"
        #Create the list of keywords that should be 5 keywords long, if there are less than 5 keywords, the rest of the list will have a string "None"
        AllKeyword1.append(keyword1) #Add the keyword to the list
        AllKeyword2.append(keyword2) #Add the keyword to the list
        AllKeyword3.append(keyword3) #Add the keyword to the list
        AllKeyword4.append(keyword4) #Add the keyword to the list
        AllKeyword5.append(keyword5) #Add the keyword to the list


        #Add the dictionary to the list

        
    return AllSentences, AllAnnotations, AllIE, AllIntent, AllKeyword1, AllKeyword2, AllKeyword3, AllKeyword4, AllKeyword5


def main():
    #Get the data
    data = get_data()

    #Remove unnecessary stuff from the data
    sentences, annotations, ie, intent, kw1, kw2, kw3, kw4, kw5 = remove_unnecessary(data)
    print(ie)
    # check the lengths of the arrays
    lengths = [len(sentences), len(annotations), len(ie), len(intent), len(kw1), len(kw2), len(kw3), len(kw4), len(kw5)]
    print(lengths)
    min_len = min(lengths)
    print(min_len)
    # remove elements that exceed the minimum length
    sentences = sentences[:min_len]
    annotations = annotations[:min_len]
    ie = ie[:min_len]
    intent = intent[:min_len]
    kw1 = kw1[:min_len]
    kw2 = kw2[:min_len]
    kw3 = kw3[:min_len]
    kw4 = kw4[:min_len]
    kw5 = kw5[:min_len]

    # create the DataFrame
    df = pd.DataFrame({"Sentence": sentences, "Annotation": annotations, "Implicit/Explicit": ie, "Intent": intent, "Keyword1": kw1, "Keyword2": kw2, "Keyword3": kw3, "Keyword4": kw4, "Keyword5": kw5})

    #Save the dataframe as a csv file
    df.to_csv("CleanedData.csv", index=False)

main()
