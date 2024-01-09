#!/bin/bash

# Instalar dependencias de Python
pip install -r requirements.txt

# Verificar que la instalación de dependencias de Python fue exitosa
if [ $? -ne 0 ]; then
    echo "Error: Fallo en la instalación de dependencias de Python."
    exit 1
fi

# Instalar Playwright
playwright install

# Verificar que la instalación de Playwright fue exitosa
if [ $? -ne 0 ]; then
    echo "Error: Fallo en la instalación de Playwright."
    exit 1
fi

# Otras tareas de construcción, si las tienes

echo "Construcción exitosa."
