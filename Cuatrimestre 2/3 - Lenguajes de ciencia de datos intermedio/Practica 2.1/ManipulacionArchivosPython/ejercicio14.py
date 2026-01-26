import os
import csv

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "winequality-both.csv")
archivo_vino_blanco = "winequality-white.csv"
archivo_vino_tinto = "winequality-red.csv"

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        print("Procesando archivo de vinos...")
        print("-" * 60)
        
        # Contadores
        contador_blanco = 0
        contador_tinto = 0
        
        # Listas para almacenar los datos
        datos_blancos = []
        datos_tintos = []
        encabezados = None
        
        # Leer el archivo CSV
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            # Guardar los encabezados
            encabezados = lector.fieldnames
            print(f"Columnas detectadas: {len(encabezados)}")
            print(f"  {', '.join(encabezados[:5])}...")
            print("-" * 60)
            
            # Procesar cada fila
            for fila in lector:
                tipo_vino = fila['type'].strip().lower()
                
                if tipo_vino == 'white':
                    datos_blancos.append(fila)
                    contador_blanco += 1
                elif tipo_vino == 'red':
                    datos_tintos.append(fila)
                    contador_tinto += 1
        
        print("✓ Archivo leído completamente")
        print(f"  Vinos blancos encontrados: {contador_blanco}")
        print(f"  Vinos tintos encontrados: {contador_tinto}")
        print(f"  Total de registros: {contador_blanco + contador_tinto}")
        print("-" * 60)
        
        # Escribir archivo de vinos blancos
        if datos_blancos:
            with open(archivo_vino_blanco, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(datos_blancos)
            
            print(f"✓ Archivo '{archivo_vino_blanco}' creado")
            print(f"  Registros escritos: {contador_blanco}")
        else:
            print("⚠ No se encontraron vinos blancos")
        
        # Escribir archivo de vinos tintos
        if datos_tintos:
            with open(archivo_vino_tinto, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(datos_tintos)
            
            print(f"✓ Archivo '{archivo_vino_tinto}' creado")
            print(f"  Registros escritos: {contador_tinto}")
        else:
            print("⚠ No se encontraron vinos tintos")
        
        print("-" * 60)
        print("✓ Separación completada exitosamente")
        
        # Mostrar muestra de datos
        if datos_blancos:
            print("\nMuestra de vino blanco (primer registro):")
            print(f"  Acidez fija: {datos_blancos[0]['fixed acidity']}")
            print(f"  pH: {datos_blancos[0]['pH']}")
            print(f"  Alcohol: {datos_blancos[0]['alcohol']}%")
            print(f"  Calidad: {datos_blancos[0]['quality']}")
        
        if datos_tintos:
            print("\nMuestra de vino tinto (primer registro):")
            print(f"  Acidez fija: {datos_tintos[0]['fixed acidity']}")
            print(f"  pH: {datos_tintos[0]['pH']}")
            print(f"  Alcohol: {datos_tintos[0]['alcohol']}%")
            print(f"  Calidad: {datos_tintos[0]['quality']}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()