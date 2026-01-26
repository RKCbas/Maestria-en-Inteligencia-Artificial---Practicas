import os
import csv

# Archivo de entrada y salida
archivo_entrada = "produceSales_with_totals.csv"
archivo_salida = "produceSales_updated.csv"

# Precios actualizados para productos específicos
PRECIOS_ACTUALIZADOS = {
    'Celery': 1.19,
    'Garlic': 3.07,
    'Lemon': 1.27
}

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
    print("\n💡 Sugerencia: Primero ejecuta el script anterior (problema 6)")
    print("   para generar el archivo 'produceSales_with_totals.csv'")
else:
    try:
        print("Actualizando precios de productos agrícolas...")
        print("=" * 70)
        
        # Listas para almacenar los datos
        productos_actualizados = []
        productos_modificados = []
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
                    costo_original = float(fila['COST PER POUND'].strip())
                except ValueError:
                    costo_original = 0.0
                
                try:
                    libras_vendidas = float(fila['POUNDS SOLD'].strip())
                except ValueError:
                    libras_vendidas = 0.0
                
                # Verificar si este producto necesita actualización
                if producto in PRECIOS_ACTUALIZADOS:
                    # Guardar información del cambio
                    nuevo_precio = PRECIOS_ACTUALIZADOS[producto]
                    ingreso_original = costo_original * libras_vendidas
                    nuevo_ingreso = nuevo_precio * libras_vendidas
                    
                    productos_modificados.append({
                        'producto': producto,
                        'precio_original': costo_original,
                        'precio_nuevo': nuevo_precio,
                        'libras': libras_vendidas,
                        'ingreso_original': ingreso_original,
                        'ingreso_nuevo': nuevo_ingreso,
                        'diferencia': nuevo_ingreso - ingreso_original
                    })
                    
                    # Usar el nuevo precio
                    costo_por_libra = nuevo_precio
                else:
                    # Mantener el precio original
                    costo_por_libra = costo_original
                
                # Recalcular ingreso total
                ingreso_total = costo_por_libra * libras_vendidas
                
                # Agregar a la lista
                productos_actualizados.append({
                    'PRODUCE': producto,
                    'COST PER POUND': round(costo_por_libra, 2),
                    'POUNDS SOLD': libras_vendidas,
                    'TOTAL REVENUE': round(ingreso_total, 2)
                })
        
        print(f"✓ Productos procesados: {total_productos}")
        print(f"✓ Productos actualizados: {len(productos_modificados)}")
        print("=" * 70)
        
        # Mostrar detalles de los productos modificados
        if productos_modificados:
            print("\nDETALLE DE PRODUCTOS ACTUALIZADOS:")
            print("-" * 70)
            
            for item in productos_modificados:
                print(f"\n{item['producto']}:")
                print(f"  Precio anterior:      ${item['precio_original']:.2f} por libra")
                print(f"  Precio nuevo:         ${item['precio_nuevo']:.2f} por libra")
                print(f"  Libras vendidas:      {item['libras']:.1f}")
                print(f"  Ingreso anterior:     ${item['ingreso_original']:.2f}")
                print(f"  Ingreso nuevo:        ${item['ingreso_nuevo']:.2f}")
                print(f"  Diferencia:           ${item['diferencia']:+.2f}")
            
            # Calcular impacto total
            diferencia_total = sum(p['diferencia'] for p in productos_modificados)
            print("\n" + "-" * 70)
            print(f"Impacto total en ingresos: ${diferencia_total:+,.2f}")
            print("-" * 70)
        
        # Escribir archivo actualizado
        if productos_actualizados:
            encabezados = ['PRODUCE', 'COST PER POUND', 'POUNDS SOLD', 'TOTAL REVENUE']
            
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(productos_actualizados)
            
            print(f"\n✓ Archivo actualizado creado: '{archivo_salida}'")
            
            # Calcular estadísticas finales
            ingresos_totales_nuevos = sum(p['TOTAL REVENUE'] for p in productos_actualizados)
            
            print("\nESTADÍSTICAS FINALES:")
            print("-" * 70)
            print(f"  Total de productos:    {len(productos_actualizados)}")
            print(f"  Ingresos totales:      ${ingresos_totales_nuevos:,.2f}")
            
            # Mostrar vista previa de productos actualizados
            print("\nVISTA PREVIA DE PRODUCTOS ACTUALIZADOS:")
            print("-" * 70)
            print(f"{'Producto':<20} {'Precio/lb':<15} {'Libras':<12} {'Ingreso':<15}")
            print("-" * 70)
            
            for producto in productos_actualizados:
                if producto['PRODUCE'] in PRECIOS_ACTUALIZADOS:
                    print(f"{producto['PRODUCE']:<20} "
                          f"${producto['COST PER POUND']:<14.2f} "
                          f"{producto['POUNDS SOLD']:<12.1f} "
                          f"${producto['TOTAL REVENUE']:>13.2f} ✓")
            
            print("=" * 70)
            print("✓ Proceso completado exitosamente")
        else:
            print("⚠ No se encontraron productos para actualizar")
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()