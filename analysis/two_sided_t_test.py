import numpy as np
from scipy.stats import ttest_ind

alpha = 0.01

# Range benchmark

print("Range benchmark ...")

range_mongo = [0.2944681644439697,0.28916096687316895,0.28372716903686523,0.2791900634765625,0.2728259563446045,0.26642394065856934,0.2685720920562744,0.2707080841064453,0.2879960536956787,0.2799499034881592]
range_couch = [0.031234025955200195,0.014580965042114258,0.010600090026855469,0.007702827453613281,0.010009050369262695,0.007850170135498047,0.008256912231445312,0.008105039596557617,0.007946968078613281,0.008790969848632812]

t, p = ttest_ind(range_mongo, range_couch, equal_var=False)
reject_null_hypothesis = p < alpha
print("t = %g  p = %g" % (t, p))
print("Reject null hypothesis: " + str(reject_null_hypothesis))

# MapReduce benchmark