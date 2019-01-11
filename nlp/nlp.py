#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:16:29 2018

@author: leobix
"""

import os
import sys
from collections import defaultdict
import requests
import json

from itertools import islice

###Some helpers functions

def partitions(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def window(seq, n):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def default_tokenizer(doc):
    return doc.split()

def bigram_tokenizer(doc):
    tokens = doc.split()
    for t1,t2 in zip(tokens,tokens[1:]):
        yield t1
        yield t1+"_"+t2
    yield tokens[-1]

def window_tokenizer(window_size, targets):
    def window_func(doc,target_dic={t:t for t in targets}):
        tokens = doc.split()
        for w in partitions(tokens, window_size):
            if any([x in target_dic for x in w]):
                for w_ in w:
                    yield w_
    return window_func


##This class allows the user to make a sentimental and topic analysis of a text.
class Nlp:
    def __init__(self, backend_url="http://54.148.189.209:8000"):
        self.cats = defaultdict(list)
        self.staging = {}
        self.backend_url = backend_url
        #self.base_dir = os.path.dirname(__file__)
        self.inv_cache = {}
        #complete path
        self.load("/Users/leobix/Desktop/nlp/data/categories.tsv")
        for f in os.listdir("/Users/leobix/Desktop/nlp/data/user/"):
            if len(f.split(".")) > 1 and f.split(".")[1] == "nlp":
                self.load("/Users/leobix/Desktop/nlp/data/user/"+f)

    def load(self,file):
        with open(file,"r") as f:
            for line in f:
                cols = line.strip().split("\t")
                name = cols[0]
                terms = cols[1:]
                for t in set(terms):
                    self.cats[name].append(t)
                    #self.invcats[t].append(name)

    def analyze_term_window(self,doc,targets,categories=None,window_size=10,normalize=False):
        tokenizer = window_tokenizer(window_size,targets)
        return self.analyze(doc,categories,tokenizer,normalize)

    #To analyze a text with nlp. 
    #only_present allows to only display the relevant categories for the analysis
    def analyze(self,doc,categories=None,tokenizer="default",normalize=False, only_present=False):
        if isinstance(doc,list):
            doc = "\n".join(doc)
        if tokenizer == "default":
            tokenizer = default_tokenizer
        elif tokenizer == "bigrams":
            tokenizer = bigram_tokenizer
        if not hasattr(tokenizer,"__call__"):
            raise Exception("invalid tokenizer")
        if not categories:
            categories = self.cats.keys()
        invcats = defaultdict(list)
        key = tuple(sorted(categories))
        if key in self.inv_cache:
            invcats = self.inv_cache[key]
        else:
            for k in categories:
                for t in self.cats[k]: invcats[t].append(k)
            self.inv_cache[key] = invcats
        count = {}
        tokens = 0.0
        for cat in categories: count[cat] = 0.0
        for tk in tokenizer(doc):
            tokens += 1.0
            for cat in invcats[tk]:
                count[cat]+=1.0
        if normalize:
            for cat in count.keys():
                if tokens == 0:
                    return None
                else:
                    count[cat] = count[cat] / tokens
        
        dict=count.copy()
        if only_present:
    
            for key in count:
                if count[key]==0:
                    del dict[key]
        return dict


    def create_category(self,name,seeds,model="fiction",size=100,write=True):
        resp = requests.post(self.backend_url + "/create_category", json={"terms":seeds,"size":size,"model":model})
        print(resp.text)
        results = json.loads(resp.text)
        self.cats[name] = list(set(results))
        if write:
            with open(self.base_dir+"/data/user/"+name+".nlp","w") as f:
                f.write("\t".join([name]+results))

    def delete_category(self,name):
        if name in self.cats: del self.cats[name]
        filename = self.base_dir+"/data/user/"+name+".nlp"
        if os.path.isfile(filename):
            os.remove(filename)

#to test the code
print(Nlp().analyze("Trump is stupid", normalize=True, only_present=True))