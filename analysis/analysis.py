import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from numpy import mean

# Results

mongo_cluster_range = [100.93114280700684,71.80550003051758,55.45289897918701,46.0928680896759,55.04187893867493,41.64346694946289,54.222923040390015,53.23900890350342,53.54686093330383,62.96205687522888]
mongo_cluster_mapreduce = [1370.023847103119,1341.8973879814148,1201.9470319747925,1101.0186870098114,925.3350760936737,963.5756092071533,952.7875270843506,902.9152321815491,915.1759791374207,891.0098221302032]
mongo_cluster_aggregation = [71.55515789985657,73.43277192115784,72.37821102142334,66.65902900695801,71.04068994522095,74.20883202552795,79.80509400367737,73.34342813491821,73.93640208244324,79.35453081130981]
mongo_cluster_workload = [2.889254093170166,5.898728847503662,2.1262810230255127,3.3497440814971924,6.472569942474365,3.125412940979004,4.673470973968506,3.9514598846435547,4.459208965301514,5.753173828125]

mongo_cluster_range_indexed = [0.051548004150390625,0.003155946731567383,0.029726028442382812,0.006534099578857422,0.0027680397033691406,0.0018811225891113281,0.001970052719116211,0.0016131401062011719,0.0014078617095947266,0.0014641284942626953]
mongo_cluster_mapreduce_indexed = [961.7279920578003,1113.6034150123596,1048.0824069976807,1054.8998720645905,1019.4707942008972,1010.1945240497589,1064.5851848125458,1113.8588199615479,1163.598140001297,1226.2772281169891]
mongo_cluster_aggregation_indexed = [123.98098516464233,109.95539498329163,123.33184385299683,119.20797681808472,117.25105094909668,126.40408515930176,120.38669800758362,107.85638308525085,120.82602596282959,121.9907579421997]
mongo_cluster_workload_indexed = [0.5037438869476318,0.46160197257995605,0.5094461441040039,0.4451479911804199,0.5410511493682861,0.4662001132965088,0.5513091087341309,0.5034191608428955,0.5136399269104004,0.5340790748596191]

mongo_local_range = [1.537452220916748,1.4982678890228271,1.584867000579834,1.4465100765228271,1.5388529300689697,1.4753007888793945,1.4885880947113037,1.4813950061798096,1.4529831409454346,1.5689620971679688]
mongo_local_mapreduce = [62.19282412528992,65.44253492355347,64.16715788841248,64.48591113090515,61.895941972732544,62.1324360370636,65.70919895172119,68.709645986557,66.3074631690979,63.465463161468506]
mongo_local_aggregation = [3.4584100246429443,3.669288158416748,3.6119561195373535,3.696101188659668,3.694905996322632,3.6486189365386963,3.6786680221557617,3.6790759563446045,3.6201560497283936,3.6455800533294678]
mongo_local_workload = [10.58463191986084,11.393532037734985,12.528899908065796,12.81727409362793,12.542778015136719,13.069864988327026,13.300586938858032,12.517919778823853,12.297145128250122,12.421753883361816]

mongo_local_range_indexed = [0.007910013198852539,0.0006358623504638672,0.0005471706390380859,0.0005609989166259766,0.0004749298095703125,0.0004589557647705078,0.0004680156707763672,0.0004799365997314453,0.0004711151123046875,0.0004448890686035156]
mongo_local_mapreduce_indexed = [65.65224409103394,67.63052201271057,66.34363198280334,63.61748003959656,64.01935386657715,63.476316928863525,64.35691595077515,63.765695095062256,63.046119928359985,67.01061081886292]
mongo_local_aggregation_indexed = [3.665208101272583,3.8204469680786133,3.9059488773345947,3.920048952102661,3.895702838897705,3.886436939239502,3.8630530834198,3.84720516204834,3.8535640239715576,3.8897809982299805]
mongo_local_workload_indexed = [0.20926499366760254,0.1772160530090332,0.20344805717468262,0.19283199310302734,0.2025470733642578,0.2164769172668457,0.29968905448913574,0.2579619884490967,0.2788808345794678,0.2901451587677002]

