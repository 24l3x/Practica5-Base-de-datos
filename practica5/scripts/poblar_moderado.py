import mysql.connector
import os
import random
import time
from faker import Faker

# --- CONFIGURACIÓN ---
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'mero'),
    'password': os.environ.get('DB_PASSWORD', 'mero_password'),
    'database': os.environ.get('DB_NAME', 'tienda_abarrotes'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

fake = Faker('es_MX')

def get_connection():
    MAX_RETRIES = 15
    for i in range(MAX_RETRIES):
        try:
            return mysql.connector.connect(**db_config)
        except mysql.connector.Error:
            print(f"⏳ Esperando DB... ({i+1}/{MAX_RETRIES})")
            time.sleep(3)
    raise Exception("❌ Sin conexión a DB.")

def run():
    print("--- 🚀 INICIANDO POBLADO MODERADO (NIVEL 2) ---")
    start_time_global = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Configuración de Lotes (Batch Insert)
    BATCH_SIZE = 2000 
    
    try:
        # ---------------------------------------------------------
        # TÉCNICA 1: DESACTIVACIÓN TEMPORAL DE ÍNDICES 
        # ---------------------------------------------------------
        print("🔧 Optimizando: Desactivando autocommit y foreign keys...")
        conn.autocommit = False
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("SET UNIQUE_CHECKS = 0")
        # cursor.execute("SET SQL_LOG_BIN = 0") # Desactiva logs binarios para más velocidad

        # ---------------------------------------------------------
        # 1. CATEGORÍAS (Base)
        # ---------------------------------------------------------
        # Insertamos pocas categorías fijas
        cats = ['Lácteos', 'Carnes', 'Frutas', 'Verduras', 'Limpieza', 'Electrónica', 'Ropa', 'Juguetes', 'Farmacia', 'Panadería']
        for c in cats:
            cursor.execute("INSERT IGNORE INTO Categoria (nombre, descripcion) VALUES (%s, %s)", (c, "Categoría general"))
        conn.commit()
        
        # Recuperar IDs
        cursor.execute("SELECT id_categoria FROM Categoria")
        ids_cats = [r[0] for r in cursor.fetchall()]

        # ---------------------------------------------------------
        # 2. PRODUCTOS (Meta: 6,000) [cite: 34]
        # ---------------------------------------------------------
        print("📦 Generando 6,000 Productos...")
        start_step = time.time()
        
        productos_batch = []
        ids_productos = [] # Simularemos los IDs para no consultar la BD a cada rato
        
        # Obtenemos el último ID actual para saber dónde empezar
        cursor.execute("SELECT MAX(id_producto) FROM Productos")
        last_id = cursor.fetchone()[0] or 0
        
        for i in range(6000):
            nombre = f"Producto {fake.word()} {i}" # Nombre simple es más rápido que Faker completo
            precio = round(random.uniform(10, 1000), 2)
            stock = random.randint(0, 500)
            id_cat = random.choice(ids_cats)
            
            productos_batch.append((nombre, precio, stock, id_cat))
            
            # Guardamos el ID que tendrá este producto
            last_id += 1
            ids_productos.append(last_id)
            
            if len(productos_batch) >= BATCH_SIZE:
                cursor.executemany("INSERT INTO Productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)", productos_batch)
                conn.commit()
                productos_batch = []
                print(f"   -> {i+1} productos insertados...")
                
        # Insertar remanentes
        if productos_batch:
            cursor.executemany("INSERT INTO Productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)", productos_batch)
            conn.commit()
            
        print(f"   ⏱️ Tiempo Productos: {round(time.time() - start_step, 2)}s")

        # ---------------------------------------------------------
        # 3. CLIENTES (Meta: 6,000) [cite: 34]
        # ---------------------------------------------------------
        print("busts_in_silhouette Generando 6,000 Clientes...")
        start_step = time.time()
        
        clientes_batch = []
        ids_clientes = []
        
        cursor.execute("SELECT MAX(id_usuario) FROM Cliente")
        last_id_cli = cursor.fetchone()[0] or 0
        
        for i in range(6000):
            nombre = fake.name()
            email = f"user_{last_id_cli + i + 1}_{random.randint(1000,9999)}@example.com" # Email rápido
            direccion = "Direccion Generica #123"
            
            clientes_batch.append((nombre, email, direccion))
            ids_clientes.append(last_id_cli + i + 1)
            
            if len(clientes_batch) >= BATCH_SIZE:
                cursor.executemany("INSERT INTO Cliente (nombre, email, direccion) VALUES (%s, %s, %s)", clientes_batch)
                conn.commit()
                clientes_batch = []
        
        if clientes_batch:
            cursor.executemany("INSERT INTO Cliente (nombre, email, direccion) VALUES (%s, %s, %s)", clientes_batch)
            conn.commit()
            
        print(f"   ⏱️ Tiempo Clientes: {round(time.time() - start_step, 2)}s")

        # ---------------------------------------------------------
        # 4. PEDIDOS (Meta: 8,000) [cite: 34]
        # ---------------------------------------------------------
        print("📝 Generando 8,000 Pedidos...")
        start_step = time.time()
        
        pedidos_batch = []
        ids_pedidos_generados = [] # Guardamos IDs para usarlos en detalles
        
        cursor.execute("SELECT MAX(id_pedido) FROM Pedido")
        last_id_ped = cursor.fetchone()[0] or 0
        
        for i in range(8000):
            uid = random.choice(ids_clientes)
            fecha = "2025-01-01 12:00:00" # Fecha fija es más rápido que generar objetos datetime
            estado = 'Entregado'
            
            pedidos_batch.append((uid, fecha, estado, 0))
            ids_pedidos_generados.append(last_id_ped + i + 1)
            
            if len(pedidos_batch) >= BATCH_SIZE:
                cursor.executemany("INSERT INTO Pedido (id_usuario, fecha, estado, total) VALUES (%s, %s, %s, %s)", pedidos_batch)
                conn.commit()
                pedidos_batch = []
                
        if pedidos_batch:
            cursor.executemany("INSERT INTO Pedido (id_usuario, fecha, estado, total) VALUES (%s, %s, %s, %s)", pedidos_batch)
            conn.commit()
            
        print(f"   ⏱️ Tiempo Pedidos: {round(time.time() - start_step, 2)}s")

        # ---------------------------------------------------------
        # 5. DETALLES Y PAGOS (Meta: ~64,000 registros) [cite: 35]
        # ---------------------------------------------------------
        print("🛒 Generando Detalles (Tablas Secundarias Massivas)...")
        start_step = time.time()
        
        detalles_batch = []
        pagos_batch = []
        total_detalles = 0
        
        for id_pedido in ids_pedidos_generados:
            # Promedio 8 items por pedido -> 8,000 * 8 = 64,000 registros
            num_items = random.randint(5, 10) 
            total_pedido = 0
            
            for _ in range(num_items):
                pid = random.choice(ids_productos)
                cant = random.randint(1, 3)
                precio = 50.00 # Precio fijo simulado para velocidad
                
                detalles_batch.append((id_pedido, pid, cant, precio))
                total_pedido += (precio * cant)
                total_detalles += 1
            
            # Pago (Sin acentos)
            pagos_batch.append((id_pedido, 'Efectivo', total_pedido))
            
            # Insertar en lotes grandes
            if len(detalles_batch) >= BATCH_SIZE:
                cursor.executemany("INSERT INTO Detalle_Pedido (id_pedido, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", detalles_batch)
                cursor.executemany("INSERT INTO Pagos (id_pedido, metodo_pago, monto) VALUES (%s, %s, %s)", pagos_batch)
                conn.commit()
                detalles_batch = []
                pagos_batch = []
                print(f"   -> {total_detalles} detalles insertados...")

        # Remanentes
        if detalles_batch:
            cursor.executemany("INSERT INTO Detalle_Pedido (id_pedido, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", detalles_batch)
            cursor.executemany("INSERT INTO Pagos (id_pedido, metodo_pago, monto) VALUES (%s, %s, %s)", pagos_batch)
            conn.commit()

        print(f"   ⏱️ Tiempo Detalles: {round(time.time() - start_step, 2)}s")

        # ---------------------------------------------------------
        # REACTIVAR ÍNDICES
        # ---------------------------------------------------------
        print("🔧 Reactivando índices y verificaciones...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        cursor.execute("SET UNIQUE_CHECKS = 1")
        conn.commit()

        total_time = time.time() - start_time_global
        print(f"✅ ¡Poblado Moderado Terminado!")
        print(f"   📊 Totales: 6k Clientes, 6k Productos, 8k Pedidos, {total_detalles} Detalles")
        print(f"   ⏱️ Tiempo Total: {round(total_time, 2)} segundos")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error en moderado: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run()