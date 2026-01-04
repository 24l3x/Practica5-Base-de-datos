#!/bin/bash
# Archivo: entrypoint.sh

echo "⏳ Esperando a que MySQL esté listo..."
# Un sleep simple para dar tiempo a que la BD arranque (en producción se usa wait-for-it)
sleep 15 

echo "🚀 Iniciando contenedor de poblado..."
echo "📊 Nivel seleccionado: $NIVEL_POBLADO"

if [ "$NIVEL_POBLADO" = "leve" ]; then
    echo "--- Ejecutando Poblado LEVE (Nivel 1) ---"
    python scripts/poblar_leve.py
    
elif [ "$NIVEL_POBLADO" = "moderado" ]; then
    echo "--- Ejecutando Poblado MODERADO (Nivel 2) ---"
    python scripts/poblar_moderado.py
    
elif [ "$NIVEL_POBLADO" = "masivo" ]; then
    echo "--- Ejecutando Poblado MASIVO (Nivel 3) ---"
    python scripts/poblar_masivo.py
    
else
    echo "⚠️ No se seleccionó nivel de poblado o es 'ninguno'. Manteninedo contenedor activo."
    # Mantiene el contenedor vivo para que puedas entrar manualmente si quieres
    tail -f /dev/null
fi