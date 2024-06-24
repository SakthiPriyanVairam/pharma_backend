
POST http://localhost:5000//api/business: Create a new business.
GET http://localhost:5000//api/business: Get all businesses.
PUT http://localhost:5000//api/business: Update the details of the first business (consider adding support for updating by ID).
DELETE http://localhost:5000//api/business: Delete the first business.



{
  "name": "Sugam Pharma",
  "address": "D-224,Kurichi Housing Unit,Phase II, Sidco,Coimbatore-641021",
  "gst_no": "GST1234567890",
  "phone_number": "7010562258",
  "dl_no": "DL1234567890",
  "email_id": "sugampharma4u@gmail.com"
}


POST http://localhost:5000/api/suppliers: Create a new supplier.
GET http://localhost:5000//api/suppliers: Get all suppliers.
GET http://localhost:5000//api/suppliers/<id>: Get a specific supplier by ID.
PUT http://localhost:5000//api/suppliers/<id>: Update a specific supplier by ID.
DELETE http://localhost:5000//api/suppliers/<id>: Delete a specific supplier by ID.


{
  "name": "YN Pharma",
  "address": "Podanur",
  "gst_no": "GST167890",
  "phone_number": "7056565258",
  "dl_no": "DL1234567890",
  "email_id": ""
}



LOGO UPLOAD

POST http://localhost:5000/api/logo/upload :UPLOAD LOGO
GET http://localhost:5000/api/logo :Get LOGO
DELETE http://localhost:5000/api/logo/delete :delete LOGO


Form-DATA : 

file,type:file,value:select files


