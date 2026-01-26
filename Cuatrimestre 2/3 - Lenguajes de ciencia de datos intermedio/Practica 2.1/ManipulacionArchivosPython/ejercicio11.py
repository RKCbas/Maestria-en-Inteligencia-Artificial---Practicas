import os
import csv

# Definir las carpetas de entrada y salida
carpeta_entrada = "input_data"
carpeta_salida = "output_data"

# Crear las carpetas si no existen
if not os.path.exists(carpeta_entrada):
    os.mkdir(carpeta_entrada)
    print(f"✓ Carpeta creada: '{carpeta_entrada}'")
else:
    print(f"ℹ La carpeta '{carpeta_entrada}' ya existe")

if not os.path.exists(carpeta_salida):
    os.mkdir(carpeta_salida)
    print(f"✓ Carpeta creada: '{carpeta_salida}'")
else:
    print(f"ℹ La carpeta '{carpeta_salida}' ya existe")

print("-" * 60)

# Crear archivos CSV de ejemplo en input_data (solo si la carpeta está vacía)
archivos_ejemplo = os.listdir(carpeta_entrada)
if not archivos_ejemplo or all(not f.endswith('.csv') for f in archivos_ejemplo):
    print("Creando archivos CSV de ejemplo...")
    
    # Archivo 1: ventas_enero.csv
    datos_enero = [
        ['producto', 'precio', 'unidades_vendidas'],
        ['Laptop', '15000', '5'],
        ['Mouse', '250', '20'],
        ['Teclado', '800', '15'],
        ['Monitor', '3500', '8']
    ]
    
    with open(os.path.join(carpeta_entrada, 'ventas_enero.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(datos_enero)
    
    # Archivo 2: ventas_febrero.csv
    datos_febrero = [
        ['producto', 'precio', 'unidades_vendidas'],
        ['Laptop', '15000', '7'],
        ['Mouse', '250', '25'],
        ['Teclado', '800', '18'],
        ['Webcam', '1200', '10']
    ]
    
    with open(os.path.join(carpeta_entrada, 'ventas_febrero.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(datos_febrero)
    
    print("✓ Archivos de ejemplo creados")
    print("-" * 60)

# Procesar todos los archivos CSV en input_data
archivos_csv = [f for f in os.listdir(carpeta_entrada) if f.endswith('.csv')]

if not archivos_csv:
    print("✗ No se encontraron archivos CSV en la carpeta de entrada")
else:
    print(f"Procesando {len(archivos_csv)} archivo(s) CSV...")
    print("-" * 60)
    
    for archivo in archivos_csv:
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        nombre_salida = archivo.replace('.csv', '_procesado.csv')
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        
        print(f"\nProcesando: {archivo}")
        
        try:
            # Leer el archivo de entrada
            with open(ruta_entrada, 'r', encoding='utf-8') as f_entrada:
                lector = csv.DictReader(f_entrada)
                datos_procesados = []
                total_general = 0
                
                for fila in lector:
                    producto = fila['producto']
                    precio = float(fila['precio'])
                    unidades = int(fila['unidades_vendidas'])
                    total = precio * unidades
                    total_general += total
                    
                    datos_procesados.append({
                        'producto': producto,
                        'precio': precio,
                        'unidades_vendidas': unidades,
                        'total_venta': total
                    })
            
            # Escribir el archivo de salida
            with open(ruta_salida, 'w', newline='', encoding='utf-8') as f_salida:
                campos = ['producto', 'precio', 'unidades_vendidas', 'total_venta']
                escritor = csv.DictWriter(f_salida, fieldnames=campos)
                
                escritor.writeheader()
                escritor.writerows(datos_procesados)
                
                # Agregar fila de total
                escritor.writerow({
                    'producto': 'TOTAL',
                    'precio': '',
                    'unidades_vendidas': '',
                    'total_venta': total_general
                })
            
            print("  ✓ Procesado exitosamente")
            print(f"  → Total general: ${total_general:,.2f}")
            print(f"  → Guardado en: {ruta_salida}")
            
        except Exception as e:
            print(f"  ✗ Error al procesar {archivo}: {e}")
    
    print("\n" + "=" * 60)
    print("✓ Procesamiento completado")
    print(f"Archivos de salida guardados en: {os.path.abspath(carpeta_salida)}")