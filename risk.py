import itertools
from dataclasses import dataclass
from typing import List, Tuple, Dict
import numpy as np
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

@dataclass
class Territorio:
    nombre: str
    fuerza_defensa: int
    puntos_recompensa: int
    posicion: Tuple[int, int]  # Posición en el tablero
    tipo_terreno: str  # plano, montañoso, etc.

class TableroJuego:
    def __init__(self, tamanio: Tuple[int, int] = (5, 5)):
        self.tamanio = tamanio
        self.tablero = np.zeros(tamanio, dtype=int)  # 0: vacío, 1: territorio enemigo, 2: conquistado
        self.posiciones_territorio = {}

    def agregar_territorio(self, territorio: Territorio):
        x, y = territorio.posicion
        self.tablero[x, y] = 1
        self.posiciones_territorio[territorio.nombre] = (x, y)

    def marcar_conquistado(self, nombre_territorio: str):
        x, y = self.posiciones_territorio[nombre_territorio]
        self.tablero[x, y] = 2

    def mostrar(self):
        simbolos = {0: f'{Fore.WHITE}·', 1: f'{Fore.RED}E', 2: f'{Fore.GREEN}C'}
        print("\nTablero actual:")
        print("   " + " ".join(f"{i}" for i in range(self.tamanio[1])))
        for i, fila in enumerate(self.tablero):
            print(f"{i}  " + " ".join(simbolos[celda] for celda in fila))

class Ejercito:
    def __init__(self, infanteria: int = 0, caballeria: int = 0, artilleria: int = 0):
        self.infanteria = infanteria
        self.caballeria = caballeria
        self.artilleria = artilleria
    
    def obtener_costo_total(self) -> int:
        return (self.infanteria * 1 + 
                self.caballeria * 3 + 
                self.artilleria * 5)
    
    def obtener_poder_ataque(self, terreno: str = "plano") -> int:
        multiplicador = 1
        if terreno == "montañoso":
            multiplicador = 0.8
        elif terreno == "plano":
            multiplicador = 1.2

        return int(multiplicador * (
            self.infanteria * 1 + 
            self.caballeria * 3 + 
            self.artilleria * 5
        ))

    def __str__(self):
        return f"Infantería: {self.infanteria}, Caballería: {self.caballeria}, Artillería: {self.artilleria}"

