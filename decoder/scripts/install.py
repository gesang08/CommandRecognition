import os
import sys
lang = sys.argv[1]
path=os.getcwd()
converted_path=""
for i in range(len(path)):
    if path[i]=='/':
        converted_path+="\\"
    converted_path+=path[i]

os.popen("sed 's/($ROOT$)/"+converted_path+"/g' models/%s/_config > models/%s/config" % (lang, lang))
os.popen("sed 's/($ROOT$)/"+converted_path+"/g' models/%s/conf/ivector_extractor.conf_ > models/%s/conf/ivector_extractor.conf" % (lang, lang))
