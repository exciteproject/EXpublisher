## Version 1 (08/03/2018)

### Details about data:

By applying [EXCITE](https://www.gesis.org/forschung/drittmittelprojekte/projektuebersicht-drittmittel/excite) on 24221 SSOAR papers, their reference strings (1146424 items) are extracted and matched against a corresponding item in [Sowiport.org](http://sowiport.gesis.org/) (if such a corresponding data exists in Sowiport). 

The result set is enriched by Sowiport and SSOAR metadata. Afterward, it is stored in JSON-LD (with OCC ontology). Some information about the current version:

* Number of total brs in the corpus: 1048697
* Types of brs in these collection: 
    * "article": "fabio:JournalArticle",,
    * "book": "fabio:Book",
    * "collection": "fabio:ExpressionCollection",
    * "document": "fabio:Expression",
    * "inbook": "fabio:BookChapter",
    * "review": "fabio:ReviewArticle"
    
<img src="https://github.com/exciteproject/Convertor_EXCITEdata_OCCJson/raw/master/version/typedist.PNG" alt="Type Disturbiution" width="400" height="200">

* 145619 brs contain some information about their authors [in total 229247 authors]
* Top 5 items in year disturbiution ([more information](https://github.com/exciteproject/Convertor_EXCITEdata_OCCJson/raw/master/version/Datedist.csv)): 
    * (year=2006,count=7281),
    * (2005,7183),
    * (2004,6763),
    * (2002,6638),
    * (2003,6546)

* 131086 brs contain some information about their identifier. ('doi', 'isbn', 'issn', 'uri', 'url', 'urn')
* Top cited bibliographic resources (br) ([more information](https://github.com/exciteproject/Convertor_EXCITEdata_OCCJson/raw/master/version/inner-citation.csv)):
    * iri: "gbr:0110935"    (Cited by: 223 other brs in the Data)
    * iri: "gbr:011024114"    (Cited by: 142 other brs in the Data)
    * iri: "gbr:01101235"   (Cited by: 139 other brs in the Data)

* At least 157196 items have enriched by metadata of Sowiport and SSOAR