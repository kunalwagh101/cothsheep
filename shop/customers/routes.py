from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask ,render_template, redirect , session , request ,flash ,current_app,url_for
from shop import app ,db,search ,bcrypt,login_manager
from shop.customers.form import CustomerForm ,LoginForm
from shop.customers.models import Customer,CustomerOrder


import secrets 

@app.route("/customer_register",methods =["POST","GET"])
def customer_register():
    form= CustomerForm(request.form)
    if request.method == 'POST' and form.validate():
        try :

      
            name = form.name.data
            email = form.email.data
            
            pw_hash = bcrypt.generate_password_hash(form.password.data)

            city = form.city.data
            country = form.country.data
            contact = form.contact.data
            address = form.address.data
            zipcode = form.zipcode.data
            customer = Customer(name = name ,email = email , password = pw_hash ,
                                city = city , country = country, contact = contact,
                                  address = address, zipcode = zipcode  )
            db.session.add(customer)

            flash(f'{name} thank you registration ',"success")
            db.session.commit()
            return redirect(url_for('loginregister'))
        except ValueError as e :
             flash(f'error occured {e}')
    


    return render_template("customers/register.html",form = form )


@app.route("/loginregister",methods =["POST","GET"])
def loginregister() :
      form = LoginForm(request.form)
      if request.method == 'POST' and form.validate():

        try :
            email =form.email.data 
            password = form.password.data 
            
            check_email = Customer.query.filter_by(email = email).first()
         
            if check_email and bcrypt.check_password_hash(check_email.password, password) :
                login_user(check_email) 
                flash(f'welcome {check_email.name} u are logged in ','success')
                next = request.args.get('next')
                return redirect( next or url_for('index') )
            flash('wrong password or email ','danger')
            return redirect(url_for('loginregister'))

        except ValueError as e :
             flash(f'error occured {e}')
    
      


      return render_template("customers/login.html",form = form)



@app.route("/customer_order")
def customer_order() :
            if current_user.is_authenticated : # type: ignore
                customer_id = current_user.id # type: ignore
                print("customer_id = ", customer_id)
                invoice = secrets.token_hex(5)
                try :
                        data_id = CustomerOrder.query.get_or_404(customer_id)
                        if data_id :
                            CustomerOrder.query.filter_by(id = customer_id).update(dict(orders=session["shoppingcart"]))
                             
                        else:
                            order = CustomerOrder(invoice = invoice , customer_id = customer_id ,orders= session["shoppingcart"])     
                            db.session.add(order)
                            flash("You'er order has been placed ","success")
                        
                        db.session.commit()
                        session.pop('shoppingcart')
                        return redirect(url_for("order",invoice=invoice))
                except Exception as e  :
                        print(e)
            else :
                 flash("soemthing went wrong ","danger")
                 return redirect(url_for('cart'))
            return redirect(url_for('cart'))




@app.route("/order/<invoice>")
def order(invoice) :
      
      if current_user.is_authenticated : # type: ignore
              customer_id = current_user.id # type: ignore
              grandtotal = 0
              customer = Customer.query.filter_by(id = customer_id).first()
              customer_order = CustomerOrder.query.filter_by(id = customer_id).order_by(CustomerOrder.id.desc()).first()
              for key ,product in customer_order.orders.items() :
            
                total1 = float(product['price']) * int(product["quantity"])
                discount_max = (product["discount"]/100) * float(total1)
                grandtotal += float(total1) - float(discount_max)

      else :
            return redirect(url_for('customer_register'))
      return render_template("customers/order.html", invoice = invoice ,grandtotal = grandtotal ,customer = customer ,customer_order = customer_order)






@app.route("/customer_logout")
def customer_logout() :
      logout_user()
      return redirect(url_for('index'))
