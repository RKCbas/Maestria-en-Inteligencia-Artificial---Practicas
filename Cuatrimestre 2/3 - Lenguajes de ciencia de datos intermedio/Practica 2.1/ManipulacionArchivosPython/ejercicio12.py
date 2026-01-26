import os
import random

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "banco_preguntas.txt")
archivo_salida = "examen.txt"

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        # Leer todas las preguntas del banco
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            preguntas = f.readlines()
        
        # Limpiar las preguntas (eliminar espacios en blanco al inicio/final)
        preguntas = [p.strip() for p in preguntas if p.strip()]
        
        # Verificar que hay suficientes preguntas
        if len(preguntas) < 5:
            print(f"✗ Error: El banco solo tiene {len(preguntas)} pregunta(s)")
            print("Se necesitan al menos 5 preguntas")
        else:
            # Seleccionar 5 preguntas al azar
            preguntas_seleccionadas = random.sample(preguntas, 5)
            
            # Escribir el examen
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("EXAMEN - 5 PREGUNTAS SELECCIONADAS ALEATORIAMENTE\n")
                f.write("=" * 60 + "\n\n")
                
                for i, pregunta in enumerate(preguntas_seleccionadas, 1):
                    f.write(f"{i}. {pregunta}\n\n")
            
            print("✓ Examen generado exitosamente")
            print(f"  Total de preguntas en el banco: {len(preguntas)}")
            print("  Preguntas seleccionadas: 5")
            print(f"  Archivo creado: '{archivo_salida}'")
            print("\nPreguntas del examen:")
            print("-" * 60)
            for i, pregunta in enumerate(preguntas_seleccionadas, 1):
                print(f"{i}. {pregunta}")
    
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")