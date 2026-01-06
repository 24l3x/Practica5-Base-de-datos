
USE tienda_abarrotes;

-- 3.1

-- 1
SELECT 
    c.nombre AS Cliente,
    cat.nombre AS Categoria,
    p.nombre AS Producto,
    dp.cantidad,
    dp.precio_unitario,
    (dp.cantidad * dp.precio_unitario) AS Subtotal
FROM Detalle_Pedido dp
JOIN Pedido ped ON dp.id_pedido = ped.id_pedido
JOIN Cliente c ON ped.id_usuario = c.id_usuario
JOIN Productos p ON dp.id_producto = p.id_producto
JOIN Categoria cat ON p.id_categoria = cat.id_categoria
LIMIT 20;

-- 2
SELECT p.nombre, p.precio, p.id_categoria
FROM Productos p
WHERE p.precio > (
    SELECT AVG(p2.precio)
    FROM Productos p2
    WHERE p2.id_categoria = p.id_categoria
)
ORDER BY p.id_categoria;

-- 4
SELECT 
    nombre, 
    precio, 
    id_categoria,
    RANK() OVER (PARTITION BY id_categoria ORDER BY precio DESC) as ranking_precio
FROM Productos;

-- 6
SELECT nombre, email, 'Cliente' as tipo FROM Cliente
WHERE id_usuario <= 10
UNION
SELECT nombre, 'N/A' as email, 'Vendedor' as tipo FROM Cliente WHERE id_usuario > 100 AND id_usuario <= 110;

-- 7
SELECT 
    id_pedido, 
    total,
    CASE 
        WHEN total < 500 THEN 'Compra Pequeña'
        WHEN total BETWEEN 500 AND 2000 THEN 'Compra Estándar'
        ELSE 'Compra Grande'
    END AS clasificacion
FROM Pedido
LIMIT 20;


-- 10
SELECT nombre, email 
FROM Cliente 
WHERE email LIKE '%@example.com' OR email LIKE '%@mail.com';

-- 3.2

-- 2
INSERT INTO Categoria (nombre, descripcion) VALUES 
('Mascotas', 'Alimentos y accesorios para animales'),
('Jardinería', 'Herramientas y semillas'),
('Automotriz', 'Accesorios básicos para autos');

-- 3
INSERT INTO Productos (nombre, stock, id_categoria, precio)
VALUES ('Kit Limpieza Premium', 50, 3, 100.00 * 1.16);

-- 4
INSERT INTO Productos (id_producto, nombre, precio, stock, id_categoria)
VALUES (1, 'Producto Actualizado', 55.00, 100, 1)
ON DUPLICATE KEY UPDATE precio = 55.00, stock = 100;

-- 3.3

-- 1
UPDATE Productos p
JOIN Categoria c ON p.id_categoria = c.id_categoria
SET p.precio = p.precio * 1.10
WHERE c.nombre = 'Lácteos';

-- 2
UPDATE Productos
SET stock = CASE 
    WHEN stock < 10 THEN 50
    ELSE stock
END;

-- 3
UPDATE Pedido
SET estado = 'Procesado'
WHERE fecha < '2024-01-01' AND estado = 'Pendiente';

-- 4
UPDATE Productos
SET precio = precio * 0.90
WHERE id_producto NOT IN (SELECT DISTINCT id_producto FROM Detalle_Pedido);


