# Simulador Risk

## Descripción del Proyecto

Este proyecto es una simulación simplificada inspirada en el clásico juego de estrategia **Risk**. Permite a los jugadores configurar ejércitos, planificar estrategias de ataque y conquistar territorios en un tablero virtual. El objetivo principal es optimizar los recursos disponibles para obtener la máxima puntuación posible conquistando territorios enemigos.

## Características Principales

- **Tablero Visual**: Representación de territorios enemigos, celdas vacías y territorios conquistados en un tablero en la consola.
- **Configuración Personalizada**: El jugador define el número de puntos disponibles para crear un ejército y el número de territorios en el tablero.
- **Optimización de Estrategias**:
  - Generación de combinaciones óptimas de ejércitos según los puntos disponibles.
  - Generación de órdenes de ataque priorizando territorios más débiles.
- **Interacción Intuitiva**: Menús claros y mensajes con colores para mejorar la experiencia de usuario.

## Requisitos Previos

### Software Necesario:

- **Python 3.7 o superior**
- **Módulos instalados**:
  - `numpy`
  - `colorama`

### Configuración Inicial:

1. **Introduce los puntos disponibles** para crear tu ejército (valor predeterminado: 20).
2. **Especifica el número de territorios** a crear (valor predeterminado: 3).

### Menú Principal:

Al iniciar, el juego mostrará un menú con las siguientes opciones:

1. **Ver todas las combinaciones posibles de ejército**:  
   Muestra las 5 configuraciones de tropas más óptimas basadas en el poder de ataque.

2. **Ver todas las permutaciones de orden de ataque**:  
   Muestra las 5 mejores secuencias de ataque priorizando territorios más débiles.

3. **Analizar mejor estrategia**:  
   Calcula y muestra la mejor combinación de ejército y orden de ataque.

4. **Crear ejército manualmente**:  
   Permite al jugador definir manualmente su ejército y atacar los territorios seleccionados.

5. **Salir**:  
   Termina el programa.

### Simulación de Ataques:

1. **Selecciona el orden de ataque** de los territorios.
2. El programa calculará el resultado de cada batalla basándose en el poder de ataque y la defensa de los territorios.
3. Actualiza el tablero con los territorios conquistados y muestra la puntuación obtenida.