couch_cluster_range = [0.05099081993103027,0.01820516586303711,0.024192094802856445,0.024460792541503906,0.027560949325561523,0.02137899398803711,0.03088212013244629,0.031225919723510742,0.03730416297912598,0.026895999908447266]
couch_cluster_mapreduce = [85.71805691719055,63.585816860198975,63.444742918014526,63.490386962890625,57.55432605743408,59.880393981933594,52.723257064819336,54.8951690196991,55.33956813812256,60.97784090042114]
couch_cluster_workload = [2.7237250804901123,3.2064437866210938,4.070245981216431,2.7459540367126465,2.644986152648926,2.959406852722168,2.76987886428833,3.4383649826049805,3.506753921508789,3.289702892303467]

couch_local_range = [0.03515315055847168,0.009013891220092773,0.009728193283081055,0.009359121322631836,0.008511781692504883,0.007858037948608398,0.01070713996887207,0.017590045928955078,0.013683080673217773,0.009644031524658203]
couch_local_mapreduce = [15.44310712814331,10.242525815963745,10.181946039199829,9.721312999725342,9.076616048812866,10.87264895439148,9.184498071670532,9.470959186553955,12.332551956176758,10.479483127593994]
couch_local_workload = [2.4130780696868896,2.4163219928741455,2.4111108779907227,2.352385997772217,2.533130168914795,2.601045846939087,2.85852313041687,3.0654098987579346,3.473952054977417,3.4809629917144775]

# Functions

alpha = 0.01

def two_sided_ttest(values_1, values_2):
	print("Values 1 mean: %g" % mean(values_1))
	print("Values 2 mean: %g" % mean(values_2))
	t, p = ttest_ind(values_1, values_2, equal_var=False)
	reject_null_hypothesis = p < alpha
	print("t = %g  p = %g" % (t, p))
	print("Reject null hypothesis: " + str(reject_null_hypothesis))

# Main

print("")

# Mongo cluster index vs non index

print("Mongo cluster range - not indexed vs indexed")
two_sided_ttest(mongo_cluster_range, mongo_cluster_range_indexed)
print("")

print("Mongo cluster mapreduce - not indexed vs indexed")
two_sided_ttest(mongo_cluster_mapreduce, mongo_cluster_mapreduce_indexed)
print("")

print("Mongo cluster aggregation - not indexed vs indexed")
two_sided_ttest(mongo_cluster_aggregation, mongo_cluster_aggregation_indexed)
print("")

print("Mongo cluster workload - not indexed vs indexed")
two_sided_ttest(mongo_cluster_workload, mongo_cluster_workload_indexed)
print("")

# Mongo vs Couch - cluster

print("Mongo cluster range indexed - couch cluster range")
two_sided_ttest(mongo_cluster_range_indexed, couch_cluster_range)
print("")

print("Mongo cluster aggregation indexed - couch cluster mapreduce")
two_sided_ttest(mongo_cluster_aggregation_indexed, couch_cluster_mapreduce)
print("")

print("Mongo cluster workload indexed - couch cluster workload")
two_sided_ttest(mongo_cluster_workload_indexed, couch_cluster_workload)
print("")

# Mongo vs Couch - local

print("Mongo local range indexed - couch local range")
two_sided_ttest(mongo_local_range_indexed, couch_local_range)
print("")

print("Mongo local aggregation indexed - couch local mapreduce")
two_sided_ttest(mongo_local_aggregation_indexed, couch_local_mapreduce)
print("")

print("Mongo local workload indexed - couch local workload")
two_sided_ttest(mongo_local_workload_indexed, couch_local_workload)
print("")

# Barcharts

# Cluster

# Range cluster - mongo indexed vs couch

N = 2
x = np.arange(N)
y = [mean(mongo_cluster_range_indexed)*1000, mean(couch_cluster_range)*1000]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed', 'CouchDB'])
ax.set_ylabel('Milliseconds')
ax.set_title('Range benchmark - cluster')
f.show()

