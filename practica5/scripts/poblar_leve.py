import mysql.connector
import os
import random
import time
from faker import Faker

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
            print(f" Intentando conectar a MySQL ({i+1}/{MAX_RETRIES})...")
            conn = mysql.connector.connect(**db_config)
            print(" ¡Conexión exitosa!")
            return conn
        except mysql.connector.Error as err:
            print(f" La base de datos aún no responde: {err}")
            print(" Esperando 3 segundos...")
            time.sleep(3)
    
    raise Exception(" No se pudo conectar a la BD tras varios intentos.")

def run():
    print("--- INICIANDO POBLADO LEVE (NIVEL 1) ---")
    print(" Meta: 50-100 registros principales / 100-1000 secundarios")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        conn.start_transaction()

        print(" Insertando Categorías...")
        categorias = ['Lácteos', 'Bebidas', 'Limpieza', 'Botanas', 'Enlatados', 'Harinas', 'Dulces', 'Higiene']
        for cat in categorias:
            cursor.execute("INSERT IGNORE INTO Categoria (nombre, descripcion) VALUES (%s, %s)", 
                           (cat, fake.sentence()))
        
        cursor.execute("SELECT id_categoria FROM Categoria")
        ids_categorias = [row[0] for row in cursor.fetchall()]


        print(" Insertando 60 Productos...")
        ids_productos = []
        for _ in range(60):
            nombre_prod = fake.word().capitalize() + " " + fake.word()
            precio = round(random.uniform(10.50, 500.00), 2)
            stock = random.randint(10, 100)
            id_cat = random.choice(ids_categorias)
            
            cursor.execute("INSERT INTO Productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)", 
                           (nombre_prod, precio, stock, id_cat))
            ids_productos.append(cursor.lastrowid)

        print("busts_in_silhouette Insertando 60 Clientes...")
        ids_clientes = []
        for _ in range(60): 
            nombre = fake.name()
            email = fake.unique.email()
            direccion = fake.address().replace('\n', ', ')
            
            cursor.execute("INSERT INTO Cliente (nombre, email, direccion) VALUES (%s, %s, %s)", 
                           (nombre, email, direccion))
            ids_clientes.append(cursor.lastrowid)


        print(" Insertando 60 Pedidos...")
        ids_pedidos = []
        for _ in range(60): 
            id_cliente = random.choice(ids_clientes)
            fecha = fake.date_time_between(start_date='-1y', end_date='now')
            estado = random.choice(['Pendiente', 'Enviado', 'Entregado'])
            
            cursor.execute("INSERT INTO Pedido (id_usuario, fecha, estado, total) VALUES (%s, %s, %s, 0)", 
                           (id_cliente, fecha, estado))
            ids_pedidos.append(cursor.lastrowid)


        print(" Generando Detalles (Secundarios)...")
        
        count_detalles = 0
        for id_pedido in ids_pedidos:
            total_pedido = 0
            
            num_items = random.randint(3, 6) 
            
            for _ in range(num_items):
                id_prod = random.choice(ids_productos)
                cantidad = random.randint(1, 5)

                precio_unitario = round(random.uniform(10, 100), 2)
                
                cursor.execute("""INSERT INTO Detalle_Pedido (id_pedido, id_producto, cantidad, precio_unitario) 
                                  VALUES (%s, %s, %s, %s)""", 
                               (id_pedido, id_prod, cantidad, precio_unitario))
                
                total_pedido += (precio_unitario * cantidad)
                count_detalles += 1
            

            cursor.execute("UPDATE Pedido SET total = %s WHERE id_pedido = %s", (total_pedido, id_pedido))
            

            metodo = random.choice(['Efectivo', 'Transferencia']) 
            cursor.execute("INSERT INTO Pagos (id_pedido, metodo_pago, monto) VALUES (%s, %s, %s)", 
                           (id_pedido, metodo, total_pedido))

        conn.commit()
        print(f" ¡Poblado Leve Exitoso!")
        print(f"    Resumen: {len(ids_clientes)} Clientes, {len(ids_pedidos)} Pedidos, {count_detalles} Detalles insertados.")
        
    except Exception as e:
        conn.rollback()
        print(f" Error durante el poblado: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run()