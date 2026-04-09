from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import Identifier, get_db 
from authdb import IdentifierCreate, IdentifierUpdate, IdentifierResponse

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/app", include_in_schema=False)
async def serve_frontend():
    return FileResponse("frontend/index.html")


@app.get('/')
async def root():
    return {'message': 'Manufacturing API System'}

@app.post("/identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
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
import io
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse

# Ruta care genereaza si trimite graficul ca imagine
@app.get("/stats/consumers-chart")
def get_consumers_chart(db: Session = Depends(get_db)):
    # 1. Extragem datele cu Pandas folosind conexiunea existenta a FastAPI
    # (Folosim engine-ul din baza noastra de date curenta)
    from database import engine 
    
    df_consumers = pd.read_sql("""
        SELECT cu.number_of_consumers as total, c.name as country 
        FROM ConsumerUnits cu 
        JOIN Countries c ON cu.country_name = c.name
        ORDER BY total ASC
    """, engine)

    flag_colors = {
        'France': ['#002395', '#FFFFFF', '#ED2939'],    
        'Germany': ['#000000', '#DD0000', '#FFCE00'],     
        'Luxembourg': ['#EA141D', '#FFFFFF', '#00A1DE'],
        'Belgium': ['#000000', '#FAE042', '#ED2939'],    
        'Netherlands': ['#AE1C28', '#FFFFFF', '#21468B'], 
        'Norway': ['#EF2B2D', '#FFFFFF', '#00205B'],      
        'Sweden': ['#006AA7', '#FECC00', '#006AA7']     
    }

    plt.figure(figsize=(10, 6))

    for i, row in df_consumers.iterrows():
        country = row['country']
        total_val = row['total']
        segment = total_val / 3
        
        colors = flag_colors.get(country, ['#808080', '#A0A0A0', '#C0C0C0'])
        
        plt.bar(country, segment, bottom=0, color=colors[0], edgecolor='none')
        plt.bar(country, segment, bottom=segment, color=colors[1], edgecolor='none')
        plt.bar(country, segment, bottom=segment*2, color=colors[2], edgecolor='none')

    plt.title('Numarul de consumatori pe tara', fontsize=15)
    plt.ylabel('Nr. Consumatori')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 2. SALVAREA IN MEMORIE (Inlocuim plt.show())
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close() # Curatam memoria serverului

    # 3. Trimitem poza direct catre browser
    return StreamingResponse(buf, media_type="image/png")

@app.get("/ownership/")
def get_ownership_stats(db: Session = Depends(get_db)):
    # Extragem datele din tabela Ownership folosind modelul tau SQLAlchemy
    rezultate = db.query(Ownership).all()
    
    date_tabel = []
    for rand in rezultate:
        date_tabel.append({
            "identifier_name": rand.identifier_name,
            "originator_first_name": rand.originator_first_name,
            "originator_last_name": rand.originator_last_name,
            "email": rand.email,
            "owner_last_name": rand.owner_last_name
        })
        
    return date_tabel

@app.delete("/identifiers/{identifier_name}")
def delete_full_identifier(identifier_name: str, db: Session = Depends(get_db)):
    db_item = db.query(Identifier).filter(Identifier.identifier_name == identifier_name).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Produsul nu a fost gasit")

    try:
        
        db.query(Ownership).filter(Ownership.identifier_name == identifier_name).delete()
        
        db.query(Relationship).filter(
            (Relationship.from_identifier_name == identifier_name) | 
            (Relationship.to_identifier_name == identifier_name)
        ).delete()
        
        db.query(IdentifierCharacteristic).filter(
            IdentifierCharacteristic.identifier_name == identifier_name
        ).delete()

        db.delete(db_item)
        
        db.commit()
        
        return {"message": f"Succes! Produsul {identifier_name} si toate legaturile sale au fost sterse."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Eroare la stergere: {str(e)}")