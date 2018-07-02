import json
from pprint import pprint
import pandas as pd

br_json1 = json.load(open('data4.json', encoding="utf8"))

br_dict_rep={}
br_ls_rep=[]
count=1
for index,item in enumerate(br_json1["@graph"]):
    gbr=item["iri"]
    gbr=gbr.replace("gbr:","").strip()
    br_dict_rep[gbr]="0110"+str(count)
    br_ls_rep.append(gbr)
    br_json1["@graph"][index]["iri"]="gbr:"+"0110"+str(count)
    br_json1["@graph"][index]["label"]=br_json1["@graph"][index]["label"].replace(gbr,str("0110"+str(count)))
    count+=1

with open('br_id.json', 'w', encoding="utf8") as fp:
    json.dump(br_dict_rep, fp, indent=4,ensure_ascii=False)

iden_dict_rep={}
iden_ls_rep=[]
count=1
for index,item in enumerate(br_json1["@graph"]):
    if "identifier" in list(item.keys()):
        for index1,iden_item in enumerate(item["identifier"]):
            gid=iden_item["iri"]
            gid=gid.replace("gid:","").strip()
            iden_dict_rep[gid]="0110"+str(count)
            iden_ls_rep.append(gid)
            br_json1["@graph"][index]["identifier"][index1]["iri"]="gid:"+"0110"+str(count)
            br_json1["@graph"][index]["identifier"][index1]["label"]=iden_item["label"].replace(gid,str("0110"+str(count)))
            count+=1

with open('id_id.json', 'w', encoding="utf8") as fp:
    json.dump(iden_dict_rep, fp, indent=4,ensure_ascii=False)


ar_dict_rep={}
ar_ls_rep=[]
count=1
for index,item in enumerate(br_json1["@graph"]):
    if "contributor" in list(item.keys()):
        for index1,ar_item in enumerate(item["contributor"]):
            gar=ar_item["iri"]
            gar=gar.replace("gar:","").strip()
            ar_dict_rep[gar]="0110"+str(count)
            ar_ls_rep.append(gar)
            br_json1["@graph"][index]["contributor"][index1]["iri"]="gar:"+"0110"+str(count)
            br_json1["@graph"][index]["contributor"][index1]['role_of']["iri"]="gra:"+"0110"+str(count)
            br_json1["@graph"][index]["contributor"][index1]["label"]=ar_item["label"].replace(gar,str("0110"+str(count)))
            br_json1["@graph"][index]["contributor"][index1]['role_of']["label"]=br_json1["@graph"][index]["contributor"][index1]['role_of']["label"].replace("agent 011004","agent 011003").replace("ra/011004","ra/011003").replace(gar,str("0110"+str(count)))
            count+=1

with open('ra_ar_id.json', 'w', encoding="utf8") as fp:
    json.dump(ar_dict_rep, fp, indent=4,ensure_ascii=False)


be_dict_rep={}
be_ls_rep=[]
count=1
for index,item in enumerate(br_json1["@graph"]):
    if "reference" in list(item.keys()):
        for index1,be_item in enumerate(item["reference"]):
            gbe=be_item["iri"]
            gbe=gbe.replace("gbe:","").strip()
            be_dict_rep[gbe]="0110"+str(count)
            be_ls_rep.append(gbe)
            br_json1["@graph"][index]["reference"][index1]["iri"]="gbe:"+"0110"+str(count)
            br_json1["@graph"][index]["reference"][index1]["label"]=be_item["label"].replace(gbe,str("0110"+str(count)))
            crossref=br_json1["@graph"][index]["reference"][index1]["crossref"].replace("gbr:","").strip()
            br_json1["@graph"][index]["reference"][index1]["crossref"]="gbr:"+str(br_dict_rep[crossref])
            count+=1

with open('be_id.json', 'w', encoding="utf8") as fp:
    json.dump(be_dict_rep, fp, indent=4,ensure_ascii=False)

for index,item in enumerate(br_json1["@graph"]):
    if "citation" in list(item.keys()):
        for index1,be_item in enumerate(item["citation"]):
            crossref=br_json1["@graph"][index]["citation"][index1].replace("gbr:","").strip()
            br_json1["@graph"][index]["citation"][index1]="gbr:"+str(br_dict_rep[crossref])

with open('data1.json', 'w', encoding="utf8") as fp:
    json.dump(br_json1, fp, indent=4,ensure_ascii=False)