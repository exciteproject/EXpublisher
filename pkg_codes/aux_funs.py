import re

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


def creat_iden_part(set_source_dict_keys,ssoar_id,source_dict):
    id_counter=0
    temp_id_list=[]
    ids_only_list=[]
    if 124 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        if validate_url_stirng(source_dict[124]):
            temp_id_set["type"]="url"
        else:
            temp_id_set["type"]="pmid"
        temp_id_set["id"]=source_dict[124]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"124")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"124"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"124"+" [id/0000"+str(ssoar_id)+"124"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 72 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="url"
        #temp_id_set["id"]=source_dict[72][-1]
        temp_id_set["id"]=source_dict[72]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"72")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"72"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"72"+" [id/0000"+str(ssoar_id)+"72"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 25 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        if validate_url_stirng(source_dict[25]):
            temp_id_set["type"]="url"
        else:
            temp_id_set["type"]="uri"
        temp_id_set["id"]=source_dict[25]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"25")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"25"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"25"+" [id/0000"+str(ssoar_id)+"25"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    """
    if 21 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="issn"
        #temp_id_set["id"]=source_dict[21][-1]
        temp_id_set["id"]=source_dict[21]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    """
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        if validate_url_stirng(source_dict[20]):
            temp_id_set["type"]="url"
        else:
            temp_id_set["type"]="isbn"
        temp_id_set["id"]=source_dict[20]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"20")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"20"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"20"+" [id/0000"+str(ssoar_id)+"20"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 137 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        
        doi_url=source_dict[137]
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
        
        
        #temp_id_set["type"]="doi"
        #temp_id_set["id"]=source_dict[137][-1]
        #temp_id_set["id"]=source_dict[137]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"137")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"137"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"137"+" [id/0000"+str(ssoar_id)+"137"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        
        urn_url=source_dict[85]
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
        
        
        #temp_id_set["type"]="urn"
        #temp_id_set["id"]=source_dict[85][-1]
        #temp_id_set["id"]=source_dict[85]
        ids_only_list.append("gid:0000"+str(ssoar_id)+"85")
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"85"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"85"+" [id/0000"+str(ssoar_id)+"85"+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    return ids_only_list,temp_id_list