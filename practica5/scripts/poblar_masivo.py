import mysql.connector
import os
import random
import time
import csv
from faker import Faker
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURACIÓN ---
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': 'root',
    'password': 'root', 
    'database': os.environ.get('DB_NAME', 'tienda_abarrotes'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'allow_local_infile': True
}

fake = Faker('es_MX')
CSV_DIR = '/app/scripts/csv_data'
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

def get_connection():
    MAX_RETRIES = 20 
    for i in range(MAX_RETRIES):
        try:
            return mysql.connector.connect(**db_config)
        except mysql.connector.Error:
            print(f"Esperando a que MySQL despierte... ({i+1}/{MAX_RETRIES})")
            time.sleep(5)
    raise Exception(" La base de datos no respondió a tiempo.")

def generar_clientes_csv(n_rows):
    print(f" Generando {n_rows} Clientes en CSV...")
    filename = os.path.join(CSV_DIR, 'clientes.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(1, n_rows + 1):
            writer.writerow([i, fake.name(), f"user{i}_{random.randint(100,999)}@mail.com", "Dir Genérica"])
    return filename

def generar_productos_csv(n_rows):
    print(f"  Generando {n_rows} Productos en CSV...")
    filename = os.path.join(CSV_DIR, 'productos.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(1, n_rows + 1):

            writer.writerow([i, f"Prod Masivo {i}", round(random.uniform(10, 500), 2), random.randint(10, 200), random.randint(1, 8)])
    return filename

def generar_pedidos_csv(n_rows, total_clientes):
    print(f" Generando {n_rows} Pedidos en CSV...")
    filename = os.path.join(CSV_DIR, 'pedidos.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(1, n_rows + 1):
            writer.writerow([i, random.randint(1, total_clientes), "2025-12-01 12:00:00", "Entregado", 0])
    return filename

def generar_detalles_y_pagos(n_pedidos, total_productos):
    print(f" Generando Detalles y Pagos (Esto tardará un poco)...")
    file_detalles = os.path.join(CSV_DIR, 'detalles.csv')
    file_pagos = os.path.join(CSV_DIR, 'pagos.csv')
    
    with open(file_detalles, 'w', newline='', encoding='utf-8') as fd, \
         open(file_pagos, 'w', newline='', encoding='utf-8') as fp:
        
        writer_d = csv.writer(fd, delimiter=',')
        writer_p = csv.writer(fp, delimiter=',')
        
        contador_detalles = 0
        for id_pedido in range(1, n_pedidos + 1):
            n_items = random.randint(5, 10)
            total_pedido = 0
            
            for _ in range(n_items):
                precio = 50.00
                cant = random.randint(1, 3)
                writer_d.writerow([id_pedido, random.randint(1, total_productos), cant, precio])
                total_pedido += (precio * cant)
                contador_detalles += 1
            
            writer_p.writerow([id_pedido, "Efectivo", "2025-12-01 12:00:00", total_pedido])
            
            if id_pedido % 20000 == 0:
                print(f"      ... {contador_detalles} detalles generados")
                
    return file_detalles, file_pagos

def cargar_csv_mysql(conn, file_path, table_name, columns):
    print(f" Inyectando {table_name} vía LOAD DATA LOCAL...")
    cursor = conn.cursor()
    path = os.path.abspath(file_path)
    sql = f"""
        LOAD DATA LOCAL INFILE '{path}'
        INTO TABLE {table_name}
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\\n'
        ({columns})
    """
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"       {table_name} cargada exitosamente.")
    except Exception as e:
        print(f"       Error cargando {table_name}: {e}")

def run():
    print("---  INICIANDO POBLADO MASIVO (NIVEL 3: PRODUCCIÓN) ---")
    start_global = time.time()
    
    CANT_CLIENTES = 100000   
    CANT_PRODUCTOS = 10000   
    CANT_PEDIDOS = 100000    
    
    conn = get_connection()
    cursor = conn.cursor()

    print(" Limpiando base de datos...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    tablas = ['Detalle_Pedido', 'Pagos', 'Pedido', 'Productos', 'Cliente', 'Categoria']
    for t in tablas:
        cursor.execute(f"TRUNCATE TABLE {t}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    

    print(" Insertando Categorías base...")
    cats = ['Lácteos', 'Bebidas', 'Limpieza', 'Botanas', 'Enlatados', 'Harinas', 'Dulces', 'Higiene']

    for c in cats:
        cursor.execute("INSERT INTO Categoria (nombre, descripcion) VALUES (%s, %s)", (c, "Cat. Masiva"))
    conn.commit()
    

    conn.close() 


    print(" Iniciando Generación CSV...")
    t_start_gen = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_cli = executor.submit(generar_clientes_csv, CANT_CLIENTES)
        future_prod = executor.submit(generar_productos_csv, CANT_PRODUCTOS)
        future_ped = executor.submit(generar_pedidos_csv, CANT_PEDIDOS, CANT_CLIENTES)
        
        file_cli = future_cli.result()
        file_prod = future_prod.result()
        file_ped = future_ped.result()

    file_det, file_pagos = generar_detalles_y_pagos(CANT_PEDIDOS, CANT_PRODUCTOS)
    t_end_gen = time.time()

    print(" Iniciando Ingesta de Datos...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("SET UNIQUE_CHECKS = 0")
    cursor.execute("SET SQL_LOG_BIN = 0")
    
    t_start_load = time.time()
    
    cargar_csv_mysql(conn, file_cli, 'Cliente', 'id_usuario, nombre, email, direccion')
    cargar_csv_mysql(conn, file_prod, 'Productos', 'id_producto, nombre, precio, stock, id_categoria')
    cargar_csv_mysql(conn, file_ped, 'Pedido', 'id_pedido, id_usuario, fecha, estado, total')
    cargar_csv_mysql(conn, file_det, 'Detalle_Pedido', 'id_pedido, id_producto, cantidad, precio_unitario')
    cargar_csv_mysql(conn, file_pagos, 'Pagos', 'id_pedido, metodo_pago, fecha_pago, monto')

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    cursor.execute("SET UNIQUE_CHECKS = 1")
    
    t_end_load = time.time()
    
    print("\n" + "="*40)
    print("✅ REPORTE FINAL DE POBLADO MASIVO")
    print("="*40)
    print(f" Registros Clientes: {CANT_CLIENTES}")
    print(f" Registros Pedidos: {CANT_PEDIDOS}")
    print(f" Tiempo Generación: {round(t_end_gen - t_start_gen, 2)} s")
    print(f" Tiempo Ingesta: {round(t_end_load - t_start_load, 2)} s")
    print(f" TIEMPO TOTAL: {round(time.time() - start_global, 2)} s")
    print("="*40)

if __name__ == "__main__":
    run()