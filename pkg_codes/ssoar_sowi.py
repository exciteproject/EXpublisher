import pandas as pd
import numpy as np
import json

def rfi(lst):
    return lst[0]
    
def ret_map(text):
    try:
        return str(int(hand_map_dict2[str(text)]))
    except:
        return (np.nan)

def ret_ssoar_handler(txt):
    return txt.split("/")[-1]
    
    
def retunrn_value_for_an_id(id_str,metadatavalue):
    tempdf=metadatavalue[metadatavalue["resource_id"]==int(id_str)][["metadata_field_id","text_value"]]
    tempdf=tempdf.groupby('metadata_field_id').apply(lambda tempdf: tempdf.to_dict(orient='list')).to_dict()
    temp_dict={}
    for key, item in tempdf.items():
        temp_dict[key]=item['text_value']
    return temp_dict

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
    

with open('./support_data/sowiport_duplicates_17_03_14.json') as f:
        sowidublicates = json.load(f)    

with open('./support_data/select.json') as f:
        selectjson = json.load(f) 

dic_selet={}
for item in selectjson["response"]["docs"]:
    try:
        dic_selet[item['id']]=int(item['recordurl_str_mv'][0].split("/")[-1])
    except:
        pass
    
def list_ssoar_dub(sowid):
    lisofdub=sowidublicates.get(sowid,[sowid])
    ls=[]
    for item in lisofdub:
        ssoarid=dic_selet.get(item,"")
        if ssoarid!="":
            ls.append(ssoarid)
    if len(ls)==0:
        ls=np.nan
    else:
        ls=str(int(list(set(ls))[0]))
    return(ls)
    
def sowi_ssoar_match(REF_SSOAR_file="support_data/reference_ssorid_matchedid.csv"):
    match_info = pd.read_csv(REF_SSOAR_file, sep=";")
    ndic=conversowiport_dublicate(sowidublicates)
    ndic1={}
    for key, val in ndic.items():
        for item in val:
            ndic1[item]=key                   
    match_info["ssoar_match"]=match_info["match_id"].apply(list_ssoar_dub)
    match_info["sowi_id"]=match_info[match_info["match_id"]!="not_match"]["match_id"].apply(lambda x: ndic1.get(x,x))   
    match_info["sowi_id"]=match_info["sowi_id"].fillna("not_match")    
    match_info.columns=["ref_id","ref_text","source_ssoar_id","match_id","ssoar_match","sowi_id"]
    match_info=match_info[["ref_id","source_ssoar_id","ref_text","sowi_id","ssoar_match"]]    
    embargo = list(pd.read_csv("./support_data/embargoHandles.txt")["header"].apply(np.int64))
    match_info[~match_info['source_ssoar_id'].isin(embargo)]    
    return match_info
    
    
def sowi_ssoar_match1(REF_SSOAR_file="support_data/reference_ssorid_matchedid.csv"):
    match_info = pd.read_csv(REF_SSOAR_file, sep=";")
    match_info=match_info[["ref_id","ssoar_id","ref_text","match_id"]]
    sowiport_info = pd.read_json("support_data/select.json")
    
    embargo = list(pd.read_csv("support_data/embargoHandles.txt")["header"].apply(np.int64))
    sowiport_info=pd.DataFrame(sowiport_info["response"]["docs"])
    sowiport_ssoar_info=sowiport_info[~sowiport_info["recordurl_str_mv"].isnull()]
    sowiport_ssoar_info["recordurl_str_mv"]=sowiport_ssoar_info["recordurl_str_mv"].apply(rfi)
    match_info.columns=['ref_id','newmodel_ssoar_id', 'ref_text', 'sowi_id']
    sowiport_ssoar_info.columns=['sowi_id', 'recordurl_str_mv']
    match_sowi_ssoar_info=pd.merge(match_info,sowiport_ssoar_info, on='sowi_id', how="left")    
    match_sowi_ssoar_info["ssoar_match"]=match_sowi_ssoar_info[~match_sowi_ssoar_info["recordurl_str_mv"].isnull()]["recordurl_str_mv"].apply(ret_ssoar_handler)
    match_sowi_ssoar_info.columns=['ref_id','source_ssoar_id', 'ref_text', 'sowi_id', 'recordurl_str_mv','ssoar_match']
    match_sowi_ssoar_info_ne=match_sowi_ssoar_info[~match_sowi_ssoar_info['source_ssoar_id'].isin(embargo)]
    match_info_s=match_sowi_ssoar_info_ne[['ref_id','source_ssoar_id', 'ref_text', 'sowi_id','ssoar_match']]
    return match_info_s    

    
def metavalgen(match_info_s):    
    metadatavalue=pd.read_csv("support_data/metadatavalue.csv",sep=";")
    handeler_mapper=metadatavalue[metadatavalue["metadata_field_id"]==25][["resource_id","text_value"]]
    handeler_mapper.columns=["inter_id","handeler"]
    handeler_mapper["handeler"]=handeler_mapper["handeler"].apply(ret_ssoar_handler)
    handeler_mapper.set_index('inter_id', inplace=True)
    hand_map_dict=handeler_mapper.to_dict()
    hand_map_dict=hand_map_dict['handeler']
    hand_map_dict2={}
    for key, val in hand_map_dict.items():
        hand_map_dict2[val]=key
    match_info_s["source_ssoar_int_id"]=match_info_s["source_ssoar_id"].apply(ret_map)
    match_info_s["ssoar_match_int_id"]=match_info_s["ssoar_match"].apply(ret_map)
    metadatavalue.sort_values(by=["resource_id", "metadata_field_id", "resource_type_id"], inplace=True)
    metadatavalue.fillna("nan", inplace=True)
    return metadatavalue