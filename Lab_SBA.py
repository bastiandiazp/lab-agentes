import random
from datetime import datetime, timedelta
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivationByType
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer



SEMAFOROS = [(189, 13), (189, 15), (188, 20), (188, 22), (187, 26), (187, 29)]

PARADEROS = [(190, 10), (189, 17), (188, 24), (187, 31), (186, 38), (185, 45), (184, 52), (183, 59), (182, 66), (181, 73), 
(180, 80), (179, 87), (178, 94), (177, 101), (176, 108), (175, 115), (174, 122), (173, 129), (172, 136), (171, 143), 
(170, 150), (167, 159), (164, 168), (161, 177), (158, 186), (155, 195), (152, 204), (149, 213), (143, 218), (138, 223), 
(133, 228), (128, 233), (123, 238), (118, 243), (113, 248), (112, 254), (111, 260), (110, 266), (109, 272), (108, 278), 
(107, 284), (106, 290), (105, 296), (104, 302), (103, 308), (102, 314), (101, 320), (100, 326), (99, 332), (98, 338), 
(97, 344), (96, 350), (95, 356), (94, 362), (88, 361), (82, 360), (76, 359), (70, 358), (64, 357), (58, 356), (52, 355), 
(46, 354), (40, 353), (34, 352), (28, 351), (22, 350), (23, 346), (19,342)]

