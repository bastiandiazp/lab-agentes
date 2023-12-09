import random
from datetime import datetime, timedelta
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivationByType
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


SEMAFOROS = [(190, 12), (189, 14), (189, 19), (188, 21), (188, 26), (187, 28), (187, 33), (186, 35), (186, 40), (185, 42), (185, 47),
    (184, 49), (184, 54), (183, 56), (183, 61), (182, 63), (182, 68), (181, 70), (181, 75), (180, 77), (180, 82), (179, 84),
    (179, 89), (178, 91), (178, 96), (177, 98), (177, 103), (176, 105), (176, 110), (175, 112), (175, 117), (174, 119),
    (174, 124), (173, 126), (173, 131), (172, 133), (172, 138), (171, 140), (171, 145), (170, 147), (169, 153), (168, 156),
    (166, 162), (165, 165), (163, 171), (162, 174), (160, 180), (159, 183), (157, 189), (156, 192), (154, 198), (153, 201),
    (151, 207), (150, 210), (148, 214), (145, 216), (142, 219), (140, 221), (137, 224), (135, 226), (132, 229), (130, 231),
    (127, 234), (125, 236), (122, 239), (120, 241), (117, 244), (115, 246), (113, 250), (112, 252), (112, 256), (111, 258),
    (111, 262), (110, 264), (110, 268), (109, 270), (109, 274), (108, 276), (108, 280), (107, 282), (107, 286), (106, 288),
    (106, 292), (105, 294), (105, 298), (104, 300), (104, 304), (103, 306), (103, 310), (102, 312), (102, 316), (101, 318),
    (101, 322), (100, 324), (100, 328), (99, 330), (99, 334), (98, 336), (98, 340), (97, 342), (97, 346), (96, 348), (96, 352),
    (95, 354), (95, 358), (94, 360), (92, 362), (90, 361), (86, 361), (84, 360), (80, 360), (78, 359), (74, 359), (72, 358),
    (68, 358), (66, 357), (62, 357), (60, 356), (56, 356), (54, 355), (50, 355), (48, 354), (44, 354), (42, 353), (38, 353),
    (36, 352), (32, 352), (30, 351), (26, 351), (24, 350), (22, 348), (22, 345), (20, 343)]
#134 semaforos
    
PARADEROS = [(190, 10), (189, 17), (188, 24), (187, 31), (186, 38), (185, 45), (184, 52), (183, 59), (182, 66), (181, 73), 
(180, 80), (179, 87), (178, 94), (177, 101), (176, 108), (175, 115), (174, 122), (173, 129), (172, 136), (171, 143), 
(170, 150), (167, 159), (164, 168), (161, 177), (158, 186), (155, 195), (152, 204), (149, 213), (143, 218), (138, 223), 
(133, 228), (128, 233), (123, 238), (118, 243), (113, 248), (112, 254), (111, 260), (110, 266), (109, 272), (108, 278), 
(107, 284), (106, 290), (105, 296), (104, 302), (103, 308), (102, 314), (101, 320), (100, 326), (99, 332), (98, 338), 
(97, 344), (96, 350), (95, 356), (94, 362), (88, 361), (82, 360), (76, 359), (70, 358), (64, 357), (58, 356), (52, 355), 
(46, 354), (40, 353), (34, 352), (28, 351), (22, 350), (23, 346), (19,342)]
#68 paraderos

PERSONAS_ESPERANDO_PARADERO_INICIAL = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]


