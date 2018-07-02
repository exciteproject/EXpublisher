import json
import pandas as pd
import psycopg2
import timeit



conn = psycopg2.connect("dbname='' user='' host='' password=''")
cur = conn.cursor()
cur.execute("""SELECT  iri, citation,auxnr FROM Test_data_publication;""")
rows = cur.fetchall()


start = timeit.default_timer()
ls_paper_cit=[]
print("step0")
for index1,records in enumerate(rows):
    ls_paper_cit.append(list(records))
    
print("step1") 
cited_dict = {}
for citing, all_cited, auxnr in ls_paper_cit:
    if all_cited!='NoData':
        for cited in eval(all_cited):
            cited_dict[cited] = cited_dict.get(cited, []) + [citing]


result_ls=[[auxnr, citing, cited, cited_dict.get(citing, [])] for citing, cited, auxnr in ls_paper_cit]

stop = timeit.default_timer()

print("step2")
for item in result_ls:
    cur = conn.cursor()
    query = """UPDATE Test_data_publication SET incit= %s WHERE auxnr=%s;"""
    cur.execute(query, (str(item[3]),str(item[0]),))
    conn.commit() 
        

print (stop - start) 
