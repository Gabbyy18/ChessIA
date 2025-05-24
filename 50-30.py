def LLenar_Jarra(capacity, jug_name):
    print(f"{jug_name}: Llenar de capacidad {capacity} litros")
    return capacity

def Vaciar_Jarra(jug_name):
    print(f"{jug_name}: Vaciar")
    return 0

def pour(source_volume, source_name, target_volume, target_name, target_capacity):
    amount = min(source_volume, target_capacity - target_volume)
    print(f"Verter {amount} litros de {source_name} a {target_name}")
    source_volume -= amount
    target_volume += amount
    return source_volume, target_volume

def Jarra_problem(target, jarraA_Capacidad, jarraB_Capacidad):
    JarraA = 0
    JarraB = 0
    Movimientos = 0

    print(f"\nObjetivo: {target} litros\n")
    while Movimientos < 100:
        if JarraA == target or JarraB == target:
            print(f"\nObjetivo alcanzado en {Movimientos} movimientos")
            print(f"Estado final: Jarra A= Total de {JarraA} litros, Jarra B= Total de {JarraB} litros")
            return

        if JarraA == 0:
            JarraA = LLenar_Jarra(jarraA_Capacidad, "Jarra A")
            Movimientos += 1
        elif JarraB == jarraB_Capacidad:
            JarraB =Vaciar_Jarra("Jarra B")
            Movimientos += 1
        else:
            JarraA, JarraB = pour(JarraA, "Jarra A", JarraB, "Jarra B", jarraB_Capacidad)
            Movimientos += 1

    print(f"\nNo se pudo alcanzar el objetivo en 100 movimientos.")

while True:
    try:
        target_str = input("\n*Nota: tome en cuenta que el numero debe ser un múltiplo de 10 y menor o igual a 50) \nIngresa la cantidad de litros a alcanzar:  ")
        target = int(target_str)
        if target % 10 == 0 and 0 < target <= 50:
            break
        else:
            print("\nNo es posible alcanzar esa cantidad con las jarras disponibles.")
    except ValueError:
        print("Por favor, ingresa un número entero válido.")

jarraA_Capacidad = 50
jarraB_Capacidad = 30
Jarra_problem(target, jarraA_Capacidad, jarraB_Capacidad)