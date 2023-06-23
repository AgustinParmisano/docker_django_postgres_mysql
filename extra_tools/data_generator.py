import requests
import json

def login(usuario, password):

    url = 'http://localhost:8000/api/token/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': '8IDsChX6sCEvZwOylvHUe91aLBeXWX0a9aiaDEBfaN1cCJqFiKV1qyzinGrZrqG1'
    }
    data = {
        'username': 'admin',
        'password': 'password'
    }

    response = requests.post(url, headers=headers, json=data)

    token = response.json()["access"]

    return token

def crear_alumnos(datos_alumnos, token):
    url = 'http://localhost:8000/api/academico/alumno/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': '8IDsChX6sCEvZwOylvHUe91aLBeXWX0a9aiaDEBfaN1cCJqFiKV1qyzinGrZrqG1',
        'Authorization': 'Bearer ' + token
    }
    
    for alumno in datos_alumnos:
        response = requests.post(url, headers=headers, data=json.dumps(alumno))
        if response.status_code == 201:
            print("Alumno creado exitosamente:", alumno)
        else:
            print("Error al crear el alumno:", response.text)

# Lista de diccionarios con los datos de los alumnos
alumnos = [
    {
        "dni": 123456,
        "nombre": "Maria",
        "apellido": "Perez",
        "telefono": "3421224",
        "email": "user@example.com"
    },
    {
        "dni": 234567,
        "nombre": "Juan",
        "apellido": "Lopez",
        "telefono": "3421225",
        "email": "user2@example.com"
    },
    {
        "dni": 345678,
        "nombre": "Ana",
        "apellido": "González",
        "telefono": "3421226",
        "email": "user3@example.com"
    },
    {
        "dni": 456789,
        "nombre": "Pedro",
        "apellido": "Martínez",
        "telefono": "3421227",
        "email": "user4@example.com"
    },
    {
        "dni": 567890,
        "nombre": "Laura",
        "apellido": "Rodríguez",
        "telefono": "3421228",
        "email": "user5@example.com"
    },
    # Agrega los datos de los otros alumnos aquí
]

# Se autentica
usuario = "admin"
password = "password"
token = login(usuario, password)

# Llamada a la función para crear los alumnos
crear_alumnos(alumnos, token)
