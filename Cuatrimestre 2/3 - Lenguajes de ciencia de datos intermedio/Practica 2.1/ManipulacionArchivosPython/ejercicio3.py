import os

# Nombre del directorio a crear
nombre_directorio = "mi_directorio"

# Verificar si el directorio ya existe
if not os.path.exists(nombre_directorio):
    # Crear el directorio
    os.mkdir(nombre_directorio)
    print(f"✓ Directorio creado exitosamente: '{nombre_directorio}'")
    print(f"Ubicación: {os.path.abspath(nombre_directorio)}")
else:
    print(f"✗ El directorio '{nombre_directorio}' ya existe")
    print(f"Ubicación: {os.path.abspath(nombre_directorio)}")