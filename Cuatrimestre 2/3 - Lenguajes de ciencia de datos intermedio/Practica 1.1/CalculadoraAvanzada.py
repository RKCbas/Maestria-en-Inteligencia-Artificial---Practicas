"""
Calculadora de Operaciones Matemáticas Avanzadas
================================================
Programa modular que implementa operaciones matemáticas básicas y avanzadas
siguiendo principios de programación estructurada.

Autor: Sistema de Desarrollo
Fecha: Enero 2026
"""

import math
import sys


# ============================================================================
# MÓDULO: OPERACIONES BÁSICAS
# ============================================================================

def add(num1, num2):
    """
    Suma dos números.
    
    Args:
        num1 (float): Primer número
        num2 (float): Segundo número
    
    Returns:
        float: Resultado de la suma
    """
    return num1 + num2


def subtract(num1, num2):
    """
    Resta dos números.
    
    Args:
        num1 (float): Número minuendo
        num2 (float): Número sustraendo
    
    Returns:
        float: Resultado de la resta
    """
    return num1 - num2


def multiply(num1, num2):
    """
    Multiplica dos números.
    
    Args:
        num1 (float): Primer factor
        num2 (float): Segundo factor
    
    Returns:
        float: Resultado de la multiplicación
    """
    return num1 * num2


def divide(num1, num2):
    """
    Divide dos números con validación de división por cero.
    
    Args:
        num1 (float): Número dividendo
        num2 (float): Número divisor
    
    Returns:
        float: Resultado de la división
        
    Raises:
        ValueError: Si el divisor es cero
    """
    if num2 == 0:
        raise ValueError("Error: No se puede dividir por cero")
    return num1 / num2


# ============================================================================
# MÓDULO: OPERACIONES AVANZADAS
# ============================================================================

def power(base, exponent):
    """
    Calcula la potencia de un número.
    
    Args:
        base (float): Número base
        exponent (float): Exponente
    
    Returns:
        float: Resultado de elevar la base al exponente
    """
    return base ** exponent


def square_root(number):
    """
    Calcula la raíz cuadrada de un número.
    
    Args:
        number (float): Número del cual calcular la raíz
    
    Returns:
        float: Raíz cuadrada del número
        
    Raises:
        ValueError: Si el número es negativo
    """
    if number < 0:
        raise ValueError("Error: No se puede calcular la raíz cuadrada de un número negativo")
    return math.sqrt(number)


def factorial(number):
    """
    Calcula el factorial de un número entero.
    
    Args:
        number (int): Número entero positivo
    
    Returns:
        int: Factorial del número
        
    Raises:
        ValueError: Si el número es negativo o no es entero
    """
    if number < 0:
        raise ValueError("Error: El factorial no está definido para números negativos")
    
    if not isinstance(number, int) and not number.is_integer():
        raise ValueError("Error: El factorial solo se calcula para números enteros")
    
    number = int(number)
    result = 1
    
    for i in range(1, number + 1):
        result *= i
    
    return result


def logarithm(number, base=10):
    """
    Calcula el logaritmo de un número en una base específica.
    
    Args:
        number (float): Número del cual calcular el logaritmo
        base (float): Base del logaritmo (por defecto 10)
    
    Returns:
        float: Logaritmo del número en la base especificada
        
    Raises:
        ValueError: Si el número o la base son inválidos
    """
    if number <= 0:
        raise ValueError("Error: El logaritmo solo está definido para números positivos")
    
    if base <= 0 or base == 1:
        raise ValueError("Error: La base del logaritmo debe ser positiva y diferente de 1")
    
    return math.log(number, base)


def sine(angle_degrees):
    """
    Calcula el seno de un ángulo en grados.
    
    Args:
        angle_degrees (float): Ángulo en grados
    
    Returns:
        float: Seno del ángulo
    """
    angle_radians = math.radians(angle_degrees)
    return math.sin(angle_radians)


