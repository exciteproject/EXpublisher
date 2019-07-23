## EXCITE Data Converter to OCC ontology

### Description:

This code is dedicated to the task of converting [EXCITE](https://west.uni-koblenz.de/en/research/excite) Data to a JSON-LD format with ([OCC](http://opencitations.net/corpus) ontology).
The aim of [EXCITE](https://west.uni-koblenz.de/en/research/excite) project is the extraction of references out of PDFs, which will be done in three main steps:

1. Extraction of reference strings out of PDFs
2. Segmentation of each reference string
3. Match each bibliographical item against corresponding items in bibliographical databases

After this processes, the output of [EXCITE](https://west.uni-koblenz.de/en/research/excite) will be a set of reference strings and their Match information.

The [OCC](http://opencitations.net/corpus) includes information about six different kinds of bibliographic entities:

* bibliographic resources (br): Cited/citing bibliographic resources
* resource embodiments (re): Details about the bibliographic resources made (such as pages)
* bibliographic entries (be): Reference strings
* responsible agents (ra):  names of agents having specific roles concerning bibliographic resources (i.e., names of authors, editors, publishers, etc.)
* agent roles (ar): roles held by agents concerning bibliographic resources (e.g., author, editor, publisher)
* identifiers (id): external identifiers (e.g. DOI, ORCID, PubMedID) associated with the bibliographic entities.

The purpose of the codes in the repository is converting generated data by [EXCITE](https://west.uni-koblenz.de/en/research/excite) project to [OCC](http://opencitations.net/corpus) ontology. Besides that, these data will be enriched by metadata of records in [Sowiport.org](http://sowiport.gesis.org/) and [SSOAR](http://www.ssoar.info/).
Since a portion of extracted references have match information, we use this opportunity to extract metadata from corresponding records in these databases and add it to reference strings and then convert it to a 
JSON file.

### Details about data:

Besides EXCITE data availability in OCC portal, the bulk download is accessible via EXCITE server:

* [Version 1 (17/07/2018)](http://excite-compute.west.uni-koblenz.de/download/OCC/ssoar_17jul2018/data/data_20180717183529.json)

In this version of data we have a part of extracted references from [SSOAR](http://www.ssoar.info/) PDF corpus (about 24 k of SSOAR PDFS):
1. The total number of brs: 1,045,189
2. The total number of bes: 1,146,213



### How to use the code:
How to run summary for developers:
```html
step 1: prepareing a csv file as input:
* columns name in csv file: ref_id;ref_text;ssoar_id;match_id
* put csv input file somewhere in Expublisher folder

step 2: bulding json file
for other corpus:
* open sample_othercorpus_code.py
* edit file for new input : Target_dir= ...., ID_courpus="0001", SourceDir=....
* ID_courpus --> SSOAR: 0000, Arxiv: 0005, and Sowiport: 0001
* run python file: python3 sample_othercorpus_code.py
* output is json file and will save in "Target_dir"

step 3: insert data in postgres table:
* Create a table in postgres : CREATE TABLE Test_data_publication_sowi(auxnr SERIAL, Corpus TEXT,iri TEXT, br_value TEXT,a TEXT,contributor TEXT,date TEXT,identifier TEXT,label TEXT,title TEXT,citation TEXt,reference TEXT, inserttoken Text, ex_mat_cor TEXT);
* open load_df_into.py file: 
* set database information (line 21) : Example = "dbname='dbexcit' user='postgres' host='localhost' password='123'"
* change name of table (line 73)
* change last line with this: loaddata_from_csv_to_table("0001",1, file_fulldirectory)
* change corpus id in last line (0001 for sowi)
* run python file: --> python3 load_df_into.py
* now we can check table: select count(*) from test_data_publication_sowi;

Step 4: remove_dublicate in table
* open this file: remove_dublicate.py
* set database information (line 3)
* change name of table 
* run python file: --> python3 remove_dublicate.py
* now we can check table: select count(*) from test_data_publication_sowi;

Step 5: generate occ format
* open replaceid_gen.py
* set database information (line 165)
* change name of table (line 167)
* change Target_dir (line 179)
* Create two Empty Folder in root: ( Final_br_json/data AND Final_br_json/dictionary_rep)
* run python file: --> python3 replaceid_gen.py
```

To read full details Please check the [documentation file](https://github.com/exciteproject/Convertor_EXCITEdata_OCCJson/blob/master/documents/EXCITE%20Data%20Converter%20to%20OCC%20ontology.pdf).
