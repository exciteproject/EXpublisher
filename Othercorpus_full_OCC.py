import urllib
from urllib.request import urlopen
import json
import re
from pkg_codes.sowiportharvestor import *
from pkg_codes.ssoarharvestor import *
from pkg_codes.aux_funs import *
from pkg_codes.convert_ssoar_dict import *
import numpy as np
import operator
import re
from pkg_codes.ssoar_sowi import *
import json
import datetime
from pprint import pprint
import pandas as pd


filter_list=["id","issn","journal_full_txt_mv","language","norm_pagerange_str","norm_publishDate_str",
             "title_full","isbn","person_author_txtP_mv","recordfulltext_str_mv","recordurl_str_mv",
             "recordurn_str_mv","recorddoi_str_mv","doctype_lit_str","publisher"]


regexurlfilter = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
def validate_url_stirng(url_str):
    return re.match(regexurlfilter, url_str) is not None 

#========================================
with open('support_data/urlexts.txt', 'r') as f:
    urlexts = f.readlines()
urlexts1=[]
for ext_url in urlexts:
        urlexts1.append(ext_url.replace("\n","").strip()[1:].split(".")[-1])
urlexts1=list(set(urlexts1))
#=======================================    

def check_url_ext(urlselected):
    if urlselected[-1] == "/":
        urlselected=urlselected[:-1]
    if urlselected.split(".")[-1] in urlexts1:
        return False
    else:
        return True 

progisbn = re.compile("^([0-9]+(\-|\_)*)*[0-9]*[a-zA-Z]*$")        
def valfilter_isbn(isbn):   
    result=progisbn.match(isbn)
    if result:
        return True
    else:
        return False  


def remove_substr_frombegining(inputstr,substr):
    if inputstr.find(substr)==-1:
        return -1
    else:
        return inputstr[inputstr.find(substr)+len(substr):]

def doiurlcheck(urldoi):
    r = requests.get(urldoi)
    if r.url[:18]!="https://dx.doi.org":
        return True
    else:
        return False  

progdoi = re.compile("^10.\d{4,9}\/[-._;()\/:A-Z0-9a-z]+$")
def valfilter_doi(doicheck):
    result=progdoi.match(doicheck) 
    if result:
        return True
    else:
        return False        

progurn = re.compile("^urn:[a-z0-9][a-z0-9-]{0,31}:([a-z0-9()+,\-.:=@;$_!*']|%[0-9a-f]{2})+$")
def valfilter_urn(urncheck):
    result=progurn.match(urncheck)
    if result:
        return True
    else:
        return False


with open('support_data/doi_sowi_correctedversion.json') as f:
    doi_sowi_correctedversion = json.load(f)
