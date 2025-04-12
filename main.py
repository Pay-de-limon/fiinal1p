from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ModelLibro(BaseModel):
    id: int
    Titulo: str
    Año: str
    Autor: str


libros = [
    {"id": 1, "Titulo": "Cien años de soledad", "Año": "1967", "Autor": "Gabriel García Márquez"},
    {"id": 2, "Titulo": "1984", "Año": "1949", "Autor": "George Orwell"},
    {"id": 3, "Titulo": "Don Quijote de la Mancha", "Año": "1605", "Autor": "Miguel de Cervantes"}
]

# Endpoint para consultar todos los libros
@app.get("/todosLibros", tags=["Operaciones CRUD"])
def leer_libros():
    return {"Libros Registrados": libros}

# Endpoint para guardar un libro
@app.post("/libros/", response_model=ModelLibro, tags=["Operaciones CRUD"])
def guardar_libro(libro: ModelLibro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El libro ya existe")
    libros.append(libro.dict())
    return libro

# Endpoint para actualizar un libro
@app.put("/libros/{id}", response_model=ModelLibro, tags=["Operaciones CRUD"])
def actualizar_libro(id: int, libro_actualizado: ModelLibro):
    for index, l in enumerate(libros):
        if l["id"] == id:
            libros[index] = libro_actualizado.dict()
            return libros[index]
    raise HTTPException(status_code=404, detail="El libro no existe")

# Endpoint para eliminar un libro
@app.delete("/libros/{id}", tags=["Operaciones CRUD"])
def eliminar_libro(id: int):
    for index, l in enumerate(libros):
        if l["id"] == id:
            libros.pop(index)
            return {"mensaje": "Libro eliminado correctamente"}
    raise HTTPException(status_code=404, detail="El libro no existe")

# Endpoint para consultar un libro por ID
@app.get("/libros/{id}", response_model=ModelLibro, tags=["Operaciones CRUD"])
def obtener_libro(id: int):
    for l in libros:
        if l["id"] == id:
            return l
    raise HTTPException(status_code=404, detail="Libro no encontrado")
