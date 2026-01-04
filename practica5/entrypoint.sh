

echo " Esperando a que MySQL esté listo..."
sleep 15 

echo " Iniciando contenedor de poblado..."
echo " Nivel seleccionado: $NIVEL_POBLADO"

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
    echo " No se seleccionó nivel de poblado o es 'ninguno'. Manteninedo contenedor activo."
    tail -f /dev/null
fi