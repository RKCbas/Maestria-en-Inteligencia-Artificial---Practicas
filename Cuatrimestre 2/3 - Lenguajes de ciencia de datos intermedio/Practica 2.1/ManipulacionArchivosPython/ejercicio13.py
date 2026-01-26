import os
import csv

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "censuspopdata.csv")
archivo_salida = "estadisticas_condados.csv"

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        print("Procesando datos del censo...")
        print("-" * 60)
        
        # Diccionario para almacenar estadísticas por condado
        # Estructura: {condado: {'sectores': contador, 'poblacion': total}}
        estadisticas_condados = {}
        
        # Leer el archivo CSV
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            # Mostrar las columnas disponibles (para verificar)
            columnas = lector.fieldnames
            print("Columnas detectadas en el archivo:")
            print(f"  {', '.join(columnas)}")
            print("-" * 60)
            
            # Procesar cada fila (sector censal)
            total_filas = 0
            for fila in lector:
                total_filas += 1
                
                # Extraer información del condado y población
                condado = fila['County'].strip()
                estado = fila['State'].strip()
                
                try:
                    poblacion = int(fila['POP2010'].strip())
                except ValueError:
                    poblacion = 0
                
                # Usar combinación de Estado y Condado como clave única
                clave_condado = f"{condado}, {estado}"
                
                if clave_condado:
                    # Si el condado no existe en el diccionario, inicializarlo
                    if condado not in estadisticas_condados:
                        estadisticas_condados[condado] = {
                            'sectores': 0,
                            'poblacion': 0
                        }
                    
                    # Incrementar contador de sectores y sumar población
                    estadisticas_condados[condado]['sectores'] += 1
                    estadisticas_condados[condado]['poblacion'] += poblacion
        
        print(f"✓ Datos leídos: {total_filas} sectores censales")
        print(f"✓ Condados encontrados: {len(estadisticas_condados)}")
        print("-" * 60)
        
        # Escribir resultados en el archivo CSV de salida
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
            campos = ['condado', 'numero_sectores', 'poblacion_total']
            escritor = csv.DictWriter(f, fieldnames=campos)
            
            # Escribir encabezado
            escritor.writeheader()
            
            # Escribir datos de cada condado (ordenados alfabéticamente)
            for condado in sorted(estadisticas_condados.keys()):
                escritor.writerow({
                    'condado': condado,
                    'numero_sectores': estadisticas_condados[condado]['sectores'],
                    'poblacion_total': estadisticas_condados[condado]['poblacion']
                })
        
        print(f"✓ Resultados escritos en '{archivo_salida}'")
        print("\nPrimeros 10 condados (muestra):")
        print("-" * 60)
        print(f"{'Condado':<30} {'Sectores':<12} {'Población':<15}")
        print("-" * 60)
        
        # Mostrar los primeros 10 condados como muestra
        for i, condado in enumerate(sorted(estadisticas_condados.keys())[:10]):
            sectores = estadisticas_condados[condado]['sectores']
            poblacion = estadisticas_condados[condado]['poblacion']
            print(f"{condado:<30} {sectores:<12} {poblacion:>14,}")
        
        if len(estadisticas_condados) > 10:
            print(f"... y {len(estadisticas_condados) - 10} condados más")
        
        # Calcular y mostrar totales generales
        total_sectores = sum(e['sectores'] for e in estadisticas_condados.values())
        total_poblacion = sum(e['poblacion'] for e in estadisticas_condados.values())
        
        print("-" * 60)
        print(f"{'TOTALES':<30} {total_sectores:<12} {total_poblacion:>14,}")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()