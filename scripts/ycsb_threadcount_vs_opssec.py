import sys
import os
from subprocess import call

def getHelpText():
	return "Usage: python XXX.py [YCSB folder path] [output folder path] [mongodb/couchdb]"

# Input parameter parsing

if len(sys.argv) != 4:
    print(getHelpText())
    sys.exit(0)

ycsb_path = str(sys.argv[1])
print("YCSB path: " + ycsb_path)

output_path = str(sys.argv[2])
print("Output path: " + output_path)

db_to_use = str(sys.argv[3])
if not (db_to_use == "mongodb" or db_to_use == "couchdb"):
	print(getHelpText())
	sys.exit(0)

thread_counts = [1, 2, 4, 8, 16, 32, 64, 128]

for thread_count in thread_counts:
	print("Running with " + str(thread_count) + " threads ...")
	output_file_name = output_path + "/ycsb_output_" + db_to_use + "_threads_vs_opssec_numthreads_" + str(thread_count) + ".txt"
	output_file = open(output_file_name, "w")
	if db_to_use == "mongodb":
		call(["./bin/ycsb", "run", "mongodb-async", "-s", "-P", "workloads/workloada_mongocouch", "-p", "mongodb.url=mongodb://localhost:27017/ycsb", "-threads", str(thread_count)], cwd=ycsb_path, stdout=output_file)
	elif db_to_use == "couchdb":
		print("TODO Set couch db call")
	output_file.close()
