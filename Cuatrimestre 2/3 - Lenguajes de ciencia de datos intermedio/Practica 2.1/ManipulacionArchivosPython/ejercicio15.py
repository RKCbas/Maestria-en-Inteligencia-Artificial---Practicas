import os
import csv

# Rutas de los archivos
carpeta_datos = "Datos_para_la_actividad"
archivo_entrada = os.path.join(carpeta_datos, "TitanicSurvival.csv")
archivo_salida = "analisis_supervivencia_titanic.txt"

# Verificar que el archivo de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"✗ Error: El archivo '{archivo_entrada}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
else:
    try:
        print("Analizando datos de supervivencia del Titanic...")
        print("-" * 60)
        
        # Diccionario para almacenar estadísticas por clase
        # Estructura: {clase: {'total': n, 'sobrevivientes': n}}
        estadisticas_clase = {}
        
        # Leer el archivo CSV
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            # Procesar cada pasajero
            total_pasajeros = 0
            for fila in lector:
                total_pasajeros += 1
                
                # Extraer información
                clase = fila['passengerClass'].strip()
                supervivencia = fila['survived'].strip().lower()
                
                # Inicializar clase si no existe
                if clase not in estadisticas_clase:
                    estadisticas_clase[clase] = {
                        'total': 0,
                        'sobrevivientes': 0
                    }
                
                # Incrementar contador total
                estadisticas_clase[clase]['total'] += 1
                
                # Incrementar contador de sobrevivientes
                if supervivencia == 'yes':
                    estadisticas_clase[clase]['sobrevivientes'] += 1
        
        print(f"✓ Datos leídos: {total_pasajeros} pasajeros")
        print(f"✓ Clases encontradas: {len(estadisticas_clase)}")
        print("-" * 60)
        
        # Calcular porcentajes y preparar resultados
        resultados = []
        for clase in sorted(estadisticas_clase.keys()):
            total = estadisticas_clase[clase]['total']
            sobrevivientes = estadisticas_clase[clase]['sobrevivientes']
            fallecidos = total - sobrevivientes
            porcentaje_supervivencia = (sobrevivientes / total * 100) if total > 0 else 0
            porcentaje_fallecidos = (fallecidos / total * 100) if total > 0 else 0
            
            resultados.append({
                'clase': clase,
                'total': total,
                'sobrevivientes': sobrevivientes,
                'fallecidos': fallecidos,
                'porcentaje_supervivencia': porcentaje_supervivencia,
                'porcentaje_fallecidos': porcentaje_fallecidos
            })
        
        # Escribir resultados en archivo TXT
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ANÁLISIS DE SUPERVIVENCIA DEL TITANIC POR CLASE DE PASAJERO\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Total de pasajeros analizados: {total_pasajeros}\n")
            f.write("Fecha del análisis: (generado automáticamente)\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("ESTADÍSTICAS POR CLASE\n")
            f.write("-" * 70 + "\n\n")
            
            for resultado in resultados:
                f.write(f"Clase: {resultado['clase']}\n")
                f.write(f"  Total de pasajeros:      {resultado['total']:>6}\n")
                f.write(f"  Sobrevivientes:          {resultado['sobrevivientes']:>6}  ({resultado['porcentaje_supervivencia']:>5.2f}%)\n")
                f.write(f"  Fallecidos:              {resultado['fallecidos']:>6}  ({resultado['porcentaje_fallecidos']:>5.2f}%)\n")
                f.write("\n")
            
            # Calcular totales generales
            total_general = sum(r['total'] for r in resultados)
            sobrevivientes_general = sum(r['sobrevivientes'] for r in resultados)
            fallecidos_general = sum(r['fallecidos'] for r in resultados)
            porcentaje_general = (sobrevivientes_general / total_general * 100) if total_general > 0 else 0
            
            f.write("-" * 70 + "\n")
            f.write("TOTALES GENERALES\n")
            f.write("-" * 70 + "\n")
            f.write(f"  Total de pasajeros:      {total_general:>6}\n")
            f.write(f"  Sobrevivientes:          {sobrevivientes_general:>6}  ({porcentaje_general:>5.2f}%)\n")
            f.write(f"  Fallecidos:              {fallecidos_general:>6}  ({100-porcentaje_general:>5.2f}%)\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("CONCLUSIONES\n")
            f.write("=" * 70 + "\n\n")
            
            # Identificar la clase con mayor supervivencia
            clase_mayor_supervivencia = max(resultados, key=lambda x: x['porcentaje_supervivencia'])
            clase_menor_supervivencia = min(resultados, key=lambda x: x['porcentaje_supervivencia'])
            
            f.write(f"- La clase con mayor tasa de supervivencia fue: {clase_mayor_supervivencia['clase']}\n")
            f.write(f"  ({clase_mayor_supervivencia['porcentaje_supervivencia']:.2f}%)\n\n")
            f.write(f"- La clase con menor tasa de supervivencia fue: {clase_menor_supervivencia['clase']}\n")
            f.write(f"  ({clase_menor_supervivencia['porcentaje_supervivencia']:.2f}%)\n\n")
            
            f.write("=" * 70 + "\n")
        
        print(f"✓ Archivo de análisis creado: '{archivo_salida}'")
        print("\nRESUMEN DE RESULTADOS:")
        print("-" * 60)
        
        # Mostrar resultados en consola
        for resultado in resultados:
            print(f"\n{resultado['clase']}:")
            print(f"  Total: {resultado['total']} pasajeros")
            print(f"  Sobrevivientes: {resultado['sobrevivientes']} ({resultado['porcentaje_supervivencia']:.2f}%)")
            print(f"  Fallecidos: {resultado['fallecidos']} ({resultado['porcentaje_fallecidos']:.2f}%)")
        
        print("\n" + "=" * 60)
        print(f"Tasa general de supervivencia: {porcentaje_general:.2f}%")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()