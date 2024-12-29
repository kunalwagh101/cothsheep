from shop.products.models import Brand, Category ,Addproduct
from flask import Flask ,render_template, redirect , session , request ,flash ,current_app,url_for
from shop import app ,db,search
from shop.products.forms import AddproductForm
import secrets
import os 




def save_image(photo):
     
     try:

        hash_photo = secrets.token_urlsafe(10)
        _, file_extention = os.path.splitext(photo.filename)
        photo_name  =hash_photo + file_extention
        file_path = os.path.join(current_app.root_path, 'static/images',photo_name)
        photo.save(file_path)
        return photo_name
     except ValueError as e :
           flash(f"Error: {e}", 'danger')



@app.route('/' , methods= ['GET','POST'])
def index() :
    
    products = Addproduct.query.filter(Addproduct.category.has(Category.name == 'Trends')).filter(Addproduct.stock > 0).all()

    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
   
    categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    sort_cats = Addproduct.query.filter(Addproduct.category.has(Category.name == 'Movies')).all()

   

    return render_template('products/index.html',products = products, sort_cats = sort_cats,categorys = categorys , brands = brands) 


@app.route('/single_page/<int:id>' , methods= ['GET','POST'])
def single_page(id) :
  
    product = Addproduct.query.get_or_404(id)
    cat_filters = Addproduct.query.filter_by(category_id = product.category_id).all()
  
   # cat_filters = Addproduct.query.filter(Addproduct.category.has( Addproduct.category_id == )).all()



    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    
    return render_template('products/single_page.html',product = product, cat_filters = cat_filters ,category = category,brands = brands  ,categorys =categorys)


@app.route("/result")
def result() :
    keyword = request.args.get('q')
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    
    categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()

    products = Addproduct.query.msearch(keyword,fields=['name','description'],limit=20)
     
    return render_template("products/result.html",products = products ,brands = brands ,categorys= categorys)
    



@app.route('/brand/<int:id>' , methods= ['GET','POST'])
def brand(id) :
  
    brand =  Addproduct.query.filter_by(brand_id = id).all()
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    
    categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()

    
    return render_template('products/index.html', brand = brand,categorys = categorys  ,brands =brands)

 




@app.route('/category/<int:id>' , methods= ['GET','POST'])
def category(id) :
  
    category =  Addproduct.query.filter_by(category_id = id).all()
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categorys = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    
    return render_template('products/index.html', category = category,brands = brands  ,categorys =categorys)


@app.route('/updatebrand/<int:id>' , methods= ['GET','POST'])
def updatebrand(id) :
    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    
    updatebrands = Brand.query.get_or_404(id)
    if request.method == 'POST' :
        brand = request.form.get('brand')
        updatebrands.name = brand
        db.session.commit()
        flash(" Updated successfully ! ",'success') 
        return redirect(url_for('brands'))
    

    return render_template('products/updatebrand.html' ,  updatebrands = updatebrands)

     

@app.route('/updatecategory/<int:id>' , methods= ['GET','POST'])
def updatecategory(id) :
    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    
    updatecategorys = Category.query.get_or_404(id)
    if request.method == 'POST' :
        category = request.form.get('category')
        updatecategorys.name = category
        db.session.commit()
        flash(" Updated successfully ! ",'success')
        return redirect(url_for('categorys'))
    

    return render_template('products/updatebrand.html' ,  updatecategorys = updatecategorys)





@app.route('/updateproduct/<int:id>' , methods= ['GET','POST'])
def updateproduct(id) :
    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    
    updateproducts = Addproduct.query.get_or_404(id)
    print("updateproducts = ", updateproducts)
    brands  = Brand.query.all()
    categorys = Category.query.all()
    brand = request.form.get("brand")
    category = request.form.get("category")
    form = AddproductForm(request.form )
    
        

    
    if request.method == 'POST' :
        updateproducts.name = form.name.data
        updateproducts.gender  = form.gender.data
        updateproducts.price  = form.price.data
        updateproducts.discount  = form.discount.data
        updateproducts.stock  = form.stock.data
        updateproducts.description  = form.description.data
        updateproducts.color  = form.color.data
        updateproducts.brand_id  = brand
        updateproducts.category_id  = category

        if request.files.get('image1') :
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image1))
                updateproducts.image1 = save_image(request.files.get('image1'))
            except :
                updateproducts.image1 = save_image(request.files.get('image1'))

            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image2))
                updateproducts.image2 = save_image(request.files.get('image2'))
            except :
                updateproducts.image2 = save_image(request.files.get('image2'))

            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image3))
                updateproducts.image3 = save_image(request.files.get('image3'))
            except :
                updateproducts.image3 = save_image(request.files.get('image3'))


        db.session.commit()
        flash(" Updated successfully ! ",'success')
        return redirect(url_for('admin'))
    
    form.name.data = updateproducts.name
    form.gender.data = updateproducts.gender
    form.price.data = updateproducts.price
    form.discount.data = updateproducts.discount
    form.stock.data = updateproducts.stock
    form.description.data = updateproducts.description
    form.color.data = updateproducts.color
            

    return render_template('products/updateproduct.html'  ,form = form  ,brands = brands, categorys = categorys  , updateproducts = updateproducts)