doi_sowi_correctedversion_key=list(doi_sowi_correctedversion.keys())        
#sowidupids = json.load(open("support_data/sowiport_duplicates_17_03_14.json", encoding="utf8"))        
def creat_iden_part1(set_source_dict_keys,sowi_id,source_dict):
    temp_id_list=[]
    ids_only_list=[]
    
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["id"]=source_dict[20][0]
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"20"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"20"+" [id/0001"+str(sowi_id)+"20"+"]"
        if validate_url_stirng(temp_id_set["id"]):
            temp_id_set["type"]="url"
            if check_url_ext(temp_id_set["id"])==True:
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0001"+str(sowi_id)+"20")
        else:
            temp_id_set["type"]="isbn"
            if valfilter_isbn(temp_id_set["id"]):
                temp_id_list.append(temp_id_set) 
                ids_only_list.append("gid:0001"+str(sowi_id)+"20")
    
    #======================================================================
    if 137 in list(set_source_dict_keys) and sowi_id in doi_sowi_correctedversion_key:
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        doi_url=source_dict[137][0]
        #temp_id_set["id"]=source_dict[137][-1]
        #temp_id_set["id"]=source_dict[137][0]
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"137"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"137"+" [id/0001"+str(sowi_id)+"137"+"]"
        #numberofreturn=return_numfound_sowiport("recorddoi_str_mv","10.1093/ijpor")
        #and (numberofreturn<len(sowidupids.get(sowi_id,[])))
        if validate_url_stirng(doi_url):
            if "https://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"https://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
                if valfilter_doi(doi_url):
                    #if doiurlcheck("https://dx.doi.org/"+doi_url):
                        temp_id_list.append(temp_id_set)
                        ids_only_list.append("gid:0001"+str(sowi_id)+"137")
            elif "http://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"http://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
                if valfilter_doi(doi_url):
                    #if doiurlcheck("https://dx.doi.org/"+doi_url):
                        temp_id_list.append(temp_id_set)
                        ids_only_list.append("gid:0001"+str(sowi_id)+"137")
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=doi_url
                if check_url_ext(doi_url):
                    temp_id_list.append(temp_id_set)
                    ids_only_list.append("gid:0001"+str(sowi_id)+"137")
        else:
            temp_id_set["type"]="doi"
            temp_id_set["id"]=doi_url
            if valfilter_doi(doi_url):
                    #if doiurlcheck("https://dx.doi.org/"+doi_url):
                        temp_id_list.append(temp_id_set)
                        ids_only_list.append("gid:0001"+str(sowi_id)+"137")
    #========================================================================
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        urn_url=source_dict[85][0]
        #temp_id_set["id"]=source_dict[85][-1]
        #temp_id_set["id"]=source_dict[85][0]
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"85"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"85"+" [id/0001"+str(sowi_id)+"85"+"]"
        
        if validate_url_stirng(urn_url):
            if "http://hdl.handle.net/" in urn_url:
                urn_url=remove_substr_frombegining(urn_url,"http://hdl.handle.net/")
                temp_id_set["id"]=urn_url
                temp_id_set["type"]="urn"
                if valfilter_urn(urn_url):
                    temp_id_list.append(temp_id_set)
                    ids_only_list.append("gid:0001"+str(sowi_id)+"85")
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=urn_url
                if check_url_ext(urn_url):
                    temp_id_list.append(temp_id_set)
                    ids_only_list.append("gid:0001"+str(sowi_id)+"85")
        else:
            temp_id_set["type"]="urn"
            temp_id_set["id"]=urn_url
            if valfilter_urn(urn_url):
                    temp_id_list.append(temp_id_set)
                    ids_only_list.append("gid:0001"+str(sowi_id)+"85")
       
    return ids_only_list,temp_id_list
    
