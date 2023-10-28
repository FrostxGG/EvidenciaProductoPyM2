
import pymysql
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear') 

class DataBase:
    def _init_(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1725',
            db='hoc'
        )
        self.cursor = self.connection.cursor()
        print("Conexión a la base de datos exitosa")

    def close(self):
        if self.connection:
            self.connection.close()

    def insert_user(self, idCliente, Nombres, Apellidos, Direccion):
        try:
            self.cursor.execute("SELECT idCliente FROM clientes WHERE idCliente = %s", (idCliente,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                print(f"El usuario con (idCliente > {idCliente} < ) ya existe. Por favor, cree otro ID.")
            else:
                self.cursor.execute(
                    "INSERT INTO clientes (idCliente, Nombres, Apellidos, Direccion) VALUES (%s, %s, %s, %s)",
                    (idCliente, Nombres, Apellidos, Direccion)
                )
                self.connection.commit()
                print(f"Usuario {Nombres} insertado en la base de datos.")
        except pymysql.Error as e:
            print(f"Error al insertar usuario: {e}")

    def insert_tortas(self, nombreCliente, Sabor, Porciones):
        try:
            self.cursor.execute(
                "INSERT INTO tortas (nombreCliente, Sabor, Porciones) VALUES (%s, %s, %s)",
                (nombreCliente, Sabor, Porciones)
            )
            self.connection.commit()
            print(f"Torta para {nombreCliente} insertada en la base de datos.")
        except pymysql.Error as e:
            print(f"Error al insertar torta: {e}")

dataBase = DataBase()

class Usuario:
    def _init_(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def set_password(self, password):
        self.__password = password

    def login(self, entered_password):
        return self.__password == entered_password

    def _str_(self):
        return f'Usuario: {self.__username}'

class Administrador(Usuario):
    def _init_(self, username, password):
        super()._init_(username, password)

    def _str_(self):
        return f'Usuario Admin: {self.get_username()}'

class Cliente(Usuario):
    def _init_(self, username, password):
        super()._init_(username, password)

    def _str_(self):
        return f'Usuario Regular: {self.get_username()}'

def imprimir_info_usuario(usuario):
    print(usuario)

es_admin = lambda usuario: isinstance(usuario, Administrador)

admin = Administrador("admin", "admin123")
regular_user = Cliente("user", "user123")

# Menú de inicio de sesión
def menu_inicio_sesion():
    while True:
        print("-----------------------------------")
        print("🧁Bienvenidos a tienda de pasteles")
        print(" 1. Iniciar sesión                 ")
        print(" 2. Salir                          ")
        print("_____________")
        
        opcion = input("Elija una opción: ")

        if opcion == "1":
            limpiar_consola()
            
            username = input("Usuario: ")
            password = input("Contraseña: ")
            
            limpiar_consola()
            
            

            if admin.get_username() == username and admin.login(password):
                dataBase.connect()
                print("¡Inicio de sesión exitoso!")
                imprimir_info_usuario(admin)
                while True:
                    opcion_admin = input("¿Desea agregar un usuario? (s/n): ").lower()
                    if opcion_admin == "s":
                        limpiar_consola()
                        
                        idCliente = input("Id cliente: ")
                        Nombres = input("Nombres:  ")
                        Apellidos = input("Apellidos: ")
                        Direccion = input("Direccion: ")
                         
                        dataBase.insert_user(idCliente, Nombres, Apellidos, Direccion)
                        print(f"Usuario {Nombres} agregado a nuestros clientes.")
                        
                        
                    elif opcion_admin == "n":
                        break
                    else:
                        print("Opción no válida. Intente de nuevo.")
            elif regular_user.get_username() == username and regular_user.login(password):
                dataBase.connect() 
                print("¡Inicio de sesión exitoso!")
                imprimir_info_usuario(regular_user)
                while True:
                    opcion_user = input("¿Desea agregar una torta? (s/n): ").lower()
                    if opcion_user == "s":
                        limpiar_consola()   
                        
                        nombreCliente = input("Nombre cliente: ")
                        Sabor = input("Sabor:  ")
                        Porciones = input("Porciones: ")

                        dataBase.insert_tortas(nombreCliente, Sabor, Porciones)
                        print(f"Torta para {nombreCliente} agregada.")
                      
                        
                    elif opcion_user == "n":
                        break
                dataBase.close()
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        elif opcion == "2":
            print("hasta luego")
            dataBase.close()  
            break
        else:
            print("Opción no válida. Intente de nuevo.")

menu_inicio_sesion()