RECORRIDO = [(190, 10), (190, 11), (190, 12), (190, 13), (189, 14), (189, 15), (189, 16), (189, 17), (189, 17), (189, 18), 
             (189, 19), (189, 20), (188, 21), (188, 22), (188, 23), (188, 24), (188, 24), (188, 25), (188, 26), (188, 27), 
             (187, 28), (187, 29), (187, 30), (187, 31), (187, 31), (187, 32), (187, 33), (187, 34), (186, 35), (186, 36), 
             (186, 37), (186, 38), (186, 38), (186, 39), (186, 40), (186, 41), (185, 42), (185, 43), (185, 44), (185, 45), 
             (185, 45), (185, 46), (185, 47), (185, 48), (184, 49), (184, 50), (184, 51), (184, 52), (184, 52), (184, 53), 
             (184, 54), (184, 55), (183, 56), (183, 57), (183, 58), (183, 59), (183, 59), (183, 60), (183, 61), (183, 62), 
             (182, 63), (182, 64), (182, 65), (182, 66), (182, 66), (182, 67), (182, 68), (182, 69), (181, 70), (181, 71), 
             (181, 72), (181, 73), (181, 73), (181, 74), (181, 75), (181, 76), (180, 77), (180, 78), (180, 79), (180, 80), 
             (180, 80), (180, 81), (180, 82), (180, 83), (179, 84), (179, 85), (179, 86), (179, 87), (179, 87), (179, 88), 
             (179, 89), (179, 90), (178, 91), (178, 92), (178, 93), (178, 94), (178, 94), (178, 95), (178, 96), (178, 97), 
             (177, 98), (177, 99), (177, 100), (177, 101), (177, 101), (177, 102), (177, 103), (177, 104), (176, 105), (176, 106), 
             (176, 107), (176, 108), (176, 108), (176, 109), (176, 110), (176, 111), (175, 112), (175, 113), (175, 114), (175, 115), 
             (175, 115), (175, 116), (175, 117), (175, 118), (174, 119), (174, 120), (174, 121), (174, 122), (174, 122), (174, 123), 
             (174, 124), (174, 125), (173, 126), (173, 127), (173, 128), (173, 129), (173, 129), (173, 130), (173, 131), (173, 132), 
             (172, 133), (172, 134), (172, 135), (172, 136), (172, 136), (172, 137), (172, 138), (172, 139), (171, 140), (171, 141), 
             (171, 142), (171, 143), (171, 143), (171, 144), (171, 145), (171, 146), (170, 147), (170, 148), (170, 149), (170, 150), 
             (170, 150), (170, 151), (169, 152), (169, 153), (169, 154), (168, 155), (168, 156), (168, 157), (167, 158), (167, 159), 
             (167, 159), (167, 160), (166, 161), (166, 162), (166, 163), (165, 164), (165, 165), (165, 166), (164, 167), (164, 168), 
             (164, 168), (164, 169), (163, 170), (163, 171), (163, 172), (162, 173), (162, 174), (162, 175), (161, 176), (161, 177), 
             (161, 177), (161, 178), (160, 179), (160, 180), (160, 181), (159, 182), (159, 183), (159, 184), (158, 185), (158, 186), 
             (158, 186), (158, 187), (157, 188), (157, 189), (157, 190), (156, 191), (156, 192), (156, 193), (155, 194), (155, 195), 
             (155, 195), (155, 196), (154, 197), (154, 198), (154, 199), (153, 200), (153, 201), (153, 202), (152, 203), (152, 204), 
             (152, 204), (152, 205), (151, 206), (151, 207), (151, 208), (150, 209), (150, 210), (150, 211), (149, 212), (149, 213), 
             (149, 213), (148, 214), (147, 215), (146, 216), (145, 216), (144, 217), (143, 218), (143, 218), (142, 219), (141, 220), 
             (140, 221), (139, 222), (138, 223), (138, 223), (137, 224), (136, 225), (135, 226), (134, 227), (133, 228), (133, 228), 
             (132, 229), (131, 230), (130, 231), (129, 232), (128, 233), (128, 233), (127, 234), (126, 235), (125, 236), (124, 237), 
             (123, 238), (123, 238), (122, 239), (121, 240), (120, 241), (119, 242), (118, 243), (118, 243), (117, 244), (116, 245), 
             (115, 246), (114, 247), (113, 248), (113, 248), (113, 249), (113, 250), (112, 251), (112, 252), (112, 253), (112, 254), 
             (112, 254), (112, 255), (112, 256), (112, 257), (111, 258), (111, 259), (111, 260), (111, 260), (111, 261), (111, 262), 
             (110, 263), (110, 264), (110, 265), (110, 266), (110, 266), (110, 267), (110, 268), (110, 269), (109, 270), (109, 271), 
             (109, 272), (109, 272), (109, 273), (109, 274), (108, 275), (108, 276), (108, 277), (108, 278), (108, 278), (108, 279), 
             (108, 280), (108, 281), (107, 282), (107, 283), (107, 284), (107, 284), (107, 285), (107, 286), (106, 287), (106, 288), 
             (106, 289), (106, 290), (106, 290), (106, 291), (106, 292), (106, 293), (105, 294), (105, 295), (105, 296), (105, 296), 
             (105, 297), (105, 298), (104, 299), (104, 300), (104, 301), (104, 302), (104, 302), (104, 303), (104, 304), (104, 305), 
             (103, 306), (103, 307), (103, 308), (103, 308), (103, 309), (103, 310), (102, 311), (102, 312), (102, 313), (102, 314), 
             (102, 314), (102, 315), (102, 316), (102, 317), (101, 318), (101, 319), (101, 320), (101, 320), (101, 321), (101, 322), 
             (100, 323), (100, 324), (100, 325), (100, 326), (100, 326), (100, 327), (100, 328), (100, 329), (99, 330), (99, 331), 
             (99, 332), (99, 332), (99, 333), (99, 334), (98, 335), (98, 336), (98, 337), (98, 338), (98, 338), (98, 339), (98, 340), 
             (98, 341), (97, 342), (97, 343), (97, 344), (97, 344), (97, 345), (97, 346), (96, 347), (96, 348), (96, 349), (96, 350), 
             (96, 350), (96, 351), (96, 352), (96, 353), (95, 354), (95, 355), (95, 356), (95, 356), (95, 357), (95, 358), (94, 359), 
             (94, 360), (94, 361), (94, 362), (94, 362), (93, 362), (92, 362), (91, 362), (90, 361), (89, 361), (88, 361), (88, 361), 
             (87, 361), (86, 361), (85, 360), (84, 360), (83, 360), (82, 360), (82, 360), (81, 360), (80, 360), (79, 360), (78, 359), 
             (77, 359), (76, 359), (76, 359), (75, 359), (74, 359), (73, 358), (72, 358), (71, 358), (70, 358), (70, 358), (69, 358), 
             (68, 358), (67, 358), (66, 357), (65, 357), (64, 357), (64, 357), (63, 357), (62, 357), (61, 356), (60, 356), (59, 356), 
             (58, 356), (58, 356), (57, 356), (56, 356), (55, 356), (54, 355), (53, 355), (52, 355), (52, 355), (51, 355), (50, 355), 
             (49, 354), (48, 354), (47, 354), (46, 354), (46, 354), (45, 354), (44, 354), (43, 354), (42, 353), (41, 353), (40, 353), 
             (40, 353), (39, 353), (38, 353), (37, 352), (36, 352), (35, 352), (34, 352), (34, 352), (33, 352), (32, 352), (31, 352), 
             (30, 351), (29, 351), (28, 351), (28, 351), (27, 351), (26, 351), (25, 350), (24, 350), (23, 350), (22, 350), (22, 350), 
             (22, 349), (22, 348), (23, 347), (23, 346), (23, 346), (22, 345), (21, 344), (20, 343), (19, 342), (19, 342)]


