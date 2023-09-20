from flask import *
import pymysql

#start
app=Flask(__name__)
#sessions
#ster1 provide secret key to your application
# avoid sessioning hijacking,cross_site scription
app.secret_key="12325436542nkghghdfhgfghfd@@#$"

#home route
@app.route('/')
def main():
     return render_template('index.html')

#vendor registration route
@app.route('/vendor_registration',methods=['POST','GET'])
def register_vendor():
    if request.method=='POST':
        vendor_name=request.form['name']
        vendor_contact=request.form['contact']
        vendor_email=request.form['email']
        vendor_location=request.form['location']
        vendor_password=request.form['password']

        vendor_photo=request.files['photo']
        vendor_photo.save('static/images/' + vendor_photo.filename)

        vendor_desc=request.form['desc']

        connection= pymysql.connect(host='localhost',user='root',password='',database='simba_eshop')

        cursor = connection.cursor()

        sql = "insert into vendorstable(vendor_name,vendor_contact,vendor_email, vendor_location, vendor_password,vendor_photo,vendor_desc)values(%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql,(vendor_name,vendor_contact,vendor_email, vendor_location, vendor_password,vendor_photo.filename,vendor_desc))

        connection.commit()

        return render_template('vendor_register.html',message='vendor registration successful')
    else:
        return render_template('vendor_register.html',message='please register here')
    





    #vendor_login route
@app.route('/vendor_login',methods=['POST','GET'])
def vendor_login():
        if request.method=='POST':
            vendor_name=request.form['name']

            vendor_password=request.form['password']


            connection= pymysql.connect(host='localhost',user='root',password='',database='simba_eshop')

            cursor = connection.cursor()

            sql="select*from vendorstable where vendor_name=%s and vendor_password=%s"


            cursor.execute(sql,(vendor_name,vendor_password))

            

            count=cursor.rowcount
            if count==0:
                 

                 return render_template('vendor_login.html', message='invalid credentials')
            else:
                 #session
                 user_record=cursor.fetchone()
                 session['key']=user_record[1]
                 session['vendor_id']=user_record[0]
                 session['contact']=user_record[2]
                 session['location']=user_record[4]
                 session['image']=user_record[6]
                 session['desc']=user_record[7]

                 return redirect('/vendor_profile')
        else:
             return render_template('vendor_login.html',message='please login here')
        



#user log out
@app.route('/user_logout')
def user_logout():
     if 'user_key' in session:
            session.clear()
     return redirect('/user_login')



        #vendor profile_profile

@app.route('/vendor_profile')
def vendor_profile():
     return render_template('vendor_profile.html')
#vendor log out
@app.route('/vendor_logout')
def vendor_logout():
     if 'key' in session:
            session.clear()
     return redirect('/vendor_login')

#add product route
@app.route('/add_product', methods=['POST','GET'])
def add_product():
     if request.method=='POST':
          product_name=request.form['name']
          product_desc=request.form['desc']
          product_cost=request.form['cost']
          product_discount=request.form['discount']
          product_category=request.form['category']
          product_brand=request.form['brand']
          product_image=request.files['image']
          product_image.save ('static/products/' + product_image.filename)
          vendor_id=request.form['vendor']
          
          
          connection = pymysql.connect(
            host='localhost', user='root', password='', database='simba_eshop')

          cursor = connection.cursor()

          data = (product_name, product_desc, product_cost, product_discount,
                product_category, product_brand, product_image.filename, vendor_id)

          sql = "insert into products (product_name, product_desc, product_cost, product_discount, product_category, product_brand, product_image, vendor_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"

          cursor.execute(sql, data)

          connection.commit()
          return render_template('vendor_profile.html', message='Product Added Successfully')

     else:
        return render_template('vendor_profile.html', message='Please Add Product Details')
     
     #view products
@app.route('/view_products')
def view_products():
       connection = pymysql.connect(
            host='localhost', user='root', password='', database='simba_eshop')
       cursor=connection.cursor()
       sql="select*from products where vendor_id=%s"
       cursor.execute(sql,session['vendor_id'])
       count=cursor.rowcount
       if count ==0:
         return render_template('view_products.html', message='No product available')
       else:
              data=cursor.fetchall()
              return render_template('view_products.html',products= data)
           

