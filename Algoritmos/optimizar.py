
import numpy as np

#Calcula la radiacion en un punto destino debido a una fuente
def radiacionPuntual(fuente, destino):  # Add your parameters here!
    radiacion = fuente*destino
    
    print (" %d to the power of %d is %d " % (fuente,destino,radiacion))
    
    return radiacion    


def inicializarFuentes(inicioFuentes):
    global numFuentes
    inicioFuentes = np.random.rand(numFuentes,3) #Inicializa las fuentes a una posicion aleatoria
    #Escala los valores aleatorios al rango del Grid
    for i in range(numFuentes):
        inicioFuentes[i] = escalarVector(inicioFuentes[i])
    
    return inicioFuentes
    
    

def escalarVector(vector):
    global minX, minY, minZ, maxX, maxY, maxZ
    vector[0] = (maxX-minX) * vector[0] + minX
    vector[1] = (maxY-minY) * vector[1] + minY
    vector[2] = (maxZ-minZ) * vector[2] + minZ
    
    return vector



def puntoDentro(puntoCentro, puntoVecindad):
    return True



def generarFuenteVecino(actualFuente):
    global dimensionGrid, gridFuentes, dimensionVecinos

    contador = 0
    indicesVecinos = np.zeros((dimensionVecinos))
    for i in range(dimensionGrid):
        if(puntoDentro(actualFuente, gridFuentes[i])):
            indicesVecinos[contador] = i #Si el punto esta en la vecindad se guarda el indice
            contador += 1
            
    indice = np.random.randint(contador) #Genera un indice aleatorio para escoger al vecino
    indice = indicesVecinos[indice] #Recupera el indice del punto del grid seleccionado aleatoriamente
    
    return  gridFuentes[indice] #Retorna el punto del grid fuente seleccionado aleatoriamente
    
    

def generarFuentesVecinos(actualFuentes):
    global numFuentes
    
    vecinoFuentes = np.zeros((numFuentes,3))
    for i in range(numFuentes):
        vecinoFuentes[i] = generarFuenteVecinos(actualFuentes[i])
     
    return vecinoFuentes

    
      
def generarGrid(gridVector):
    global dimensionGrid, dimensionGridX, dimensionGridY, dimensionGridZ
    global minX,minY,minZ,dx,dy,dz
    
    indice = 0
    x = minX
    for i in range(dimensionGridX):
        y = minY
        for j in range(dimensionGridY):
            z = minZ
            for k in range(dimensionGridZ):   
                gridVector[indice][0] = x
                gridVector[indice][1] = y
                gridVector[indice][2] = z
                indice += 1
                z += dz
            y += dy
        x += dx
    return gridVector
    
    
    
    
    
    
    
    
    
def calcularEnergia(posicionFuentes):
    global dimensionGrid, gridDestinos
    energia = 0.0
    
    
    return energia



#Variables del Grid
minX = -30.0
maxX = 30.0
minY = -30.0
maxY = 30.0
minZ = 0.0
maxZ = 10.0
numFuentes = 5
dx = 1.0
dy = 1.0
dz = 1.0
dimensionGridX = int((maxX-minX)/dx)
dimensionGridY = int((maxY-minY)/dy)
dimensionGridZ = int((maxZ-minZ)/dz)
dimensionGrid = dimensionGridX * dimensionGridY * dimensionGridZ

gridDestinos = np.zeros((dimensionGrid,3))
gridFuentes = np.zeros((dimensionGrid,3))

gridFuentes = generarGrid(gridFuentes)
gridDestinos = generarGrid(gridDestinos)


#Variables y constantes de Enfriamiento Simulado
To = 1
Tf = 0.001
maxIteraciones = 50
deltaVecinosX = dx * 3
deltaVecinosY = dy * 3
deltaVecinosZ = dz * 3
dimensionVecinos = deltaVecinosX * deltaVecinosY * deltaVecinosZ


#ENFRIAMIENTO SIMULADO
inicioFuentes = np.zeros((numFuentes,3))
inicioFuentes = inicializarFuentes(inicioFuentes) #Inicializa a valores aleatorios dentro de los rangos permitidos
actualFuentes = inicioFuentes
mejorFuentes = inicioFuentes
vecinoFuentes = np.zeros((numFuentes,3))

energiaMejor = calcularEnergia(mejorFuentes)
T = To
while T>Tf:
    
    iteracion = 0
    while iteracion < maxIteraciones:
        vecinoFuentes = generarFuentesVecinos(actualFuentes) #Genera fuentes en la vecindad de las fuentes actuales
        energiaActual = calcularEnergia(actualFuentes)
        energiaVecinos = calcularEnergia(vecinoFuentes)

        deltaEnergia = energiaVecinos - energiaActual 
        if(deltaEnergia < 0):
            actualFuentes = vecinoFuentes #Si la energia disminuye se acepta la nueva posicion de las fuentes
            if(energiaVecinos < energiaMejor):
                mejorFuentes = vecinoFuentes #Se actualiza el mejor estado
                energiaMejor = calcularEnergia(mejorFuentes)
        else:
            if(exp(deltaEnergia/T) > np.random.random.random()): 
                actualFuente = vecinoFuentes  #Se elije un estado con mayor energia con cierta probabilidad
                
        iteracion += 1
    T = 0.1 * T #Disminuye la tempreratura por un factor








#for i in range(3):
#    print(gridDestinos[i,1])

#gridDestinos[1][0] = 555

#print(gridDestinos[1][0])

#print(inicioFuentes)
print("DIMENSIONES")
print("DimensionX = %d  DimensionY = %d   DimensionZ = %d \n" % (dimensionGridX,dimensionGridY,dimensionGridZ))
print(gridFuentes)


