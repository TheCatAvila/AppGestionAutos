from pymongo import MongoClient
from bson.objectid import ObjectId
from os import system

class Autos():
    
    def __init__(self):
        self.tipoAuto = 0
        cliente = MongoClient('mongodb://localhost:27017')
        db = cliente['vehiculos']
        self.coleccion = db['usados']
        self.coleccion2 = db['nuevos']

    def IngresarAuto(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        print("-------- Ingreso de auto --------")
        print("=================================")
        Nombre      = input("Ingrese el nombre del auto .......: ")
        Anio        = int(input("Ingrese el año del auto ..........: "))
        Pais        = input("Ingrese el país del auto .........: ")
        Kilometraje = int(input("Ingrese el kilometraje del auto ..: "))
        HP          = int(input("Ingrese el HP del motor ..........: "))
        Cilindros   = int(input("Ingrese los cilindros del motor ..: "))
        Cilindrada  = int(input("Ingrese la cilindrada del motor ..: "))
        Peso        = int(input("Ingrese el peso del auto .........: "))
        Aceleracion = float(input("Ingrese la aceleración del auto ..: "))
        
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
        print("=================================")
        print("--- ¡Auto agregado con éxito! ---")
        print("=================================")
        self.Seguir()

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
        print("Ingrese el número de página en donde")
        pagina     = int(input("quiere realizar la búsqueda .........: "))
        paginaOP   = (pagina * 5) -5
        
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
            }},
            {"$sort":{"Nombre": 1}},
            {"$skip": paginaOP},
            {"$limit": 5}
        ]
        
        if self.tipoAuto == 1:
            documentos = self.coleccion.aggregate(pipeline)
        elif self.tipoAuto == 2:
            documentos = self.coleccion2.aggregate(pipeline)

        system("cls")
        print("=================================")
        print(f"| Usted está en la página N° {pagina} | ")
        print("=================================")
        print("/////////////////////////////////")
        print("--- Resultados de la busqueda ---")
        contador = 0
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
            contador +=1
        print("=================================")
        if contador == 1:
            print("-- Se ha encontrado 1 registro --")
        else:
            print(f"- Se han encontrado {contador} registros -")
        print("--------- en esta página --------")
        print("=================================")
        self.Seguir()
    
    def UpdateAuto(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        print("---- Actualizar auto de la BD ---")
        print("=================================")
        id_auto = input("Ingrese el ID del auto a actualizar: ")
        print("/////////////////////////////////")
        
        try:
            object_id = ObjectId(id_auto)
        except Exception as e:
            print("El ID ingresado no es válido.", e)

        print("Ingrese los nuevos valores para el auto")
        nombre      = input("Nombre del auto ..........: ")
        anio        = input("Año del auto .............: ")
        pais        = input("País del auto ............: ")
        kilometraje = input("Kilometraje del auto .....: ")
        cilindros   = input("Cilindros del motor ......: ")
        cilindrada  = input("Cilindrada del motor .....: ")
        hp          = input("HP del motor .............: ")
        peso        = input("Peso del auto ............: ")
        aceleracion = input("Aceleración del auto .....: ")
        if self.tipoAuto == 2:
            caracteristicas = input("Características del auto .: ")

        update_fields = {}
        
        if nombre:
            update_fields["Nombre"] = nombre
        if anio:
            update_fields["Anio"] = int(anio)
        if pais:
            update_fields["Pais"] = pais
        if kilometraje:
            update_fields["Kilometraje"] = int(kilometraje)
        if peso:
            update_fields["Peso"] = int(peso)
        if aceleracion:
            update_fields["Aceleracion"] = float(aceleracion)
        if cilindros or cilindrada or hp:
            update_fields["Motor"] = {}
            if cilindros:
                update_fields["Motor"]["Cilindros"] = int(cilindros)
            if cilindrada:
                update_fields["Motor"]["Cilindrada"] = int(cilindrada)
            if hp:
                update_fields["Motor"]["HP"] = int(hp)
        if self.tipoAuto == 2 and caracteristicas:
            update_fields["caracteristicas"] = caracteristicas

        if self.tipoAuto == 1:
            resultado = self.coleccion.update_one({"_id": object_id}, {"$set": update_fields})
        elif self.tipoAuto == 2:
            resultado = self.coleccion2.update_one({"_id": object_id}, {"$set": update_fields})
        else:
            self.UpdateAuto()

        if resultado.matched_count > 0:
            if resultado.modified_count > 0:
                print("=================================")
                print("-- Auto actualizado con éxito ---")
                print("=================================")
            else:
                print("=================================")
                print("--- No se realizaron cambios ----")
                print("=================================")
        else:
            print("=================================")
            print("---- No se encontró el auto -----")
            print("=================================")
        self.Seguir()

    def DeleteAuto(self):
        system("cls")
        print("=================================")
        print("---- Gestión de BD de autos -----")
        print("=================================")
        print("----- Borrar auto de la BD ------")
        print("=================================")
        id_auto = input("Ingrese el ID del auto a eliminar: ")
        try:
            object_id = ObjectId(id_auto)
        except Exception as e:
            print("El ID ingresado no es válido.", e)

        if self.tipoAuto == 1:
            resultado = self.coleccion.delete_one({"_id": object_id})
        elif self.tipoAuto == 2:
            resultado = self.coleccion2.delete_one({"_id": object_id})
        else:
            self.DeleteAuto()

        if resultado.deleted_count > 0:
            print("=================================")
            print("---- ¡Auto borrado con éxito! ---")
            print("=================================")
        else:
            print("=================================")
            print("---- No se encontró el auto -----")
            print("=================================")
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
        print("3.- Actualizar auto usado")
        print("4.- Borrar auto usado")
        print("---------------------------------")
        print("5.- Volver ")
        print("=================================")
        resp = int(input("Respuesta: "))
        
        if resp == 1:
            self.IngresarAuto()
        elif resp == 2:
            self.BuscarAuto()
        elif resp == 3:
            self.UpdateAuto()
        elif resp == 4:
            self.DeleteAuto()
        elif resp == 5:
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
        print("3.- Actualizar auto nuevo")
        print("4.- Borrar auto nuevo")
        print("---------------------------------")
        print("5.- Volver ")
        print("=================================")
        resp = int(input("Respuesta: "))
        
        if resp == 1:
            self.IngresarAuto()
        elif resp == 2:
            self.BuscarAuto()
        elif resp == 3:
            self.UpdateAuto()
        elif resp == 4:
            self.DeleteAuto()
        elif resp == 5:
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