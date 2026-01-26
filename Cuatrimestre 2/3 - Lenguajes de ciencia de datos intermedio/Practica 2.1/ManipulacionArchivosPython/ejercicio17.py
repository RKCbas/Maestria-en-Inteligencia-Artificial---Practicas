import os
import csv

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "produceSales.csv")
archivo_salida = "produceSales_with_totals.csv"

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        print("Calculando ingresos totales por producto...")
        print("-" * 70)
        
        # Listas para almacenar los datos
        productos_con_totales = []
        total_productos = 0
        
        # Leer el archivo CSV
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            # Procesar cada producto
            for fila in lector:
                total_productos += 1
                
                # Extraer información
                producto = fila['PRODUCE'].strip()
                
                try:
                    costo_por_libra = float(fila['COST PER POUND'].strip())
                except ValueError:
                    costo_por_libra = 0.0
                
                try:
                    libras_vendidas = float(fila['POUNDS SOLD'].strip())
                except ValueError:
                    libras_vendidas = 0.0
                
                # Calcular ingreso total
                ingreso_total = costo_por_libra * libras_vendidas
                
                # Agregar a la lista con la nueva columna
                productos_con_totales.append({
                    'PRODUCE': producto,
                    'COST PER POUND': costo_por_libra,
                    'POUNDS SOLD': libras_vendidas,
                    'TOTAL REVENUE': round(ingreso_total, 2)
                })
        
        print(f"✓ Productos procesados: {total_productos}")
        print("-" * 70)
        
        # Escribir archivo de salida con la columna adicional
        if productos_con_totales:
            # Definir los encabezados incluyendo la nueva columna
            encabezados = ['PRODUCE', 'COST PER POUND', 'POUNDS SOLD', 'TOTAL REVENUE']
            
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(productos_con_totales)
            
            print(f"✓ Archivo creado: '{archivo_salida}'")
            print("  Nueva columna agregada: 'TOTAL REVENUE'")
            print("-" * 70)
            
            # Calcular estadísticas
            ingresos_totales = sum(p['TOTAL REVENUE'] for p in productos_con_totales)
            promedio_ingresos = ingresos_totales / len(productos_con_totales)
            producto_mayor_ingreso = max(productos_con_totales, key=lambda x: x['TOTAL REVENUE'])
            producto_menor_ingreso = min(productos_con_totales, key=lambda x: x['TOTAL REVENUE'])
            
            print("\nESTADÍSTICAS DE INGRESOS:")
            print("-" * 70)
            print(f"  Ingresos totales: ${ingresos_totales:,.2f}")
            print(f"  Promedio por producto: ${promedio_ingresos:,.2f}")
            print(f"  Mayor ingreso: ${producto_mayor_ingreso['TOTAL REVENUE']:,.2f} ({producto_mayor_ingreso['PRODUCE']})")
            print(f"  Menor ingreso: ${producto_menor_ingreso['TOTAL REVENUE']:,.2f} ({producto_menor_ingreso['PRODUCE']})")
            
            # Mostrar todos los productos con sus ingresos
            print("\nDETALLE DE PRODUCTOS CON INGRESOS:")
            print("-" * 70)
            print(f"{'Producto':<20} {'Costo/lb':<12} {'Libras':<12} {'Ingreso Total':<15}")
            print("-" * 70)
            
            for producto in productos_con_totales:
                print(f"{producto['PRODUCE']:<20} "
                      f"${producto['COST PER POUND']:<11.2f} "
                      f"{producto['POUNDS SOLD']:<12.1f} "
                      f"${producto['TOTAL REVENUE']:>13.2f}")
            
            print("-" * 70)
            print(f"{'TOTAL':<20} {'':<12} {'':<12} ${ingresos_totales:>13.2f}")
            print("=" * 70)
        else:
            print("⚠ No se encontraron productos en el archivo")
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()