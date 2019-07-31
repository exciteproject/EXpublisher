import json
import pandas as pd
import psycopg2
from configs import *


def remove_dub_record():
    conn = psycopg2.connect(psqlConfig())
    cur = conn.cursor()
    cur.execute(
        """SELECT iri,COUNT(*) AS "Number of iri"  FROM """ + publicationTableName() + """  GROUP BY iri;""")
    rows = cur.fetchall()
    df1 = pd.DataFrame(rows)
    df1.columns = ["iri", "count"]
    more_thanone = list(df1[df1["count"] > 1]["iri"])

    print(set(more_thanone))

    for item in list(set(more_thanone)):
        print(item)
        query = """SELECT Corpus,iri,auxnr,title, reference FROM """ + \
            publicationTableName() + """  WHERE iri LIKE %s;"""
        cur.execute(query, (str(item),))
        rows = cur.fetchall()
        df1 = pd.DataFrame(rows)
        if len(df1[df1[4] != "NoData"]) != 0:
            tempdf = df1[df1[4] != "NoData"]
            tempdf.reset_index(inplace=True)
            luckyid = tempdf.ix[0][2]
            query = """DELETE FROM """ + publicationTableName() + \
                """ WHERE auxnr <> %s AND iri LIKE %s;"""
            cur.execute(query, (str(luckyid), str(item),))
            conn.commit()
            print("lukyid1:")
            print(luckyid)
        elif len(df1[df1[3] != "NoData"]) != 0:
            tempdf = df1[df1[3] != "NoData"]
            tempdf.reset_index(inplace=True)
            luckyid = tempdf.ix[0][2]
            query = """DELETE FROM """ + publicationTableName() + \
                """ WHERE auxnr <> %s AND iri LIKE %s;"""
            cur.execute(query, (str(luckyid), str(item),))
            conn.commit()
            print("lukyid1:")
            print(luckyid)
        else:
            df1.reset_index(inplace=True)
            luckyid = tempdf.ix[0][2]
            query = """DELETE FROM """ + publicationTableName() + \
                """ WHERE auxnr <> %s AND iri LIKE %s;"""
            cur.execute(query, (str(luckyid), str(item),))
            conn.commit()
            print("lukyid2:")
            print(luckyid)

    cur.close()
    conn.close()

# remove_dub_record()
