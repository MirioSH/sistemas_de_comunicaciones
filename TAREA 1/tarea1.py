import sounddevice as sd
import wavio
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de grabación
duracion = 4  # segundos
frecuencia_muestreo = 44100  # Hz

def grabar_voz(nombre_archivo, duracion=4):

    try:
        print(f"Grabando {nombre_archivo}...")
        audio = sd.rec(int(duracion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1, dtype='float64')
        sd.wait()  # Espera hasta que termine la grabación
        print(f"Grabación completada: {nombre_archivo}")
        wavio.write(nombre_archivo, audio, frecuencia_muestreo, sampwidth=2)
        return audio
    except Exception as e:
        print(f"Error durante la grabación: {e}")
        return None

def graficar_audio(audio_data, frecuencia_muestreo, titulo, labels=None):
  
    plt.figure(figsize=(12, 6))
    
    # Graficar en el dominio del tiempo
    plt.subplot(2, 1, 1)
    for i, audio in enumerate(audio_data):
        tiempo = np.linspace(0, len(audio) / frecuencia_muestreo, num=len(audio))
        label = labels[i] if labels else f'Audio {i+1}'
        plt.plot(tiempo, audio, label=label)
    plt.title(f"{titulo} - Dominio del Tiempo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    if labels:
        plt.legend()

    # Graficar en el dominio de la frecuencia
    plt.subplot(2, 1, 2)
    for i, audio in enumerate(audio_data):
        frecuencia = np.fft.fftfreq(len(audio), 1 / frecuencia_muestreo)
        transformada = np.abs(np.fft.fft(audio))
        label = labels[i] if labels else f'Audio {i+1}'
        plt.plot(frecuencia, transformada, label=label)
    plt.title(f"{titulo} - Dominio de la Frecuencia")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    if labels:
        plt.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    # Almacenar grabaciones en una lista
    nombres_archivos = ["persona1.wav", "persona2.wav", "persona3.wav"]
    audios = []
    
    for nombre_archivo in nombres_archivos:
        audio = grabar_voz(nombre_archivo, duracion)
        if audio is not None:
            audios.append(audio)
            input("Presiona Enter para comenzar la siguiente grabación...")
        else:
            print(f"No se pudo grabar el archivo {nombre_archivo}. Saltando...")

    if len(audios) > 0:
        # Graficar cada grabación individualmente
        for i, audio in enumerate(audios):
            graficar_audio([audio], frecuencia_muestreo, f"Persona {i+1}")

        # Comparar las grabaciones en una sola gráfica
        graficar_audio(audios, frecuencia_muestreo, "Comparación de Grabaciones", labels=[f'Persona {i+1}' for i in range(len(audios))])

if __name__ == "__main__":
    main()
