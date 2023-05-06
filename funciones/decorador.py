# pylint: disable=C0114
import time


def calcular_tiempo(funcion_decorada):
    """
    La función "calcular_tiempo" es un decorador que calcula el tiempo de ejecución de
    una determinada función.

    :param func: una función que será cronometrada cuando sea llamada

    :return: La función `execution_time()` se devuelve como una función de decorador.
    """
    def tiempo_ejecucion():
        inicio = time.time()
        retorno = funcion_decorada()
        fin = time.time()

        print(f"Ejecutado en: {round((fin - inicio), 2)} segundos.")
        return retorno

    return tiempo_ejecucion


def calcular_tiempo_arg(funcion_decorada):
    """
    La función `calcular_tiempo_arg` es un decorador de Python que calcula
    el tiempo de ejecución de una función dada.

    :param func: función que será decorada con el decorador `calcular_tiempo_arg`

    :return: Se está devolviendo la función `tiempo_ejecucion`, que es una
    función wrapper que calcula el tiempo de ejecución de la función decorada
    y devuelve su resultado.
    """
    def tiempo_ejecucion(*args):
        inicio = time.time()
        retorno = funcion_decorada(*args)
        fin = time.time()

        print(f"Ejecutado en: {round((fin - inicio), 2)} segundos.")
        return retorno

    return tiempo_ejecucion
