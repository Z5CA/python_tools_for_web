from os import listdir
from os.path import isfile, join
from myinit import *
onlyfiles = [f for f in listdir(payload_path) if isfile(join(payload_path, f))]
len_onlyfiles = len(onlyfiles)
for i in range(len_onlyfiles):
    print(i,">",onlyfiles[i])