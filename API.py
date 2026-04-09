from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import pyodbc

# Connect to SQL Server using Windows Authentication (SSMS)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\localhost;'       # ex: localhost\SQLEXPRESS
    'DATABASE=Schita;'                
    'Trusted_Connection=yes;'        # Windows Authentication
)

cursor = conn.cursor()

# Drop any FK constraints referencing courses, then drop tables in dependency order
cursor.execute("""
    DECLARE @sql NVARCHAR(MAX) = ''
    SELECT @sql = @sql + 'ALTER TABLE [' + OBJECT_NAME(parent_object_id) + '] DROP CONSTRAINT [' + name + ']; '
    FROM sys.foreign_keys
    WHERE referenced_object_id = OBJECT_ID('courses')
    IF LEN(@sql) > 0 EXEC(@sql)
""")
cursor.execute("IF OBJECT_ID('courses', 'U') IS NOT NULL DROP TABLE courses")
cursor.execute("IF OBJECT_ID('students', 'U') IS NOT NULL DROP TABLE students")
cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY IDENTITY(1,1), name VARCHAR(255), dept VARCHAR(255), age INT)")
cursor.execute("CREATE TABLE courses (courseid INTEGER PRIMARY KEY IDENTITY(1,1), name VARCHAR(255), professor_name VARCHAR(255), studentid INT, FOREIGN KEY (studentid) REFERENCES students(id))")


app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Products'}

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=list[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()  
    return products  

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only the fields that were provided in the request
    if product_update.name is not None:
        db_product.name = product_update.name
    if product_update.description is not None:
        db_product.description = product_update.description
    if product_update.price is not None:
        db_product.price = product_update.price

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
