#!/usr/bin/env python3

from xml.dom import minidom
import re
try:
    import simplejson as json
except ImportError:
    print("ERROR: Module simplejson is not installed in the system.")
    exit()

dictData={}
identifyTag="Identifier"

def parse_nodes(dictData, dictTags, testclient, identifyName, description):
    dictData=dictData[testclient][identifyName][description]
    for tagname in dictTags:
        domObj=dictTags[tagname]
        for child in domObj.childNodes:
            domObj=child.nodeValue
            dictData[tagname]=domObj
    return dictData

def parse_element(element):
    collection=element.documentElement

    testclient=collection.getElementsByTagName("TestClient")[0]
    testclient=testclient.childNodes[0].data
    results=collection.getElementsByTagName("Result")

    dictData[testclient]={}

    for result in results:
        try:
            identifier=result.getElementsByTagName(identifyTag)[0]
            if len(identifier.childNodes) == 0:
                identifier=result.getElementsByTagName(identifyTag)[1]
            identity=identifier.childNodes[0].data
            dictData[testclient][identity]={}
        except:
            dictData[testclient]["others"]={}


    for identifyName in sorted(dictData[testclient].keys()):
        for result in results:
            try:
                identifier=result.getElementsByTagName("Identifier")[0]
                if len(identifier.childNodes) == 0:
                    identifier=result.getElementsByTagName("Identifier")[1]
                identity=identifier.childNodes[0].data
            except:
                continue

            try:
                if re.match(identity, identifyName):
                    desc=result.getElementsByTagName("Description")[0]
                    title=result.getElementsByTagName("Title")[0]
                    appver=result.getElementsByTagName("AppVersion")[0]
                    args=result.getElementsByTagName("Arguments")[0]
                    scale=result.getElementsByTagName("Scale")[0]
                    propor=result.getElementsByTagName("Proportion")[0]
                    dispform=result.getElementsByTagName("DisplayFormat")[0]
                    values=result.getElementsByTagName("Value")[0]
                    rawstring=result.getElementsByTagName("RawString")[0]
                    jsonstring=result.getElementsByTagName("JSON")[0]

                    for child in desc.childNodes:
                        description=child.nodeValue
                        dictData[testclient][identifyName][description]={}

                    dictTags={
                        "Title": title,
                        "AppVersion": appver,
                        "Arguements": args,
                        "Scale": scale,
                        "Proportion": propor,
                        "DisplayFormat": dispform,
                        "Value": values,
                        "RawString": rawstring,
                        "JSON": jsonstring
                    }
                    parse_nodes(dictData, dictTags, testclient, identifyName, description)
                    #for child in title.childNodes:
                    #    title=child.nodeValue
                    #    dictData[testclient][identifyName][description]["Title"]=title
            except:
                continue

    print(json.dumps(dictData, sort_keys=True, indent=4))
    return dictData

def convert_xmltojson(url):
    dom = minidom.parse(url)
    f = open('phoronix-test-suite.json', 'w')
    f.write(json.dumps(parse_element(dom), sort_keys=True, indent=4))
    f.close()
