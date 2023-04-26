import time

def calcular_tiempo(func):
    def tiempo_ejecucion():
        inicio = time.time()
        func()
        fin = time.time()

        print(f"Tiempo de ejecución: {fin - inicio} segundos")
    
    return tiempo_ejecucion


def calcular_tiempo_arg(func):
    def tiempo_ejecucion(*args):
        inicio = time.time()
        func(*args)
        fin = time.time()

        print(f"Tiempo de ejecución: {fin - inicio} segundos")
    
    return tiempo_ejecucion