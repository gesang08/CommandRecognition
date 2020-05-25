import sys
import os

ref_file = sys.argv[1]
hyp_file = sys.argv[2]

refList=[]
hypList=[]

with open(ref_file, 'r') as reff:
    ref_content = reff.readlines()
    for line1 in ref_content:
        line1List = line1.strip('\n').split(' ')
        refList.append(line1List[1])


with open(hyp_file, 'r') as hypf:
    hyp_content = hypf.readlines()
    for line2 in hyp_content:
        line2List = line2.strip('\n').split(' ')
        hypList.append(line2List[1])

corr = 0
for x,y in zip(refList, hypList):
    for i in range(len(x)):
        try:
            if x[i]==y[i]:
                corr = corr + 1
        except:
            continue
print(corr)

