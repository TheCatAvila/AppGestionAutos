from pymongo import MongoClient
from os import system

class Autos():
    
    def __init__(self):
        self.tipoAuto = 0
        cliente = MongoClient('mongodb://localhost:27017')
        db = cliente['vehiculos']
        self.coleccion = db['usados']
        self.coleccion2 = db['nuevos']

    def IngresarAuto(self):
        Nombre      = input("Ingrese el nombre del auto .......: ")
        Anio        = int(input("Ingrese el año del auto ..........: "))
        Pais        = input("Ingrese el país del auto .........: ")
        Kilometraje = int(input("Ingrese el kilometraje del auto ..: "))
        HP          = int(input("Ingrese el HP del motor ..........: "))
        Cilindros   = int(input("Ingrese los cilindros del motor ..: "))
        Cilindrada  = int(input("Ingrese la cilindrada del motor ..: "))
        Peso        = int(input("Ingrese el peso del auto .........: "))
        Aceleracion = int(input("Ingrese la aceleración del auto ..: "))
        
        auto_data = {
            "Nombre": Nombre,
            "Anio": Anio,
            "Pais": Pais,
            "Kilometraje": Kilometraje,
            "Motor": {
                "HP": HP,
                "Cilindros": Cilindros,
                "Cilindrada": Cilindrada
            },
            "Peso": Peso,
            "Aceleracion": Aceleracion
        }

        if self.tipoAuto == 1:
            self.coleccion.insert_one(auto_data)
        elif self.tipoAuto == 2:
            caracteristicas = input("Ingrese las características del auto: ")
            auto_data["caracteristicas"] = caracteristicas
            self.coleccion2.insert_one(auto_data)

    def BuscarAuto(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        if self.tipoAuto == 1:
            print("---- Busqueda de autos usados ---")
        elif self.tipoAuto == 2:
            print("---- Busqueda de autos nuevos ---")
        print("=================================")
        nombreAuto =     input("Ingrese el nombre completo del auto .: ")
        potenciaHP = int(input("Ingrese la potencia del motor (HP) ..: "))
        
        pipeline = [
            {"$match": {"Nombre": nombreAuto, "Motor.HP": potenciaHP}},
            {"$project": {
                "_id": 1,
                "Nombre": 1,
                "Anio": 1,
                "Pais": 1,
                "Kilometraje": 1,
                "Motor.Cilindros": 1,
                "Motor.Cilindrada": 1,
                "Motor.HP": 1,
                "Peso": 1,
                "Aceleracion": 1,
                "caracteristicas": {"$ifNull": ["$caracteristicas", "N/A"]}
            }}
        ]
        
        if self.tipoAuto == 1:
            documentos = self.coleccion.aggregate(pipeline)
        elif self.tipoAuto == 2:
            documentos = self.coleccion2.aggregate(pipeline)

        print("/////////////////////////////////")
        print("--- Resultados de la busqueda ---")
        for auto in documentos:
            print("/////////////////////////////////")
            print("ID del auto ...............: ", auto['_id'])
            print("Nombre del auto ...........: ", auto['Nombre'])
            print("Año del auto ..............: ", auto['Anio'])
            print("País del auto .............: ", auto['Pais'])
            print("Kilometraje del auto ......: ", auto['Kilometraje'])
            print("Peso del auto .............: ", auto['Peso'])
            print("Aceleración del auto ......: ", auto['Aceleracion'])
            print(f"Motor: HP: {auto['Motor']['HP']}, Cilindros: {auto['Motor']['Cilindros']}, Cilindrada: {auto['Motor']['Cilindrada']}")
            if self.tipoAuto == 2:
                print("Características del auto ..: ", auto['caracteristicas'])
            print("/////////////////////////////////")
            self.Seguir()

    def MenuP(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        print("--- Elija una de las opciones ---")
        print("=================================")
        print("1.- Autos usados")
        print("2.- Autos nuevos")
        print("---------------------------------")
        print("3.- Salir ")
        print("=================================")
        resp = int(input("Respuesta: "))
        
        if resp == 1:
            self.tipoAuto = 1
            self.MenuU()
        elif resp == 2:
            self.tipoAuto = 2
            self.MenuN()
        elif resp == 3:
            self.Salir()
        else:
            print("Ingrese un número válido")
            self.MenuP()
    
    def MenuU(self):
        system("cls")
        print("=================================")
        print("- Gestión de BD de autos usados -")
        print("=================================")
        print("------ ¿Que desea hacer? --------")
        print("=================================")
        print("1.- Ingresar auto usado")
        print("2.- Buscar auto usado")
        print("---------------------------------")
        print("3.- Volver ")
        print("=================================")
        resp = int(input("Respuesta: "))
        
        if resp == 1:
            self.IngresarAuto()
        elif resp == 2:
            self.BuscarAuto()
        elif resp == 3:
            self.MenuP()
        else:
            print("Ingrese un número válido")
            self.MenuU()
            
    def MenuN(self):
        system("cls")
        print("=================================")
        print("- Gestión de BD de autos nuevos -")
        print("=================================")
        print("------ ¿Que desea hacer? --------")
        print("=================================")
        print("1.- Ingresar auto nuevo")
        print("2.- Buscar auto nuevo")
        print("---------------------------------")
        print("3.- Volver ")
        print("=================================")
        resp = int(input("Respuesta: "))
        
        if resp == 1:
            self.IngresarAuto()
        elif resp == 2:
            self.BuscarAuto()
        elif resp == 3:
            self.MenuP()
        else:
            print("Ingrese un número válido")
            self.MenuN()

    def Seguir(self):
        print("=================================")
        print("- ¿Desea seguir en el programa? -")
        print("=================================")
        print("1.- Sí, seguir en el programa")
        print("2.- No, salir del programa")
        print("=================================")
        resp = int(input("Respuesta: "))
        if resp == 1:
            self.MenuP()
        elif resp == 2:
            self.Salir()
        else:
            print("Ingrese un número válido")
            self.Seguir()

    def Salir(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        print("-------- ¡Hasta pronto! ---------")
        print("=================================")
        print("---------------------------------")
        print("  Usted ha salido del programa   ")
        print("---------------------------------")
        print("=================================")

objeto1 = Autos()
objeto1.MenuP()