#VEL_MAX = 11.11 # m/s 40km/h
#VEL_MAX_PUNTA = 5.56  # m/s 20km/h
VEL_MAX = 11.11 # m/s 40km/h
VEL_MAX_PUNTA = 5.56  # m/s 20km/h
ACELERACION = VEL_MAX/30 
ACELERACION_PUNTA = VEL_MAX_PUNTA/20
ESCALA =50 # metros que representa cada bloque
LIMITE_PASAJEROS_BUS = 30
INTERVALO_ADICION_PEATONES_EN_PARADERO = 60 #STEPS
INTERVALO_SEMAFORO = 30 #STEPS
tiempos_de_espera = [timedelta(seconds=300)]


# Configuración de la simulación
num_paraderos = 68
num_semaforos = 74
#City = City(num_paraderos, num_semaforos)

def random_within_bounds(lower, upper):
    """
    Genera un número aleatorio dentro de un rango [lower, upper),
    excluyendo el valor especificado en exclude.
    """
    if lower >= upper:
        aux = lower
        lower = upper
        upper = aux
    random_number = random.randint(lower, upper - 1)
    return random_number

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
        if self.model.schedule.steps % INTERVALO_SEMAFORO == 0:
            if self.color == "green":
                self.color = "red"
            else:
                self.color = "green"

