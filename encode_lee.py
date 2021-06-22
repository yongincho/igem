import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np
import glob, os
plt.rcParams['svg.fonttype'] = 'none'
from re import sub

class Lee(object):

    def nextBase(self, prevBase, wantedTrit):
        transitionTable = {'A0':'G', 'A1':'C', 'A2':'T','C0':'T', 'C1':'G', 'C2':'A','G0':'A', 'G1':'T', 'G2':'C','T0':'C', 'T1':'A', 'T2':'G'}

        return transitionTable[prevBase+str(wantedTrit)]

    def encodeStr(self, inputInfo_string):
        inputInfo = [int(s) for s in list(inputInfo_string)]
        outStr = []
        for i in range(len(inputInfo)):
            if(i==0):
                prevBase = 'G'
            else:
                prevBase = outStr[i-1]
            currtrit = inputInfo[i]

            outStr.append(self.nextBase(prevBase,currtrit))
        return outStr

    def findpossiblehits(self, row):
        curr_seq = row['strandC']
        desired_seq = row['template']
        
        # filter rule - look for strands of a set length and the desired terminal 'C'
        if((len(curr_seq) == len(desired_seq)) and len(curr_seq)>0 and (curr_seq[-1] is desired_seq[-1])):
            return 1
        else:
            return 0

    def decoding(self, df, templateID):
        currdf = df[df["template_ID"]==templateID]
        currdf_possiblehits  = currdf[currdf["possiblehit"]==1]
        print(templateID,currdf.iloc[0]["template"])
        print(currdf_possiblehits['strandC'].value_counts(ascending=False).head(5).to_frame(),"\n\n")


if __name__ == "__main__":

    csv_path = input("Input your csv file: ")

    print("TEST DATA")

    lee = Lee()

    lee.encodeStr("00010212")

    hello_world = ["00010212","00110202","00211000","01011000","01111010","01201012",
                    "02011102","02111010","02211020","10011000","10110201","10201020"]

    for string in hello_world:
        print(string + " " + ''.join(lee.encodeStr(string)))

    print("CSV DATA")
    
    import pandas as pd

    data = pd.read_csv(csv_path, sep=",", header=0,
        dtype={"template_ID":str,"match":int,"template":str,"strandC":str,"strandR":str,"strandR_len":int,"strandC_len":int,"template_align":str,"strand_align":str})

    data["possiblehit"] = data.apply(lee.findpossiblehits,axis=1)

    templates_to_decode = ['H01','H02','H03','H04','H05','H06','H07','H08','H09','H10','H11','H12']

    for template in templates_to_decode: 
        lee.decoding(data,template)
