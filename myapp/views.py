import base64
import json
import random
import time

from django.shortcuts import render
from django.http import JsonResponse
import matplotlib.pyplot as plt
import io


def index(request):
    return render(request, 'myapp/index.html')


# Función para la visualización de datos
def visualizacion_datos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tiempos = data.get('tiempos', [])
        valores = data.get('valores', [])

        plt.figure(figsize=(10, 5))
        plt.plot(tiempos, valores, 'ro-')
        plt.xlabel('Tiempo (h)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Visualización de Temperatura Corporal en Tiempo Real')
        plt.grid(True)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return JsonResponse({'image': image_base64})
    return render(request, 'myapp/visualizacion_datos.html')

def simular_datos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tiempo_simulacion = int(data.get('tiempo_simulacion', 1))  # Tiempo en minutos
        intervalos = int(data.get('intervalos', 1))  # Número de intervalos de simulación
        intervalo_tiempo = tiempo_simulacion * 60 / intervalos  # Convertir minutos a segundos
        tiempos = []
        valores = []

        for i in range(intervalos):  # Dividir en intervalos
            tiempo_actual = i * (intervalo_tiempo / 60)  # Convertir segundos a horas
            valor = random.uniform(35, 40)
            tiempos.append(tiempo_actual)
            valores.append(valor)

        return JsonResponse({'tiempos': tiempos, 'valores': valores})

# Función para calcular IMC
def calcular_imc(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        estatura = float(data['estatura'])
        peso = float(data['peso'])
        indice = peso / (estatura * estatura)
        clasificacion = obtener_clasificacion_imc(indice)
        image_base64 = mostrar_grafico_imc(indice, clasificacion)
        return JsonResponse({'indice': indice, 'clasificacion': clasificacion, 'image': image_base64})
    return render(request, 'myapp/imc.html')

def obtener_clasificacion_imc(indice):
    if indice > 50:
        return "DOBLE OBESIDAD MORBIDA"
    elif indice > 40:
        return "OBESIDAD MORBIDA"
    elif indice > 35:
        return "OBESIDAD GRAVE"
    elif indice > 30:
        return "OBESIDAD MODERADA"
    elif indice > 25:
        return "SOBREPESO"
    else:
        return "PESO NORMAL"

def mostrar_grafico_imc(indice, clasificacion):
    header = ['IMC', 'Clasificación']
    data = [
        ['< 25', 'Peso Normal'],
        ['25-30', 'Sobrepeso'],
        ['30-35', 'Obesidad Moderada'],
        ['35-40', 'Obesidad Grave'],
        ['40-50', 'Obesidad Mórbida'],
        ['> 50', 'Doble Obesidad Mórbida']
    ]
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=header, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.2, 1.2)
    plt.title(clasificacion)
    plt.xlabel(f"IMC: {indice:.2f}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64


# Función para obtener frecuencia cardíaca
def frecuencia_cardiaca(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        edad = int(data['edad'])
        frecuencia = int(data['frecuencia'])
        resultado = comparar_con_parametros_normales(frecuencia, edad)
        return JsonResponse({'resultado': resultado})
    return render(request, 'myapp/frecuencia_cardiaca.html')


def comparar_con_parametros_normales(frecuencia_cardiaca, edad):
    parametros_normales = {
        "niño": (60, 100),
        "adulto_joven": (60, 100),
        "adulto_mayor": (50, 60)
    }
    if edad < 18:
        grupo_edad = "niño"
    elif 18 <= edad <= 65:
        grupo_edad = "adulto_joven"
    else:
        grupo_edad = "adulto_mayor"
    rango_normal = parametros_normales[grupo_edad]
    if frecuencia_cardiaca < rango_normal[0]:
        return "La frecuencia cardíaca está por debajo de lo normal."
    elif frecuencia_cardiaca > rango_normal[1]:
        return "La frecuencia cardíaca está por encima de lo normal."
    else:
        return "La frecuencia cardíaca está dentro de los parámetros normales."