@app.route('/update/<product_id>', methods=['POST', 'GET'])
def update_product(product_id):
    if request.method == 'POST':
        product_name = request.form['name']
        product_desc = request.form['desc']
        product_cost = request.form['cost']
        product_discount = request.form['discount']
        product_category = request.form['category']
        product_brand = request.form['brand']
        product_image = request.files['image']
        product_image.save('static/products/' + product_image.filename)

        vendor_id = request.form['vendor']

        connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')
        
        cursor = connection.cursor()
        sql = "update products set product_name = %s, product_desc=%s, product_cost = %s, product_discount = %s, product_category = %s, product_brand = %s, product_image = %s where product_id = %s"

        data = (product_name, product_desc, product_cost, product_discount, product_category, product_brand, product_image.filename, product_id)

        cursor.execute(sql, data)
        connection.commit()

        return redirect('/view_products')

    else:
        connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')

        cursor = connection.cursor()
        sql = "select * from products where product_id = %s"
        cursor.execute(sql, product_id)
        data = cursor.fetchone()
        return render_template('update.html', data=data)


#delete products

@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product():
    if request.method=='POST':
          product_name=request.form['name']
          product_desc=request.form['desc']
          product_cost=request.form['cost']
          product_discount=request.form['discount']
          product_category=request.form['category']
          product_brand=request.form['brand']
          product_image=request.files['image']
          product_image.save ('static/products/' + product_image.filename)
          vendor_id=request.form['vendor']
      
          connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')
        
          cursor = connection.cursor()
          sql = "delete *from vendorstable where products (product_name, product_desc, product_cost, product_discount, product_category, product_brand, product_image, vendor_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"
          data = (product_name, product_desc, product_cost, product_discount, product_category, product_brand, product_image.filename, vendor_id)

          cursor.execute(sql, data)

          connection.commit()
          return redirect('/delete_product')
    else:
         return render_template('delete.html')
        



    








@app.route('/buy_products')
def buy_products():
      connection = pymysql.connect(
            host='localhost', user='root', password='', database='simba_eshop')
      
      #shoes
      cursor_shoes=connection.cursor()
      sql_shoes='select* from products where product_category= "shoes" '
      cursor_shoes.execute(sql_shoes)
      shoes=cursor_shoes.fetchall()

      #fruits

      cursor_fruits=connection.cursor()
      sql_fruits='select* from products where product_category= "fruits" '
      cursor_fruits.execute(sql_fruits)
      fruits=cursor_fruits.fetchall()


      #heels
      cursor_heels=connection.cursor()
      sql_heels='select* from products where product_category= "heels" '
      cursor_heels.execute(sql_heels)
      heels=cursor_heels.fetchall()

      #cake


      cursor_cake=connection.cursor()
      sql_cake='select* from products where product_category= "cakes" '
      cursor_cake.execute(sql_cake)
      cake=cursor_cake.fetchall()

      return render_template('buy_products.html',shoes=shoes,fruits=fruits,heels=heels,cake=cake)

     
@app.route('/single_item/<product_id>')
def single_item(product_id):
    connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')

    cursor = connection.cursor()

    sql = "select * from products where product_id = %s"

    cursor.execute(sql, product_id)

    single_record = cursor.fetchone()


    

    category = single_record[6]

    cursor_similar = connection.cursor()
    sql_similar = "select * from products where product_category = %s ORDER BY RAND() LIMIT 3"
    cursor_similar.execute(sql_similar, category)

    similar_products = cursor_similar.fetchall()

    return render_template('single_item.html', single_record=single_record, similar_products=similar_products)




@app.route('/user_register',methods=['POST','GET'])
def user_register():
     if request.method=='POST':
          username =request.form['username']
          phone=request.form['phone']
          password=request.form['password']

          connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')
          
          cursor=connection.cursor()

          sql="insert into users (username,phone,password) values (%s,%s,%s)"

          cursor.execute(sql,(username,phone,password))

          connection.commit()

          return render_template('user_register.html',message='Success')
     else:
          return render_template('user_register.html', message='Register here')
     

@app.route('/user_login',methods=['POST','GET'])
def user_login():
    if request.method=='POST':
         username=request.form['username']
         password=request.form['password']

         connection = pymysql.connect(
        host='localhost', user='root', password='', database='simba_eshop')
          
         cursor=connection.cursor()

         sql='select*from users where username=%s and password=%s'

         cursor.execute(sql,(username,password))

         count=cursor.rowcount
         if count==0:
              return render_template('user_login.html',message='invalid credentials')
         else:
              user_record=cursor.fetchone()
              session['user_key']=user_record[0]
              session['phone']=user_record[1]

              return redirect('/buy_products')
    else:
         return render_template('user_login.html',message='please login here')
              
         
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "10",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Modcom",
            "TransactionDesc": "Modcom"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return "Please check YOur Phone to complete payment"
    else:
        return render_template('single_item.html')

app.run(debug=True)














        


 
      
 
        






    

