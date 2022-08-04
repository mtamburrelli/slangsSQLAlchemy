import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

#Crear engine

engine = sqlalchemy.create_engine("sqlite:///slangs2.db")

Base = declarative_base()

#Crear diccionario

class Diccionario(Base):
   __tablename__ = "diccionario"
   id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   palabra = sqlalchemy.Column(sqlalchemy.String(length=100))
   significado = sqlalchemy.Column(sqlalchemy.String(length=100))
  

Base.metadata.create_all(engine)

#Crear y empezar la sesión

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

#Funciones

def addSlang(palabra, significado):
    slang = Diccionario(palabra=palabra, significado=significado)
    session.add(slang)
    session.commit()


def editSlang(palabra, nuevo_significado):
    session.query(Diccionario).filter(
        Diccionario.palabra==palabra
    ).update({
        Diccionario.palabra: palabra,
        Diccionario.significado: nuevo_significado
    })   
    session.commit()


def delSlang(palabra):
    session.query(Diccionario).filter(Diccionario.palabra == palabra).delete()
    session.commit()


def get_slangs(): 
    return session.query(Diccionario).all() 


def buscar_def(palabra):    
    return session.query(Diccionario).filter_by(palabra=palabra)

#Función principal de menú

def menu():   
    menu = """
1) Agregar nuevo slang
2) Editar slang
3) Eliminar palabra existente
4) Ver diccionario
5) Buscar definición
6) Salir
Selecciona una opción: """

    opt = ""
    while opt != "6":   #Mientras el usuario no escoja 6 para salir, se mostrará el menú
        opt = input(menu)
        if opt == "1":  #Buscar si existe el slang ingresado y agregarlo si no
            palabra = input("\nIngrese un slang: ")
            posible_significado = buscar_def(palabra).count()
            if posible_significado > 0:       
                print(f"El slang '{palabra}' ya existe")
            else:
                significado = input("Ingrese el significado: ")
                addSlang(palabra, significado)
                print("¡Slang agregado con éxito!")
        if opt == "2":  #Buscar el slang que se quiere editar y cambiar su significado, si no existe, te da la opción de agregarlo
            palabra = input("\n¿Qué slang desea editar?: ")
            posible_significado = buscar_def(palabra).count()
            if posible_significado > 0:       
                nuevo_significado = input("Ingrese el nuevo significado: ")
                editSlang(palabra, nuevo_significado)
                print("¡Slang actualizado exitosamente!")              
            else:
                yn=input(f"El slang '{palabra}' no existe. ¿Deseas agregarlo? Y/N: ")
                if yn == 'Y' or yn == 'y':
                    significado = input("Ingrese el significado: ")
                    addSlang(palabra, significado)
                    print("¡Slang agregado con éxito!")
                else:
                    continue              
        if opt == "3":  #Eliminar un slang
            palabra = input("\n¿Qué slang desea eliminar?: ")
            delSlang(palabra)
        if opt == "4":  #Mostrar todos los slangs y sus definiciones usando un ciclo for
            palabras = get_slangs()           
            print("\n--------Diccionario de Slangs--------\n")
            for palabra in palabras:
                print(palabra.palabra + ": " + palabra.significado)
        if opt == "5":  #Mostrar el significado del slang escogido, si no existe, te da la opción de agregarlo
            palabra = input(
                "\n¿Qué significado deseas saber?: ")
            significado = buscar_def(palabra)
            if significado.count() > 0:
                print(f"El significado de '{palabra}' es:\n{significado[0].significado}")
            else:
                yn=input(f"El slang '{palabra}' no existe. ¿Deseas agregarlo? Y/N: ")
                if yn == 'Y' or yn == 'y':
                    significado = input("Ingrese el significado: ")
                    addSlang(palabra, significado)
                    print("¡Slang agregado con éxito!")
                else:
                    continue
                
#Inicialización del programa

if __name__ == '__main__':
    menu()