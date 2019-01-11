

Dear Tett,

In this folder, you have our empath.py code that allows the user to perform NLP on a given text. 
The data folder contains just the categories the NLP algorithm needs.

Here is also some additional code around iris. 

Part 1 Iris-agent programming:


Section 1:

Python Prototype:

import twitter
api = twitter.Api()
tweets = api.GetUserTimeline(
    screen_name="realDonaldTrump", count=200)
tweet_text = [x.text for x in tweets]

from nlp import Nlp
lexicon = Nlp()
topics = lexicon.analyze(tweets)

# ready for command


Section 2:

Command DSL (adding commands to iris):

from iris import state_types as t
from iris import IrisCommand

class GenerateArray(IrisCommand):
    # what iris will call the command + how it will appear in a hint
    title = "generate a random array of {n} numbers"
    
    # give an example for iris to recognize the command
    examples = ["generate numpy array of size {n}"]
    
    # type annotations for each command argument, to help Iris collect missing values from a user
    argument_types = {"n":t.Int("Please enter size of array:")}
    
    # core logic of the command
    def command(self, n):
        import numpy
        return numpy.random.randint(100, size=n)
        
    # wrap the output of a command to display to user
    # by default this will be an identity function
    # each element of the list defines a separate chat bubble
    def explanation(self, result):
        return ["Here are the numbers", result]


Part 2 Function prototyping:


Section 1: Probability


Probability of event:

P(event) = event / total


Probability of event1 || event2:

P(event1 or event2) = P(event1) + P(event2) - P(event1 && event2)

for mutually exclusive event1 and event2:

P(event1 && event2) = 0


Probability of both event1 && event2:

P(event1 and event2) = P(event1) * P(event2 when event1)

Probability of all event1 && event2 && event3:

P(event1 and event2 and event3) = P(event1) * P(event2 when event1) * P(event3 when event1 and event2)

for independent event1 and event2:

P(event1 && event2) = P(event1) * P(event2)

for indenpendent event1 and event2 and event3:

P(event1 && event2 && event3) = P(event1) * P(event2) * P(event3)


Probability of success in trials:

Probablity of r success in n tirals with p success in individual trial = (n! / r!(n-r)!) * p^r * (1 - p)^(n-r)


Section 2: Finance


Effective Annual Yield:

Effective annual yield on 1 unit of capital = (1 + holding period yield) ^ (365 / n) - 1


Bank discount yield:

The annualized return on a bank discount basis r<bd> with a dollar discount D (face value of the bill F - purchase price of the bill P) when the number of days remaining until maturity is t

r<bd> = (D / F) * (360 / t)
r<bd> = ((F - P) / F) * (360 / t)


Money market yield:

Convert the equivalent bank discount yield Rbd to annual money market yield Rmm with the dollar discount D and the face value of the bill F and the purchase price of the bill P

Rmm = (D / (F - D)) * (360 / t)
Rmm = (D / P) * (360 / t)


Bond equivalent yield:

Convert the equivalent bank discount yield Rbd to annual bond to annual bond equivalent yield BEY

BEY = (D / P) * (365 / t)