@app.route('/deletebrand/<int:id>', methods= ['GET','POST'])
def deletebrand(id) :

    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id) 
    if request.method ==  "POST" :
        db.session.delete(brand)
        db.session.commit()
        flash(f'{brand.name} is delete succussfull','success')
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))


@app.route('/deletecategory/<int:id>', methods= ['GET','POST'])
def deletecategory(id) :

    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    category  = Category.query.get_or_404(id) 
    if request.method ==  "POST" :
        db.session.delete(category)

        
        db.session.commit()
        flash(f'{category.name} is delete succussfull' ,'success')
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))



@app.route('/deleteproduct/<int:id>', methods= ['GET','POST'])
def deleteproduct(id) :

    if 'email' not in session:
        flash('your are not Logged in !', 'danger')
        return redirect(url_for('login'))
    
    updateproducts  = Addproduct.query.get_or_404(id) 

    if request.method ==  "POST" :
        try:

                
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + updateproducts.image3))
        
        except Exception as e :
            print(e)

        db.session.delete(updateproducts)
        db.session.commit()
        flash(f'{updateproducts.name} is delete succussfull' ,'success')
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))



# @app.route('/updatebrand' , methods= ['GET','POST'])
# def updatebrand() :
#     if 'email' not in session:
#         flash('your are not Logged in !', 'danger')
#         return redirect(url_for('login'))
#     find_id = request.form.get("brand_id")
#    need to put id ="brand_id " in input 
#     print("find_id = ",find_id)
#     updatebrands = Brand.query.filter_by(id = find_id ).first()
#     print("updatebrands = ",updatebrands)
#     if request.method == 'POST' :
#         brand = request.form.get('brand')
#         updatebrands.name = brand
#         db.session.commit()
#         return redirect(url_for('brands'))
    

#     return render_template('products/updatebrand.html' ,  updatebrands = updatebrands)


@app.route("/addbrand", methods =['GET','POST'])
def addbrand() :
    if "email" not in session  :
        flash("you are not loggid in  " , "danger")
        return redirect(url_for("login"))
    if request.method == "POST" :
        brand_name = request.form.get("brand")
        print("brand_name = " ,brand_name)
        brand = Brand( name = brand_name)
        db.session.add(brand)
        flash( f'Brand {brand_name}  added succesfully !','success')
        db.session.commit()
        return redirect('addbrand')


    return render_template("products/addbrand.html",brands ='brands')
    




@app.route("/addcat", methods =['GET','POST'])
def addcat() :
    if "email" not in session  :
        flash("you are not loggid in  " , "danger")
        return redirect(url_for("login"))
    if request.method == "POST" :
        cat_name = request.form.get("category")
        print("cat_name =  " ,cat_name)
        cat = Category( name = cat_name)
        db.session.add(cat)
        flash( f'Category {cat_name}  added succesfully !','success')
        db.session.commit()
        return redirect('addcat')


    return render_template("products/addbrand.html")
    

@app.route('/addproduct',methods = ['GET','POST']) 
def addproduct() :
    if "email" not in session  :
        flash("you are not loggid in  " , "danger")
        return redirect(url_for("login"))
    form = AddproductForm(request.form)
    brands = Brand.query.all()
    categorys = Category.query.all()
    if request.method == 'POST'   :

        #   and form.validate()
        try:
            name = form.name.data
            gender = form.gender.data
            discount = form.discount.data
            description = form.description.data
            stock =form.stock.data
            color = form.color.data
            price = form.price.data
            brand = request.form.get('brand')
            category = request.form.get('category')

               


            image1 = save_image(request.files.get('image1'))
            image2 = save_image(request.files.get('image2'))
            image3 = save_image(request.files.get('image3'))

            addproduct = Addproduct( name=name , gender = gender ,discount=discount, description = description,
                                 stock = stock ,color = color, price = price ,brand_id= brand, 
                                 category_id =category , image1 = image1 , image2 = image2 ,image3 = image3) 


            db.session.add(addproduct)


            flash(f'Product {name} added succesfully !' ,'success' )
            db.session.commit()
            return redirect(url_for('admin'))
        except ValueError as e :
           flash(f"Error: {e}", 'danger')
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'error is : { error_msg}',category='danger')
    

    
        # photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
        # photos.save(request.files.get('image2'), name=secrets.token_hex(10) + ".")
        # photos.save(request.files.get('image3'), name=secrets.token_hex(10) + ".")

    return render_template("products/addproduct.html",form = form,title ='add products' ,brands = brands, categorys = categorys)

