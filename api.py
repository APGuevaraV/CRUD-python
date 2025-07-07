from fastapi import FastAPI,Response,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
import database as db

class ModeloCliente(BaseModel):
    dni:str= Field(min_length=3, max_length=3)
    nombre:str = Field(min_length=2, max_length=30)
    apellido:str = Field(min_length=2, max_length=30)
    

headers = {"content-type":"application/json;charset=utf-8"}
app = FastAPI()

##decorador para operacion get
@app.get("/")
async def index():
    
    content = {"mensaje":"¡Hola Mundo"}
    return JSONResponse(content=content,headers=headers,media_type="application/json")

@app.get("/html/")
async def html():
    
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>¡Hola mundo!</title>
    </head>
    <body>
        <h1>¡Hola mundo!</h1>
    </body>
    </html>
    """
    return Response(content=content,headers=headers,media_type="text/html")

@app.get("/clientes/")
async def clientes():
    content = [ cliente.to_dict() for cliente in  db.Clientes.lista ] 
    return JSONResponse(content=content,headers=headers,media_type="application/json")

@app.get("/clientes/buscar/{dni}")
async def clientes_buscar(dni:str):
    cliente = db.Clientes.buscar(dni=dni)
    if not cliente:
        raise HTTPException(status_code=404,detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(),headers=headers,media_type="application/json")

@app.post("/clientes/crear")
async def clientes_crear(datos:ModeloCliente):
    cliente = db.Clientes.crear(datos.dni,datos.nombre,datos.apellido)
    if cliente:
       return JSONResponse(content=cliente.to_dict(),headers=headers)
    raise HTTPException(status_code=404,detail="Cliente no creado")