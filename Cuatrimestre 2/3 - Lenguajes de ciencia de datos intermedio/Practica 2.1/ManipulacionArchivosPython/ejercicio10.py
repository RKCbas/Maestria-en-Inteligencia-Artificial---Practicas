import os

# Nombre del archivo a leer
archivo = "archivo1.txt"

# Verificar si el archivo existe
if os.path.exists(archivo):
    try:
        # Abrir y leer el archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            num_caracteres = len(contenido)
        
        print(f"✓ Archivo leído exitosamente: '{archivo}'")
        print(f"  Número de caracteres: {num_caracteres}")
        
        # Información adicional
        # Contar caracteres sin espacios
        caracteres_sin_espacios = len(contenido.replace(' ', '').replace('\n', '').replace('\t', ''))
        print(f"  Caracteres (sin espacios): {caracteres_sin_espacios}")
        
        tamaño = os.path.getsize(archivo)
        print(f"  Tamaño del archivo: {tamaño} bytes")
        
    except Exception as e:
        print(f"✗ Error al leer el archivo: {e}")
else:
    print(f"✗ Error: El archivo '{archivo}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")