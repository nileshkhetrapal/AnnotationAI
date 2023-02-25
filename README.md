# AnnotationAI
This is meant to annotate an article from a link
# Main.py

The code first defines three functions: `get_article_info`, `get_sentences`, and `get_codes`.

`get_article_info` takes a URL as input, downloads the article from the URL using the `extrablatt` program, reads the JSON file created by `extrablatt`, extracts the website name, article title, publication date, author, and text, and returns a dictionary containing this information.

`get_sentences` takes a dictionary returned by `get_article_info` and splits the text into sentences, removes empty sentences, and removes newlines from the remaining sentences. It returns a list of sentences.

`get_codes` takes a list of sentences as input and uses the OpenAI GPT API to generate codes for each sentence. The codes are stored in a dictionary along with the sentence and returned as the output of the function.

The main code then sets the OpenAI API key, calls `get_article_info` for each URL passed to it, calls `get_sentences` and `get_codes` for each article, and stores the resulting information in a JSON file for each article.

Introduction:
This script is designed to extract relevant information from articles provided by the user, and generate a JSON file for each article that contains various pieces of information such as the link, name of the website, each line from the article, the date of the article, author of the article, and a code for each line based on the context.

The code works by utilizing the Extrablatt program to extract information from the article and then uses the OpenAI GPT API to generate the codes for each line in the article based on the context. The codes are designed to help categorize each line of the article into one of five categories based on the context - Economy/Money/Finance/Trade/GDP, Trust/Stability/Security/Peace, Violence/Conflict/Protest, Unity/Cooperation/Alliance, and Change/Reform/Revolution. Additionally, each line is classified as being either explicit or implicit, and whether the sentiment expressed is positive or negative.

The script is written in Python and requires various libraries such as Requests, Beautiful Soup, OpenAI, and JSON. It is designed to be run from the command line and accepts a list of article links as input. Once the script has finished processing the articles, it generates a JSON file for each article that contains all of the extracted information.

This code could be useful for individuals or organizations that need to analyze large amounts of news articles quickly and efficiently. By using the OpenAI GPT API, it can generate codes for each line in the article quickly and accurately, saving a considerable amount of time and effort. The output JSON file format makes it easy to integrate with other tools or systems for further analysis.

The code is available on GitHub and can be downloaded, modified, or improved upon as needed.

# Data.py

This code is a Python script designed to clean data stored in CSV format and create a new CSV file with the cleaned data. The script reads all CSV files in the same directory and extracts the data stored in the format of "Website,Title,Date,Author,Sentence,Code," where the Code number is translated to the annotation using a predefined dictionary.

The script has two main functions, `get_data()` and `remove_unnecessary()`. The `get_data()` function reads the data from the CSV files and returns a list of dictionaries, where each dictionary contains the information for one sentence. The `remove_unnecessary()` function removes all unnecessary information from the data, translates the code number to the annotation, removes "b'" from the beginning of the sentence, removes "'" from the end of the sentence, removes any byte characters from the sentence, and removes specific lines and columns that are not needed.

The output CSV file contains the following headers: "Sentence, Annotation, Explicit/Implicit, Intent, Keywords1, Keywords2, Keywords3, Keywords4, Keywords5." The script uses Pandas library to create the output CSV file.
