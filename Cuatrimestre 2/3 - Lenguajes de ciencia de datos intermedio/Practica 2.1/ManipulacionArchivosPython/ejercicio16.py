import os
import csv

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "supplier_data.csv")
archivo_salida = "filtered_supplier_data.csv"

# Umbral de productos (puedes cambiar este valor)
UMBRAL_PRODUCTOS = 100

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        print("Filtrando proveedores...")
        print("-" * 60)
        print(f"Criterio: Proveedores con más de {UMBRAL_PRODUCTOS} productos")
        print("-" * 60)
        
        # Listas para almacenar los datos
        proveedores_filtrados = []
        total_proveedores = 0
        
        # Leer el archivo CSV
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            # Guardar los encabezados
            encabezados = lector.fieldnames
            
            # Procesar cada proveedor
            for fila in lector:
                total_proveedores += 1
                
                # Extraer información
                supplier_id = fila['supplier_id'].strip()
                supplier_name = fila['supplier_name'].strip()
                
                try:
                    products_supplied = int(fila['products_supplied'].strip())
                except ValueError:
                    products_supplied = 0
                
                # Filtrar proveedores que cumplen el criterio
                if products_supplied > UMBRAL_PRODUCTOS:
                    proveedores_filtrados.append({
                        'supplier_id': supplier_id,
                        'supplier_name': supplier_name,
                        'products_supplied': products_supplied
                    })
        
        print(f"✓ Total de proveedores en el archivo: {total_proveedores}")
        print(f"✓ Proveedores que cumplen el criterio: {len(proveedores_filtrados)}")
        print(f"  ({len(proveedores_filtrados)/total_proveedores*100:.2f}% del total)")
        print("-" * 60)
        
        # Escribir archivo de salida con proveedores filtrados
        if proveedores_filtrados:
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(proveedores_filtrados)
            
            print(f"✓ Archivo creado: '{archivo_salida}'")
            print(f"  Registros escritos: {len(proveedores_filtrados)}")
            print("-" * 60)
            
            # Calcular estadísticas
            productos_totales = sum(p['products_supplied'] for p in proveedores_filtrados)
            promedio_productos = productos_totales / len(proveedores_filtrados)
            max_productos = max(proveedores_filtrados, key=lambda x: x['products_supplied'])
            min_productos = min(proveedores_filtrados, key=lambda x: x['products_supplied'])
            
            print("\nESTADÍSTICAS DE PROVEEDORES FILTRADOS:")
            print("-" * 60)
            print(f"  Total de productos suministrados: {productos_totales:,}")
            print(f"  Promedio por proveedor: {promedio_productos:.2f}")
            print(f"  Máximo: {max_productos['products_supplied']} ({max_productos['supplier_name']})")
            print(f"  Mínimo: {min_productos['products_supplied']} ({min_productos['supplier_name']})")
            
            # Mostrar los primeros 10 proveedores filtrados
            print("\nPRIMEROS 10 PROVEEDORES FILTRADOS:")
            print("-" * 60)
            print(f"{'ID':<8} {'Nombre':<30} {'Productos':<12}")
            print("-" * 60)
            
            for i, proveedor in enumerate(proveedores_filtrados[:10]):
                print(f"{proveedor['supplier_id']:<8} {proveedor['supplier_name']:<30} {proveedor['products_supplied']:>10,}")
            
            if len(proveedores_filtrados) > 10:
                print(f"... y {len(proveedores_filtrados) - 10} proveedores más")
            
            print("=" * 60)
        else:
            print(f"⚠ No se encontraron proveedores con más de {UMBRAL_PRODUCTOS} productos")
            print("No se creó el archivo de salida")
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()