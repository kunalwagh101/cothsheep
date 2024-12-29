from shop.products.models import Brand, Category ,Addproduct
from flask import Flask ,render_template, redirect , session , request ,flash ,current_app,url_for
from shop import app ,db,login_manager
from flask_login import login_user, current_user



def mergeDicts(dict1,dict2):
     if isinstance(dict1,list) and isinstance(dict2,list) :
        return dict1 + dict2
     elif  isinstance(dict1,dict) and isinstance(dict2,dict) :
         return dict(list(dict1.items())+ list(dict2.items()))
     return False



@app.route("/carts" , methods =["GET", "POST"])
def cart():
    if  current_user.is_authenticated :  # type: ignore
    
        if "shoppingcart" not in session or len(session["shoppingcart"]) <=0  :
            return redirect(url_for('index'))
        
        brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
        categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
        
        grandtotal = 0
    
        

        for key ,product in session["shoppingcart"].items() :
            
            total1 = float(product['price']) * int(product["quantity"])
            discount_max = (product["discount"]/100) * float(total1)
            grandtotal += float(total1) - float(discount_max)

    else :
        flash("please login ","danger")
        return redirect(url_for('loginregister'))

    
    return render_template("products/cart.html",grandtotal = grandtotal,brands = brands,categorys =categorys    )






@app.route("/addcart" , methods =["GET", "POST"])
def addcart():


   

    try:
         product_id = request.form.get('product_id')
         quantity = request.form.get('quantity')
         colors = request.form.get('color')
         product = Addproduct.query.filter_by(id = product_id).first()
         if request.method == "POST" :
              Dict_items =  {product_id : {"name": product.name , "price": product.price,
                                             "discount":product.discount,"quantity":quantity, "stock":product.stock,
                                            "color":  colors,"image": product.image1 , "colors" :product.color  }}
            
              if "shoppingcart" in session:
                
                if product_id in session["shoppingcart"] :
                    print("it is working 123")
                    for key,item in session["shoppingcart"].items() :
                        # print("key , produc_id",type(key),type(product_id))
                        print("shoping",session['shoppingcart'])
                      
                        if str(key) == str(product_id)  :
                            print("it is working")
                            session.modified =True
                            quan = int(item["quantity"] )  
                            quan += 1 
                            item["quantity"] = str(quan)
                            flash("Added to the cart successfully ","success")  

                
                else :
                   flash("Added to the cart successfully ","success")
                   session['shoppingcart'] = mergeDicts(session["shoppingcart"],Dict_items)

                   

                   return redirect(request.referrer)
              else :
                flash("Added to the cart successfully ","success")
                session['shoppingcart'] =  Dict_items
                
                return redirect(request.referrer)


              
    except Exception as e :
            print("erorr = " ,e)
    finally:
          
        return redirect(request.referrer)



@app.route("/updatecarts/<int:code>" , methods =["POST"])
def updatecart(code):
        if "shoppingcart" not in session or  len(session["shoppingcart"]) <=0 :
            return redirect(url_for('index'))
        if request.method == "POST" :
            quantity = request.form.get('quantity')
           
            colors  = request.form.get('colors')
            try :
                session.modified = True
                
                for key,item in session["shoppingcart"].items() :
                    if int(key)  == int(code) :
                        item['color'] =  colors
                        item['quantity'] = quantity
                        flash("Updated succesfully ","success")
                        return redirect(url_for('cart'))
            except Exception as e :
                print(e)
                return redirect(url_for('cart'))
        return render_template("products/cart.html")



@app.route("/deletecarts/<int:id>" , methods =["POST","GET"])
def deletecart(id):
        if "shoppingcart" not in session or len(session["shoppingcart"]) <=0 :
            return redirect(url_for('index'))
        
        try :
            session.modified = True
            
            for key,item in session["shoppingcart"].items() :
                if int(key)  == id :
                    session["shoppingcart"].pop(key,None)
                    flash("Deleted succesfully ","success")
                    return redirect(url_for('cart'))
        except Exception as e :
            print(e)
            return redirect(url_for('cart'))
        return render_template("products/cart.html")
                



@app.route("/alldeletecarts" , methods =["POST","GET"])
def alldeletecart():
        if "shoppingcart" not in session or len(session["shoppingcart"]) <=0 :
            return redirect(url_for('index'))
        
        try :
            session.clear()

            session.pop("shoppingcart",None)
            flash("Entire cart deleted succesfully ","success")
            return redirect(url_for('cart'))
        except Exception as e :
            print(e)
            return redirect(url_for('cart'))
        
       

   
                
        


# @app.route("/empty")
# def empty():
#         try:
#             session["shoppimgcart"].clear()
#             return redirect(url_for('index'))
#         except Exception as e:
#              print(e)
 


        


