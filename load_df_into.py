import json
import pandas as pd
import psycopg2
import datetime
from configs import *


def loaddata_from_csv_to_table(Corpus_id_name, flag_source_dir=0, file_fulldirectory=""):
    if flag_source_dir == 0:
        br_json1 = json.load(
            open("data/"+Corpus_id_name+"/json_fv_flatten_occ.json", encoding="utf8"))
    else:
        br_json1 = json.load(open(file_fulldirectory, encoding="utf8"))
    conn = psycopg2.connect(psqlConfig())
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    uniquer_token = str(now).replace(" ", "").replace(
        "-", "").replace(":", "").replace(".", "")
    count = 0
    for item in br_json1['@graph']:
        count += 1
        temp = {}
        temp['Corpus'] = Corpus_id_name
        if 'iri' in item.keys():
            temp['iri'] = item['iri']
        else:
            temp['iri'] = "NoData"

        temp['br_value'] = item

        if 'a' in item.keys():
            temp['a'] = item['a']
        else:
            temp['a'] = "NoData"

        if 'contributor' in item.keys():
            temp['contributor'] = item['contributor']
        else:
            temp['contributor'] = "NoData"

        if 'date' in item.keys():
            temp['date'] = item['date']
        else:
            temp['date'] = "NoData"

        if 'identifier' in item.keys():
            temp['identifier'] = item['identifier']
        else:
            temp['identifier'] = "NoData"

        if 'label' in item.keys():
            temp['label'] = item['label']
        else:
            temp['label'] = "NoData"

        if 'title' in item.keys():
            temp['title'] = item['title']
        else:
            temp['title'] = "NoData"

        if 'citation' in item.keys():
            temp['citation'] = item['citation']
        else:
            temp['citation'] = "NoData"

        if 'reference' in item.keys():
            temp['reference'] = item['reference']
        else:
            temp['reference'] = "NoData"
        DATA_QUERY = (str(temp['Corpus']), str(temp['iri']), str(temp['br_value']), str(temp['a']), str(temp['contributor']), str(temp['date']), str(
            temp['identifier']), str(temp['label']), str(temp['title']), str(temp['citation']), str(temp['reference']), uniquer_token, str(temp['iri'])[4:8])

        if count % 1000 == 0:
            print(count)

        cur = conn.cursor()
        query = """INSERT INTO """ + publicationTableName() + \
            """(Corpus,iri, br_value,a ,contributor ,date ,identifier ,label ,title ,citation ,reference, inserttoken, ex_mat_cor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
        cur.execute(query, DATA_QUERY)
        conn.commit()
    cur.close()
    conn.close()
    return uniquer_token


inputFile = 'data/' + otherCorpusID() + '.json'
flag_source_dir = 1
loaddata_from_csv_to_table(otherCorpusID(), flag_source_dir, inputFile)
