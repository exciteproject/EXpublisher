


def creat_iden_part(set_source_dict_keys,ssoar_id,source_dict):
    id_counter=0
    temp_id_list=[]
    ids_only_list=[]
    if 124 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="pmid"
        #temp_id_set["id"]=source_dict[124]
        temp_id_set["id"]=source_dict[124]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 72 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="url"
        #temp_id_set["id"]=source_dict[72][-1]
        temp_id_set["id"]=source_dict[72]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 25 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="uri"
        #temp_id_set["id"]=source_dict[25][-1]
        temp_id_set["id"]=source_dict[25]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
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
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="isbn"
        #temp_id_set["id"]=source_dict[20][-1]
        temp_id_set["id"]=source_dict[20]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 137 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="doi"
        #temp_id_set["id"]=source_dict[137][-1]
        temp_id_set["id"]=source_dict[137]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["type"]="urn"
        #temp_id_set["id"]=source_dict[85][-1]
        temp_id_set["id"]=source_dict[85]
        ids_only_list.append("gid:01100005"+str(ssoar_id)+str(id_counter))
        temp_id_set["iri"]="gid:01100005"+str(ssoar_id)+str(id_counter)
        temp_id_set["label"]="identifier 01100005"+str(ssoar_id)+str(id_counter)+" [id/01100005"+str(ssoar_id)+str(id_counter)+"]"
        id_counter+=1
        temp_id_list.append(temp_id_set)
    return ids_only_list,temp_id_list