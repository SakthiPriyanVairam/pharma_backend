from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_migrate import Migrate
from flask_cors import CORS  
from marshmallow import Schema, fields
import os
from werkzeug.utils import secure_filename






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Limit file size to 16MB


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)


CORS(app)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Business model
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200))
    gst_no = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    dl_no = db.Column(db.String(50))
    email_id = db.Column(db.String(100))

class Logo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), nullable=False)

# Business schema
class BusinessSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    gst_no = fields.Str()
    phone_number = fields.Str()
    dl_no = fields.Str()
    email_id = fields.Str()

business_schema = BusinessSchema()
businesses_schema = BusinessSchema(many=True)

# Supplier model
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    gst_no = db.Column(db.String(50))
    dl_no = db.Column(db.String(50))

    def __init__(self, name, address=None, phone_number=None, email=None, gst_no=None, dl_no=None):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.gst_no = gst_no
        self.dl_no = dl_no

# Supplier schema
class SupplierSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    gst_no = fields.Str()
    dl_no = fields.Str()

supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)

class HSNCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
   

    def __init__(self, code, description=None):
        self.code = code
        

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False) 
    price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    sgst_percent = db.Column(db.Float, nullable=False)
    igst_percent = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    batch_no = db.Column(db.String(50))
    hsn_code_id = db.Column(db.Integer, db.ForeignKey('hsn_code.id'), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    mrp = db.Column(db.Float)
    expiry_date = db.Column(db.Date)
    hsn_code = db.relationship('HSNCode', backref=db.backref('purchase_orders', lazy=True))

    def __init__(self, product_name, quantity, unit, price, discount_percent, sgst_percent, igst_percent, batch_no, hsn_code_id, purchase_date, mrp, expiry_date):
        self.product_name = product_name
        self.quantity = quantity
        self.unit = unit
        self.price = price
        self.discount_percent = discount_percent
        self.sgst_percent = sgst_percent
        self.igst_percent = igst_percent
        self.batch_no = batch_no
        self.hsn_code_id = hsn_code_id
        self.purchase_date = purchase_date
        self.mrp = mrp
        self.expiry_date = expiry_date
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self):
        discount_amount = self.price * (self.discount_percent / 100)
        sgst_amount = self.price * (self.sgst_percent / 100)
        igst_amount = self.price * (self.igst_percent / 100)
        total=(self.price - discount_amount) + sgst_amount + igst_amount
        print(total)
        return total
    
class HSNCodeSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
  
class PurchaseOrderSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    product_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    unit = fields.Str(required=True)
    price = fields.Float(required=True)
    discount_percent = fields.Float(required=True)
    sgst_percent = fields.Float(required=True)
    igst_percent = fields.Float(required=True)
    total_cost = fields.Float(dump_only=True)
    batch_no = fields.Str(required=True)
    hsn_code_id = fields.Int(required=True)
    purchase_date = fields.Date(required=True)
    mrp = fields.Float(required=True)
    expiry_date = fields.Date(required=True)

hsn_code_schema = HSNCodeSchema()
hsn_codes_schema = HSNCodeSchema(many=True)

purchase_order_schema = PurchaseOrderSchema()
purchase_orders_schema = PurchaseOrderSchema(many=True)

# Initialize the database
with app.app_context():
    db.create_all()




class CustomerSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    gst_no = fields.Str()
    dl_no = fields.Str()    


class ProductSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)



class InvoiceSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    invoice_date = fields.DateTime()
    customer_id = fields.Int()

class TransactionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    transaction_date = fields.DateTime()
    type = fields.Str()
    amount = fields.Float()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    gst_no = db.Column(db.String(50))
    dl_no = db.Column(db.String(50))

    def __init__(self, name, address=None, phone_number=None, email=None, gst_no=None, dl_no=None):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.gst_no = gst_no
        self.dl_no = dl_no



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('invoices', lazy=True))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    type = db.Column(db.String(50), nullable=False)  # e.g., 'purchase', 'sale', 'payment', 'refund'
    amount = db.Column(db.Float, nullable=False)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

purchase_order_schema = PurchaseOrderSchema()
purchase_orders_schema = PurchaseOrderSchema(many=True)

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

@app.route('/api/business', methods=['POST'])
def add_business():
    data = request.get_json()
    new_business = Business(
        name=data['name'],
        address=data['address'],
        gst_no=data['gst_no'],
        phone_number=data['phone_number'],
        dl_no=data['dl_no'],
        email_id=data['email_id']
    )
    db.session.add(new_business)
    db.session.commit()
    return jsonify({'message': 'Business added successfully'}), 201

