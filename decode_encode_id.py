def decode_id(str_id,type_data):
    if type_data=="gid":
        dict_resutlt={}
        dict_resutlt["corpus"]=str_id[:4]
        idtype2=str_id[-2:]
        idtype3=str_id[-3:]
        if idtype2=="85":
            dict_resutlt["type"]="urn"
            dict_resutlt["id"]=idtype2=str_id[4:-2]
        elif idtype2=="20":
            dict_resutlt["type"]="isbn"
            dict_resutlt["id"]=idtype2=str_id[4:-2]
        elif idtype2=="72":
            dict_resutlt["type"]="URL"
            dict_resutlt["id"]=idtype2=str_id[4:-2]
        elif idtype2=="25":
            dict_resutlt["type"]="URI"
            dict_resutlt["id"]=idtype2=str_id[4:-2]
        elif idtype3=="137":
            dict_resutlt["type"]="doi"
            dict_resutlt["id"]=idtype2=str_id[4:-3]
        elif idtype3=="124":
            dict_resutlt["type"]="PMID"
            dict_resutlt["id"]=idtype2=str_id[4:-3]
        return(dict_resutlt)
    elif type_data=="gbr":
        dict_resutlt={}
        dict_resutlt["corpus"]=str_id[:4]
        if dict_resutlt["corpus"][0]=="2":
            dict_resutlt["corpus"]="0"+dict_resutlt["corpus"][1:]
            dict_resutlt["refid"]=str_id[4:]
        elif dict_resutlt["corpus"]=="0000":
            dict_resutlt["ssoarid"]=str_id[4:]
        else:
            dict_resutlt["sowi_id"]=str_id[4:]
        return dict_resutlt
    elif type_data=="gbe":
        dict_resutlt={}
        dict_resutlt["corpus"]=str_id[:4]
        dict_resutlt["refid"]=str_id[4:]
        return dict_resutlt
    elif type_data=="gar" or type_data=="gra":
        dict_resutlt={}
        if str_id[:2]=="00":
            dict_resutlt["role"]="author"
        elif str_id[:2]=="01":
            dict_resutlt["role"]="publisher"
        
        dict_resutlt["corpus"]=str_id[2:6]
        dict_resutlt["index"]=str_id[6:8]
        dict_resutlt["id"]=str_id[8:]
        return dict_resutlt

#decode_id("0001gesis-solis-0022305720","gid")
#decode_id("0000650585","gid")
#decode_id("2000256944","gbr")
#decode_id("0001gesis-solis-00546900","gbr")
#decode_id("000048144","gbr")
#decode_id("00001140243","gbe")
#decode_id("01000100csa-assia-200824116","gar")
#decode_id("0000000111143","gra")

# br > 0000: ssoar , 0001: sowiport, 0005: arxiv


#Gid: match_corpus(0001) sowi_id(csa-pais-1994-0302653) idtype
#Gid: match_corpus(0000) ssoar_id(43864) idtype


#Gbr: corpus(0000) ssoarid
#Gbr: corpus(2000) ref_id ? not match
#Gbr: corpus(0001) sowi_id
#Gbr: corpus(2005) ref_id
#Gbr: corpus(0005) paper_id




#Gar: author(00) sowi_match(0001) (indexaut) (sowiportid)
#Gar: publisher(01) ssoar_match(0000) (indexaut) (ssoarid)
#Gra: author(00) sowi_match(0001) (indexaut) (sowiportid)
#Gra: publisher(01) ssoar_match(0000) (indexaut) (ssoarid)


#Gbe: corpus(0000) ref_id
#Gbe: corpus(0005) ref_id



        
        
