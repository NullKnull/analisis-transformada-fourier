"""
Análisis de señales en el dominio del tiempo y la frecuencia
mediante la Transformada de Fourier.

En este programa se estudian tres señales básicas: un pulso
rectangular, una función escalón y una señal senoidal.

El objetivo es observar cómo se representan estas señales en
el dominio del tiempo y cómo se distribuye su contenido en
frecuencia mediante la Transformada Rápida de Fourier (FFT).

También se comprueban algunas propiedades de la transformada,
como la linealidad y el desplazamiento temporal, y se compara
el espectro de señales senoidales de distintas frecuencias.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================================
# 1. CONFIGURACIÓN DE LA SIMULACIÓN
# ==========================================================

# La frecuencia de muestreo indica cuántas muestras se toman
# por segundo. En este caso se utilizan 1000 muestras por segundo.
fs = 1000

# Duración total de la simulación, expresada en segundos.
T = 2.0

# Número total de muestras que tendrá cada señal.
N = int(fs * T)

# Intervalo de tiempo entre dos muestras consecutivas.
dt = 1 / fs

# Se crea el eje temporal desde -1 hasta aproximadamente 1 s.
# Centrar el tiempo en cero facilita la visualización de las señales.
t = np.arange(N) / fs - T / 2

# Las gráficas se guardarán en esta carpeta.
# Si no existe, se crea automáticamente.
carpeta = Path("resultados")
carpeta.mkdir(exist_ok=True)


# ==========================================================
# 2. GENERACIÓN DE LAS SEÑALES
# ==========================================================

# Pulso rectangular:
# La señal vale 1 entre -0.2 y 0.2 segundos y vale 0 fuera
# de ese intervalo. Por lo tanto, su duración es de 0.4 s.
pulso = np.where(np.abs(t) <= 0.2, 1.0, 0.0)

# Función escalón unitario:
# Su valor es 0 antes de t = 0 y 1 a partir de t = 0.
# Esta versión está limitada al intervalo de simulación.
escalon = np.where(t >= 0, 1.0, 0.0)

# Señal senoidal:
# Se genera una onda de amplitud 1 y frecuencia de 10 Hz.
# Esto significa que completa 10 ciclos por segundo.
f0 = 10
senoidal = np.sin(2 * np.pi * f0 * t)

# Se agrupan las señales para poder analizarlas con la misma función.
senales = {
    "Pulso rectangular": pulso,
    "Funcion escalon": escalon,
    "Senal senoidal": senoidal
}


# ==========================================================
# 3. TRANSFORMADA DE FOURIER Y REPRESENTACIÓN GRÁFICA
# ==========================================================

def analizar_senal(nombre, x):
    """
    Analiza una señal en los dominios del tiempo y la frecuencia.

    Parámetros:
        nombre (str): Nombre utilizado para identificar la señal.
        x (array): Valores de la señal en cada instante de muestreo.

    La función calcula la FFT, obtiene su magnitud y fase, y
    genera tres gráficas. Finalmente, guarda la figura en disco.
    """

    # Calcular la Transformada Discreta de Fourier mediante la FFT.
    # La división entre N normaliza la magnitud del espectro.
    X = np.fft.fft(x) / N

    # Obtener las frecuencias asociadas a las muestras.
    # fftfreq utiliza la frecuencia de muestreo para calcularlas.
    f = np.fft.fftfreq(N, d=dt)

    # Reordenar el espectro para colocar la frecuencia cero
    # en el centro y mostrar las frecuencias negativas y positivas.
    X = np.fft.fftshift(X)
    f = np.fft.fftshift(f)

    # La magnitud indica cuánto aporta cada componente de frecuencia.
    magnitud = np.abs(X)

    # La fase representa el ángulo de cada componente compleja,
    # expresado en radianes.
    fase = np.angle(X)

    # Cuando la magnitud es prácticamente cero, la fase no aporta
    # información útil. Se ocultan esos puntos en la gráfica.
    fase[magnitud < 1e-8] = np.nan

    # Crear tres gráficas verticales para comparar los resultados.
    fig, ax = plt.subplots(3, 1, figsize=(10, 9))

    # Primera gráfica: señal original en el dominio del tiempo.
    ax[0].plot(t, x)
    ax[0].set_title(f"{nombre}: dominio del tiempo")
    ax[0].set_xlabel("Tiempo (s)")
    ax[0].set_ylabel("Amplitud")
    ax[0].grid(True)

    # Segunda gráfica: magnitud del espectro de frecuencia.
    # Se muestran las frecuencias cercanas al origen para facilitar
    # la interpretación de las componentes principales.
    ax[1].plot(f, magnitud)
    ax[1].set_title("Magnitud del espectro de Fourier")
    ax[1].set_xlabel("Frecuencia (Hz)")
    ax[1].set_ylabel("Magnitud normalizada")
    ax[1].set_xlim(-60, 60)
    ax[1].grid(True)

    # Tercera gráfica: fase de las componentes de frecuencia.
    ax[2].plot(f, fase)
    ax[2].set_title("Fase del espectro de Fourier")
    ax[2].set_xlabel("Frecuencia (Hz)")
    ax[2].set_ylabel("Fase (rad)")
    ax[2].set_xlim(-60, 60)
    ax[2].grid(True)

    # Ajustar los espacios para evitar que los títulos y ejes
    # se encimen. Después, guardar la figura como imagen PNG.
    fig.tight_layout()

    nombre_archivo = nombre.replace(" ", "_")
    fig.savefig(carpeta / f"{nombre_archivo}.png", dpi=150)

    # Mostrar la figura en pantalla.
    plt.show()


# Analizar las tres señales utilizando la misma función.
for nombre, x in senales.items():
    analizar_senal(nombre, x)


# ==========================================================
# 4. COMPROBACIÓN DE LA PROPIEDAD DE LINEALIDAD
# ==========================================================

# La propiedad de linealidad establece que la transformada
# de una suma ponderada de señales es igual a la suma ponderada
# de sus transformadas:
#
# FFT(a*x + b*y) = a*FFT(x) + b*FFT(y)
#
# Para comprobarla, combinamos el pulso rectangular y la senoide.

a = 2
b = 3

x = pulso
y = senoidal

# Transformada de la señal combinada.
fft_combinada = np.fft.fft(a * x + b * y)

# Combinación de las transformadas calculadas por separado.
fft_separada = (
    a * np.fft.fft(x) +
    b * np.fft.fft(y)
)

# Medir la mayor diferencia entre ambos resultados.
error_linealidad = np.max(
    np.abs(fft_combinada - fft_separada)
)

print("\nCOMPROBACIÓN DE LINEALIDAD")
print(f"Error máximo: {error_linealidad:.3e}")
print(
    "¿Se cumple la propiedad?:",
    np.allclose(fft_combinada, fft_separada, atol=1e-10)
)

# El error debería ser prácticamente cero, salvo pequeñas
# diferencias numéricas propias de los cálculos computacionales.


# ==========================================================
# 5. COMPROBACIÓN DEL DESPLAZAMIENTO TEMPORAL
# ==========================================================

# La propiedad de desplazamiento temporal indica que mover una
# señal en el tiempo modifica la fase de su transformada, pero
# conserva la magnitud del espectro.
#
# Para una señal desplazada x[n-m]:
#
# X_desplazada[k] = X[k] * exp(-j*2*pi*k*m/N)
#
# np.roll realiza un desplazamiento circular de las muestras.
# Por ello, esta prueba verifica específicamente la propiedad
# para un desplazamiento circular en una señal discreta.

desplazamiento = 100

# Desplazar el pulso 100 muestras, equivalentes a 0.1 segundos.
x_desplazada = np.roll(pulso, desplazamiento)

# Calcular las transformadas sin centrar el espectro.
X_original = np.fft.fft(pulso)
X_desplazada = np.fft.fft(x_desplazada)

# Obtener las frecuencias en el orden original de la FFT.
f_sin_centrar = np.fft.fftfreq(N, d=dt)

# Calcular el factor complejo que representa el cambio de fase.
factor_fase = np.exp(
    -2j * np.pi * f_sin_centrar * desplazamiento * dt
)

# Comparar la FFT de la señal desplazada con la expresión teórica.
error_desplazamiento = np.max(
    np.abs(
        X_desplazada -
        X_original * factor_fase
    )
)

print("\nCOMPROBACIÓN DEL DESPLAZAMIENTO TEMPORAL")
print(f"Desplazamiento: {desplazamiento * dt:.3f} segundos")
print(f"Error máximo: {error_desplazamiento:.3e}")
print(
    "¿Se cumple la propiedad?:",
    np.allclose(
        X_desplazada,
        X_original * factor_fase,
        atol=1e-8
    )
)

# En este caso, el resultado debería confirmar la relación
# entre el desplazamiento circular y el cambio de fase.


# ==========================================================
# 6. COMPARACIÓN DE SEÑALES DE DISTINTA FRECUENCIA
# ==========================================================

# El escalamiento temporal permite estudiar cómo cambia el
# espectro cuando una señal se comprime o se expande en el tiempo.
#
# En esta sección se comparan dos senoidales: una de 10 Hz y otra
# de 20 Hz. La segunda completa el doble de ciclos por segundo.

senoidal_10 = np.sin(2 * np.pi * 10 * t)
senoidal_20 = np.sin(2 * np.pi * 20 * t)

# Crear una figura con dos gráficas: tiempo y frecuencia.
fig, ax = plt.subplots(2, 1, figsize=(10, 7))

# Comparación en el dominio del tiempo.
# Se limita el intervalo mostrado para distinguir los ciclos.
ax[0].plot(t, senoidal_10, label="Senoidal de 10 Hz")
ax[0].plot(t, senoidal_20, label="Senoidal de 20 Hz", alpha=0.7)

ax[0].set_xlim(0, 0.3)
ax[0].set_title("Comparación en el dominio del tiempo")
ax[0].set_xlabel("Tiempo (s)")
ax[0].set_ylabel("Amplitud")
ax[0].legend()
ax[0].grid(True)

# Calcular el eje de frecuencias centrado.
f = np.fft.fftshift(np.fft.fftfreq(N, d=dt))

# Calcular y graficar el espectro de magnitud de ambas señales.
for senal, etiqueta in [
    (senoidal_10, "10 Hz"),
    (senoidal_20, "20 Hz")
]:
    X = np.fft.fft(senal) / N
    X = np.fft.fftshift(X)

    ax[1].plot(f, np.abs(X), label=etiqueta)

# Mostrar el intervalo de frecuencias de interés.
ax[1].set_xlim(-40, 40)
ax[1].set_title("Comparación de los espectros de magnitud")
ax[1].set_xlabel("Frecuencia (Hz)")
ax[1].set_ylabel("Magnitud normalizada")
ax[1].legend()
ax[1].grid(True)

# Ajustar y guardar la figura comparativa.
fig.tight_layout()
fig.savefig(carpeta / "comparacion_frecuencias.png", dpi=150)

plt.show()


# ==========================================================
# 7. FINALIZACIÓN DEL ANÁLISIS
# ==========================================================

print("\nANÁLISIS FINALIZADO")
print("Se analizaron tres señales elementales.")
print("Se calcularon sus espectros de magnitud y fase.")
print("Se comprobaron las propiedades de linealidad y")
print("desplazamiento circular de las muestras.")
print("También se compararon señales senoidales de 10 Hz y 20 Hz.")
print(f"Las gráficas se guardaron en la carpeta: {carpeta}")