#68 paraderos
PERSONAS_ESPERANDO_PARADERO_INICIAL = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
RECORRIDO = [(190, 10), (189, 11), (189, 12), (189, 13), (189, 14), (189, 15), (189, 16), (189, 17), (188, 18), (188, 19), (188, 20), (188, 21), (188, 22), (188, 23), (188, 24), (187, 25), (187, 26), (187, 27), (187, 28), (187, 29), (187, 30), (187, 31), (186, 32), (186, 33), (186, 34), (186, 35), (186, 36), (186, 37), (186, 38), (185, 45)]
#RECORRIDO = [(61, 369) ,(60, 370) ,(59, 371) ,(58, 372) ,(58, 373) ,(58, 374) ,(58, 375) ,(58, 376) ,(58, 377) ,(58, 378) ,(58, 379) ,(58, 380) ,(58, 381) ,(58, 382) ,(57, 383) ,(56, 384) ,(55, 385) ,(54, 386) ,(53, 387) ,(52, 388) ,(51, 389) ,(50, 390) ,(49, 390) ,(48, 390) ,(47, 390) ,(46, 390) ,(45, 390) ,(44, 390) ,(43, 390) ,(42, 389) ,(41, 389) ,(40, 389) ,(39, 388) ,(38, 388) ,(37, 388) ,(36, 388) ,(35, 388) ,(34, 388) ,(33, 388) ,(32, 388) ,(31, 388) ,(30, 387) ,(29, 387) ,(28, 387) ,(27, 387) ,(26, 387) ,(25, 387) ,(24, 387) ,(23, 387) ,(22, 387) ,(22, 386) ,(22, 385) ,(22, 384) ,(22, 383) ,(22, 382) ,(22, 381) ,(22, 380) ,(22, 379) ,(22, 378) ,(22, 377) ,(22, 376) ,(22, 375) ,(22, 374) ,(22, 373) ,(22, 372) ,(22, 371) ,(22, 370) ,(22, 369) ,(23, 368) ,(24, 367) ,(24, 366) ,(24, 365) ,(24, 364) ,(24, 363) ,(24, 362) ,(24, 361) ,(24, 360) ,(24, 359) ,(24, 358) ,(24, 357) ,(24, 356) ,(24, 355) ,(24, 354) ,(24, 353) ,(24, 352) ,(24, 351) ,(24, 350) ,(24, 349) ,(24, 348) ,(24, 347) ,(24, 346) ,(24, 345) ,(24, 344) ,(24, 343) ,(24, 342) ,(24, 341) ,(24, 340) ,(24, 339) ,(24, 338) ,(24, 337) ,(24, 336) ,(24, 335) ,(24, 334) ,(24, 333) ,(24, 332) ,(24, 331) ,(24, 330) ,(24, 329) ,(24, 328) ,(24, 327) ,(24, 326) ,(24, 325) ,(24, 324) ,(24, 323) ,(24, 322) ,(24, 321) ,(24, 320) ,(24, 319) ,(24, 318) ,(24, 317) ,(24, 316) ,(24, 315) ,(24, 314) ,(24, 313) ,(24, 312) ,(25, 311) ,(26, 310) ,(27, 309) ,(27, 308) ,(27, 307) ,(28, 306) ,(29, 305) ,(30, 304) ,(31, 303) ,(32, 302) ,(32, 301) ,(32, 300) ,(33, 299) ,(34, 298) ,(35, 297) ,(36, 296) ,(36, 295) ,(36, 294) ,(36, 293) ,(36, 292) ,(37, 291) ,(38, 290) ,(39, 289) ,(40, 288) ,(41, 288) ,(42, 288) ,(43, 287) ,(44, 287) ,(45, 286) ,(46, 286) ,(47, 285) ,(48, 284) ,(49, 284) ,(50, 284) ,(51, 284) ,(52, 284) ,(53, 283) ,(54, 282) ,(55, 282) ,(56, 282) ,(57, 282) ,(58, 282) ,(59, 282) ,(60, 282) ,(61, 282) ,(62, 281) ,(63, 280) ,(64, 279) ,(65, 279) ,(66, 279) ,(67, 279) ,(68, 279) ,(69, 279) ,(70, 278) ,(71, 278) ,(72, 278) ,(73, 277) ,(74, 276) ,(75, 275) ,(76, 274) ,(77, 274) ,(78, 273) ,(79, 272) ,(80, 272) ,(81, 271) ,(82, 270) ,(83, 270) ,(84, 270) ,(85, 270) ,(86, 269) ,(87, 268) ,(88, 267) ,(89, 266) ,(90, 266) ,(91, 266) ,(92, 266) ,(92, 265) ,(93, 264) ,(94, 263) ,(95, 262) ,(96, 261) ,(96, 260) ,(97, 259) ,(97, 258) ,(98, 257) ,(99, 256) ,(100, 255) ,(100, 254) ,(101, 253) ,(102, 252) ,(102, 251) ,(102, 250) ,(103, 249) ,(104, 248) ,(105, 247) ,(106, 246) ,(107, 245) ,(108, 245) ,(109, 245) ,(110, 244) ,(111, 243) ,(112, 242) ,(112, 241) ,(112, 240) ,(113, 239) ,(114, 239) ,(115, 239) ,(116, 238) ,(117, 238) ,(118, 238) ,(119, 237) ,(120, 236) ,(121, 235) ,(122, 234) ,(123, 233) ,(124, 233) ,(125, 232) ,(126, 231) ,(127, 230) ,(128, 230) ,(129, 229) ,(130, 229) ,(131, 228) ,(132, 228) ,(133, 228) ,(134, 228) ,(135, 228) ,(136, 228) ,(137, 228) ,(138, 228) ,(139, 228) ,(140, 227) ,(141, 227) ,(142, 227) ,(143, 227) ,(144, 227) ,(145, 227) ,(146, 227) ,(147, 227) ,(148, 226) ,(149, 226) ,(150, 226) ,(151, 226) ,(152, 226) ,(153, 226) ,(154, 226) ,(155, 226) ,(156, 226) ,(157, 226) ,(158, 226) ,(159, 226) ,(160, 226) ,(161, 226) ,(162, 226) ,(163, 225) ,(164, 224) ,(165, 224) ,(166, 223) ,(167, 222) ,(168, 222) ,(169, 222) ,(170, 222) ,(171, 222) ,(172, 222) ,(173, 222) ,(174, 222) ,(175, 222) ,(176, 222) ,(177, 222) ,(178, 222) ,(179, 222) ,(180, 222) ,(181, 222) ,(182, 222) ,(183, 222) ,(184, 222) ,(185, 222) ,(186, 222) ,(187, 222) ,(188, 222) ,(189, 222) ,(190, 222) ,(191, 222) ,(192, 222) ,(193, 222) ,(194, 222) ,(195, 222) ,(196, 222) ,(197, 222) ,(198, 222) ,(199, 222) ,(200, 222) ,(201, 222) ,(202, 222) ,(203, 222) ,(204, 222) ,(205, 222) ,(206, 222) ,(207, 222) ,(208, 222) ,(209, 222) ,(210, 222) ,(211, 222) ,(212, 222) ,(213, 222) ,(214, 222) ,(215, 222) ,(216, 222) ,(217, 222) ,(218, 222) ,(219, 222) ,(220, 221) ,(221, 221) ,(222, 221) ,(223, 221) ,(224, 221) ,(225, 221) ,(226, 221) ,(227, 221) ,(228, 220) ,(229, 220) ,(230, 220) ,(231, 220) ,(232, 220) ,(233, 220) ,(234, 220) ,(235, 220) ,(236, 220) ,(237, 220) ,(238, 220) ,(239, 220) ,(240, 220) ,(241, 220) ,(242, 220) ,(243, 220) ,(244, 220) ,(245, 220) ,(246, 220) ,(247, 220) ,(248, 220) ,(249, 220) ,(250, 220) ,(251, 220) ,(252, 220) ,(253, 220) ,(254, 220) ,(255, 219) ,(256, 218) ,(257, 218) ,(258, 218) ,(259, 217) ,(260, 217) ,(261, 217) ,(262, 217) ,(263, 217) ,(264, 216) ,(265, 216) ,(266, 216) ,(267, 215) ,(268, 215) ,(269, 215) ,(270, 215) ,(271, 215) ,(272, 215) ,(273, 214) ,(274, 214) ,(275, 213) ,(276, 213) ,(277, 213) ,(278, 213) ,(279, 213) ,(280, 213) ,(281, 212) ,(282, 212) ,(283, 211) ,(284, 210) ,(284, 209) ,(284, 208) ,(284, 207) ,(284, 206) ,(284, 205) ,(285, 204) ,(286, 203) ,(286, 202) ,(286, 201) ,(286, 200) ,(286, 199) ,(286, 198) ,(286, 197) ,(287, 196) ,(288, 195) ,(288, 194) ,(288, 193) ,(288, 192) ,(288, 191) ,(288, 190) ,(288, 189) ,(288, 188) ,(289, 187) ,(290, 186) ,(290, 185) ,(290, 184) ,(290, 183) ,(290, 182) ,(290, 181) ,(290, 180) ,(290, 179) ,(290, 178) ,(290, 177) ,(290, 176) ,(290, 175) ,(290, 174) ,(291, 173) ,(291, 172) ,(291, 171) ,(292, 170) ,(293, 169) ,(294, 168) ,(294, 167) ,(294, 166) ,(295, 165) ,(295, 164) ,(295, 163) ,(295, 162) ,(296, 161) ,(296, 160) ,(297, 159) ,(298, 158) ,(298, 157) ,(298, 156) ,(298, 155) ,(298, 154) ,(298, 153) ,(298, 152) ,(298, 151) ,(298, 150) ,(298, 149) ,(298, 148) ,(299, 147) ,(299, 146) ,(299, 145) ,(300, 144) ,(300, 143) ,(300, 142) ,(301, 141) ,(302, 140) ,(303, 139) ,(304, 138) ,(305, 137) ,(306, 136) ,(307, 135) ,(308, 134) ,(309, 133) ,(309, 132) ,(309, 131) ,(310, 130) ,(311, 129) ,(312, 128) ,(313, 127) ,(314, 126) ,(314, 125) ,(314, 124) ,(315, 123) ,(316, 122) ,(317, 121) ,(318, 120) ,(319, 119) ,(320, 118) ,(321, 117) ,(322, 116) ,(323, 115) ,(324, 114) ,(325, 113) ,(325, 112) ,(325, 111) ,(325, 110) ,(325, 109) ,(326, 108) ,(327, 107) ,(328, 106) ,(329, 105) ,(330, 104) ,(331, 103) ,(332, 102) ,(333, 101) ,(334, 100) ,(335, 99) ,(336, 98) ,(337, 97) ,(337, 96) ,(338, 95) ,(338, 94) ,(338, 93) ,(338, 92) ,(338, 91) ,(338, 90) ,(338, 89) ,(338, 88) ,(338, 87) ,(338, 86) ,(338, 85) ,(338, 84) ,(338, 83) ,(338, 82) ,(337, 81) ,(337, 80) ,(337, 79) ,(337, 78) ,(336, 77) ,(336, 76) ,(336, 75) ,(336, 74) ,(336, 73) ,(336, 72) ,(336, 71) ,(336, 70) ,(336, 69) ,(337, 68) ,(338, 67) ,(338, 66) ,(338, 65) ,(338, 64) ,(338, 63) ,(338, 62) ,(338, 61) ,(338, 60) ,(339, 59) ,(339, 58) ,(339, 57) ,(339, 56) ,(339, 55) ,(339, 54) ,(339, 53) ,(339, 52) ,(339, 51) ,(340, 50) ,(341, 49) ,(342, 48) ,(343, 47) ,(344, 46) ,(344, 45) ,(344, 44) ,(345, 43) ,(346, 42) ,(346, 41) ,(346, 40) ,(347, 39) ,(348, 38) ,(349, 37) ,(350, 36) ,(351, 35) ,(352, 34) ,(353, 33) ,(354, 32) ,(355, 31) ,(356, 30) ,(357, 29) ,(358, 28) ,(359, 27) ,(360, 26) ,(361, 25) ,(362, 24) ,(363, 23) ,(364, 22) ,(365, 21) ,(366, 20) ,(367, 19) ,(368, 18) ,(367, 17) ,(366, 16) ,(366, 15) ,(366, 14) ,(366, 13) ,(366, 12) ,(366, 11) ,(366, 10) ,(365, 9) ,(364, 9) ,(363, 9) ,(362, 9) ,(361, 9) ,(360, 9) ,(359, 10) ,(358, 11) ,(357, 12) ,(356, 13) ,(356, 14)]
VEL_MAX = 11.11 # m/s 40km/h
VEL_MAX_PUNTA = 5.56  # m/s 20km/h
ACELERACION = VEL_MAX/30
ACELERACION_PUNTA = VEL_MAX_PUNTA/20
DESACELERACION = -VEL_MAX/4
ESCALA =44 # metros que representa cada bloque
tiempos_de_espera = [timedelta(seconds=300)]

