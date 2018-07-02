import urllib
from urllib.request import urlopen
import json
import re
from sowiportharvestor import *
from ssoarharvestor import *
from aux_funs import *
from convert_ssoar_dict import *
import numpy as np
import operator

filter_list=["id","issn","journal_full_txt_mv","language","norm_pagerange_str","norm_publishDate_str",
             "title_full","isbn","person_author_txtP_mv","recordfulltext_str_mv","recordurl_str_mv",
             "recordurn_str_mv","recorddoi_str_mv","doctype_lit_str"]

#sowidict=showrecods_sowiport_id("csa-ps-200522134",create_filter(filter_list))

sowi_dublicate = json.load(open('sowiport_duplicates_17_03_14.json'))

#ssoarharvest()

total_ssoar_handler,dictofrecords_h=json_to_new_dict()

from ssoar_sowi import *

match_info_s=sowi_ssoar_match()

match_info_s["source_ssoar_id"]=match_info_s["source_ssoar_id"].apply(float).apply(int).apply(str)

match_info_s=match_info_s.drop_duplicates(["source_ssoar_id","ref_text"]).sort_values("source_ssoar_id")

match_info_s=match_info_s[match_info_s["source_ssoar_id"]!=match_info_s["ssoar_match"]]

def ret_int(x):
    try:
        y=float(x)
        x=int(x)
        return str(x)
    except:
        return np.nan


match_info_s["ssoar_match"]=match_info_s["ssoar_match"].apply(ret_int)

#metadatavalue=metavalgen(match_info_s)

#internal id
#example_dict=retunrn_value_for_an_id(34979,metadatavalue)

ssoar_excit_sc=match_info_s

listof_ssoar_id=list(set(ssoar_excit_sc["source_ssoar_id"]))

ssoar_excit_sc["ssoar_match"]=ssoar_excit_sc["ssoar_match"].apply(str)

ssoar_excit_sc.reset_index(drop=True,inplace=True)

total_ssoar_handler_int=[]
count_err=0
for i in total_ssoar_handler:
    try:
        total_ssoar_handler_int.append(int(i))
    except:
        count_err+=1



