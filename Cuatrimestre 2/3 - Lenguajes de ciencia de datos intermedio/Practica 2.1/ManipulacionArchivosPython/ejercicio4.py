import os

# Obtener el directorio actual
directorio_actual = os.getcwd()

print("Contenido del directorio actual:")
print(f"Ruta: {directorio_actual}")
print("-" * 50)

# Listar todos los archivos y directorios
contenido = os.listdir(directorio_actual)

if contenido:
    for elemento in contenido:
        # Verificar si es archivo o directorio
        ruta_completa = os.path.join(directorio_actual, elemento)
        if os.path.isdir(ruta_completa):
            print(f"📁 [DIR]  {elemento}")
        else:
            print(f"📄 [FILE] {elemento}")
    
    print("-" * 50)
    print(f"Total: {len(contenido)} elementos")
else:
    print("El directorio está vacío")