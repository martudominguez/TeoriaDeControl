# Simulación de Control de Temperatura 🌡️

Esta aplicación permite simular el control de temperatura de un sistema, considerando perturbaciones aleatorias o personalizadas. Es ideal para experimentar con conceptos de control automático y observar cómo responde el sistema ante diferentes escenarios.

## ¿Cómo funciona la app?

- **Modos de simulación:**
  - **Aleatorio:** Se generan perturbaciones de temperatura de manera aleatoria, según parámetros definidos por el usuario (probabilidad, intensidad mínima y máxima, etc.).
  - **Personalizado:** El usuario puede definir eventos de perturbación específicos (inicio, duración e intensidad).

- **Control de temperatura:**
  El sistema simula un controlador que enciende o apaga un compresor para mantener la temperatura cerca de un valor objetivo, aplicando una lógica de histéresis. **El aire acondicionado solo enfría (no puede calentar)** y el control es proporcional de tipo **on/off** (el compresor está completamente encendido o apagado, sin estados intermedios).

- **Resultados:**
  Al finalizar la simulación, se muestra un gráfico de la evolución de la temperatura y se informa si hubo una falla (por ejemplo, una perturbación demasiado larga). Los resultados se guardan automáticamente en la carpeta `simulation_results`.

## ¿Cómo correr la app?

1. **Requisitos previos:**
   - Tener Python 3.8 o superior instalado.
   - Instalar las dependencias necesarias ejecutando:
     ```
     pip install -r requirements.txt
     ```
2. **Ejecutar la aplicación:**
   En la terminal, dentro de la carpeta del proyecto, ejecuta:
   ```
   streamlit run streamlit_app.py
   ```
3. **Usar la app:**
   - Se abrirá una página web en tu navegador.
   - Completa los parámetros de la simulación según el modo que elijas.
   - Haz clic en "Iniciar Simulación" para ver los resultados.

--- 