def creat_iden_part1(set_source_dict_keys,sowi_id,source_dict):
    id_counter=0
    temp_id_list=[]
    ids_only_list=[]
    if 21 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="issn"
        temp_id_set["id"]=source_dict[21][0]
        ids_only_list.append("gid:01100105"+str(sowi_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100105"+str(sowi_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100105"+str(sowi_id)+str(id_counter)+" [id/01100105"+str(sowi_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="isbn"
        #temp_id_set["id"]=source_dict[20][-1]
        temp_id_set["id"]=source_dict[20][0]
        ids_only_list.append("gid:01100105"+str(sowi_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100105"+str(sowi_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100105"+str(sowi_id)+str(id_counter)+" [id/01100105"+str(sowi_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 137 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="doi"
        #temp_id_set["id"]=source_dict[137][-1]
        temp_id_set["id"]=source_dict[137][0]
        ids_only_list.append("gid:01100105"+str(sowi_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100105"+str(sowi_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100105"+str(sowi_id)+str(id_counter)+" [id/01100105"+str(sowi_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="urn"
        #temp_id_set["id"]=source_dict[85][-1]
        temp_id_set["id"]=source_dict[85][0]
        ids_only_list.append("gid:01100105"+str(sowi_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100105"+str(sowi_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100105"+str(sowi_id)+str(id_counter)+" [id/01100105"+str(sowi_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    return ids_only_list,temp_id_list


def sowiport_br(ref_id, sowi_id):
    br_temp1 = {"a": ["document"],
                "label": "bibliographic resource 0110050001" +
                         str(ref_id) + " [br/0110050001" + str(ref_id) + "]"}
    br_temp1["iri"] = "gbr:0110050001" + str(ref_id)
    sowi_dict = showrecods_sowiport_id(sowi_id, create_filter(filter_list))
    if 64 in list(sowi_dict.keys()):
        br_temp1["title"] = sowi_dict[64]
    if 15 in list(sowi_dict.keys()):
        br_temp1["date"] = {"value": str(sowi_dict[15]), "a": "year"}

    cont_list = []
    if 3 in list(sowi_dict.keys()):
        for index_aut, author_item in enumerate(sowi_dict[3]):
            ar_dict = {"iri": "gar:0110030001" + str(index_aut) + str(sowi_id), "a": "role",
                       "label": "agent role 0110030001" + str(index_aut) + str(sowi_id) + " [ar/0110030001" + str(
                           index_aut) + str(sowi_id) + "]",
                       "role_type": "author",
                       "role_of": {"iri": "gra:0110040001" + str(index_aut) + str(sowi_id), "a": "agent",
                                   "label": "responsible agent 0110040001" + str(index_aut) + str(
                                       sowi_id) + " [ra/0110040001" + str(index_aut) + str(sowi_id) + "]",
                                   }
                       }
            ais_ls = author_item.split(",")
            if len(ais_ls) > 1:
                ar_dict["role_of"]["fname"] = ais_ls[0]
                ar_dict["role_of"]["gname"] = ais_ls[1]
            else:
                ar_dict["role_of"]["name"] = ais_ls[0]

            cont_list.append(ar_dict)
    if len(cont_list) > 0:
        br_temp1["contributor"] = cont_list
    set_source_dict_keys = set(list(sowi_dict.keys()))
    only_id_list, temp_id_list = creat_iden_part1(set_source_dict_keys, sowi_id, sowi_dict)
    if len(temp_id_list) > 0:
        br_temp1["identifier"] = temp_id_list
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
    list_of_br = []
    ls_seen_sowiport = []
    dict_seen_sowiport = {}
    for ssoar_id in listof_ssoar_id:
        tem_df = ssoar_excit_sc[ssoar_excit_sc["source_ssoar_id"] == ssoar_id]
        index_temp_df = list(tem_df.index)
        ref_list_be = []
        ref_list_cit_br = []
        br_temp = {}
        for index_references_in_a_pdf in index_temp_df:
            be_dict = {"iri": "gbe:011001" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"]),
                       "a": "entry",
                       "label": "bibliographic entry 011001" + str(
                           tem_df.ix[index_references_in_a_pdf]["ref_id"]) + " [be/011001" + str(
                           tem_df.ix[index_references_in_a_pdf]["ref_id"]) + "]",
                       "content": tem_df.ix[index_references_in_a_pdf]["ref_text"]}

            if tem_df.ix[index_references_in_a_pdf]["ssoar_match"] != 'nan' and tem_df.ix[index_references_in_a_pdf][
                "ssoar_match"] in total_ssoar_handler:
                be_dict["crossref"] = "gbr:0110050000" + str(tem_df.ix[index_references_in_a_pdf]["ssoar_match"])

            elif tem_df.ix[index_references_in_a_pdf]["sowi_id"] != 'error' and tem_df.ix[index_references_in_a_pdf][
                "sowi_id"] != 'not_match':
                sowid_item = tem_df.ix[index_references_in_a_pdf]["sowi_id"]
                try:
                    setofdubsowi = set(sowi_dublicate[sowid_item])
                except:
                    setofdubsowi = set([sowid_item])
                listinter_sowid = list(set(ls_seen_sowiport).intersection(setofdubsowi))
                if len(listinter_sowid) > 0:
                    be_dict["crossref"] = "gbr:0110050001" + dict_seen_sowiport[listinter_sowid[0]]
                else:
                    try:
                        be_dict["crossref"] = "gbr:0110050001" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        br_temp1 = sowiport_br(tem_df.ix[index_references_in_a_pdf]["ref_id"],
                                               tem_df.ix[index_references_in_a_pdf]["sowi_id"])
                        list_of_br.append(br_temp1)
                        ls_seen_sowiport.append(sowid_item)
                        dict_seen_sowiport[sowid_item] = str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                    except:
                        be_dict["crossref"] = "gbr:0110050002" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        br_temp1 = {"a": ["document"],
                                    "label": "bibliographic resource 0110050002" +
                                             str(tem_df.ix[index_references_in_a_pdf]["ref_id"]) +
                                             " [br/0110050002" + str(
                                        tem_df.ix[index_references_in_a_pdf]["ref_id"]) + "]"}
                        br_temp1["iri"] = "gbr:0110050002" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                        list_of_br.append(br_temp1)
            else:
                be_dict["crossref"] = "gbr:0110050002" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                br_temp1 = {"a": ["document"],
                            "label": "bibliographic resource 0110050002" +
                                     str(tem_df.ix[index_references_in_a_pdf]["ref_id"]) +
                                     " [br/0110050002" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"]) + "]"}
                br_temp1["iri"] = "gbr:0110050002" + str(tem_df.ix[index_references_in_a_pdf]["ref_id"])
                list_of_br.append(br_temp1)
            if tem_df.ix[index_references_in_a_pdf]["ssoar_match"] != str(ssoar_id):
                ref_list_be.append(be_dict)
                ref_list_cit_br.append(be_dict["crossref"])

        if len(ref_list_be) > 0:
            br_temp["reference"] = ref_list_be
            br_temp["citation"] = ref_list_cit_br
        br_temp["iri"] = "gbr:0110050000" + str(ssoar_id)
        # source_dict=eval(tem_df.ix[index_references_in_a_pdf]["ssoar_source_dict"])
        # indexforssoardict=str(tem_df.ix[index_references_in_a_pdf]["source_ssoar_id"])
        source_dict = dictofrecords_h[str(ssoar_id)]

        br_temp["a"] = ["document",
                        source_dict[101].replace("incollection", "inbook").replace("recension", "review").replace(
                            "monograph", "book")]

        list_source_dict_keys = list(source_dict.keys())
        setofindex_pd = {111, 104, 116, 118, 119}
        set_source_dict_keys = set(list_source_dict_keys)
        checkmylenght = list(setofindex_pd.intersection(set_source_dict_keys))
        if len(checkmylenght) > 0:
            gre_dict = {"iri": "gre:0110020000" + str(ssoar_id), "a": ["generic_format", "digital_format"],
                        "label": "resource embodiment 0110020000" + str(ssoar_id) + " [re/0110020000" + str(
                            ssoar_id) + "]", "mime_type": "pdf"}
            if 104 in checkmylenght:
                if '-' in source_dict[104]:
                    gre_dict["fpage"] = str(source_dict[104]).split('-')[0]
                    gre_dict["lpage"] = str(source_dict[104]).split('-')[1]

        cont_list = []
        if 3 in list(source_dict.keys()):
            for index_aut, author_item in enumerate(source_dict[3]):
                ar_dict = {"iri": "gar:0110030000" + str(index_aut) + str(ssoar_id), "a": "role",
                           "label": "agent role 0110030000" + str(index_aut) + str(ssoar_id) + " [ar/0110030000" + str(
                               index_aut) + str(ssoar_id) + "]",
                           "role_type": "author",
                           "role_of": {"iri": "gra:0110040000" + str(index_aut) + str(ssoar_id), "a": "agent",
                                       "label": "responsible agent 0110040000" + str(index_aut) + str(
                                           ssoar_id) + " [ra/0110040000" + str(index_aut) + str(ssoar_id) + "]",
                                       }
                           }
                ais_ls = author_item.split(",")
                if len(ais_ls) > 1:
                    ar_dict["role_of"]["fname"] = ais_ls[0]
                    ar_dict["role_of"]["gname"] = ais_ls[1]
                else:
                    ar_dict["role_of"]["name"] = ais_ls[0]

                cont_list.append(ar_dict)

                # br_temp["format"]= [gre_dict]
        br_temp["label"] = "bibliographic resource 0110050000" + str(ssoar_id) + " [br/0110050000" + str(ssoar_id) + "]"
        # br_temp["title"]=source_dict[64][-1]
        br_temp["title"] = source_dict[64]
        if len(cont_list):
            br_temp["contributor"] = cont_list
        # br_temp["year"]=source_dict[15][-1]
        year_entity = re.findall('(\d{4})', source_dict[15])
        br_temp["date"] = {"value": str(year_entity[0]), "a": "year"}
        only_id_list, temp_id_list = creat_iden_part(set_source_dict_keys, ssoar_id, source_dict)
        if len(temp_id_list) > 0:
            br_temp["identifier"] = temp_id_list

        if "reference" in list(br_temp.keys()):
            list_of_br.append(br_temp)
    return list_of_br


def Generat_br_for_remained_match(cross_ref_list):
    br_list = []
    for br_rec_new_id in cross_ref_list:
        try:
            source_dict = dictofrecords_h[br_rec_new_id]
            br_temp = {"iri": "gbr:0110050000" + br_rec_new_id,
                       "a": ["document",
                             source_dict[101].replace("incollection", "inbook").replace("recension", "review").replace(
                                 "monograph", "book")],
                       "label": "bibliographic resource 0110050000" + br_rec_new_id + " [br/0110050000" + br_rec_new_id + "]",
                       "title": source_dict[64]
                       }
            cont_list = []
            if 3 in list(source_dict.keys()):
                for index_aut, author_item in enumerate(source_dict[3]):
                    ar_dict = {"iri": "gar:0110030000" + str(index_aut) + br_rec_new_id, "a": "role",
                               "label": "agent role 0110030000" + str(
                                   index_aut) + br_rec_new_id + " [ar/0110030000" + str(
                                   index_aut) + br_rec_new_id + "]",
                               "role_type": "author",
                               "role_of": {"iri": "gra:0110040000" + str(index_aut) + br_rec_new_id, "a": "agent",
                                           "label": "responsible agent 0110040000" + str(
                                               index_aut) + br_rec_new_id + " [ra/0110040000" + str(
                                               index_aut) + br_rec_new_id + "]",
                                           }
                               }
                    ais_ls = author_item.split(",")
                    if len(ais_ls) > 1:
                        ar_dict["role_of"]["fname"] = ais_ls[0]
                        ar_dict["role_of"]["gname"] = ais_ls[1]
                    else:
                        ar_dict["role_of"]["name"] = ais_ls[0]
                    cont_list.append(ar_dict)
            if len(cont_list) > 0:
                br_temp["contributor"] = cont_list
            year_entity = re.findall('(\d{4})', source_dict[15])
            br_temp["date"] = {"value": str(year_entity[0]), "a": "year"}
            list_source_dict_keys = list(source_dict.keys())
            set_source_dict_keys = set(list_source_dict_keys)
            only_id_list, temp_id_list = creat_iden_part(set_source_dict_keys, int(br_rec_new_id), source_dict)
            if len(temp_id_list) > 0:
                br_temp["identifier"] = temp_id_list
            br_list.append(br_temp)
            # print(source_dict)
        except:
            pass
            # tem_br_rec["iri"]="gbr:0110050000"+str(br_rec_new_id)
            # br_temp["a"]=["document",source_dict[101].replace("incollection","inbook").replace("recension","ReviewArticle")]
    return br_list

deltaset=set(listof_ssoar_id)-set(total_ssoar_handler)

listof_ssoar_id1=list(set(listof_ssoar_id)-deltaset)  # one item is removed (2667)

#Wall time: 2h 34s
list_of_br=json_generator(listof_ssoar_id1)

df_br_list=pd.DataFrame(list_of_br)

cross_ref_list=[]
for item in list(df_br_list[~df_br_list["reference"].isnull()]["reference"]):
    for item1 in item:
        cross_ref_list.append(item1["crossref"])

list_iri=list(set(list(df_br_list["iri"])))

cross_ref_list2=[]
for item in list(set(cross_ref_list)-set(list_iri)):  # referenced but not exist in br
    cross_ref_list2.append(item.replace("gbr:0110050000",""))

list_of_br_extra=Generat_br_for_remained_match(cross_ref_list2)

list_of_br=list_of_br_extra+list_of_br

br_json={}
br_json["iri"]="gbr:"
br_json["@context"]="context.json"
br_json["@graph"]=[]
br_json["@graph"]=list_of_br
#br_json["excite_project_match"]={ "@id": "biro:references", "@type": "@vocab"}

#tmls=[]
#for item in br_json['@graph']:
#    tmls+=item["a"]
#tmls=list(set(tmls))


import json

with open('data4.json', 'w', encoding="utf8") as fp:
    json.dump(br_json, fp, indent=4,ensure_ascii=False)





