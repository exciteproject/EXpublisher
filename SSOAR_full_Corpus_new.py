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
             
"""
#sowiportharvestor.py

#create_filter
## Generate "fl=" for solr
##fl=id%2Cissn%2Cjournal_full_txt_mv%2Clanguage%2Cnorm_pagerange_str%2Cnorm_publishDate_str%2Ctitle_full%2Cisbn%2C
person_author_txtP_mv%2Crecordfulltext_str_mv%2Crecordurl_str_mv%2Crecordurn_str_mv%2Crecorddoi_str_mv%2C
doctype_lit_str
"""

"""
sowidict
"""
"""
{64: "Ukraine's 1994 Elections as an Economic Event",
 3: ['Kravchuk, Robert S.', 'Chudowsky, Victor'],
 21: ['0967-067X'],
 118: ['Communist and Post-Communist Studies'],
 104: '131-165',
 137: ['10.1016/j.postcomstud.2005.03.001'],
 'handler': 'csa-ps-200522134',
 'language': ['Englisch (EN)'],
 15: '2005'}
 """

def ret_int(x):
    try:
        y=float(x)
        x=int(x)
        return str(x)
    except:
        return np.nan
        
def pre_step_for_preparation(Dublicate_file_sowi='support_data/sowiport_duplicates_17_03_14.json',REF_SSOAR_file="support_data/reference_ssorid_matchedid.csv",ssoar_harvest_flag_collect_data=0):
    sowi_dublicate = json.load(open(Dublicate_file_sowi))
    
    """
    ssoarharvestor.py

    call ssoarharvest("name_of_file_that_save_data")
    it harvests metadata from ssoar

    It is not needed to run each time

    ssoarharvest()
    """
    if ssoar_harvest_flag_collect_data!=0:
        ssoarharvest()
    
    """
    convert ssoar data into python dictionary
    """
    total_ssoar_handler,dictofrecords_h=json_to_new_dict()
    
    """
    Find interlink of ssoar papers based on sowiport match id and meta data
    #match_info_s[~match_info_s["ssoar_match"].isnull()]
    """
    match_info_s=sowi_ssoar_match(REF_SSOAR_file)
    match_info_s["source_ssoar_id"]=match_info_s["source_ssoar_id"].apply(float).apply(int).apply(str)
    match_info_s=match_info_s.drop_duplicates(["source_ssoar_id","ref_text"]).sort("source_ssoar_id")
    """
    remove self citation
    """
    match_info_s=match_info_s[match_info_s["source_ssoar_id"]!=match_info_s["ssoar_match"]]
    #len(match_info_s) #1155974 - 1147429
    #len(set(list(match_info_s["source_ssoar_id"]))) #24310  -24258
    
    match_info_s["ssoar_match"]=match_info_s["ssoar_match"].apply(ret_int)
    ssoar_excit_sc=match_info_s
    listof_ssoar_id=list(set(ssoar_excit_sc["source_ssoar_id"]))
    ssoar_excit_sc["ssoar_match"]=ssoar_excit_sc["ssoar_match"].apply(str)
    ssoar_excit_sc.sort(["source_ssoar_id","ref_id"],inplace=True)
    ssoar_excit_sc.reset_index(drop=True,inplace=True)
    total_ssoar_handler_int=[]
    count_err=0
    for i in total_ssoar_handler:
        try:
            total_ssoar_handler_int.append(int(i))
        except:
            count_err+=1
    
    return total_ssoar_handler_int, ssoar_excit_sc,dictofrecords_h,sowi_dublicate,listof_ssoar_id,total_ssoar_handler
    
def check_validity_sowiport_id(sowiport_id):
    return len(showrecods_result(sowiport_id,create_filter(["id"])))>0
    
def validate_url_stirng(url_str):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url_str) is not None
    
    
def remove_substr_frombegining(inputstr,substr):
    if inputstr.find(substr)==-1:
        return -1
    else:
        return inputstr[inputstr.find(substr)+len(substr):]

