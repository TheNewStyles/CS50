Sentiments
tl;dr
Implement a program that categorizes a word as positive or negative.

$ ./smile love
:)
$ ./smile hate
:(
$ ./smile Stanford
:|
Implement a program that categorizes a user’s tweets as positive or negative.

$ ./tweets @cs50
 0 hello, @world
 1 I love you, @world
-1 I hate you, @world
...
Implement a website that generates a pie chart categorizing a user’s tweets.

@katyperry
Background
"Sentiment analysis," otherwise known as "opinion mining," involves inference of sentiment (i.e., opinion) from text. For instance, movie reviews on Rotten Tomatoes are often positive or negative. So are product reviews on Amazon. Similarly do opinions underlie many tweets on Twitter.

Some words tend to have positive connotations (e.g., "love"), while some words tend to have negative connotations (e.g., "hate"). And so, if someone were to tweet "I love you", you might infer positive sentiment. And if someone were to tweet "I hate you", you might infer negative sentiment. Of course, individual words alone aren’t always reliable, as "I do not love you" probably isn’t a positive sentiment, but let’s not worry about those cases. Some words, meanwhile, have neither positive nor negative connotations (e.g., "the").

A few years back, Dr. Minqing Hu and Prof. Bing Liu of the University of Illinois at Chicago kindly put together lists of 2006 positive words and 4783 negative words. We’ll use those to classify tweets! But first a tour.

Distribution
Downloading
$ wget https://github.com/cs50/problems/archive/sentiments.zip
$ unzip sentiments.zip
$ rm sentiments.zip
$ mv problems-sentiments sentiments
$ cd sentiments
$ chmod a+x smile tweets
$ ls
analyzer.py     helpers.py          positive-words.txt  smile*     tweets*
application.py  negative-words.txt  requirements.txt    templates/
Understanding
smile
Open up smile in sentiments/. Suffice it to say that file’s name doesn’t end in .py, even though the file contains a program written in Python. But that’s okay! Notice the "shebang" atop the file:

#!/usr/bin/env python3
That line tells a computer to interpret (i.e., run) the program using python3 (aka python on CS50 IDE), an interpreter that understands Python 3.

Notice next that the program imports a class called Analyzer from a module called analyzer as well as a function called colored from a module called termcolor. The former you’ll actually soon implement in a file called analyzer.py. (Recall that a class in Python is like a struct in C except that a class can also contain functions, otherwise known as "methods" when they’re inside a class.) The latter colorizes output in terminal windows, as we’ll soon see.

This program defines only one function, main, which gets called per the file’s last line. Within main, we first make sure that sys.argv contains the expected number of command-line arguments. We then "instantiate" (i.e., allocate) an Analyzer object. We then pass to that object’s analyze method the word that a user has provided in sys.argv[1]. As we’ll soon see, that method will return a positive int if its input is positive, a negative int if its input is negative, and 0 if its input is neither positive nor negative. The program ultimately prints a colored smiley accordingly.

analyzer.py
Open up anlyzer.py in sentiments/. Not much going on in there (yet)! Notice, though, that it imports the Natural Language Toolkit, among whose features is a tokenizer that you can use to split a tweet (which is maximally a 140-character str object) into a list of words (i.e., shorter str objects).

In there is our definition of that Analyzer class, which has two methods: __init__, which is called whenever Analyzer is instantiated; and analyze, which can be called to analyze some text. That first method takes two arguments in addition to self: positives, whose value is the path to a text file containing positive words; and negatives, whose value is the path to a text file containing negative words. Meanwhile, analyze takes one argument in addition to self: a str to be analyzed for sentiment. Though that function is (temporarily) hardcoded to return 0 no matter what.

Recall that methods are automatically passed that first reference to self so that they have a way of referring to objects' "instance variables."

positive-words.txt, negative-words.txt
Open up positive-words.txt and negative-words.txt (without changing them). Notice that atop each file is a bunch of comments, each of which starts with a ;. (Those are just text files, though, so the authors' choice of ; is arbitrary.) The lists of positive and negative words, respectively, begin below those comments, after a blank line.

tweets
Open up tweets. Ah, another shebang. But nothing else besides a TODO! More on that soon.

helpers.py
Open up helpers.py. You should see two functions: chart and get_user_timeline. Given three values (positive, negative, and neutral, each an int or a float), chart generates HTML (as a str) for a pie chart depicting those values. Given a screen name, meanwhile, get_user_timeline returns a list of tweets (each as a str). That function uses Twython (har har), a library for Python, to retrieve those tweets via Twitter’s API (application programming interface), a free service that can be queried programmatically for tweets. Notice how the function expects two "environment variables" to exist. Environment variables exist within your terminal window, key/value pairs that programs (like tweets) can access programmatically. We’ll soon use two, API_KEY and API_SECRET, to store credentials for Twitter.

application.py
Open up application.py. In this file is a "controller" for a Flask-based web app with two endpoints: / and /search. The first displays the simplest of forms via which you can search for a user on Twitter by screen name. The second displays one of those pie charts categorizing that user’s tweets. Notice, though, how 100% of those tweets are (temporarily) assumed to be neutral.

templates/index.html
Open up templates/index.html. In there is that simplest of forms. Notice how it figures out via url_for, a function that comes with Flask, to what URL the form should be submitted.

templates/search.html
Open up templates/search.html. Notice how this template renders a user’s screen name as well as that pie chart.

templates/layout.html
Open up templates/layout.html. In here is a layout on which index.html and search.html depend. It leverages Bootstrap to override browsers' default aesthetics.

requirements.txt
Open up requirements.txt (without changing it, though you can later if you’d like). This file specifies the libraries, one per line, on which all of this functionality depends.

Getting Started
In a terminal window execute

cd ~/workspace/pset6/sentiments/
pip3 install --user -r requirements.txt
to install these programs' dependencies.

Sign up for Twitter at twitter.com/signup if you don’t already have an account.

Visit apps.twitter.com, logging in if prompted, and click Create New App.

Any (available) Name suffices.

Any (sufficiently long) Description suffices.

For Website, input https://cs50.harvard.edu/ (or any other URL).

Leave Callback URL blank.

Click Create your Twitter application. You should see "Your application has been created."

Click Keys and Access Tokens.

Click modify app permissions.

Select Read only, then click Update Settings.

Click Keys and Access Tokens again.

Highlight and copy the value to the right of Consumer Key (API Key).

In a terminal window, execute

export API_KEY=value
where value is that (pasted) value, without any space immediately before or after the =.

Highlight and copy the value to the right of Consumer Secret (API Secret).

In a terminal window, execute

export API_SECRET=value
where value is that (pasted) value, without any space immediately before or after the =.

If you close that terminal window and/or open another, you’ll need to repeat those last five steps.

Next, try running

./smile
to see how it works. Keep in mind that all words will be classified (for now!) as neutral because of that hardcoded 0 in analyze.py.

Next, try running

flask run
and then select CS50 IDE > Web Server in CS50 IDE’s top-left corner. Search for some user’s screen name, and you should see a chart! Of course, it’s all yellow for now because of that 100.0 in application.py. Quit Flask with control-c.

Specification
analyzer.py
Complete the implementation of analyzer.py in such a way that

__init__ loads positive and negative words into memory in such a way that analyze can access them, and

analyze analyzes the sentiment of text, returning a positive score if text is more positive than negative, a negative score if text is more negative than positive, and 0 otherwise, whereby that score is computed as follows:

assign each word in text a value: 1 if the word is in positives, -1 if the word is in negatives, and 0 otherwise

consider the sum of those values to be the entire text’s score

For instance, if text were "I love you" (and Analyzer were instantiated with default values for its named parameters), then its score would be 0 + 1 + 0 = 1, since

"I" is in neither positive-words.txt nor negative-words.txt,

"love" is in positive-words.txt, and

"you" is in neither positive-words.txt nor negative-words.txt.

Suffice it to say, more sophisticated algorithms exist, but we’ll keep things simple!

tweets
Complete the implementation of main in tweets in such a way that program

accepts one and only one command-line argument, the screen name for a user on Twitter,

queries Twitter’s API for a user’s most recent 50 tweets,

analyzes the sentiment of each of those tweets, and

outputs each tweet’s score and text, colored in green if positive, red if negative, and yellow otherwise.

application.py
Complete the implementation of search in application.py in such a way that the function

queries Twitter’s API for a user’s most recent 100 tweets,

classifies each tweet as positive, negative, or neutral,

generates a chart that accurately depicts those sentiments as percentages.

If a user has tweeted fewer than 100 times, classify as many tweets as exist.
