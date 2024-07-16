from django.shortcuts import render
from django.http import JsonResponse
import random
import time

# Variables globales para almacenar datos
tiempos = []
valores = []
inicio = None

def index(request):
    global inicio
    # Asegúrate de que inicio esté configurado
    if inicio is None:
        inicio = time.time()
    return render(request, 'myapp/index.html')

def get_data(request):
    global tiempos, valores, inicio
    if inicio is None:
        return JsonResponse({'error': 'La simulación no ha comenzado'}, status=400)

    valor = random.uniform(35, 40)
    tiempo_actual = (time.time() - inicio) / 3600  # Convertir segundos a horas
    tiempos.append(tiempo_actual)
    valores.append(valor)
    return JsonResponse({'tiempos': tiempos, 'valores': valores})

def reiniciar(request):
    global tiempos, valores, inicio
    tiempos = []
    valores = []
    inicio = None  # Reinicia el estado
    return JsonResponse({'status': 'reiniciado'})
