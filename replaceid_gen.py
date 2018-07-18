import json
import pandas as pd
import psycopg2
import datetime
import os.path

def Replace_ids_in_flaten_json(ls_br_sql,uniquer_token,Target_dir,dict_count_all,listmapids):
    dict_count={}
    ####################################################
    ################[//////BR///////]###################
    ####################################################
    ####################################################
    br_dict_rep={}
    br_ls_rep=[]
    if dict_count_all.get("br","notfound")!="notfound":
        count=dict_count_all["br"]+1
    else:
       count=1 
    brdictoldmap=listmapids[1]   
    for index,item in enumerate(ls_br_sql):
        gbr=item["iri"]
        gbr=gbr.replace("gbr:","").strip()
        if brdictoldmap.get(gbr,"notfound")=="notfound":
            br_dict_rep[gbr]="0110"+str(count)
            br_ls_rep.append(gbr)
            ls_br_sql[index]["iri"]="gbr:"+"0110"+str(count)
            ls_br_sql[index]["label"]=ls_br_sql[index]["label"].replace(gbr,str("0110"+str(count)))
            count+=1
        else:
            tv=brdictoldmap[gbr]
            br_dict_rep[gbr]=tv
            br_ls_rep.append(gbr)
            ls_br_sql[index]["iri"]="gbr:"+tv
            ls_br_sql[index]["label"]=ls_br_sql[index]["label"].replace(gbr,str(tv))
    with open(Target_dir+'/dictionary_rep/br_id.json', 'w', encoding="utf8") as fp:
        json.dump(br_dict_rep, fp, indent=4,ensure_ascii=False)           
    dict_count["br"]=count
    ####################################################
    ######################[//////id///////]#############
    ####################################################
    ####################################################
    iden_dict_rep={}
    iden_ls_rep=[]
    if dict_count_all.get("id","notfound")!="notfound":
        count=dict_count_all["id"]+1
    else:
       count=1 
    brdictoldmap=listmapids[2]      
    for index,item in enumerate(ls_br_sql):
        if "identifier" in list(item.keys()):
            for index1,iden_item in enumerate(item["identifier"]):
                gid=iden_item["iri"]
                gid=gid.replace("gid:","").strip()
                if brdictoldmap.get(gid,"notfound")=="notfound":
                    iden_dict_rep[gid]="0110"+str(count)
                    iden_ls_rep.append(gid)
                    ls_br_sql[index]["identifier"][index1]["iri"]="gid:"+"0110"+str(count)
                    ls_br_sql[index]["identifier"][index1]["label"]=iden_item["label"].replace(gid,str("0110"+str(count)))
                    count+=1
                else:
                    tv=brdictoldmap[gid]
                    iden_dict_rep[gid]=tv
                    iden_ls_rep.append(gid)
                    ls_br_sql[index]["identifier"][index1]["iri"]="gid:"+tv
                    ls_br_sql[index]["identifier"][index1]["label"]=iden_item["label"].replace(gid,str(tv))
    with open(Target_dir+'/dictionary_rep/id_id.json', 'w', encoding="utf8") as fp:
        json.dump(iden_dict_rep, fp, indent=4,ensure_ascii=False)
    dict_count["id"]=count
    ####################################################
    ##################[//////ar///////]#################
    ####################################################
    ####################################################
    ar_dict_rep={}
    ar_ls_rep=[]
    if dict_count_all.get("ar","notfound")!="notfound":
        count=dict_count_all["ar"]+1
    else:
       count=1 
    brdictoldmap=listmapids[3]
    for index,item in enumerate(ls_br_sql):
        if "contributor" in list(item.keys()):
            for index1,ar_item in enumerate(item["contributor"]):
                gar=ar_item["iri"]
                gar=gar.replace("gar:","").strip()
                if brdictoldmap.get(gar,"notfound")=="notfound":
                    ar_dict_rep[gar]="0110"+str(count)
                    ar_ls_rep.append(gar)
                    ls_br_sql[index]["contributor"][index1]["iri"]="gar:"+"0110"+str(count)
                    ls_br_sql[index]["contributor"][index1]['role_of']["iri"]="gra:"+"0110"+str(count)
                    ls_br_sql[index]["contributor"][index1]["label"]=ar_item["label"].replace(gar,str("0110"+str(count)))
                    ls_br_sql[index]["contributor"][index1]['role_of']["label"]=ls_br_sql[index]["contributor"][index1]['role_of']["label"].replace(gar,str("0110"+str(count)))
                    count+=1
                else:
                    tv=brdictoldmap[gar]
                    ar_dict_rep[gar]=tv
                    ar_ls_rep.append(gar)
                    ls_br_sql[index]["contributor"][index1]["iri"]="gar:"+tv
                    ls_br_sql[index]["contributor"][index1]['role_of']["iri"]="gra:"+tv
                    ls_br_sql[index]["contributor"][index1]["label"]=ar_item["label"].replace(gar,str(tv))
                    ls_br_sql[index]["contributor"][index1]['role_of']["label"]=ls_br_sql[index]["contributor"][index1]['role_of']["label"].replace(gar,str(tv))
    with open(Target_dir+'/dictionary_rep/ra_ar.json', 'w', encoding="utf8") as fp:
        json.dump(ar_dict_rep, fp, indent=4,ensure_ascii=False)
    dict_count["ar"]=count
    ####################################################
    #################[//////be///////]##################
    ####################################################
    #################################################### 
    be_dict_rep={}
    be_ls_rep=[]
    if dict_count_all.get("be","notfound")!="notfound":
        count=dict_count_all["be"]+1
    else:
       count=1 
    brdictoldmap=listmapids[0]   
    for index,item in enumerate(ls_br_sql):
        if "reference" in list(item.keys()):
            for index1,be_item in enumerate(item["reference"]):
                gbe=be_item["iri"]
                gbe=gbe.replace("gbe:","").strip()
                if brdictoldmap.get(gbe,"notfound")=="notfound":
                    be_dict_rep[gbe]="0110"+str(count)
                    be_ls_rep.append(gbe)
                    ls_br_sql[index]["reference"][index1]["iri"]="gbe:"+"0110"+str(count)
                    ls_br_sql[index]["reference"][index1]["label"]=be_item["label"].replace(gbe,str("0110"+str(count)))
                    crossref=ls_br_sql[index]["reference"][index1]["crossref"].replace("gbr:","").strip()
                    ls_br_sql[index]["reference"][index1]["crossref"]="gbr:"+str(br_dict_rep[crossref])
                    count+=1
                else:
                    tv=brdictoldmap[gbe]
                    be_dict_rep[gbe]=tv
                    be_ls_rep.append(gbe)
                    ls_br_sql[index]["reference"][index1]["iri"]="gbe:"+tv
                    ls_br_sql[index]["reference"][index1]["label"]=be_item["label"].replace(gbe,str(tv))
                    crossref=ls_br_sql[index]["reference"][index1]["crossref"].replace("gbr:","").strip()
                    ls_br_sql[index]["reference"][index1]["crossref"]="gbr:"+str(br_dict_rep[crossref])
    
    with open(Target_dir+'/dictionary_rep/be_id.json', 'w', encoding="utf8") as fp:
        json.dump(be_dict_rep, fp, indent=4,ensure_ascii=False)
    dict_count["be"]=count
    ####################################################
    ####################################################
    ####################################################
    ####################################################
    with open(Target_dir+'/dictionary_rep/countdict.json', 'w', encoding="utf8") as fp:
        json.dump(dict_count, fp, indent=4,ensure_ascii=False)
    
    
    for index,item in enumerate(ls_br_sql):
        if "citation" in list(item.keys()):
            for index1,be_item in enumerate(item["citation"]):
                crossref=ls_br_sql[index]["citation"][index1].replace("gbr:","").strip()
                ls_br_sql[index]["citation"][index1]="gbr:"+str(br_dict_rep[crossref])
    
    
    br_json1={}
    br_json1["iri"]="gbr:"
    br_json1["@context"]="context.json"
    br_json1["@graph"]=ls_br_sql

    with open(Target_dir+'/data/data_'+uniquer_token+'.json', 'w', encoding="utf8") as fp:
        json.dump(br_json1, fp, indent=4,ensure_ascii=False)

