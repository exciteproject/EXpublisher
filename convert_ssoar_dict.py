import json

def json_to_new_dict():
    a = json.load(open('data_harvest1.json'))

    qualifierdict={3: 'author',15: 'issued',20: 'isbn',21: 'issn',25: 'uri',72: 'url',
        85: 'urn',104: 'pageinfo',111: 'corporateeditor',116: 'recensioneditor',118: 'recensiontitle',
        119: 'recensionseries',124: 'pid',137: 'doi'}

    elementdict={64:"title",10:"date"}

    counternot=0
    listofrecords_h=[]
    for item in range(0,len(a["result"])):
        records=a["result"][item]['record']
        if "metadata" in records.keys():
            values=records['metadata']['dublin_core']['dcvalue']
            temp={}
            list_authors_r=[]
            list_editor_r=[]
            for item_values in values:
                if '#text' in item_values.keys() and '@element' in item_values.keys():
                    if 'title'==item_values['@element']:
                        if "@qualifier" in item_values.keys() and 'alternative'==item_values['@qualifier']:
                            pass
                        else:
                            temp[64]= item_values['#text']
                    elif "date"==item_values['@element']:
                        temp[10]= item_values['#text']
                if '@qualifier' in item_values.keys() and '#text' in item_values.keys():
                    if 'author'==item_values['@qualifier']:
                        list_authors_r.append(item_values['#text'])
                    elif 'issued'==item_values['@qualifier'] :
                        temp[15]=item_values['#text']
                    elif 'isbn'==item_values['@qualifier']:
                        temp[20]=item_values['#text']
                    elif 'issn'==item_values['@qualifier']:
                        temp[21]=item_values['#text']
                    elif 'uri'==item_values['@qualifier']:
                        temp[25]=item_values['#text']
                    elif 'url'==item_values['@qualifier']:
                        temp[72]=item_values['#text']
                    elif 'urn'==item_values['@qualifier']:
                        temp[85]=item_values['#text']
                    elif 'pageinfo'==item_values['@qualifier']:
                        temp[104]=item_values['#text']
                    elif 'corporateeditor'==item_values['@qualifier']:
                        temp[111]=item_values['#text']
                    elif 'recensioneditor'==item_values['@qualifier']:
                        list_editor_r.append(item_values['#text'])
                    elif 'recensiontitle'==item_values['@qualifier']:
                        temp[118]=item_values['#text']
                    elif 'recensionseries'==item_values['@qualifier']:
                        temp[119]=item_values['#text']
                    elif 'pid'==item_values['@qualifier']:
                        temp[124]=item_values['#text']
                    elif 'doi'==item_values['@qualifier']:
                        temp[137]=item_values['#text']
                    elif 'stock'==item_values['@qualifier']:
                        temp[101]=item_values['#text']
            if 25 in temp.keys():
                temp["handler"]=temp[25].split('/')[-1]
            else:
                counternot+=1
            temp[3]= list_authors_r
            temp[116]=list_editor_r
            listofrecords_h.append(temp)


    dictofrecords_h={}
    lk=[]
    for item_records_h in listofrecords_h:
        try:
            dictofrecords_h[item_records_h['handler']]=item_records_h
            lk.append(item_records_h[101])
        except:
            #print(item_records_h)
            pass

    total_ssoar_handler=list(dictofrecords_h.keys())

    return  total_ssoar_handler,dictofrecords_h