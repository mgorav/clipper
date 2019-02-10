import findspark
findspark.init()

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark import SparkConf, SparkContext
from numpy import array

import sys, os, json, numpy as np, requests
headers = {"Content-type": "application/json"}

from clipper_admin import Clipper
clipper_client  = Clipper("localhost")
clipper_client.start()

clipper_client.get_all_apps()

# An application in Clipper corresponds to a REST prediction endpoint
clipper_client.register_application(
    "hr-hire",
    "pyspark_svm", "ints", "-1.0", 100000)




# Boilerplate Spark stuff:
conf = SparkConf().setMaster("local").setAppName("SparkDecisionTree")
sc = SparkContext(conf = conf)