def creat_iden_part1(set_source_dict_keys,sowi_id,source_dict):
    id_counter=0
    temp_id_list=[]
    ids_only_list=[]
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        if validate_url_stirng(source_dict[20][0]):
            temp_id_set["type"]="url"
        else:
            temp_id_set["type"]="isbn"
        temp_id_set["id"]=source_dict[20][0]
        ids_only_list.append("gid:0001"+str(sowi_id)+"20")
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"20"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"20"+" [id/0001"+str(sowi_id)+"20"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 137 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        doi_url=source_dict[137][0]
        if validate_url_stirng(doi_url):
            if "https://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"https://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
            elif "http://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"http://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=doi_url
        else:
            temp_id_set["type"]="doi"
            temp_id_set["id"]=doi_url
        #temp_id_set["id"]=source_dict[137][-1]
        #temp_id_set["id"]=source_dict[137][0]
        ids_only_list.append("gid:0001"+str(sowi_id)+"137")
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"137"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"137"+" [id/0001"+str(sowi_id)+"137"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        urn_url=source_dict[85][0]
        if validate_url_stirng(urn_url):
            if "http://hdl.handle.net/" in urn_url:
                urn_url=remove_substr_frombegining(urn_url,"http://hdl.handle.net/")
                temp_id_set["id"]=urn_url
                temp_id_set["type"]="urn"
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=urn_url
        else:
            temp_id_set["type"]="urn"
            temp_id_set["id"]=urn_url
        #temp_id_set["id"]=source_dict[85][-1]
        #temp_id_set["id"]=source_dict[85][0]
        ids_only_list.append("gid:0001"+str(sowi_id)+"85")
        temp_id_set["iri"]="gid:0001"+str(sowi_id)+"85"
        temp_id_set["label"]="identifier 0001"+str(sowi_id)+"85"+" [id/0001"+str(sowi_id)+"85"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
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
    
def Gen_replacement_id(id_rep,dict_name_id):
    if id_rep in list(dict_name_id.keys()):
        id_rep=dict_name_id[id_rep]
    else:
        if not bool(dict_name_id):
            dict_name_id[id_rep]=0
            id_rep=0
        else:
            max_int=max(dict_name_id.iteritems(), key=operator.itemgetter(1))[0]+1
            dict_name_id[id_rep]=max_int
            id_rep=max_int
    return be_dict_name_id,be_id_rep
    
    
