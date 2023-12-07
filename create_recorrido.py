PARADEROS = [(190, 10), (189, 17), (188, 24), (187, 31), (186, 38), (185, 45), (184, 52), (183, 59), (182, 66), (181, 73), (180, 80), (179, 87), (178, 94), (177, 101), (176, 108), (175, 115), (174, 122), (173, 129), (172, 136), (171, 143), (170, 150), (167, 159), (164, 168), (161, 177), (158, 186), (155, 195), (152, 204), (149, 213), (143, 218), (137, 223), (131, 228), (125, 233), (119, 238), (113, 243), (107, 248), (106, 256), (105, 262), (104, 268), (103, 274), (102, 280), (101, 286), (100, 292), (99, 298), (98, 304), (97, 310), (96, 316), (95, 322), (94, 328), (93, 334), (92, 340), (91, 346), (90, 352), (89, 358), (88, 364)]


RECORRIDO = []

for i, pos in enumerate(PARADEROS):
    distanciaX = PARADEROS[i+1][0] - pos[0]
    distanciaY = PARADEROS[i+1][1] - pos[1]
    if distanciaX >  1 or distanciaX < -1 and distanciaY > 1 or distanciaY < -1:
        pendiente = distanciaY / distanciaX
        if pendiente >0:
            if distanciaY > distanciaX:
                recorrido.append

        RECORRIDO.append((distanciaX, distanciaY))
        