# Endpoint to get business information
@app.route('/api/business', methods=['GET'])
def get_all_businesses():
    businesses = Business.query.all()
    business_list = []
    for business in businesses:
        business_info = {
            'name': business.name,
            'address': business.address,
            'gst_no': business.gst_no,
            'phone_number': business.phone_number,
            'dl_no': business.dl_no,
            'email_id': business.email_id
        }
        business_list.append(business_info)
    return jsonify(business_list), 200

# Endpoint to delete a business

@app.route('/api/business', methods=['DELETE'])
def delete_all_businesses():
    try:
        businesses = Business.query.all()
        for business in businesses:
            db.session.delete(business)
        
        # Commit all deletions to the database
        db.session.commit()
        
        return jsonify({'message': 'All businesses deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/logo/upload', methods=['POST'])
def upload_logo():
    
    file = request.files['file']
 
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    new_logo = Logo(
        
        filename=filename,
        path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    )
    db.session.add(new_logo)
    db.session.commit()
    
    return jsonify({'message': 'Logo uploaded successfully'}), 201

@app.route('/api/logo/delete', methods=['DELETE'])
def delete_all_logos():
    try:
        logos = Logo.query.all()
        for logo in logos:
            if os.path.exists(logo.path):
                os.remove(logo.path)
                
                db.session.delete(logo)
        
        db.session.commit()
        
        return jsonify({'message': 'All logos deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/logo', methods=['GET'])
def get_logo():
    logos = Logo.query.all()
    logo = logos[0]
    
    if os.path.exists(logo.path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], logo.filename)
    else:
        return jsonify({'error': 'Logo file not found on the server'}), 404

######################################################################################
@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(
        name=data['name'],
        address=data.get('address', ''),
        phone_number=data.get('phone_number', ''),
        email=data.get('email', ''),
        gst_no=data.get('gst_no', ''),
        dl_no=data.get('dl_no', '')
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@app.route('/api/customers', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    return jsonify(customers_schema.dump(all_customers))

@app.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.address = data.get('address', customer.address)
    customer.phone_number = data.get('phone_number', customer.phone_number)
    customer.email = data.get('email', customer.email)
    customer.gst_no = data.get('gst_no', customer.gst_no)
    customer.dl_no = data.get('dl_no', customer.dl_no)
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return jsonify(products_schema.dump(all_products))

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})



@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    data = request.json
    new_supplier = Supplier(
        name=data['name'],
        address=data.get('address', ''),
        phone_number=data.get('phone_number', ''),
        email=data.get('email', ''),
        gst_no=data.get('gst_no', ''),
        dl_no=data.get('dl_no', '')
    )
    db.session.add(new_supplier)
    db.session.commit()
    return supplier_schema.jsonify(new_supplier), 201

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    all_suppliers = Supplier.query.all()
    return jsonify(suppliers_schema.dump(all_suppliers))

@app.route('/api/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    return supplier_schema.jsonify(supplier)

@app.route('/api/suppliers/<int:id>', methods=['PUT'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    data = request.json
    supplier.name = data.get('name', supplier.name)
    supplier.address = data.get('address', supplier.address)
    supplier.phone_number = data.get('phone_number', supplier.phone_number)
    supplier.email = data.get('email', supplier.email)
    supplier.gst_no = data.get('gst_no', supplier.gst_no)
    supplier.dl_no = data.get('dl_no', supplier.dl_no)
    db.session.commit()
    return supplier_schema.jsonify(supplier)

@app.route('/api/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'})



@app.route('/api/hsn_codes', methods=['POST'])
def create_hsn_code():
    data = request.json
    new_hsn_code = HSNCode(code=data['code'])
    db.session.add(new_hsn_code)
    db.session.commit()
    return hsn_code_schema.jsonify(new_hsn_code), 201

@app.route('/api/hsn_codes', methods=['GET'])
def get_hsn_codes():
    all_hsn_codes = HSNCode.query.all()
    return jsonify(hsn_codes_schema.dump(all_hsn_codes))

@app.route('/api/hsn_codes/<int:id>', methods=['GET'])
def get_hsn_code(id):
    hsn_code = HSNCode.query.get_or_404(id)
    return hsn_code_schema.jsonify(hsn_code)

@app.route('/api/hsn_codes/<int:id>', methods=['PUT'])
def update_hsn_code(id):
    hsn_code = HSNCode.query.get_or_404(id)
    data = request.json
    hsn_code.code = data.get('code', hsn_code.code)
    db.session.commit()
    return hsn_code_schema.jsonify(hsn_code)

@app.route('/api/hsn_codes/<int:id>', methods=['DELETE'])
def delete_hsn_code(id):
    hsn_code = HSNCode.query.get_or_404(id)
    db.session.delete(hsn_code)
    db.session.commit()
    return jsonify({'message': 'HSN code deleted successfully'})

# API endpoints for Purchase Orders
@app.route('/api/purchase_orders', methods=['POST'])
def create_purchase_order():
    data = request.json
    purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
    expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else None
    new_purchase_order = PurchaseOrder(
        product_name=data['product_name'],
        quantity=data['quantity'],
        unit=data['unit'],
        price=data['price'],
        discount_percent=data['discount_percent'],
        sgst_percent=data['sgst_percent'],
        igst_percent=data['igst_percent'],
        batch_no=data['batch_no'],
        hsn_code_id=data['hsn_code_id'],
        purchase_date=purchase_date,
        mrp=data.get('mrp', 0.0),
        expiry_date=expiry_date
    )
    db.session.add(new_purchase_order)
    db.session.commit()
    return purchase_order_schema.jsonify(new_purchase_order), 201

@app.route('/api/purchase_orders', methods=['GET'])
def get_purchase_orders():
    all_purchase_orders = PurchaseOrder.query.all()
    return jsonify(purchase_orders_schema.dump(all_purchase_orders))

@app.route('/api/purchase_orders/<int:id>', methods=['GET'])
def get_purchase_order(id):
    purchase_order = PurchaseOrder.query.get_or_404(id)
    return purchase_order_schema.jsonify(purchase_order)

@app.route('/api/purchase_orders/<int:id>', methods=['PUT'])
def update_purchase_order(id):
    purchase_order = PurchaseOrder.query.get_or_404(id)
    data = request.json
    purchase_order.product_name = data.get('product_name', purchase_order.product_name)
    purchase_order.quantity = data.get('quantity', purchase_order.quantity)
    purchase_order.unit = data.get('unit', purchase_order.unit)
    purchase_order.price = data.get('price', purchase_order.price)
    purchase_order.discount_percent = data.get('discount_percent', purchase_order.discount_percent)
    purchase_order.sgst_percent = data.get('sgst_percent', purchase_order.sgst_percent)
    purchase_order.igst_percent = data.get('igst_percent', purchase_order.igst_percent)
    purchase_order.batch_no = data.get('batch_no', purchase_order.batch_no)
    purchase_order.hsn_code_id = data.get('hsn_code_id', purchase_order.hsn_code_id)
    purchase_order.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
    purchase_order.mrp = data.get('mrp', purchase_order.mrp)
    purchase_order.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else purchase_order.expiry_date
    purchase_order.total_cost = purchase_order.calculate_total_cost()
    db.session.commit()
    return purchase_order_schema.jsonify(purchase_order)

@app.route('/api/purchase_orders/<int:id>', methods=['DELETE'])
def delete_purchase_order(id):
    purchase_order = PurchaseOrder.query.get_or_404(id)
    db.session.delete(purchase_order)
    db.session.commit()
    return jsonify({'message': 'Purchase order deleted successfully'})


@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    new_invoice = Invoice(invoice_date=data.get('invoice_date'), customer_id=data.get('customer_id'))
    db.session.add(new_invoice)
    db.session.commit()
    return invoice_schema.jsonify(new_invoice), 201

# API endpoint to get all invoices
@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    all_invoices = Invoice.query.all()
    return jsonify(invoices_schema.dump(all_invoices))

# API endpoint to get a specific invoice by ID
@app.route('/api/invoices/<int:id>', methods=['GET'])
def get_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    return invoice_schema.jsonify(invoice)

# API endpoint to update an invoice
@app.route('/api/invoices/<int:id>', methods=['PUT'])
def update_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    data = request.json
    invoice.invoice_date = data.get('invoice_date', invoice.invoice_date)
    invoice.customer_id = data.get('customer_id', invoice.customer_id)
    db.session.commit()
    return invoice_schema.jsonify(invoice)

# API endpoint to delete an invoice
@app.route('/api/invoices/<int:id>', methods=['DELETE'])
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice deleted successfully'})


@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.json
    new_transaction = Transaction(transaction_date=data.get('transaction_date'), type=data['type'], amount=data['amount'])
    db.session.add(new_transaction)
    db.session.commit()
    return transaction_schema.jsonify(new_transaction), 201

# API endpoint to get all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    all_transactions = Transaction.query.all()
    return jsonify(transactions_schema.dump(all_transactions))

# API endpoint to get a specific transaction by ID
@app.route('/api/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return transaction_schema.jsonify(transaction)

# API endpoint to update a transaction
@app.route('/api/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    data = request.json
    transaction.transaction_date = data.get('transaction_date', transaction.transaction_date)
    transaction.type = data.get('type', transaction.type)
    transaction.amount = data.get('amount', transaction.amount)
    db.session.commit()
    return transaction_schema.jsonify(transaction)

# API endpoint to delete a transaction
@app.route('/api/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='localhost')
