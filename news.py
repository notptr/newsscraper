#!/usr/bin/env python

#this is a python 3 script that scrapes the news articles off of tl;dr
#Programmer: Matthew Deig
#Date: 2012-12-14

import urllib.request, urllib.parse, urllib.error, re

def getWebsite(websiteURL):
  #this is a function it is going to return a string back of the website data
  #the websiteURL is going to be a string that holds the website url for tl;dr
  
  try:
    webpage_data = urllib.request.urlopen(websiteURL).read().decode("utf-8")
    
  except IOError as e:
    return "Couldn't Reach host"
  
  if not404(webpage_data) == True:
    return webpage_data
  else:
    print("Something is wrong with the page skipping scrapping")
    return None
    


def not404(webData):
  #this funtion is going to see if we got the right webpage or not.
  #webData is going to be a string
  #this funtion is going to return True for it is the page we want or
  #Flase that it is a 404 or something
  
  for line in re.split('\n', webData):
    if re.findall("\<title>.*?\</title>", line) != []:
      if line == "<title>TL;DR </title>":
        return True
      else:
        return False
        

def scrapWebpage(webData):
  #this well scrap out all of the news articles on tl;dr
  #then return the data
  newsString = " "
  newsArticles = None
  
  webData = re.sub('\n', '\t', webData)
  newsData = re.findall("<section.*?</section>", webData)
  for line in newsData:
    newsString = newsString + ' ' + line
    
  newsData = re.findall("<a.*?</a>", newsString)
  
  
  for article in newsData:
    articleNewline = re.split('\t', article)
    url = None
    title = None
    cat = None
    text = ''
    for line in articleNewline:
      if line[1] == 'a' and line[2] != 'r':
        dummy = re.sub("<a href=\"",'',line)
        dummy = re.sub("\">", '', dummy)
        dummy = re.sub("&amp;", '&', dummy)  
        url = dummy
      elif line[1] == 'h':
        dummy = re.sub("<h1>", '', line)
        dummy = re.sub("</h1>", '', dummy)
        dummy = re.sub("&#8217;", "'", dummy)
        dummy = re.sub("&#8216;", "'", dummy)
        dummy = re.sub("&lsquo;", "'", dummy)
        dummy = re.sub("&rsquo;", "'", dummy)
        dummy = re.sub("&#039;", "'", dummy)
        dummy = re.sub("&#8220;", '"', dummy)
        dummy = re.sub("&#8221;", '"', dummy)
        title = dummy
      elif line[1] == 's':
        dummy = re.sub("<span.*?>", '', line)
        dummy = re.sub("</span>", '', dummy)
        cat = dummy
      elif line[1] == 'p':
        dummy = re.sub("<p>", '', line)
        dummy = re.sub("</p>", '', dummy)
        dummy = re.sub("&#8217;", "'", dummy)
        dummy = re.sub("&#8216;", "'", dummy)
        dummy = re.sub("&lsquo;", "'", dummy)
        dummy = re.sub("&rsquo;", "'", dummy)
        dummy = re.sub("&#039;", "'", dummy)
        dummy = re.sub("&#8220;", '"', dummy)
        dummy = re.sub("&#8221;", '"', dummy)
        text = dummy
          
    if newsArticles != None:
      newsArticles.append([title, cat, url, text])
    else:
      newsArticles = [[title, cat, url, text]]
  
  return newsArticles

def prettyDisplay(newsArticle):
  #this will be the finial part of the program
  #it is going to pretty the scrapings from tl;dr
  #newsArticle is a list we get from scrap which are all strings
  
  for article in newsArticle:
    print("Title: ", article[0])
    print(article[1])
    print("URL to full article: ", article[2])
    print(article[3])
    print()
    print()

def onelineOutput(newsArticle):
  #this is for pipeing and redirecting
  #it is the same as pretty but on one
  
  output = ''
  
  for article in newsArticle:
    output = output + article[1] + ' ' + article[0] + ' ' + article[2] + ' ' + article[3] + ' '
  
  print(output)
  
          

if __name__ == "__main__":
  data = getWebsite("http://toolong-didntread.com/")
  
  if data == None:
    print("Page is down or 404ed")
  else:
    data = scrapWebpage(data)
    prettyDisplay(data)