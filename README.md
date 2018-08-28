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

Please check the [documentation file](https://github.com/exciteproject/Convertor_EXCITEdata_OCCJson/blob/master/documents/EXCITE%20Data%20Converter%20to%20OCC%20ontology.pdf).
