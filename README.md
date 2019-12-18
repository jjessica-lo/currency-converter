# currency-converter

The project Currency Converter permits to convert currency online.

The API is accehttps://github.com/jjessica-lo/currency-converter/pullsssible at the URL: 

https://ancient-beach-41982.herokuapp.com/convert

The requested parameters are:
-> amount : amount to convert, float format;
-> src_currency : ISO currency code for the amount we want to convert;
-> dest_currency : ISO currency code for the converted amount that we will receive as result;
-> reference_data : date for the reference rate, yyyy-mm-dd format 

Data are provided by the European Central Bank and are relative to the last 30 days exchanging rates.

If you want more information about the implemented logic, please refer to the file "application.py".


Example:
Invoke the API using the following parameters

https://ancient-beach-41982.herokuapp.com/convert?amount=3&src_currency=AUD&dest_currency=MXN&reference_date=2019-12-12

the given response will be:

{ 
  "amount": 463.71, 
  "currency": "MXN"
}


Managed errors:

-> 'bad request' : the URL parameters could not respect the specification 
-> 'not valid CUR codes' : the inserted currency does not respect the ISO standard
-> 'date format must be yyyy-mm-dd' : error in the date format
-> 'no data found for given input' : the query has not produced results