'''
(189, 17), (188, 18), (188, 19), (188, 20), (188, 21), (188, 22), (188, 23), (188, 24), (187, 25), (187, 26), (187, 27), (187, 28), (187, 29), (187, 30), (187, 31), (186, 32), (186, 33), (186, 34), (186, 35), (186, 36), (186, 37), (186, 38), (185, 45), (184, 46), (183, 47), (182, 48), (181, 49), (180, 50), (179, 51), (178, 52), (177, 53), (176, 54), , (175, 55), (174, 56), (173, 57), (172, 58), (171, 59), (170, 60), (169, 61), (168, 62), (167, 63), (166, 64), , (165, 65), (164, 66), (163, 67), (162, 68), (161, 69), (160, 70), (159, 71), (158, 72), (157, 73), (156, 74), , (155, 75), (154, 76), (153, 77), (152, 78), (151, 79), (150, 80), (149, 81), (148, 82), (147, 83), (146, 84), , (145, 85), (144, 86), (143, 87), (142, 88), (141, 89), (140, 90), (139, 91), (138, 92), (137, 93), (136, 94), , (135, 95), (134, 96), (133, 97), (132, 98), (131, 99), (130, 100), (129, 101), (128, 102), (127, 103), (126, 104), , (125, 105), (124, 106), (123, 107), (122, 108), (121, 109), (120, 110), (119, 111), (118, 112), (117, 113), (116, 114), , (115, 115), (114, 116), (113, 117), (112, 118), (111, 119), (110, 120), (109, 121), (108, 122), (107, 123), (106, 124), , (105, 125), (104, 126), (103, 127), (102, 128), (101, 129), (100, 130), (99, 131), (98, 132), (97, 133), (96, 134), , (95, 135), (94, 136), (93, 137), (92, 138), (91, 139), (90, 140), (89, 141), (88, 142), (87, 143), (86, 144), (85, 145), , (84, 146), (83, 147), (82, 148), (81, 149), (80, 150), (79, 151), (78, 152), (77, 153), (76, 154), (75, 155), (74, 156), , (73, 157), (72, 158), (71, 159), (70, 160), (69, 161), (68, 162), (67, 163), (66, 164), (65, 165), (64, 166), (63, 167), , (62, 168), (61, 169), (60, 170), (59, 171), (58, 172), (57, 173), (56, 174), (55, 175), (54, 176), (53, 177), (52, 178), , (51, 179), (50, 180), (49, 181), (48, 182), (47, 183), (46, 184), (45, 185), (44, 186), (43, 187), (42, 188), (41, 189), , (40, 190), (39, 191), (38, 192), (37, 193), (36, 194), (35, 195), (34, 196), (33, 197), (32, 198), (31, 199), (30, 200), , (29, 201), (28, 202), (27, 203), (26, 204), (25, 205), (24, 206), (23, 207), (22, 208), (21, 209), (20, 210), (19, 211), , (18, 212), (17, 213), (16, 214), (15, 215), (14, 216), (13, 217), (12



'''
# Configuración de la simulación
num_paraderos = 68
num_semaforos = 75
#City = City(num_paraderos, num_semaforos)

