from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from xmljson import badgerfish as bf
from json import dumps
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
from urllib.request import urlopen


#Flask application
app = Flask(__name__)
api = Api(app)


#Converter class
class Converter(Resource):

    def get(self):
        args = request.args
        try:
            amount = args.get('amount', 0, type=float)
            src_currency = args.get('src_currency')
            dest_currency = args.get('dest_currency')
            reference_date = args.get('reference_date')
        except Exception as e:
            return {'amount': 0, 'currency': '', 'errorMsg': 'bad request'}

        errorMsg = ''

        if amount<=0:
            errorMsg = 'amount must be positive'

        if src_currency=='' or len(src_currency) != 3 or dest_currency=='' or len(dest_currency) != 3:
            errorMsg = 'not valid CUR codes'

        dateerrmsg = 'date format must be yyyy-mm-dd'
        if len(reference_date)!=10 or len(reference_date.split('-'))!=3:
            errorMsg = dateerrmsg
        else:
            splitteddate = reference_date.split('-')
            if len(splitteddate[0])!=4 or len(splitteddate[1])!=2 or len(splitteddate[2])!=2:
                errorMsg = dateerrmsg
            else:
                try:
                    int(splitteddate[0])
                    int(splitteddate[1])
                    int(splitteddate[2])
                except:
                    errorMsg = dateerrmsg

        inputrate = 0
        outputrate = 0

        if errorMsg=='':
            outputamout = 0
            outputcurrency = ''

            #retrieve data
            var_url = urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml')
            xmldoc = ET.parse(var_url)
            self.root = xmldoc.getroot()

            for cubes in self.root:
                if "Cube" in cubes.tag:
                    for datecube in cubes:
                        #datecube.tag: {http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube
                        #datecube.attrib: {'time': '2019-12-16'}
                        if datecube.attrib['time'] == reference_date:
                            for currnode in datecube:
                                #currNode.tag: {http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube 
                                #currNode.attrib: {'currency': 'USD', 'rate': '1.1174'}
                                if currnode.attrib['currency'] == src_currency:
                                    inputrate = currnode.attrib['rate']
                                if currnode.attrib['currency'] == dest_currency:
                                    outputrate = currnode.attrib['rate']

            if inputrate==0 or outputrate==0:
                errorMsg = 'no data found for given input'
            else:
                # amount : src_currency = [output_amount] : dest_currency
                outputamout = round((amount * float(outputrate) / float(inputrate)), 2)
                outputcurrency = dest_currency

        if errorMsg=='':
            response = {'amount': outputamout, 'currency': outputcurrency}
        else:
            response = {'amount': 0, 'currency': '', 'errorMsg': errorMsg}

        return response


api.add_resource(Converter, "/convert")

if __name__ == '__main__':
    app.run(debug=False)