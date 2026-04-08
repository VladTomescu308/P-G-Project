from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# Presupunem că ai modelele SQLAlchemy definite în 'database' sau 'models'
from database import Identifier, get_db 
from authdb import IdentifierCreate, IdentifierUpdate, IdentifierResponse

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Manufacturing API System'}

@app.post("/identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    # Verifică dacă există deja pentru a evita erori de duplicate primary key
    db_identifier = db.query(Identifier).filter(Identifier.identifier_name == identifier.identifier_name).first()
    if db_identifier:
        raise HTTPException(status_code=400, detail="Identifier already exists")
        
    new_identifier = Identifier(**identifier.model_dump())
    db.add(new_identifier)
    db.commit()
    db.refresh(new_identifier)
    return new_identifier

@app.get("/identifiers/", response_model=list[IdentifierResponse])
def read_all_identifiers(db: Session = Depends(get_db)):
    return db.query(Identifier).all()  

@app.get("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def read_identifier(identifier_name: str, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    return db_identifier

@app.put("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def update_identifier(identifier_name: str, identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    
    for key, value in identifier.model_dump().items():
        setattr(db_identifier, key, value)
    
    db.commit()
    db.refresh(db_identifier)
    return db_identifier

@app.patch("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def patch_identifier(identifier_name: str, identifier_update: IdentifierUpdate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    if identifier_update.description is not None:
        db_identifier.description = identifier_update.description
    if identifier_update.identifier_type is not None:
        db_identifier.identifier_type = identifier_update.identifier_type

    db.commit()
    db.refresh(db_identifier)
    return db_identifier

from database import Identifier, Ownership, Relationship, IdentifierCharacteristic

@app.delete("/identifiers/{identifier_name}")
def delete_full_identifier(identifier_name: str, db: Session = Depends(get_db)):
    # 1. Căutăm produsul
    db_item = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Produsul nu a fost găsit")

    try:
        # 2. Ștergem legăturile din tabelele secundare (Ordinea contează!)
        
        # Ștergem din Ownership
        db.query(Ownership).filter(Ownership.identifier_name == identifier_name).delete()
        
        # Ștergem din Relationships (unde produsul e sursă sau destinație)
        db.query(Relationship).filter(
            (Relationship.from_identifier_name == identifier_name) | 
            (Relationship.to_identifier_name == identifier_name)
        ).delete()
        
        # Ștergem din IdentifierCharacteristics (legătura cu senzorii)
        db.query(IdentifierCharacteristic).filter(
            IdentifierCharacteristic.identifier_name == identifier_name
        ).delete()

        # 3. În sfârșit, ștergem produsul principal din Identifiers
        db.delete(db_item)
        
        # 4. Salvăm toate modificările deodată (Atomic Commit)
        db.commit()
        
        return {"message": f"Succes! Produsul {identifier_name} și toate legăturile sale au fost șterse."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Eroare la ștergere: {str(e)}")