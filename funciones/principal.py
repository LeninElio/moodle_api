import time

def calcular_tiempo(func):
    def tiempo_ejecucion():
        inicio = time.time()
        func()
        fin = time.time()

        print(f"Tiempo de ejecución: {fin - inicio} segundos")
    
    return tiempo_ejecucion