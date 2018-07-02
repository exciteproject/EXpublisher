from sickle import Sickle
import xmltodict
from lxml import etree
import json


def convert(xml_file, xml_attribs=True):
    with open(xml_file) as f:
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d


def ssoarharvest(filename='support_data/data_harvest1.json'):
    sickle = Sickle('https://www.ssoar.info/OAIHandler/request')
    records = sickle.ListRecords(metadataPrefix='oai_genios')
    counter = 0
    listofcounter = []
    for r in records:
        counter += 1
        listofcounter.append(r)
        if counter % 10000 == 0:
            print(counter)

    llt = []
    errorls = []
    for index, item in enumerate(listofcounter):
        try:
            llt.append(eval(json.dumps(xmltodict.parse(etree.tostring(item.xml)))))
        except:
            errorls.append(index)

    a = {}
    a["result"] = llt

    with open(filename, 'w') as fp:
        json.dump(a, fp, indent=4)