# MapReduce and aggregate cluster - mongo indexed map reduce vs mongo indexed aggregate

N = 2
x = np.arange(N)
y = [mean(mongo_cluster_mapreduce_indexed), mean(mongo_cluster_aggregation_indexed)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MapReduce', 'Aggregation framework'])
ax.set_ylabel('Seconds')
ax.set_title('MongoDB aggregation - cluster')
f.show()

# Mongo aggregation and couchdb mapreduce cluster

N = 2
x = np.arange(N)
y = [mean(mongo_cluster_aggregation_indexed), mean(couch_cluster_mapreduce)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed - Aggregation', 'CouchDB - MapReduce'])
ax.set_ylabel('Seconds')
ax.set_title('Aggregation benchmark - cluster')
f.show()

# Workload benchmark cluster

N = 2
x = np.arange(N)
y = [mean(mongo_cluster_workload_indexed), mean(couch_cluster_workload)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed', 'CouchDB'])
ax.set_ylabel('Seconds')
ax.set_title('Workload benchmark - cluster')
f.show()

# Local

# Range local - mongo indexed vs couch

N = 2
x = np.arange(N)
y = [mean(mongo_local_range_indexed)*1000, mean(couch_local_range)*1000]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed', 'CouchDB'])
ax.set_ylabel('Milliseconds')
ax.set_title('Range benchmark - local')
f.show()

# MapReduce and aggregate local - mongo indexed map reduce vs mongo indexed aggregate

N = 2
x = np.arange(N)
y = [mean(mongo_local_mapreduce_indexed), mean(mongo_local_aggregation_indexed)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MapReduce', 'Aggregation framework'])
ax.set_ylabel('Seconds')
ax.set_title('MongoDB aggregation - local')
f.show()

# Mongo aggregation and couchdb mapreduce local

N = 2
x = np.arange(N)
y = [mean(mongo_local_aggregation_indexed), mean(couch_local_mapreduce)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed - Aggregation', 'CouchDB - MapReduce'])
ax.set_ylabel('Seconds')
ax.set_title('Aggregation benchmark - local')
f.show()

# Workload benchmark local

N = 2
x = np.arange(N)
y = [mean(mongo_local_workload_indexed), mean(couch_local_workload)]
f = plt.figure()
ax = f.add_axes([0.2, 0.15, 0.65, 0.65])
ax.bar(x, y, align='center')
ax.set_xticks(x)
ax.set_xticklabels(['MongoDB indexed', 'CouchDB'])
ax.set_ylabel('Seconds')
ax.set_title('Workload benchmark - local')
f.show()

# Show plots
plt.show()
sys.exit(0)

# BARCHART WITH ERROR BARS STUFF

#width = 0.35       # the width of the bars

#men_std = (2, 3, 4, 1, 2)
#women_std = (3, 5, 2, 3, 3)

#fig, ax = plt.subplots()
#rects1 = ax.bar(x, y, width, color='b', align='center')#, yerr=men_std)
#rects2 = ax.bar(ind, couch_means, width, color='y')#, yerr=women_std)

# add some text for labels, title and axes ticks
#ax.set_ylabel('Seconds')
#ax.set_xlabel('Range benchmark')
#ax.set_title('Benchmark results')
#ax.set_xticks(np.arange(2))
#ax.set_xticklabels(('MongoDB', 'CouchDB'))

#ax.legend((rects1[0], rects2[0]), ('MongoDB indexed', 'CouchDB'))

#def autolabel(rects):
 #   """
 #   Attach a text label above each bar displaying its height
 #   """
#    for rect in rects:
 #       height = rect.get_height()
  #      ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
   #             '%d' % int(height),
    #            ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)

#plt.tick_params(
#    axis='x',          # changes apply to the x-axis
#    which='both',      # both major and minor ticks are affected
#    bottom='off',      # ticks along the bottom edge are off
#    top='off',         # ticks along the top edge are off
#    labelbottom='off') # labels along the bottom edge are off


# OLD STUFF

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