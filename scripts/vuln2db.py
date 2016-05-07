import os
import sys
import NVD
result=[]
n=len(sys.argv)
if n==1:
    print 'no argument xml file passed'
else:
    try:
        path ="C:\\Users\\gssgu_000\\PycharmProjects\\fortinet\\download"
        for i in xrange(1,n):
            d1=[]
            filename=sys.argv[i]
            if filename.endswith('.xml'):

                fullname = os.path.join(path, filename)
                d1=NVD.extract(fullname)
                result.append(d1)

        NVD.save2db(result)

    except IOError:
        print 'XML file name Error/or File Does Not EXIST'

