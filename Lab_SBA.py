"""
Archivo: Lab_SBA.py
Autores: Bastían Díaz - Esteban Cruces - Matias Osse s- Francisco Riquelme
"""

import random
from datetime import datetime, timedelta
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivationByType
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import math
from bisect import insort_left

from variables_generales import *
#variable de inicio de simulación

def random_within_bounds(lower, upper):
    """
    Genera un número aleatorio dentro de un rango [lower, upper),
    excluyendo el valor especificado en exclude.
    """
    if lower >= upper:
        aux = lower
        lower = upper
        upper = aux
    if lower +1 == upper -1:
        return lower +1
    random_number = random.randint(lower+1, upper - 1)
    return random_number

def generar_id():
    # Definir una variable local para almacenar el valor del ID
    if not hasattr(generar_id, "id_actual"):
        generar_id.id_actual = 0

    # Incrementar el valor del ID y devolverlo
    generar_id.id_actual += 1
    return generar_id.id_actual

def getHorarioSegunHora(hora):
    #Tarifa baja: De 06:00 a 06:59 horas; y de 20:45 a 23:00 horas.  6*3600 y 6*3600+59*60 - 20*3600+45*60 y 23*3600
    #Tarifa valle: De  09:00 a 17:50 horas; y de 20:00 a 20:44 horas. 9*3600 y 17*3600+50*60 - 20*3600 y 20*3600+44*60
    #Tarifa punta: De 07:00 a 08:59 horas; y de 18:00 a 19:59 horas. 7*3600 y 8*3600+59*60 - 18*3600 y 19*3600+59*60
    if( (hora > 6*3600 and hora < 6*3600+59*60) or (hora > 6*3600+59*60 and hora < 20*3600+45*60)): #Tarifa baja
        return 'hora_baja'
    elif( (hora > 9*3600 and hora < 17*3600+50*60) or (hora > 20*3600 and hora < 20*3600+44*60)): #Tarifa valle
        return 'hora_valle'
    elif( (hora > 7*3600 and hora < 8*3600+59*60) or (hora > 18*3600 and hora < 19*3600+59*60)): #Tarifa punta
        return 'hora_punta'
    return 'no_hora'
    
    