def cosine(angle_degrees):
    """
    Calcula el coseno de un ángulo en grados.
    
    Args:
        angle_degrees (float): Ángulo en grados
    
    Returns:
        float: Coseno del ángulo
    """
    angle_radians = math.radians(angle_degrees)
    return math.cos(angle_radians)


def tangent(angle_degrees):
    """
    Calcula la tangente de un ángulo en grados.
    
    Args:
        angle_degrees (float): Ángulo en grados
    
    Returns:
        float: Tangente del ángulo
        
    Raises:
        ValueError: Si el ángulo es 90° + k*180° donde la tangente no está definida
    """
    angle_radians = math.radians(angle_degrees)
    
    # Validar ángulos donde tangente no está definida
    if abs(math.cos(angle_radians)) < 1e-10:
        raise ValueError("Error: La tangente no está definida para este ángulo")
    
    return math.tan(angle_radians)


# ============================================================================
# MÓDULO: VALIDACIÓN DE ENTRADA
# ============================================================================

def validate_numeric_input(prompt_message):
    """
    Solicita y valida la entrada numérica del usuario.
    
    Args:
        prompt_message (str): Mensaje para solicitar la entrada
    
    Returns:
        float: Número válido ingresado por el usuario
    """
    while True:
        try:
            user_input = input(prompt_message)
            number = float(user_input)
            return number
        except ValueError:
            print("Error: Por favor ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            sys.exit(0)


def validate_integer_input(prompt_message):
    """
    Solicita y valida la entrada de un número entero.
    
    Args:
        prompt_message (str): Mensaje para solicitar la entrada
    
    Returns:
        int: Número entero válido ingresado por el usuario
    """
    while True:
        try:
            user_input = input(prompt_message)
            number = int(user_input)
            return number
        except ValueError:
            print("Error: Por favor ingresa un número entero válido.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            sys.exit(0)


def validate_menu_option(min_option, max_option):
    """
    Valida que la opción del menú esté en el rango permitido.
    
    Args:
        min_option (int): Opción mínima válida
        max_option (int): Opción máxima válida
    
    Returns:
        int: Opción válida seleccionada por el usuario
    """
    while True:
        option = validate_integer_input("Selecciona una opción: ")
        
        if min_option <= option <= max_option:
            return option
        else:
            print(f"Error: Por favor selecciona una opción entre {min_option} y {max_option}.")


# ============================================================================
# MÓDULO: INTERFAZ DE USUARIO
# ============================================================================

def display_main_menu():
    """
    Muestra el menú principal de la calculadora.
    """
    print("\n" + "="*60)
    print(" CALCULADORA DE OPERACIONES MATEMÁTICAS AVANZADAS")
    print("="*60)
    print("\n--- OPERACIONES BÁSICAS ---")
    print("1.  Suma")
    print("2.  Resta")
    print("3.  Multiplicación")
    print("4.  División")
    print("\n--- OPERACIONES AVANZADAS ---")
    print("5.  Potencia")
    print("6.  Raíz cuadrada")
    print("7.  Factorial")
    print("8.  Logaritmo")
    print("\n--- FUNCIONES TRIGONOMÉTRICAS ---")
    print("9.  Seno")
    print("10. Coseno")
    print("11. Tangente")
    print("\n--- OPCIONES ---")
    print("12. Salir")
    print("="*60)


def display_result(operation_name, result):
    """
    Muestra el resultado de una operación de forma formateada.
    
    Args:
        operation_name (str): Nombre de la operación realizada
        result (float): Resultado de la operación
    """
    print("\n" + "-"*60)
    print(f"Resultado de {operation_name}: {result}")
    print("-"*60)


def display_error(error_message):
    """
    Muestra un mensaje de error de forma formateada.
    
    Args:
        error_message (str): Mensaje de error a mostrar
    """
    print("\n" + "!"*60)
    print(f"ERROR: {error_message}")
    print("!"*60)


# ============================================================================
# MÓDULO: PROCESAMIENTO DE OPERACIONES
# ============================================================================

def process_basic_operation(operation_type):
    """
    Procesa operaciones básicas (suma, resta, multiplicación, división).
    
    Args:
        operation_type (int): Tipo de operación (1-4)
    """
    num1 = validate_numeric_input("Ingresa el primer número: ")
    num2 = validate_numeric_input("Ingresa el segundo número: ")
    
    try:
        if operation_type == 1:
            result = add(num1, num2)
            display_result("SUMA", result)
        elif operation_type == 2:
            result = subtract(num1, num2)
            display_result("RESTA", result)
        elif operation_type == 3:
            result = multiply(num1, num2)
            display_result("MULTIPLICACIÓN", result)
        elif operation_type == 4:
            result = divide(num1, num2)
            display_result("DIVISIÓN", result)
    except ValueError as e:
        display_error(str(e))


def process_power_operation():
    """
    Procesa la operación de potencia.
    """
    base = validate_numeric_input("Ingresa la base: ")
    exponent = validate_numeric_input("Ingresa el exponente: ")
    
    result = power(base, exponent)
    display_result("POTENCIA", result)


def process_square_root_operation():
    """
    Procesa la operación de raíz cuadrada.
    """
    number = validate_numeric_input("Ingresa el número: ")
    
    try:
        result = square_root(number)
        display_result("RAÍZ CUADRADA", result)
    except ValueError as e:
        display_error(str(e))


def process_factorial_operation():
    """
    Procesa la operación de factorial.
    """
    number = validate_numeric_input("Ingresa el número: ")
    
    try:
        result = factorial(number)
        display_result("FACTORIAL", result)
    except ValueError as e:
        display_error(str(e))


def process_logarithm_operation():
    """
    Procesa la operación de logaritmo.
    """
    number = validate_numeric_input("Ingresa el número: ")
    base = validate_numeric_input("Ingresa la base del logaritmo (enter para base 10): ")
    
    if base == 0:
        base = 10
    
    try:
        result = logarithm(number, base)
        display_result(f"LOGARITMO base {base}", result)
    except ValueError as e:
        display_error(str(e))


def process_trigonometric_operation(trig_type):
    """
    Procesa operaciones trigonométricas (seno, coseno, tangente).
    
    Args:
        trig_type (int): Tipo de función trigonométrica (9-11)
    """
    angle = validate_numeric_input("Ingresa el ángulo en grados: ")
    
    try:
        if trig_type == 9:
            result = sine(angle)
            display_result("SENO", result)
        elif trig_type == 10:
            result = cosine(angle)
            display_result("COSENO", result)
        elif trig_type == 11:
            result = tangent(angle)
            display_result("TANGENTE", result)
    except ValueError as e:
        display_error(str(e))


# ============================================================================
# MÓDULO: PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta el bucle principal de la calculadora.
    Controla el flujo del programa y la selección de operaciones.
    """
    print("\n¡Bienvenido a la Calculadora de Operaciones Matemáticas Avanzadas!")
    
    # Bucle principal del programa
    while True:
        display_main_menu()
        option = validate_menu_option(1, 12)
        
        # Estructura de selección para procesar la opción elegida
        if option >= 1 and option <= 4:
            # Operaciones básicas
            process_basic_operation(option)
        
        elif option == 5:
            # Potencia
            process_power_operation()
        
        elif option == 6:
            # Raíz cuadrada
            process_square_root_operation()
        
        elif option == 7:
            # Factorial
            process_factorial_operation()
        
        elif option == 8:
            # Logaritmo
            process_logarithm_operation()
        
        elif option >= 9 and option <= 11:
            # Funciones trigonométricas
            process_trigonometric_operation(option)
        
        elif option == 12:
            # Salir del programa
            print("\n" + "="*60)
            print("Gracias por usar la calculadora. ¡Hasta pronto!")
            print("="*60 + "\n")
            break
        
        # Pausa antes de mostrar el menú nuevamente
        input("\nPresiona ENTER para continuar...")


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada del programa.
    Se ejecuta solo cuando el archivo se ejecuta directamente.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        print("¡Hasta pronto!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError inesperado: {e}")
        print("Por favor, contacta al desarrollador.\n")
        sys.exit(1)