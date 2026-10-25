Este proyecto tiene como objetivo analizar diferentes señales utilizando Python y la Transformada Rápida de Fourier (FFT), para observar su representación en el dominio del tiempo y en el dominio de la frecuencia.

Se estudian tres señales básicas: el pulso rectangular, la función escalón y la señal senoidal. También se comparan señales senoidales de 10 Hz y 20 Hz para identificar las diferencias en sus frecuencias.

## Objetivos

- Representar señales en el dominio del tiempo.
- Aplicar la Transformada Rápida de Fourier (FFT).
- Obtener las gráficas de magnitud y fase del espectro de Fourier.
- Comprobar las propiedades de linealidad y desplazamiento temporal.
- Comparar señales de distintas frecuencias.

## Herramientas utilizadas

- **Python:** lenguaje de programación utilizado para desarrollar la simulación.
- **NumPy:** biblioteca utilizada para generar las señales y calcular la FFT.
- **Matplotlib:** biblioteca utilizada para generar las gráficas.
- **Visual Studio Code:** editor utilizado para desarrollar y ejecutar el código.

## Señales analizadas

1. **Pulso rectangular:** señal con amplitud de 1 entre −0.2 y 0.2 segundos y amplitud de 0 fuera de ese intervalo.
2. **Función escalón:** señal que cambia de 0 a 1 en el instante \(t=0\).
3. **Señal senoidal:** onda de amplitud 1 y frecuencia de 10 Hz.
4. **Comparación de frecuencias:** análisis de dos señales senoidales de 10 Hz y 20 Hz.

## Resultados

El programa genera gráficas de las señales en el dominio del tiempo y sus respectivos espectros de magnitud y fase. Además, realiza pruebas de linealidad y desplazamiento temporal, y compara los espectros de dos señales senoidales de diferentes frecuencias.

Las gráficas generadas se guardan automáticamente en la carpeta `resultados`.

## Requisitos

Para ejecutar el programa se necesita tener instalado Python y las bibliotecas NumPy y Matplotlib.

Instala las bibliotecas con el siguiente comando:

```bash
pip install numpy matplotlib
```

## Cómo ejecutar el proyecto

1. Descarga o clona este repositorio.
2. Abre la carpeta del proyecto en Visual Studio Code o en una terminal.
3. Instala las bibliotecas necesarias.
4. Ejecuta el archivo principal con el siguiente comando:

```bash
python main.py
```

5. Observa las gráficas generadas y revisa la carpeta `resultados`.

## Autor

Raúl Fernando Lares Palacio.

## Propósito académico

Proyecto desarrollado con fines educativos para comprender la representación de señales y la aplicación de la Transformada de Fourier mediante herramientas de programación.