class Bus(Agent):
    def __init__(self, unique_id, model, velocidad_maxima, aceleracion, recorrido):
        super().__init__(unique_id, model)
        self.pasajeros = [] #lista de personas en el bus
        self.velocidad_maxima = velocidad_maxima
        self.aceleracion = aceleracion
        self.recorrido = recorrido
        self.velocidad = 0
        self.distancia_recorrida = 0
        self.posicion_actual = 0  # Índice actual en el recorrido (representa tambien el bloque actual)
        self.limite_pasajeros = LIMITE_PASAJEROS_BUS #capacidad maxima de pasajeros
        self.ultimo_semaforo=-1 #indice del ultimo semaforo en el que se detuvo
        self.ultimo_paradero=-1 #indice del ultimo paradero en el que se detuvo
        self.steps_en_standBy = 0 #indica si el bus esta en un paradero
        self.puede_moverse = True #indica si el bus puede moverse o no

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
                    print("bloque actual: " + str(self.distancia_recorrida // ESCALA)+ ", bloque anterior: "+ str(self.posicion_actual) + ",salto de bloques: " + str(int(distancia_por_recorrer // ESCALA)))                                                                                                                                                                                                                                                                                                                                                                                                    
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
                    self.steps_en_standBy+= 1   #agrego un standby por cada persona que se sube
                    self.pasajeros.append(persona) #se agregan las personas al bus
                    paradero.personas.remove(persona) #se saca la persona del paradero
                    
            #print(f"Agente {agent.unique_id} en la celda  {self.recorrido[self.posicion_actual]}")

    def abandonarPasajeros(self,agent,indice_paradero):

        for persona in self.pasajeros[:]:
            #print(f"{persona.destino}, {indice_paradero}")
            if persona.destino == indice_paradero: #si el destino de la persona es el paradero actual
                self.steps_en_standBy+= 1   #agrego un standby por cada persona que se baja
                self.pasajeros.remove(persona)
                #print("Bus " + str(self.unique_id) + " dejando persona " + str(persona.unique_id) + " en paradero " + str(self.posicion_actual))
                agent.personas.append(persona)

    def calcularDistancia(self):
        return self.velocidad+0.5*self.aceleracion

    def step(self):
        #print("soy un bus: " + str(self.unique_id) + " y estoy en la posicion " + str(self.posicion_actual))
        cell_contents = self.model.grid.get_cell_list_contents(self.recorrido[self.posicion_actual]) #obtengo los agentes en la celda actual
        for agent in cell_contents: #recorro los agentes en la celda actual
            if isinstance(agent, BusStop): #si es un paradero
                indice_paradero = PARADEROS.index(agent.posicion) #obtengo el indice del paradero
                if indice_paradero != self.ultimo_paradero: #si todavia no paso por esta paradero
                    #print("Bus " + str(self.unique_id) + " en paradero " + str(indice_paradero) + "con ultimo paradero " + str(self.ultimo_paradero) + " y ultimo semaforo " + str(self.ultimo_semaforo) + " y largo recorrido " + str(len(self.recorrido)))
                    self.abandonarPasajeros(agent,indice_paradero)
                    self.recogerPasajeros(agent)
                    self.ultimo_paradero = indice_paradero
                    self.velocidad = 0
            if isinstance(agent, TrafficLight):
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
    def __init__(self, unique_id, model,destino):
        super().__init__(unique_id, model)
        self.destino = destino #numero entre 0 y 67, corresponde al index de paradero de destino
    def step(self):
        pass

class BusStop(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero
        self.personas = [] #lista de personas esperando (lista de Clase de Peatón)
        self.cantidad_personas = 0 #cantidad de personas en el paradero
    def step(self):
        if self.model.schedule.steps % INTERVALO_ADICION_PEATONES_EN_PARADERO == 0:
            agregar = random_within_bounds(1, 5) #agrego 1 o 5 personas al paradero
            for _ in range(agregar):
                cota_inferior_destino = PARADEROS.index(self.posicion) #obtengo el indice del paradero actual
                cota_superior_destino = len(PARADEROS) #obtengo el indice del ultimo paradero
                persona = Person(self.model.schedule.get_agent_count(), self, random_within_bounds(cota_inferior_destino, cota_superior_destino))
                self.model.schedule.add(persona)
                self.personas.append(persona)
        #print("soy un paradero: " + str(self.unique_id) + " y tengo " + str(len(self.personas)) + " personas")
    
class City(Model):
    def __init__(self, N):
        
        self.num_paraderos = N
        self.paraderos = []
        self.recorrido = []
        self.semaforos = []
        self.grid = MultiGrid(200, 440, torus=True)
        #se crea un programador de agentes
        self.schedule = RandomActivationByType(self) # (CREO) se crea para posteriormente guardar los agentes e la simulación

        self.paraderos = []
         # Crear paraderos con posiciones estáticas
        #print("Creando semaforos..."+ str(len(SEMAFOROS)))
        for i,pos in enumerate(PARADEROS):
            paradero = BusStop(self.schedule.get_agent_count(), self, pos[0], pos[1]) #se crea un paradero
            self.schedule.add(paradero) #Se agrega el agente al programador de agentes
            #for _ in range(PERSONAS_ESPERANDO_PARADERO_INICIAL[i]):
            for _ in range(3):
                #print("i: " + str(i) + " num_paraderos: " + str(self.num_paraderos))
                persona = Person(self.schedule.get_agent_count(), self, random_within_bounds(i, self.num_paraderos))
                self.schedule.add(persona)
                paradero.personas.append(persona)
            self.paraderos.append(paradero)
            self.grid.place_agent(paradero, pos)

        for pos in RECORRIDO:
            posicion = PosicionRecorrido(self.schedule.get_agent_count(), self, pos[0], pos[1]) #se crea un paradero
            self.recorrido.append(posicion)
            self.grid.place_agent(posicion, pos)
            self.schedule.add(posicion) #Se agrega el agente al programador de agentes

        for pos in SEMAFOROS:
            trafficLight = TrafficLight(self.schedule.get_agent_count(), self, pos[0], pos[1]) #se crea un paradero
            self.semaforos.append(trafficLight)
            self.grid.place_agent(trafficLight, pos)
            self.schedule.add(trafficLight) #Se agrega el agente al programador de agentes

        self.bus = Bus(self.schedule.get_agent_count(), self, VEL_MAX, ACELERACION, RECORRIDO)
        self.grid.place_agent(self.bus, RECORRIDO[0])
        self.schedule.add(self.bus)

        #self.running = True
    def step(self):
        """Advance the model by one step."""
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()
        if self.schedule.steps % 120 == 0:
            self.bus = Bus(self.schedule.get_agent_count(), self, VEL_MAX, ACELERACION, RECORRIDO)
            self.grid.place_agent(self.bus, RECORRIDO[0])
            self.schedule.add(self.bus)
            #print("step: " + str(self.schedule.steps) + "agrgegue un bus")

def agent_portrayal(agent):
    if agent is None:
        return
    if isinstance(agent, BusStop):
        return {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": "blue",
                "w": 0.9,
                "h": 0.9}
    if isinstance(agent, PosicionRecorrido):
        return {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": "grey",
                "w": 0.2,
                "h": 0.2}
    if isinstance(agent, TrafficLight):
        if agent.color == "red":
            Color = "red"
        else:
            Color = "green"
        return {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": Color,
                "w": 3,
                "h": 0.6}
    if isinstance(agent, Bus):
        return {"Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "yellow",
            "w": 0.5,
            "h": 0.5,
            "stroke_color": "black"}

        
# Definir visualización
grid = CanvasGrid(agent_portrayal, 200, 440, 2500, 5500)

# Definir servidor de visualización
server = ModularServer(City, [grid], "Simulación de Transporte Urbano", {"N": num_paraderos})

# Iniciar servidor de visualización
server.port = 8528
server.launch()