class PosicionRecorrido(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero

    def step(self):
        #print("soy un paradero: " + str(self.unique_id) + " y tengo " + str(len(self.personas)) + " personas")
        pass

class TrafficLight(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero
        self.color = random.choice(["green", "red"])

    def step(self):
        if self.model.schedule.steps % FRECUENCIA_SEMAFORO == 0:
            if self.color == "green":
                self.color = "red"
            else:
                self.color = "green"

class Bus(Agent):
    def __init__(self, unique_id, model, velocidad_maxima, aceleracion, recorrido,posicion_actual,primeraGeneracion):
        super().__init__(unique_id, model)
        self.pasajeros = [] #lista de personas en el bus
        self.velocidad_maxima = velocidad_maxima
        self.aceleracion = aceleracion
        self.recorrido = recorrido
        self.velocidad = 0
        self.distancia_recorrida = posicion_actual*ESCALA #distancia recorrida en metros
        self.posicion_actual = posicion_actual  # Índice actual en el recorrido (representa tambien el bloque actual)
        self.limite_pasajeros = LIMITE_PASAJEROS_BUS #capacidad maxima de pasajeros
        self.ultimo_semaforo=-1 #indice del ultimo semaforo en el que se detuvo
        self.ultimo_paradero=-1 #indice del ultimo paradero en el que se detuvo
        self.steps_en_standBy = 0 #indica si el bus esta en un paradero
        self.puede_moverse = True #indica si el bus puede moverse o no
        self.step_creacion = self.model.schedule.steps #step en el que se creo el bus
        self.primeraGeneracion = primeraGeneracion #indica si es se genero en el init de city

    def moverse(self):
        #print("Bus " + str(self.unique_id) + "en standby: " + str(self.steps_en_standBy))
        if self.puede_moverse:
            if self.steps_en_standBy == 0:  #solo puede moverse si no tiene steps en standby
                # Ajustar velocidad y posición según el recorrido
                if self.posicion_actual < len(self.recorrido) - 1:
                    distancia_por_recorrer = self.calcularDistancia()
                    if self.velocidad >= self.velocidad_maxima:
                        self.velocidad = self.velocidad_maxima
                    elif self.velocidad < self.velocidad_maxima:
                        self.velocidad += self.aceleracion
                    self.distancia_recorrida += distancia_por_recorrer #se suma la distancia recorrida
                    #print("bloque actual: " + str(self.distancia_recorrida // ESCALA)+ ", bloque anterior: "+ str(self.posicion_actual) + ",salto de bloques: " + str(int(distancia_por_recorrer // ESCALA)))                                                                                                                                                                                                                                                                                                                                                                                                    
                    self.posicion_actual = int(self.distancia_recorrida // ESCALA) # se pasa a escala de simulacion
                    self.posicion_actual = self.posicion_actual% (len(self.recorrido)-1)
                    self.model.grid.move_agent(self, self.recorrido[self.posicion_actual])

                else:
                    # Si ya llegó al final del recorrido, reiniciar
                    self.velocidad = 0
                    self.posicion_actual = 0
            else:
                self.steps_en_standBy-=1

    def recogerPasajeros(self, paradero):
            #print("Bus " + str(self.unique_id) + " recogiendo personas en paradero " + str(agent.unique_id))
            for persona in paradero.personas[:]:
                if len(self.pasajeros) < self.limite_pasajeros: #si el bus no esta lleno
                    self.velocidad = 0  #el bus se detiene
                    self.steps_en_standBy+= 1   #agrego un standby por cada persona que se sube
                    #print(tiempos_de_espera)
                    tiempos_de_espera.append(self.model.schedule.steps - persona.step_creacion) #se agrega el tiempo de espera de la persona
                    self.pasajeros.append(persona) #se agregan las personas al bus
                    paradero.personas.remove(persona) #se saca la persona del paradero
                    
            #print(f"Agente {agent.unique_id} en la celda  {self.recorrido[self.posicion_actual]}")

    def abandonarPasajeros(self,agent,indice_paradero):

        for persona in self.pasajeros[:]:
            #print(f"{persona.destino}, {indice_paradero}")
            if persona.destino == indice_paradero: #si el destino de la persona es el paradero actual
                self.velocidad = 0 #el bus se detiene
                self.steps_en_standBy+= 1   #agrego un standby por cada persona que se baja
                self.pasajeros.remove(persona)
                #print("Bus " + str(self.unique_id) + " dejando persona " + str(persona.unique_id) + " en paradero " + str(self.posicion_actual))
                agent.personas.append(persona)

    def calcularDistancia(self):           
        return self.velocidad+0.5*self.aceleracion
    
    def calcularDistanciaAlgoritmoInteligente(self):
        encontrado_bus = False
        distanciaAdelante = 0
        for i in range(self.posicion_actual+1,len(self.recorrido)-1): #recorro el recorrido desde la posicion actual+1 hasta el final
            cell_contents = self.model.grid.get_cell_list_contents(self.recorrido[i]) #obtengo los agentes en la celda actual
            distanciaAdelante += 1
            for agent in cell_contents: #recorro los agentes en la celda actual
                if isinstance(agent, Bus):
                    encontrado_bus = True
                    break
            if encontrado_bus:
                break
        encontrado_bus = False
        distanciaAtras = 0
        for i in range(self.posicion_actual-1,0,-1): #for recorro el recorrido desde la posicion actual+1 hasta el inicio
            cell_contents = self.model.grid.get_cell_list_contents(self.recorrido[i]) #obtengo los agentes en la celda actual
            distanciaAtras += 1
            for agent in cell_contents:
                if isinstance(agent, Bus):
                    encontrado_bus = True
                    break
            if encontrado_bus:
                break
        if distanciaAdelante > distanciaAtras:
            #print("acelero, con distancia adelante: " + str(distanciaAdelante) + " y distancia atras: " + str(distanciaAtras) )
            return self.velocidad+0.5*self.aceleracion*1.5
        if distanciaAdelante == distanciaAtras:
            #print("mantengo, con distancia adelante: " + str(distanciaAdelante) + " y distancia atras: " + str(distanciaAtras) )
            return self.velocidad+0.5*self.aceleracion*1
        if distanciaAdelante < distanciaAtras:
            #print("freno, con distancia adelante: " + str(distanciaAdelante) + " y distancia atras: " + str(distanciaAtras) )
            return self.velocidad+0.5*self.aceleracion*0.5

    def step(self):
        #print("soy un bus: " + str(self.unique_id) + " y estoy en la posicion " + str(self.posicion_actual))
        cell_contents = self.model.grid.get_cell_list_contents(self.recorrido[self.posicion_actual]) #obtengo los agentes en la celda actual
        for agent in cell_contents: #recorro los agentes en la celda actual
            if isinstance(agent, Paradero): #si es un paradero
                indice_paradero = PARADEROS.index(agent.posicion) #obtengo el indice del paradero
                if indice_paradero != self.ultimo_paradero: #si todavia no paso por esta paradero
                    #print("Bus " + str(self.unique_id) + " en paradero " + str(indice_paradero) + "con ultimo paradero " + str(self.ultimo_paradero) + " y ultimo semaforo " + str(self.ultimo_semaforo) + " y largo recorrido " + str(len(self.recorrido)))
                    self.abandonarPasajeros(agent,indice_paradero)
                    self.recogerPasajeros(agent)
                    self.ultimo_paradero = indice_paradero
                    
            elif isinstance(agent, TrafficLight):
                indice_semaforo = SEMAFOROS.index(agent.posicion)
                if agent.color == "red":
                    if indice_semaforo != self.ultimo_paradero:
                        self.velocidad = 0
                        self.ultimo_semaforo = indice_semaforo
                        self.puede_moverse = False
                else:
                    self.puede_moverse = True   
        self.moverse()

class Person(Agent):
    def __init__(self, unique_id, model, destino):
        super().__init__(unique_id, model)
        self.destino = destino #numero entre 0 y 67, corresponde al index de paradero de destino
        self.step_creacion = self.model.schedule.steps #step en el que se creo la persona
    def step(self):
        pass

class Paradero(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero
        self.personas = [] #lista de personas esperando (lista de Clase de Peatón)
        self.cantidad_personas = 0 #cantidad de personas en el paradero
    def step(self):
        #self.model.horaActual
        if PARADEROS.index(self.posicion) == len(PARADEROS) - 1:
            cell_contents = self.model.grid.get_cell_list_contents(self.posicion) #obtengo los agentes en la celda actual
            for agent in cell_contents: #recorro los agentes en la celda actual
                if isinstance(agent, Bus): #si es un bus
                    self.model.buses.remove(agent)
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                    self.model.num_buses_circulando -= 1
        horario = getHorarioSegunHora(self.model.horaActual) #obtengo el horario actual
        if HORARIOS[horario] !=-1 and self.model.schedule.steps % HORARIOS[horario] == 0: #si es hora valle, punta o baja 
            if PARADEROS.index(self.posicion) < len(PARADEROS) - 1: #si no es el ultimo paradero
                agregar = random.randint(0, 2) #agrego 0 o 2 personas al paradero
                cota_inferior_destino = PARADEROS.index(self.posicion) #obtengo el indice del paradero actual
                cota_superior_destino = len(PARADEROS) #obtengo el indice del ultimo paradero
                for _ in range(agregar):
                    persona = Person(generar_id(), self.model, random_within_bounds(cota_inferior_destino, cota_superior_destino))
                    self.model.schedule.add(persona)
                    self.personas.append(persona)
            #print("soy un paradero: " + str(self.unique_id) + " y tengo " + str(len(self.personas)) + " personas")
    
class City(Model):
    def __init__(self, N):
        
        self.num_paraderos = N
        self.paraderos = []
        self.recorrido = []
        self.semaforos = []
        self.buses = []
        self.num_buses_circulando = 0
        self.grid = MultiGrid(200, 440, torus=True)
        #se crea un programador de agentes
        self.schedule = RandomActivationByType(self) # (CREO) se crea para posteriormente guardar los agentes e la simulación
        self.horaActual = HoraInicialEnSegundos #hora actual en segundos
        self.promedioTiemposEspera = 0
        self.promedioTiempoLlegadaBusFinRecorrido = 0
        self.promedioPasajerosPorBus = 0
        self.desviacionEstandarPasajerosPorBus = 0
        self.promedioDistanciaEntreBuses = 0
        self.desviacion_estandar_distancias_entre_buses = 0

        self.paraderos = []
         # Crear paraderos con posiciones estáticas
        #print("Creando semaforos..."+ str(len(SEMAFOROS)))
        for i,pos in enumerate(PARADEROS):
            paradero = Paradero(generar_id(), self, pos[0], pos[1]) #se crea un paradero
            self.schedule.add(paradero) #Se agrega el agente al programador de agentes
            #for _ in range(PERSONAS_ESPERANDO_PARADERO_INICIAL[i]):
            if i < len(PARADEROS) - 1: #para generar peatones en cada paradero menos en el último
                for _ in range(3):
                    #print("i: " + str(i) + " num_paraderos: " + str(self.num_paraderos))
                    persona = Person(generar_id(), self, random_within_bounds(i, self.num_paraderos))
                    self.schedule.add(persona)
                    paradero.personas.append(persona)
            self.paraderos.append(paradero)
            self.grid.place_agent(paradero, pos)

        for pos in RECORRIDO:
            posicion = PosicionRecorrido(generar_id(), self, pos[0], pos[1]) #se crea un paradero
            self.recorrido.append(posicion)
            self.grid.place_agent(posicion, pos)
            self.schedule.add(posicion) #Se agrega el agente al programador de agentes

        for pos in SEMAFOROS:
            trafficLight = TrafficLight(generar_id(), self, pos[0], pos[1]) #se crea un paradero
            self.semaforos.append(trafficLight)
            self.grid.place_agent(trafficLight, pos)
            self.schedule.add(trafficLight) #Se agrega el agente al programador de agentes
        
        for i,pos in enumerate(PARADEROS):
            if i% 4 == 0 and i!=0:
                bus = Bus(generar_id(), self, VEL_MAX, ACELERACION, RECORRIDO, RECORRIDO.index(pos),True)
                self.buses.append(bus)
                self.grid.place_agent(bus, pos)
                self.schedule.add(bus)
                self.num_buses_circulando += 1

        model_reporters = {}
        model_reporters["Promedio Tiempo de Espera"] = lambda model: model.promedioTiemposEspera
        chart_description = [{"Label": "Promedio Tiempo de Espera", "Color": "blue"}]
        self.chart1 = ChartModule(chart_description)

        model_reporters["Promedio Pasajeros por Bus"] = lambda model: model.promedioPasajerosPorBus
        chart_description = [{"Label": "Promedio Pasajeros por Bus", "Color": "green"}]
        self.chart2 = ChartModule(chart_description)
        self.datacollector = DataCollector(model_reporters=model_reporters)

        model_reporters["Desviacion Estandar Pasajeros en Buses"] = lambda model: model.desviacionEstandarPasajerosPorBus
        chart_description = [{"Label": "Desviacion Estandar Pasajeros en Buses", "Color": "yellow"}]
        self.chart3 = ChartModule(chart_description)
        self.datacollector = DataCollector(model_reporters=model_reporters)

        model_reporters["Promedio distancia entre en Buses"] = lambda model: model.promedioDistanciaEntreBuses
        chart_description = [{"Label": "Promedio distancia entre en Buses", "Color": "orange"}]
        self.chart4 = ChartModule(chart_description)
        self.datacollector = DataCollector(model_reporters=model_reporters)

        model_reporters["Desviacion Estandar distancia entre en Buses"] = lambda model: model.desviacion_estandar_distancias_entre_buses
        chart_description = [{"Label": "Desviacion Estandar distancia entre en Buses", "Color": "purple"}]
        self.chart5 = ChartModule(chart_description)
        self.datacollector = DataCollector(model_reporters=model_reporters)


        self.running = True


        #self.running = True
    def step(self):
        """Advance the model by one step."""
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
       
        self.schedule.step()
        if self.schedule.steps % 50 == 0:
            #print([bus.distancia_recorrida for bus in self.buses])
            self.datacollector.collect(self)
            self.promedioTiemposEspera = sum(tiempos_de_espera) / len(tiempos_de_espera)    #se calcula el promedio de tiempos de espera
            cantidad_pasajeros_por_bus = [len(bus.pasajeros) for bus in self.buses]    #se obtienen la cantidad de pasajeros por bus
            self.promedioPasajerosPorBus = sum(cantidad_pasajeros_por_bus) / len(self.buses) #se calcula el promedio de pasajeros por bus
            varianza_pasajeros_por_bus = sum([(x - self.promedioPasajerosPorBus) ** 2 for x in cantidad_pasajeros_por_bus]) / len(self.buses)
            self.desviacionEstandarPasajerosPorBus = math.sqrt(varianza_pasajeros_por_bus)
            distancias_buses = [bus.distancia_recorrida for bus in self.buses]
            distancias_entre_buses = [distancias_buses[i + 1] - distancias_buses[i] for i in range(len(distancias_buses) - 1)]
            self.promedioDistanciaEntreBuses = sum(distancias_entre_buses) / len(distancias_entre_buses)
            varianza_distancias_entre_buses = sum([(x - self.promedioDistanciaEntreBuses) ** 2 for x in distancias_entre_buses]) / len(distancias_entre_buses)
            self.desviacion_estandar_distancias_entre_buses = math.sqrt(varianza_distancias_entre_buses)
        self.horaActual = HoraInicialEnSegundos + self.schedule.steps #hora actual en segundos
        #print("buses circulando: " + str(self.num_buses_circulando))
        if self.schedule.steps % FRECUENCIA_LANZAR_BUS == 0:
            bus = Bus(generar_id(), self, VEL_MAX, ACELERACION, RECORRIDO,0, False)
            insort_left(self.buses, bus, key=lambda x: x.distancia_recorrida)
            self.grid.place_agent(bus, RECORRIDO[0])
            self.schedule.add(bus)
            self.num_buses_circulando += 1
            #print("step: " + str(self.schedule.steps) + "agrgegue un bus")
        


def agent_portrayal(agent):
    if agent is None:
        return
    if isinstance(agent, Paradero):
        return {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": "blue",
                "w": 0.9,
                "h": 0.9}

    if isinstance(agent, TrafficLight):
        if agent.color == "red":
            Color = "red"
        else:
            Color = "green"
        return {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": Color,
                "w": 0.9,
                "h": 0.9}
    if isinstance(agent, Bus):
        return {"Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": "yellow",
            "r": 0.6,
            "stroke_color": "black"}

        
# Definir visualización
grid = CanvasGrid(agent_portrayal, 200, 440, 2500, 5500)

city = City(num_paraderos)
# Definir servidor de visualización
server = ModularServer(City, [grid, city.chart1, city.chart2,city.chart3, city.chart4, city.chart5], "Simulación de Transporte Urbano 210", {"N": num_paraderos})

# Iniciar servidor de visualización
server.port = 8529
server.launch()


