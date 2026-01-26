import os

# Nombre del archivo a leer
archivo = "archivo1.txt"

# Verificar si el archivo existe
if os.path.exists(archivo):
    try:
        # Abrir y leer el archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            # Dividir el contenido en palabras y contar
            palabras = contenido.split()
            num_palabras = len(palabras)
        
        print(f"✓ Archivo leído exitosamente: '{archivo}'")
        print(f"  Número de palabras: {num_palabras}")
        
        # Información adicional
        num_caracteres = len(contenido)
        tamaño = os.path.getsize(archivo)
        print(f"  Número de caracteres: {num_caracteres}")
        print(f"  Tamaño del archivo: {tamaño} bytes")
        
    except Exception as e:
        print(f"✗ Error al leer el archivo: {e}")
else:
    print(f"✗ Error: El archivo '{archivo}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")