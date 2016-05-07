import logging
import os
import MySQLdb
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
logger =logging.getLogger("vuln")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename="C:\\Users\\gssgu_000\\PycharmProjects\\fortinet\\log\\myapp.log",
                    filemode='w')

#path="C:\\Users\\gssgu_000\\PycharmProjects\\fortinet\\download"
#filepath= os.path.join(path,"nvdcve-2015.xml")

def extract(filepath):      #This extract function provide functinality of parse_nvd_entry elements and storing them in dictionary
    datacollected={}
    count=0
    #filepath="C:\\Users\\gssgu_000\\PycharmProjects\\fortinet\\download\\nvdcve-2015.xml"
    for event,elem in ET.iterparse(filepath):
        if event=="end":
            try:
                if elem.tag=="{http://nvd.nist.gov/feeds/cve/1.2}entry":
                    count+=1
                    if 'severity' in elem.attrib and 'published' in elem.attrib and 'modified' in elem.attrib:
                        datacollected[str(elem.attrib['name'])]=[str(elem.attrib['severity']),str(elem.attrib['published']),str(elem.attrib['modified'])]
                        logger.debug("Entry created:{}".format(str(count)))
                        logger.debug("cve_id: {}".format(str(elem.attrib['name'])))
                        logger.debug("serverity: {}".format(str(elem.attrib['severity'])))
                        logger.debug("published: {}".format(str(elem.attrib['published'])))
                        logger.debug("modified: {}".format(str(elem.attrib['modified'])))

                    else:
                       # print'severity->null'
                        datacollected[str(elem.attrib['name'])]=["Not applicable",str(elem.attrib['published']),str(elem.attrib['modified'])]
                        logger.debug("Entry created:{}".format(str(count)))
                        logger.debug("cve_id: {}".format(str(elem.attrib['name'])))
                        logger.debug("published: {}".format(str(elem.attrib['published'])))
                        logger.debug("modified: {}".format(str(elem.attrib['modified'])))
                        #print datacollected to print the extracted attributes from XML file

                elem.clear()
            except KeyError:
                print 'Keyerror'
    return datacollected

def save2db(result):
    try:
        db=MySQLdb.connect(user="root",db="fortinet",passwd="1234",host='localhost')
        c=db.cursor()
        c.execute("DROP TABLE IF EXISTS exdata")
        sql="""CREATE TABLE exdata (
         cve_id  CHAR(27) NOT NULL PRIMARY KEY,
         severity  CHAR(50),
         published CHAR(50),
         modified CHAR(50))"""
        c.execute(sql)

        if not result:
            print 'list is empty'
        else:
            for i in xrange(0,len(result)):
                for item  in  result[i].iteritems():
                    query="INSERT INTO exdata (cve_id,severity, published,modified) \
       VALUES ('%s', '%s', '%s', '%s')" %(item[0], item[1][0],item[1][1],item[1][2])
                    c.execute(query)



    except MySQLdb.Error as e:
            print 'error',e
    finally:
        db.commit()
        c.close()
        db.close()