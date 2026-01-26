import os

# Nombre del archivo a leer
archivo = "archivo1.txt"

# Verificar si el archivo existe
if os.path.exists(archivo):
    try:
        # Abrir y leer el archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            num_lineas = len(lineas)
        
        print(f"✓ Archivo leído exitosamente: '{archivo}'")
        print(f"  Número de líneas: {num_lineas}")
        
        # Información adicional
        tamaño = os.path.getsize(archivo)
        print(f"  Tamaño del archivo: {tamaño} bytes")
        
    except Exception as e:
        print(f"✗ Error al leer el archivo: {e}")
else:
    print(f"✗ Error: El archivo '{archivo}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")