# Simulador Risk

## Descripción del Proyecto

El **Simulador Risk** es una adaptación simplificada del clásico juego de estrategia **Risk**. Este proyecto permite a los jugadores simular batallas, planificar estrategias y conquistar territorios en un tablero virtual. El objetivo principal es gestionar eficientemente los recursos disponibles para maximizar la puntuación mediante la conquista de territorios enemigos.

## Características Principales

- **Tablero Visual Dinámico**:
  - Representación clara de territorios enemigos, celdas vacías y territorios conquistados.
  - Actualización en tiempo real tras cada movimiento.
  
- **Configuración Personalizable**:
  - Define la cantidad de puntos iniciales para crear tu ejército.
  - Establece el número de territorios en el tablero de juego.

- **Estrategias Avanzadas**:
  - Generación automática de combinaciones óptimas de ejércitos basadas en los puntos disponibles.
  - Cálculo de órdenes de ataque priorizando los territorios más débiles.

- **Interfaz Intuitiva**:
  - Menús claros y fáciles de usar.
  - Uso de colores para resaltar mensajes importantes y mejorar la experiencia del usuario.

## Requisitos Previos

### Software Necesario

- **Python**: Versión 3.7 o superior.
- **Módulos Requeridos**:
  - `numpy`
  - `colorama`

### Configuración Inicial

1. **Asigna los puntos disponibles**: Define el número de puntos para construir tu ejército (valor predeterminado: 20).
2. **Configura el tablero**: Establece el número de territorios que se incluirán en el juego (valor predeterminado: 3).

## Menú Principal

Al iniciar el programa, se muestra un menú con las siguientes opciones:

1. **Ver combinaciones óptimas de ejército**:  
   Muestra las 5 configuraciones más efectivas de tropas basadas en su poder de ataque.

2. **Explorar permutaciones de ataque**:  
   Genera y muestra las 5 mejores secuencias de ataque, priorizando territorios con menor defensa.

3. **Analizar la mejor estrategia**:  
   Combina automáticamente el mejor ejército y el mejor orden de ataque para maximizar las posibilidades de éxito.

4. **Crear ejército manualmente**:  
   Permite al jugador diseñar su ejército y seleccionar manualmente los territorios para atacar.

5. **Salir**:  
   Finaliza el programa.

## Simulación de Ataques

La simulación de ataques sigue estos pasos:

1. **Selecciona el orden de ataque**: Escoge la secuencia en la que deseas atacar los territorios enemigos.
2. **Resolución de batallas**: El programa calcula los resultados de cada enfrentamiento basándose en las estadísticas de ataque y defensa.
3. **Actualización del tablero**:
   - Los territorios conquistados se actualizan visualmente en el tablero.
   - Se muestra la puntuación obtenida tras cada ataque.

---

Este proyecto es ideal para aquellos interesados en los fundamentos de la estrategia militar y la optimización de recursos, todo mientras disfrutan de una experiencia interactiva y dinámica.
