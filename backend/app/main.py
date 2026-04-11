from fastapi import FastAPI 
from app.api.routes import router
from app.db.database import get_db_connection

app=FastAPI(title="SurplusShare API")

app.include_router(router, prefix='/api')

@app.get("/")
def read_root():
    return {"message":"Welcome To The SurplusShare App!!!"}

@app.get("/test-db")
def test_database():
    conn=get_db_connection()
    if conn:
        conn.close()
        return {"message": "Succesfully Connected To The Database, Test Success"}
    return {"message": "Failed To Connect To The Database"}