def json_generator(listof_ssoar_id):
    list_of_br=[]
    ls_seen_sowiport=[]
    dict_seen_sowiport={}
    for ssoar_id in listof_ssoar_id:
        tem_df=ssoar_excit_sc[ssoar_excit_sc["source_ssoar_id"]==ssoar_id]
        index_temp_df=list(tem_df.index)
        ref_list_be=[]
        ref_list_cit_br=[]
        br_temp={}
        for index_references_in_a_pdf in index_temp_df:
            be_dict={"iri":"gbe:0000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"]),
                        "a":"entry",
                        "label": "bibliographic entry 0000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+" [be/0000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]",
                        "content":tem_df.ix[index_references_in_a_pdf]["ref_text"]}
        
            if tem_df.ix[index_references_in_a_pdf]["ssoar_match"]!='nan' and tem_df.ix[index_references_in_a_pdf]["ssoar_match"] in total_ssoar_handler:
                    be_dict["crossref"]="gbr:0000"+str(tem_df.ix[index_references_in_a_pdf]["ssoar_match"])
                    
            elif tem_df.ix[index_references_in_a_pdf]["sowi_id"]!='error' and tem_df.ix[index_references_in_a_pdf]["sowi_id"]!='not_match':
                sowid_item=tem_df.ix[index_references_in_a_pdf]["sowi_id"]
                try:
                    setofdubsowi=set(sowi_dublicate[sowid_item])
                except: 
                    setofdubsowi=set([sowid_item])
                listinter_sowid=list(set(ls_seen_sowiport).intersection(setofdubsowi))
                if len(listinter_sowid)>0:
                    be_dict["crossref"]="gbr:0001"+dict_seen_sowiport[listinter_sowid[0]]
                else:
                    try:
                        be_dict["crossref"]="gbr:0001"+sowid_item
                        br_temp1=sowiport_br(tem_df.ix[index_references_in_a_pdf]["ref_id"],tem_df.ix[index_references_in_a_pdf]["sowi_id"])
                        list_of_br.append(br_temp1)
                        ls_seen_sowiport.append(sowid_item)
                        dict_seen_sowiport[sowid_item]=sowid_item
                    except Exception as e: 
                        print(e)
                        print(tem_df.ix[index_references_in_a_pdf]["sowi_id"])
                        be_dict["crossref"]="gbr:2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        br_temp1={"a":["document"], 
                            "label":"bibliographic resource 2000"+
                            str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+
                            " [br/2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]"}
                        br_temp1["iri"]="gbr:2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        list_of_br.append(br_temp1)                                   
            else:
                be_dict["crossref"]="gbr:2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                br_temp1={"a":["document"], 
                          "label":"bibliographic resource 2000"+
                          str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+
                          " [br/2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])+"]"}
                br_temp1["iri"]="gbr:2000"+str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                list_of_br.append(br_temp1)
            if tem_df.ix[index_references_in_a_pdf]["ssoar_match"]!=str(ssoar_id):    
                ref_list_be.append(be_dict)
                ref_list_cit_br.append(be_dict["crossref"])
                
        if len(ref_list_be) >0:   
            br_temp["reference"]=ref_list_be
            br_temp["citation"]=ref_list_cit_br
        br_temp["iri"]="gbr:0000"+str(ssoar_id)
        #source_dict=eval(tem_df.ix[index_references_in_a_pdf]["ssoar_source_dict"])
        #indexforssoardict=str(tem_df.ix[index_references_in_a_pdf]["source_ssoar_id"])
        source_dict=dictofrecords_h[str(ssoar_id)]

        br_temp["a"]=["document",source_dict[101].replace("incollection","inbook").replace("recension","review").replace("monograph","book")]

        list_source_dict_keys=list(source_dict.keys())
        setofindex_pd={111,104,116,118,119}
        set_source_dict_keys=set(list_source_dict_keys)
        checkmylenght=list(setofindex_pd.intersection(set_source_dict_keys))
        if  len(checkmylenght)>0:
            gre_dict={"iri":"gre:0110020000"+str(ssoar_id), "a": [ "generic_format", "digital_format"], "label": "resource embodiment 0110020000"+str(ssoar_id)+ " [re/0110020000"+str(ssoar_id)+ "]","mime_type": "pdf"}
            if 104 in checkmylenght:
                if '-' in source_dict[104]:
                    gre_dict["fpage"]=str(source_dict[104]).split('-')[0]
                    gre_dict["lpage"]=str(source_dict[104]).split('-')[1]
        
        
        cont_list=[]
        if 3 in list(source_dict.keys()):
            for index_aut,author_item in enumerate(source_dict[3]):
                ar_dict={"iri": "gar:000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id), "a":"role",
                         "label": "agent role 000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+" [ar/000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+"]",       
                         "role_type": "author", 
                         "role_of": {"iri": "gra:000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id), "a":"agent",
                         "label": "responsible agent 000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+" [ra/000000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+"]",
                                }
                         }
                ais_ls=author_item.split(",")
                if len(ais_ls)>1:
                    ar_dict["role_of"]["fname"]= ais_ls[0]            
                    ar_dict["role_of"]["gname"]= ais_ls[1]
                else:
                    ar_dict["role_of"]["name"]=ais_ls[0]
                
                cont_list.append(ar_dict)
                
        #--------------------------------------------------------------------------------------------------------
        if 39 in list(source_dict.keys()):
            for index_aut,author_item in enumerate([source_dict[39]]):
                ar_dict={"iri": "gar:010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id), "a":"role",
                         "label": "agent role 010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+" [ar/010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+"]",       
                         "role_type": "publisher", 
                         "role_of": {"iri": "gra:010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id), "a":"agent",
                         "label": "responsible agent 010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+" [ra/010000"+str("{0:0=2d}".format(index_aut))+str(ssoar_id)+"]",
                                }
                         }
                ais_ls=author_item.replace("(ed.)","")
                ar_dict["role_of"]["name"]=ais_ls
                
                cont_list.append(ar_dict)
        
        
        #--------------------------------------------------------------------------------------------------------

        br_temp["label"]= "bibliographic resource 0000"+str(ssoar_id)+" [br/0000"+str(ssoar_id)+"]"
        br_temp["title"]=source_dict[64]
        if len(cont_list):
            br_temp["contributor"]=cont_list
        year_entity = re.findall('(\d{4})',source_dict[15])
        br_temp["date"]={"value":str(year_entity[0]),"a":"year"}
        only_id_list,temp_id_list=creat_iden_part(set_source_dict_keys,ssoar_id,source_dict)
        if len(temp_id_list)>0:
            br_temp["identifier"]=temp_id_list
        
        if "reference" in list(br_temp.keys()):
            list_of_br.append(br_temp)
    return list_of_br
    
    
def Generat_br_for_remained_match(cross_ref_list):
    br_list=[]
    for br_rec_new_id in cross_ref_list:
        try:
            source_dict=dictofrecords_h[br_rec_new_id]
            br_temp={"iri": "gbr:0000"+br_rec_new_id,
                      "a":["document",source_dict[101].replace("incollection","inbook").replace("recension","review").replace("monograph","book")], 
                      "label":"bibliographic resource 0000"+br_rec_new_id+" [br/0000"+br_rec_new_id+"]",
                      "title":source_dict[64]
                     }
            cont_list=[]
            if 3 in list(source_dict.keys()):
                for index_aut,author_item in enumerate(source_dict[3]):
                    ar_dict={"iri": "gar:000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id, "a":"role",
                             "label": "agent role 000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+" [ar/000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+"]",       
                             "role_type": "author", 
                             "role_of": {"iri": "gra:000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id, "a":"agent",
                             "label": "responsible agent 000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+" [ra/000000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+"]",
                            }
                         }
                    ais_ls=author_item.split(",")
                    if len(ais_ls)>1:
                        ar_dict["role_of"]["fname"]= ais_ls[0]            
                        ar_dict["role_of"]["gname"]= ais_ls[1]
                    else:
                        ar_dict["role_of"]["name"]=ais_ls[0]
                    cont_list.append(ar_dict)
                    
            #-------------------------------------------------------------------------------------------------
            if 39 in list(source_dict.keys()):
                for index_aut,author_item in enumerate([source_dict[39]]):
                    ar_dict={"iri": "gar:010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id, "a":"role",
                             "label": "agent role 010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+" [ar/010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+"]",       
                             "role_type": "publisher", 
                             "role_of": {"iri": "gra:010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id, "a":"agent",
                             "label": "responsible agent 010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+" [ra/010000"+str("{0:0=2d}".format(index_aut))+br_rec_new_id+"]",
                            }
                         }
                    ais_ls=author_item.replace("(ed.)","")
                    ar_dict["role_of"]["name"]=ais_ls
                    cont_list.append(ar_dict)
            
            
            
            #-------------------------------------------------------------------------------------------------
            if len(cont_list)>0:        
                br_temp["contributor"]=cont_list
            year_entity = re.findall('(\d{4})',source_dict[15])
            br_temp["date"]={"value":str(year_entity[0]),"a":"year"}
            list_source_dict_keys=list(source_dict.keys())
            set_source_dict_keys=set(list_source_dict_keys)
            only_id_list,temp_id_list=creat_iden_part(set_source_dict_keys,int(br_rec_new_id),source_dict)
            if len(temp_id_list)>0:
                br_temp["identifier"]=temp_id_list
            br_list.append(br_temp)
            #print(source_dict)
        except:
            pass
        #tem_br_rec["iri"]="gbr:0110050000"+str(br_rec_new_id)
        #br_temp["a"]=["document",source_dict[101].replace("incollection","inbook").replace("recension","ReviewArticle")]
    return br_list
        
        
def Generate_Flatten_json_OCC_For_SSOAR(REF_SSOAR_file="support_data/reference_ssorid_matchedid.csv",Target_dir="data"):  
    Dublicate_file_sowi='support_data/sowiport_duplicates_17_03_14.json'
    global total_ssoar_handler_int
    global ssoar_excit_sc
    global ssoar_excit_sc
    global dictofrecords_h
    global sowi_dublicate
    global listof_ssoar_id
    global total_ssoar_handler
    total_ssoar_handler_int, ssoar_excit_sc,dictofrecords_h,sowi_dublicate,listof_ssoar_id,total_ssoar_handler=pre_step_for_preparation(Dublicate_file_sowi,REF_SSOAR_file) 
    deltaset=set(listof_ssoar_id)-set(total_ssoar_handler)
    listof_ssoar_id1=list(set(listof_ssoar_id)-deltaset)
    listof_ssoar_id1.sort()
    list_of_br=json_generator(listof_ssoar_id1)
    df_br_list=pd.DataFrame(list_of_br)
    cross_ref_list=[]
    for item in list(df_br_list[~df_br_list["reference"].isnull()]["reference"]):
        for item1 in item:
            cross_ref_list.append(item1["crossref"])
    list_iri=list(set(list(df_br_list["iri"])))
    cross_ref_list2=[]
    for item in list(set(cross_ref_list)-set(list_iri)):# referenced but not exist in br # please check
        if item.startswith("gbr:0000"):
            cross_ref_list2.append(item.replace("gbr:0000",""))

    list_of_br_extra=Generat_br_for_remained_match(cross_ref_list2)
    list_of_br=list_of_br_extra+list_of_br
    br_json={}
    br_json["iri"]="gbr:"
    br_json["@context"]="context.json"
    br_json["@graph"]=[]
    br_json["@graph"]=list_of_br
    
    now = datetime.datetime.now()
    uniquer_token=str(now).replace(" ","").replace("-","").replace(":","").replace(".","")
    with open(Target_dir+'/'+'0001'+'.json', 'w', encoding="utf8") as fp:
        json.dump(br_json, fp, indent=4,ensure_ascii=False)
    return uniquer_token
    
def Replace_ids_in_flaten_json(uniquer_token,Target_dir):
    br_json1 = json.load(open(Target_dir+'/'+uniquer_token+'.json', encoding="utf8"))
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
    with open(Target_dir+'/br_id_'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
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
    
    with open(Target_dir+'/id_id_'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
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
    
    with open(Target_dir+'/ra_ar_id_'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
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
    
    with open(Target_dir+'/be_id_'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
        json.dump(be_dict_rep, fp, indent=4,ensure_ascii=False)
    
    
    for index,item in enumerate(br_json1["@graph"]):
        if "citation" in list(item.keys()):
            for index1,be_item in enumerate(item["citation"]):
                crossref=br_json1["@graph"][index]["citation"][index1].replace("gbr:","").strip()
                br_json1["@graph"][index]["citation"][index1]="gbr:"+str(br_dict_rep[crossref])
    
    
    with open(Target_dir+'/data_'+uniquer_token+'_1.json', 'w', encoding="utf8") as fp:
        json.dump(br_json1, fp, indent=4,ensure_ascii=False)