class JuegoRisk:
    def __init__(self):
        print(f"{Fore.GREEN}\n¡Bienvenido al Analizador de Risk!{Style.RESET_ALL}")
        self.tablero = TableroJuego()
        self.ejercito_jugador = None
        self.orden_conquista = []
        self.puntuacion = 0
        self.configurar_juego()

    def _leer_entero(self, mensaje: str, minimo: int = None, maximo: int = None, defecto: int = None) -> int:
        while True:
            entrada = input(mensaje)
            if not entrada and defecto is not None:
                return defecto
            try:
                valor = int(entrada)
                if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                    raise ValueError
                return valor
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Ingresa un número entero válido.{Style.RESET_ALL}")

    def _leer_texto(self, mensaje: str, opciones: List[str] = None, defecto: str = None) -> str:
        while True:
            entrada = input(mensaje).strip()
            if not entrada and defecto is not None:
                return defecto
            if opciones and entrada not in opciones:
                print(f"{Fore.RED}Entrada inválida. Opciones válidas: {', '.join(opciones)}.{Style.RESET_ALL}")
                continue
            return entrada

    def configurar_juego(self):
        print(f"{Fore.CYAN}\nComencemos configurando el juego.{Style.RESET_ALL}")
        self.puntos_disponibles = self._leer_entero("Introduce los puntos disponibles (por defecto 20): ", minimo=1, defecto=20)
        
        self.territorios = []
        num_territorios = self._leer_entero("Número de territorios a crear (por defecto 3): ", minimo=1, defecto=3)
        
        for i in range(num_territorios):
            print(f"\nTerritorio {i+1}:")
            nombre = input(f"Nombre (por defecto 'Territorio {i+1}'): ") or f"Territorio {i+1}"
            defensa = self._leer_entero("Fuerza de defensa: ", minimo=1, defecto=10 + i*2)
            puntos = self._leer_entero("Puntos de recompensa: ", minimo=1, defecto=5 + i)
            tipo_terreno = self._leer_texto("Tipo de terreno (plano/montañoso, por defecto plano): ", opciones=["plano", "montañoso"], defecto="plano")
            posicion = (i, i)  # Posición simple diagonal

            territorio = Territorio(nombre, defensa, puntos, posicion, tipo_terreno)
            self.territorios.append(territorio)
            self.tablero.agregar_territorio(territorio)

    def generar_combinaciones_ejercito(self) -> List[Ejercito]:
        combinaciones = []
        max_infanteria = self.puntos_disponibles
        max_caballeria = self.puntos_disponibles // 3
        max_artilleria = self.puntos_disponibles // 5

        for i in range(1, max_infanteria + 1):
            for j in range(1, max_caballeria + 1):
                for k in range(1, max_artilleria + 1):
                    ejercito = Ejercito(i, j, k)
                    if ejercito.obtener_costo_total() <= self.puntos_disponibles:
                        combinaciones.append(ejercito)

        print(f"\n{Fore.YELLOW}Se encontraron {len(combinaciones)} combinaciones válidas de ejército.{Style.RESET_ALL}")
        return combinaciones

    def generar_ordenes_territorio(self) -> List[List[Territorio]]:
        territorios_ordenados = sorted(self.territorios, key=lambda t: t.fuerza_defensa)
        ordenes = list(itertools.permutations(territorios_ordenados))
        print(f"\n{Fore.YELLOW}Se generaron {len(ordenes)} órdenes posibles de ataque.{Style.RESET_ALL}")
        return ordenes

    def analizar_posibilidades(self):
        print(f"{Fore.CYAN}\nAnalizando todas las posibilidades...{Style.RESET_ALL}")
        ejercitos = self.generar_combinaciones_ejercito()
        ordenes = self.generar_ordenes_territorio()
        
        mejor_estrategia = None
        mejor_puntuacion = -1
        
        for ejercito in ejercitos:
            for orden in ordenes:
                poder_actual = ejercito.obtener_poder_ataque()
                exito = True
                puntuacion = 0
                
                for territorio in orden:
                    ataque_efectivo = ejercito.obtener_poder_ataque(territorio.tipo_terreno)
                    if ataque_efectivo >= territorio.fuerza_defensa:
                        puntuacion += territorio.puntos_recompensa
                        poder_actual = int(poder_actual * 0.8)
                    else:
                        exito = False
                        break
                
                if exito and puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_estrategia = (ejercito, list(orden))

        return mejor_estrategia, mejor_puntuacion

    def jugar(self):
        print(f"{Fore.CYAN}\nConfiguración completa. ¡Listo para jugar!{Style.RESET_ALL}")
        self.tablero.mostrar()
        
        while True:
            print(f"{Fore.CYAN}\nOpciones:{Style.RESET_ALL}")
            print("1. Ver todas las combinaciones posibles de ejército")
            print("2. Ver todas las permutaciones de orden de ataque")
            print("3. Analizar mejor estrategia")
            print("4. Crear ejército manualmente")
            print("5. Salir")
            
            opcion = self._leer_entero(f"{Fore.YELLOW}\nElige una opción (1-5): {Style.RESET_ALL}", minimo=1, maximo=5)
            
            if opcion == 1:
                combinaciones = self.generar_combinaciones_ejercito()
                print("\nPrimeras 5 combinaciones posibles:")
                for i, ejercito in enumerate(combinaciones[:5]):
                    print(f"{i+1}. {ejercito} - Poder total: {ejercito.obtener_poder_ataque()}")
                
            elif opcion == 2:
                ordenes = self.generar_ordenes_territorio()
                print("\nPrimeros 5 órdenes posibles:")
                for i, orden in enumerate(ordenes[:5]):
                    print(f"{i+1}. {' -> '.join(t.nombre for t in orden)}")
                
            elif opcion == 3:
                mejor_estrategia, mejor_puntuacion = self.analizar_posibilidades()
                if mejor_estrategia:
                    ejercito, orden = mejor_estrategia
                    print("\nMejor estrategia encontrada:")
                    print(f"Ejército: {ejercito}")
                    print(f"Orden de ataque: {' -> '.join(t.nombre for t in orden)}")
                    print(f"Puntuación total: {mejor_puntuacion}")
                else:
                    print(f"\n{Fore.RED}No se encontró una estrategia viable.{Style.RESET_ALL}")
                
            elif opcion == 4:
                self._crear_ejercito_manual()
                
            elif opcion == 5:
                print(f"{Fore.GREEN}\n¡Gracias por jugar!{Style.RESET_ALL}")
                break

    def _crear_ejercito_manual(self):
        while True:
            try:
                print(f"\n{Fore.CYAN}Puntos disponibles: {self.puntos_disponibles}{Style.RESET_ALL}")
                infanteria = self._leer_entero("Número de unidades de infantería: ", minimo=1)
                caballeria = self._leer_entero("Número de unidades de caballería: ", minimo=1)
                artilleria = self._leer_entero("Número de unidades de artillería: ", minimo=1)
                
                ejercito = Ejercito(infanteria, caballeria, artilleria)
                
                if ejercito.obtener_costo_total() > self.puntos_disponibles:
                    print(f"\n{Fore.RED}¡Error! No tienes suficientes puntos.{Style.RESET_ALL}")
                    continue
                
                self.ejercito_jugador = ejercito
                print("\nEjército creado:")
                print(f"Poder total de ataque: {ejercito.obtener_poder_ataque()}")
                self._simular_campania()
                break
                
            except ValueError:
                print(f"\n{Fore.RED}¡Error! Por favor ingresa números válidos.{Style.RESET_ALL}")

    def _simular_campania(self):
        if not self.ejercito_jugador:
            return
        
        print("\nSimulación de la campaña:")
        poder_actual = self.ejercito_jugador.obtener_poder_ataque()
        
        print("\nElige el orden de ataque:")
        territorios_disponibles = self.territorios.copy()
        orden_ataque = []
        
        for i in range(len(self.territorios)):
            print(f"\nTerritorios disponibles para el ataque #{i+1}:")
            for j, territorio in enumerate(territorios_disponibles, 1):
                print(f"{j}. {territorio.nombre} (Defensa: {territorio.fuerza_defensa})")
            
            eleccion = self._leer_entero("Elige el número del territorio: ", minimo=1, maximo=len(territorios_disponibles)) - 1
            orden_ataque.append(territorios_disponibles.pop(eleccion))
        
        for territorio in orden_ataque:
            print(f"\nAtacando {territorio.nombre}")
            print(f"Poder de ataque: {poder_actual}")
            print(f"Defensa enemiga: {territorio.fuerza_defensa}")
            
            ataque_efectivo = self.ejercito_jugador.obtener_poder_ataque(territorio.tipo_terreno)
            if ataque_efectivo >= territorio.fuerza_defensa:
                print(f"{Fore.GREEN}¡Victoria! Has conquistado {territorio.nombre}{Style.RESET_ALL}")
                self.puntuacion += territorio.puntos_recompensa
                self.tablero.marcar_conquistado(territorio.nombre)
                self.tablero.mostrar()
            else:
                print(f"{Fore.RED}Derrota. Tu ejército no pudo conquistar {territorio.nombre}{Style.RESET_ALL}")
                break
            
            poder_actual = int(poder_actual * 0.8)
            print(f"Poder restante: {poder_actual}")
        
        print(f"\n{Fore.CYAN}Fin de la campaña. Puntuación final: {self.puntuacion}{Style.RESET_ALL}")

if __name__ == "__main__":
    juego = JuegoRisk()
    juego.jugar()
