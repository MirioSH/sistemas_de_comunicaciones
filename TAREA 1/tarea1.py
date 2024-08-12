import sounddevice as sd
import wavio
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de grabación
duracion = 4  # segundos
frecuencia_muestreo = 44100  # Hz

def grabar_voz(nombre_archivo, duracion=4):
    print(f"Grabando {nombre_archivo}...")
    audio = sd.rec(int(duracion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1, dtype='float64')
    sd.wait()  # Espera hasta que termine la grabación
    print(f"Grabación completada: {nombre_archivo}")
    wavio.write(nombre_archivo, audio, frecuencia_muestreo, sampwidth=2)
    return audio

# Grabar las voces de tres personas con pausa entre cada grabación
audio1 = grabar_voz("persona1.wav")
input("Presiona Enter para comenzar la siguiente grabación...")
audio2 = grabar_voz("persona2.wav")
input("Presiona Enter para comenzar la siguiente grabación...")
audio3 = grabar_voz("persona3.wav")

# Función para graficar en el dominio del tiempo y de la frecuencia
def graficar_audio(audio, frecuencia_muestreo, titulo):
    tiempo = np.linspace(0, len(audio) / frecuencia_muestreo, num=len(audio))
    
    plt.figure(figsize=(12, 6))
    
    # Dominio del tiempo
    plt.subplot(2, 1, 1)
    plt.plot(tiempo, audio)
    plt.title(f"{titulo} - Dominio del Tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    
    # Transformada de Fourier
    frecuencia = np.fft.fftfreq(len(audio), 1 / frecuencia_muestreo)
    transformada = np.fft.fft(audio)
    
    # Dominio de la frecuencia
    plt.subplot(2, 1, 2)
    plt.plot(frecuencia, np.abs(transformada))
    plt.title(f"{titulo} - Dominio de la Frecuencia")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    
    plt.tight_layout()
    plt.show()

# Graficar las tres grabaciones individualmente
graficar_audio(audio1, frecuencia_muestreo, "Persona 1")
graficar_audio(audio2, frecuencia_muestreo, "Persona 2")
graficar_audio(audio3, frecuencia_muestreo, "Persona 3")

# Función para comparar las tres grabaciones en una sola gráfica
def comparar_audios(audio1, audio2, audio3, frecuencia_muestreo):
    tiempo = np.linspace(0, len(audio1) / frecuencia_muestreo, num=len(audio1))

    plt.figure(figsize=(12, 6))
    
    # Comparación en el dominio del tiempo
    plt.subplot(2, 1, 1)
    plt.plot(tiempo, audio1, label='Persona 1')
    plt.plot(tiempo, audio2, label='Persona 2')
    plt.plot(tiempo, audio3, label='Persona 3')
    plt.title("Comparación en el Dominio del Tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend()

    # Transformada de Fourier para cada audio
    frecuencia = np.fft.fftfreq(len(audio1), 1 / frecuencia_muestreo)
    transformada1 = np.fft.fft(audio1)
    transformada2 = np.fft.fft(audio2)
    transformada3 = np.fft.fft(audio3)

    # Comparación en el dominio de la frecuencia
    plt.subplot(2, 1, 2)
    plt.plot(frecuencia, np.abs(transformada1), label='Persona 1')
    plt.plot(frecuencia, np.abs(transformada2), label='Persona 2')
    plt.plot(frecuencia, np.abs(transformada3), label='Persona 3')
    plt.title("Comparación en el Dominio de la Frecuencia")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Comparar las tres grabaciones en una sola gráfica
comparar_audios(audio1, audio2, audio3, frecuencia_muestreo)
