import os
import sys
import NVD
result=[]
n=len(sys.argv)

def print_xml_extracted_files(res):
    for i in xrange(0,len(result)):
            for item in  result[i].iteritems():
                print item[0],item[1][0],item[1][1],item[1][2]


if n==1:
    print 'no argument xml file passed'
else:
    try:
        path ="C:\\Users\\gssgu_000\\PycharmProjects\\fortinet\\download"
        for i in xrange(1,n):
            d1=[]
            filename=sys.argv[i]
            fullname = os.path.join(path, filename)
            d1=NVD.extract(fullname)
            result.append(d1)
        #print_xml_extracted_files(result)

        NVD.save2db(result)

    except IOError:
        print 'XML file name Error/or File Does Not EXITS'


