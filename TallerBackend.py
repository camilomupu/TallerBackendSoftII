import random
import time
from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, velocidad_maxima, capacidad_gasolina):
        self.velocidad_maxima = velocidad_maxima
        self.capacidad_gasolina = capacidad_gasolina
        self.velocidad_actual = 0
        self.gasolina_actual = capacidad_gasolina
        self.nombre_coche = ""
    @abstractmethod
    def acelerar(self):
        pass

    def obtener_informacion(self):
        return f"\n{self.nombre_coche}, Velocidad actual: {self.velocidad_actual} km/h, Gasolina: {self.gasolina_actual} L"

class Coche(Vehiculo):
    def __init__(self, nombre):
        super().__init__(velocidad_maxima=180, capacidad_gasolina=50)
        self.nombre_coche = nombre
        self.turbo_activado = False

    def acelerar(self):
        if self.velocidad_actual < self.velocidad_maxima:
            if self.turbo_activado:
                self.velocidad_actual += 20
            else:
                self.velocidad_actual += 10

    def activar_turbo(self):
        self.turbo_activado = True

    def desactivar_turbo(self):
        self.turbo_activado = False

class Moto(Vehiculo):
    def __init__(self, nombre):
        super().__init__(velocidad_maxima=150, capacidad_gasolina=30)
        self.nombre_coche = nombre

    def acelerar(self):
        self.velocidad_actual += 15

class Camion(Vehiculo):
    def __init__(self, nombre):
        super().__init__(velocidad_maxima=100, capacidad_gasolina=80)
        self.nombre_coche = nombre

    def acelerar(self):
        self.velocidad_actual += 5

#una lista de objetos vehiculo
def iniciar_carrera(vehiculos, estadisticas=None):
    #Condicion de carrera
    if len(vehiculos) <= 1:
        raise ValueError("No hay vehículos suficientes para la carrera.")
    
    distancia_carrera = 10000  # Distancia de la carrera en metros
    tiempo_inicio = time.time()

    distancias_recorridas = [0] * len(vehiculos)

    while True:
        tiempo_transcurrido = time.time() - tiempo_inicio

        # Mostrar información sobre los vehículos en cada iteración
        for i, vehiculo in enumerate(vehiculos):
            vehiculo.acelerar()
            vehiculo.gasolina_actual -= random.uniform(2.5, 5)

            if vehiculo.velocidad_actual >= vehiculo.velocidad_maxima:
                vehiculo.velocidad_actual = vehiculo.velocidad_maxima

            distancias_recorridas[i] += vehiculo.velocidad_actual * tiempo_transcurrido
            
            if vehiculo.gasolina_actual <= 0 and vehiculo in vehiculos:
                print("\n-----------------------------")
                print(f"{type(vehiculo).__name__} se quedó sin gasolina y se retiró de la carrera.")
                print("-----------------------------\n")
                vehiculos.remove(vehiculo)
                distancias_recorridas.pop(i)

            
            # Comprobar si algún vehículo ha llegado a la meta
            if max(distancias_recorridas) >= distancia_carrera or len(vehiculos) == 1:
                ganador = vehiculos[distancias_recorridas.index(max(distancias_recorridas))]
                print(f"\n¡El ganador es {type(ganador).__name__} con una distancia recorrida de {max(distancias_recorridas)} metros!")
                return
            if estadisticas == True:
                print(vehiculo.obtener_informacion())

        time.sleep(1) # Esperar 1 segundo antes de la siguiente iteración
    
    

# ...

if __name__ == "__main__":
    vehiculos = []
    print("Comienza la carrera, para hacerla mas interesante escribe si o no las siguientes preguntas, recuerda que debes tener minimo dos vehiculos para la carrera: ")
    try:
        coche = input("Desea agregar coche?: ").upper()
        if coche == "SI":
            nombre = input("Que nombre quieres para tu coche: ")
            turbo = input("Desea activar turbo en el coche?: ").upper()
            coche = Coche(nombre=nombre)
            if turbo == "SI":
                coche.activar_turbo()
            vehiculos.append(coche)
        moto = input("Desea agregar moto?: ").upper()
        if moto == "SI":
            nombre = input("Que nombre quieres para tu moto: ")
            moto = Moto(nombre=nombre)
            vehiculos.append(moto)
        camion = input("Desea agregar camion?: ").upper()
        if camion == "SI":
            nombre = input("Que nombre quieres para tu camion: ")
            camion = Camion(nombre=nombre)
            vehiculos.append(camion)
        
        estadisticas = input("Desea ver estadisticas de la carrera en todo momento? En caso contrario se mostraran solo las necesarias:").upper()
        print("¡Comienza la carrera!\n")
        if estadisticas == "SI":
            iniciar_carrera(vehiculos, True)
        else:
            iniciar_carrera(vehiculos)
    except Exception as e:
        print("Ingresaste mal los datos, sigue bien las instrucciones")
        raise e
