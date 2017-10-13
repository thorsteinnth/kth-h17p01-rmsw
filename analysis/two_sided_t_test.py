import numpy as np
from scipy.stats import ttest_ind
from numpy import mean

alpha = 0.01

# Range benchmark

print("Range benchmark ...")

range_mongo = [0.2944681644439697,0.28916096687316895,0.28372716903686523,0.2791900634765625,0.2728259563446045,0.26642394065856934,0.2685720920562744,0.2707080841064453,0.2879960536956787,0.2799499034881592]
range_couch = [0.031234025955200195,0.014580965042114258,0.010600090026855469,0.007702827453613281,0.010009050369262695,0.007850170135498047,0.008256912231445312,0.008105039596557617,0.007946968078613281,0.008790969848632812]

print("Mongo mean: %g" % mean(range_mongo))
print("Couch mean: %g" % mean(range_couch))

t, p = ttest_ind(range_mongo, range_couch, equal_var=False)
reject_null_hypothesis = p < alpha
print("t = %g  p = %g" % (t, p))
print("Reject null hypothesis: " + str(reject_null_hypothesis))

# MapReduce benchmark

print("MapReduce benchmark ...")

mapreduce_mongo = [18.051552057266235,18.613569021224976,18.319264888763428,17.81685209274292,17.945057153701782,18.78616499900818,18.92860722541809,19.2401340007782,19.187970876693726,17.783262968063354]
mapreduce_couch = [4.510771989822388,3.27237606048584,3.4142661094665527,3.416632890701294,3.4731881618499756,6.38683295249939,6.0542449951171875,3.8828580379486084,9.240603923797607,4.087347030639648]

print("Mongo mean: %g" % mean(mapreduce_mongo))
print("Couch mean: %g" % mean(mapreduce_couch))

t, p = ttest_ind(mapreduce_mongo, mapreduce_couch, equal_var=False)
reject_null_hypothesis = p < alpha
print("t = %g  p = %g" % (t, p))
print("Reject null hypothesis: " + str(reject_null_hypothesis))

# Workload benchmark

print("Workload benchmark ...")

workload_mongo = [6.945255994796753,7.298089981079102,7.059103012084961,7.227065801620483,7.4749579429626465,7.59293007850647,8.128200054168701,8.516998052597046,7.649991035461426,7.728899002075195]
workload_couch = [2.2395811080932617,1.8961679935455322,2.164030075073242,1.8612802028656006,1.9332408905029297,1.900036096572876,2.1305110454559326,2.496000051498413,2.28153395652771,2.447028160095215]

print("Mongo mean: %g" % mean(workload_mongo))
print("Couch mean: %g" % mean(workload_couch))

t, p = ttest_ind(workload_mongo, workload_couch, equal_var=False)
reject_null_hypothesis = p < alpha
print("t = %g  p = %g" % (t, p))
print("Reject null hypothesis: " + str(reject_null_hypothesis))