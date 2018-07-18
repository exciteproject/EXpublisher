from multiprocessing import Pool
from urllib.request import urlopen
import json
import pandas as pd

with open('sowiport_duplicates_17_03_14.json') as f:
        sowidublicates = json.load(f) 

moredublicate=pd.read_csv("dftouse.csv")

def conversowiport_dublicate(dublicateddd):
    ndict={}
    help1={}
    #count=0
    for key, val in dublicateddd.items():
        #count+=1
        #if count%1000000==0:
            #print(count)
        try:
            if (help1[key]==1):
                pass
        except:
            for item in val:
                #[a[i] for i in (1,2,5)]
                ndict[key]=[item , dublicateddd[item]]
                ndict[key] = list(set(flatten(ndict[key])))
                for i in ndict[key]:
                    help1[i]=1;
            
    return ndict

def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list

ndic=conversowiport_dublicate(sowidublicates)
ndic1={}
for key, val in ndic.items():
    for item in val:
        ndic1[item]=key  
moredublicate["dubid"]=moredublicate.id.apply(lambda x: ndic1.get(x,x))
doiset=set(moredublicate.recorddoi_str_mv)


def process_image(item):
    temp=moredublicate[moredublicate["recorddoi_str_mv"]==item]
    if len(set(temp["dubid"]))==1:
        return []
    elif len(temp[temp["doctype_lit_str"]=="Buch"])>0:
        return list(temp[temp["doctype_lit_str"]!="Buch"].index)
    else:
        return list(temp.index)
    
if __name__ == '__main__':
    print(len(moredublicate))
    pool = Pool(20)
    p=pool.map(process_image, list(doiset))
    lindexs=[]
    for item in p:
        for item1 in item:
            lindexs.append(item1)
    lindexs=list(set(lindexs))
    print(len(lindexs))
    moredublicate.drop(list(set(lindexs)),inplace=True)
    moredublicate.to_csv("reult.csv",index=False)
    print(len(moredublicate))
