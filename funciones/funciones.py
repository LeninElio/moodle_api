import time

def calcular_tiempo(func):
    def tiempo_ejecucion():
        inicio = time.time()
        retorno = func()
        fin = time.time()

        print(f"Ejecutado en: {round((fin - inicio), 2)} segundos.")
        return retorno
    
    return tiempo_ejecucion


def calcular_tiempo_arg(func):
    def tiempo_ejecucion(*args):
        inicio = time.time()
        retorno = func(*args)
        fin = time.time()

        print(f"Ejecutado en: {round((fin - inicio), 2)} segundos.")
        return retorno
    
    return tiempo_ejecucion