def main_replace_id():
    conn = psycopg2.connect("dbname='' user='' host='' password=''")
    cur = conn.cursor()
    cur.execute("""SELECT br_value from Test_data_publication ORDER BY auxnr""")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    ls_br_sql=[]
    for item in rows:
        ls_br_sql.append(eval(item[0]))

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    uniquer_token=str(now).replace(" ","").replace("-","").replace(":","").replace(".","")

    Target_dir="/Final_br_json"
    #######
    if os.path.exists("/home/behnam/Opencitation_run_area/Final_br_json/countdict.json"):
        with open("/home/behnam/Opencitation_run_area/Final_br_json/countdict.json") as f:
            dict_count_all = json.load(f)
    else:
        dict_count_all={}
    #######
    if os.path.exists("/Final_br_json/dictionary_rep/be_id.json"):
        with open("/Final_br_json/dictionary_rep/be_id.json") as f:
            be_id_map = json.load(f)
    else:
        be_id_map={}

    if os.path.exists("/Final_br_json/dictionary_rep/br_id.json"):
        with open("/Final_br_json/dictionary_rep/br_id.json") as f:
            br_id_map = json.load(f)
    else:
        br_id_map={}

    if os.path.exists("/Final_br_json/dictionary_rep/id_id.json"):
        with open("/Final_br_json/dictionary_rep/id_id.json") as f:
            id_id_map = json.load(f)
    else:
        id_id_map={}

    if os.path.exists("/Final_br_json/dictionary_rep/ra_ar_id.json"):
        with open("/Final_br_json/dictionary_rep/ra_ar_id.json") as f:
            ra_ar_id_map = json.load(f)
    else:
        ra_ar_id_map={}
    #######
    Replace_ids_in_flaten_json(ls_br_sql,uniquer_token,Target_dir,dict_count_all,[be_id_map,br_id_map,id_id_map,ra_ar_id_map])
 
 
main_replace_id()