def sowiport_br(ref_id,sowi_id):
    br_temp1={"a":["document"], 
              "label":"bibliographic resource 0001"+
               sowi_id+" [br/0001"+sowi_id+"]"}
    br_temp1["iri"]="gbr:0001"+sowi_id  
    sowi_dict=showrecods_sowiport_id(sowi_id,create_filter(filter_list))
    if 64 in list(sowi_dict.keys()):
        br_temp1["title"]=sowi_dict[64]
    if 15 in list(sowi_dict.keys()):    
        br_temp1["date"]={"value":str(sowi_dict[15]),"a":"year"}
        
    cont_list=[]    
    if 3 in list(sowi_dict.keys()):
        for index_aut,author_item in enumerate(sowi_dict[3]):
            ar_dict={"iri": "gar:000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id), "a":"role",
                         "label": "agent role 000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+" [ar/000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+"]",       
                         "role_type": "author", 
                         "role_of": {"iri": "gra:000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id), "a":"agent",
                         "label": "responsible agent 000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+" [ra/000001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+"]",
                                }
                         }    
            ais_ls=author_item.replace("(ed.)","").split(",")
            if len(ais_ls)>1:
                ar_dict["role_of"]["fname"]= ais_ls[0]            
                ar_dict["role_of"]["gname"]= ais_ls[1]
            else:
                ar_dict["role_of"]["name"]=ais_ls[0]
            
            cont_list.append(ar_dict)
            
            
        #--------------------------------------------------------------------------------------------------------
    if 39 in list(sowi_dict.keys()):
         for index_aut,author_item in enumerate(sowi_dict[39]):
            ar_dict={"iri": "gar:010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id), "a":"role",
                         "label": "agent role 010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+" [ar/010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+"]",       
                         "role_type": "publisher", 
                         "role_of": {"iri": "gra:010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id), "a":"agent",
                         "label": "responsible agent 010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+" [ra/010001"+str("{0:0=2d}".format(index_aut))+str(sowi_id)+"]",
                                }
                         }    
            ais_ls=author_item.replace("(ed.)","")
            ar_dict["role_of"]["name"]=ais_ls
            
            cont_list.append(ar_dict)
        
        #---------------------------------------------------------------------------------------------------------
        
    if len(cont_list)>0:        
        br_temp1["contributor"]=cont_list
    set_source_dict_keys=set(list(sowi_dict.keys()))
    only_id_list,temp_id_list=creat_iden_part1(set_source_dict_keys,sowi_id,sowi_dict)
    if len(temp_id_list)>0:
        br_temp1["identifier"]=temp_id_list
    return br_temp1


def json_generator(listof_paper_id,Corpus_id,paper_df):
    list_of_br=[]
    ls_seen_sowiport=[]
    for paper_id in listof_paper_id:
        tem_df=paper_df[paper_df["ssoar_id"]==paper_id]
        index_temp_df=list(tem_df.index)
        ref_list_be=[]
        ref_list_cit_br=[]
        br_temp={}
        
        
        #######################
        if Corpus_id!="0005":
            #######
            br_temp=sowiport_br("default",paper_id)
            #remove rest of br_temp
        else:
            br_temp["iri"]="gbr:"+Corpus_id+str(paper_id)
            br_temp["a"]=["document"]
            br_temp["label"]= "bibliographic resource "+Corpus_id+str(paper_id)+" [br/"+Corpus_id+str(paper_id)+"]"
        ######################
        
        
        for index_references_in_a_pdf in index_temp_df:
            be_dict={"iri":"gbe:"+Corpus_id+str(tem_df.ix[index_references_in_a_pdf]["ref_id"]),
                        "a":"entry",
                        "label": "bibliographic entry "+Corpus_id+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+" [be/"+Corpus_id+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]",
                        "content":tem_df.ix[index_references_in_a_pdf]["ref_text"]}
                    
            if tem_df.ix[index_references_in_a_pdf]["match_id"]!='error' and tem_df.ix[index_references_in_a_pdf]["match_id"]!='not_match':
                sowid_item=tem_df.ix[index_references_in_a_pdf]["match_id"]
                if sowid_item in ls_seen_sowiport:
                    be_dict["crossref"]="gbr:0001"+sowid_item
                else:
                    try:
                        be_dict["crossref"]="gbr:0001"+sowid_item
                        br_temp1=sowiport_br(tem_df.ix[index_references_in_a_pdf]["ref_id"],sowid_item)
                        list_of_br.append(br_temp1)
                        ls_seen_sowiport.append(sowid_item)
                    #except Exception as e: 
                    except:
                        #print(e)
                        be_dict["crossref"]="gbr:2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        br_temp1={"a":["document"], 
                            "label":"bibliographic resource 2"+Corpus_id[1:]+
                            str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+
                            " [br/2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]"}
                        br_temp1["iri"]="gbr:2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        list_of_br.append(br_temp1)                                   
            else:
                be_dict["crossref"]="gbr:2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                br_temp1={"a":["document"], 
                          "label":"bibliographic resource 2"+Corpus_id[1:]+
                          str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+
                          " [br/2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]"}
                br_temp1["iri"]="gbr:2"+Corpus_id[1:]+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                list_of_br.append(br_temp1)
                
            ref_list_be.append(be_dict)
            ref_list_cit_br.append(be_dict["crossref"])
                
        if len(ref_list_be) >0:   
            br_temp["reference"]=ref_list_be
            br_temp["citation"]=ref_list_cit_br
        
            
        list_of_br.append(br_temp)
    return list_of_br


def Generate_data_other_corpus(Target_dir="data",ID_courpus="0005",SourceDir="match_table.csv"):
    match_info = pd.read_csv(SourceDir,sep=";")
    match_info["ssoar_id"]=match_info["ssoar_id"].apply(int)
    listofpapers=list(set(match_info["ssoar_id"]))
    list_of_br=json_generator(listofpapers,ID_courpus,match_info)
    br_json={}
    br_json["iri"]="gbr:"
    br_json["@context"]="context.json"
    br_json["@graph"]=[]
    br_json["@graph"]=list_of_br
    now = datetime.datetime.now()
    uniquer_token=str(now).replace(" ","").replace("-","").replace(":","").replace(".","")
    #with open(Target_dir+'/'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
    with open(Target_dir+'/'+ID_courpus+'.json', 'w', encoding="utf8") as fp:
        json.dump(br_json, fp, indent=4,ensure_ascii=False)
    return uniquer_token
