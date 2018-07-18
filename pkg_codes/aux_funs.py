import re
import requests 

regexurlfilter = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url_stirng(url_str):
    return re.match(regexurlfilter, url_str) is not None
    
def remove_substr_frombegining(inputstr,substr):
    if inputstr.find(substr)==-1:
        return -1
    else:
        return inputstr[inputstr.find(substr)+len(substr):]


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
        
def creat_iden_part(set_source_dict_keys,ssoar_id,source_dict):
    temp_id_list=[]
    ids_only_list=[]
    if 124 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["id"]=source_dict[124]
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"124"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"124"+" [id/0000"+str(ssoar_id)+"124"+"]"
        
        if validate_url_stirng(source_dict[124]):
            if check_url_ext(temp_id_set["id"])==True:
                temp_id_set["type"]="url"
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"124")
        else:
            temp_id_set["type"]="pmid"
            temp_id_list.append(temp_id_set)   
            ids_only_list.append("gid:0000"+str(ssoar_id)+"124")
    #=======================================================================
    if 72 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["id"]=source_dict[72]
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"72"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"72"+" [id/0000"+str(ssoar_id)+"72"+"]"
        if validate_url_stirng(temp_id_set["id"]):
            if check_url_ext(temp_id_set["id"])==True:
                temp_id_set["type"]="url"     
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"72")
    #=========================================================================
    if 25 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["id"]=source_dict[25]
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"25"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"25"+" [id/0000"+str(ssoar_id)+"25"+"]"
        
        if validate_url_stirng(temp_id_set["id"]):
            if check_url_ext(temp_id_set["id"])==True:
                temp_id_set["type"]="url"
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"25")
        else:
                temp_id_set["type"]="uri"
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"25")
    #=========================================================================   
    if 20 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        temp_id_set["id"]=source_dict[20]
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"20"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"20"+" [id/0000"+str(ssoar_id)+"20"+"]"
        
        if validate_url_stirng(temp_id_set["id"]):
            if check_url_ext(temp_id_set["id"])==True:
                temp_id_set["type"]="url"
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"20")
        else:
            if valfilter_isbn(temp_id_set["id"]):
                temp_id_set["type"]="isbn"
                temp_id_list.append(temp_id_set)
                ids_only_list.append("gid:0000"+str(ssoar_id)+"20")
    #==========================================================================
    if 137 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        
        doi_url=source_dict[137]     
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"137"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"137"+" [id/0000"+str(ssoar_id)+"137"+"]"
        
        if validate_url_stirng(doi_url):
            if "https://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"https://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
                if valfilter_doi(doi_url):
                    #if doiurlcheck("https://dx.doi.org/"+doi_url):
                           temp_id_list.append(temp_id_set) 
                           ids_only_list.append("gid:0000"+str(ssoar_id)+"137")
            elif "http://dx.doi.org/" in doi_url:
                doi_url=remove_substr_frombegining(doi_url,"http://dx.doi.org/")
                temp_id_set["id"]=doi_url
                temp_id_set["type"]="doi"
                if valfilter_doi(doi_url):
                    #if doiurlcheck("https://dx.doi.org/"+doi_url):
                        temp_id_list.append(temp_id_set) 
                        ids_only_list.append("gid:0000"+str(ssoar_id)+"137")
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=doi_url
                if check_url_ext(doi_url):
                    temp_id_list.append(temp_id_set) 
                    ids_only_list.append("gid:0000"+str(ssoar_id)+"137")        
        else:
            temp_id_set["type"]="doi"
            temp_id_set["id"]=doi_url
            if valfilter_doi(doi_url):
                #if doiurlcheck("https://dx.doi.org/"+doi_url):
                    temp_id_list.append(temp_id_set) 
                    ids_only_list.append("gid:0000"+str(ssoar_id)+"137")        
    #=========================================================================
    if 85 in list(set_source_dict_keys):
        temp_id_set={}
        temp_id_set["a"]="unique_identifier"
        
        urn_url=source_dict[85]
        temp_id_set["iri"]="gid:0000"+str(ssoar_id)+"85"
        temp_id_set["label"]="identifier 0000"+str(ssoar_id)+"85"+" [id/0000"+str(ssoar_id)+"85"+"]"
        
        if validate_url_stirng(urn_url):
            if "http://hdl.handle.net/" in urn_url:
                urn_url=remove_substr_frombegining(urn_url,"http://hdl.handle.net/")
                temp_id_set["id"]=urn_url
                temp_id_set["type"]="urn"
                if valfilter_urn(urn_url):
                    ids_only_list.append("gid:0000"+str(ssoar_id)+"85")
                    temp_id_list.append(temp_id_set)
            else:
                temp_id_set["type"]="url"
                temp_id_set["id"]=urn_url
                if check_url_ext(urn_url):
                    ids_only_list.append("gid:0000"+str(ssoar_id)+"85")
                    temp_id_list.append(temp_id_set)
        else:
            temp_id_set["type"]="urn"
            temp_id_set["id"]=urn_url
            if valfilter_urn(urn_url):
                 ids_only_list.append("gid:0000"+str(ssoar_id)+"85")
                 temp_id_list.append(temp_id_set)
    #=========================================================================
    return ids_only_list,temp_id_list