def random_within_bounds(lower, upper, exclude):
    """
    Genera un número aleatorio dentro de un rango [lower, upper),
    excluyendo el valor especificado en exclude.
    """
    if lower >= upper:
        raise ValueError("La cota inferior debe ser menor que la cota superior.")

    while True:
        random_number = random.randint(lower, upper - 1)
        if random_number != exclude:
            return random_number

class PosicionRecorrido(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero
        #self.peatones = [] #lista de peatones (lista de Clase de Peatón)
        #self.cant_peatones = 0 #cantidad de peatones en el paradero
    def step(self):
        #print("soy un paradero: " + str(self.unique_id) + " y tengo " + str(len(self.personas)) + " personas")
        pass

class TrafficLight(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.posicion = (x, y) #Posición del paradero
        self.color = "green"

    def step(self):
        
        pass

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
        self.limite_pasajeros = 30 #capacidad maxima de pasajeros
        self.ultimo_semaforo=-1 #indice del ultimo semaforo en el que se detuvo
        self.ultimo_paradero=-1 #indice del ultimo paradero en el que se detuvo

    def moverse(self):
        # Ajustar velocidad y posición según el recorrido
        if self.posicion_actual < len(self.recorrido) - 1:
            distancia_por_recorrer = self.calcularDistancia()
            if self.velocidad >= self.velocidad_maxima:
                self.velocidad = self.velocidad_maxima
            elif self.velocidad < self.velocidad_maxima:
                self.velocidad += self.aceleracion
            self.distancia_recorrida += distancia_por_recorrer
            self.posicion_actual += int(self.distancia_recorrida // ESCALA) # se pasa a escala de simulacion
            self.posicion_actual = self.posicion_actual% (len(self.recorrido)-1)
            #print ("posicion actual: " + str(self.posicion_actual) + "len recorrido: " + str(len(self.recorrido)))
            self.model.grid.move_agent(self, self.recorrido[self.posicion_actual])

        else:
            # Si ya llegó al final del recorrido, reiniciar
            self.velocidad = 0
            self.posicion_actual = 0


    def recogerPasajeros(self, agent,indice_paradero):
        if indice_paradero != self.ultimo_paradero: #si todavia no paso por esta paradero
            #print("Bus " + str(self.unique_id) + " recogiendo personas en paradero " + str(agent.unique_id))
            for persona in agent.personas:
                if len(self.pasajeros) < self.limite_pasajeros: #si el bus no esta lleno
                    self.pasajeros.append(persona) #se agregan las personas al bus
            agent.personas = [] #se vacia la lista de personas en el paradero
                    
            #print(f"Agente {agent.unique_id} en la celda  {self.recorrido[self.posicion_actual]}")

    def abandonarPasajeros(self,agent,indice_paradero):
        print("largo pasajeros: " + str(len(self.pasajeros)) + " indice paradero: " + str(indice_paradero) + " posicion actual: " + str(self.posicion_actual) + " ultimo paradero: " + str(self.ultimo_paradero) + " ultimo semaforo: " + str(self.ultimo_semaforo) + " largo recorrido: " + str(len(self.recorrido)))
        for persona in self.pasajeros[:]:
            print(f"{persona.destino}, {indice_paradero}")
            if persona.destino == indice_paradero: #si el destino de la persona es el paradero actual
                self.pasajeros.remove(persona)
                print("Bus " + str(self.unique_id) + " dejando persona " + str(persona.unique_id) + " en paradero " + str(self.posicion_actual))
                agent.personas.append(persona)

    def calcularDistancia(self):
        return self.velocidad+0.5*self.aceleracion

    def step(self):
        #print("soy un bus: " + str(self.unique_id) + " y estoy en la posicion " + str(self.posicion_actual))
        cell_contents = self.model.grid.get_cell_list_contents(self.recorrido[self.posicion_actual]) #obtengo los agentes en la celda actual
        for agent in cell_contents: #recorro los agentes en la celda actual
            if isinstance(agent, BusStop): #si es un paradero
                indice_paradero = PARADEROS.index(agent.posicion) #obtengo el indice en la lista de paraderos
                print("Bus " + str(self.unique_id) + " en paradero " + str(indice_paradero))
                self.abandonarPasajeros(agent,indice_paradero)
                self.recogerPasajeros(agent,indice_paradero)
                self.ultimo_paradero = indice_paradero
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
        #self.peatones = [] #lista de peatones (lista de Clase de Peatón)
        #self.cant_peatones = 0 #cantidad de peatones en el paradero
    def step(self):
        #print("soy un paradero: " + str(self.unique_id) + " y tengo " + str(len(self.personas)) + " personas")
        pass

class City(Model):
    def __init__(self, N):
        self.num_paraderos = N
        self.paraderos = []
        self.recorrido = []
        self.semaforos = []
        self.personaparadero = 0
        self.grid = MultiGrid(200, 440, torus=True)
        #se crea un programador de agentes
        self.schedule = RandomActivationByType(self) # (CREO) se crea para posteriormente guardar los agentes e la simulación

        self.paraderos = []
         # Crear paraderos con posiciones estáticas
        print("Creando paraderos..."+ str(len(PARADEROS)))
        for i,pos in enumerate(PARADEROS):
            paradero = BusStop(self.schedule.get_agent_count(), self, pos[0], pos[1]) #se crea un paradero
            self.schedule.add(paradero) #Se agrega el agente al programador de agentes
            #for _ in range(PERSONAS_ESPERANDO_PARADERO_INICIAL[i]):
            for _ in range(3):
                persona = Person(self.schedule.get_agent_count(), self, random_within_bounds(0, 5, i))
                self.schedule.add(persona)
                paradero.personas.append(persona)
            self.paraderos.append(paradero)
            self.grid.place_agent(paradero, pos)
        # Crear el autobús y añadirlo al programa de agentes
        self.bus = Bus(self.schedule.get_agent_count(), self, VEL_MAX, ACELERACION, RECORRIDO)
        self.grid.place_agent(self.bus, RECORRIDO[0])
        self.schedule.add(self.bus)
        #agentes = self.schedule.agents #obtiene todos los agentes
        #paraderos = [obj for obj in agentes if isinstance(obj, BusStop)] #guarda todas los agentes paradero en una lista
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

        #self.running = True
    def step(self):
        """Advance the model by one step."""

        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()


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
    if isinstance(agent, Bus):
        return {"Shape": "rect",
            "Filled": "true",
            "Layer": 1,
            "Color": "black",
            "w": 0.5,
            "h": 0.5}
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
                "w": 0.6,
                "h": 0.6}

        
# Definir visualización
grid = CanvasGrid(agent_portrayal, 200, 440, 2500, 5500)

# Definir servidor de visualización
server = ModularServer(City, [grid], "Simulación de Transporte Urbano", {"N": num_paraderos})

# Iniciar servidor de visualización
server.port = 8524
server.launch()