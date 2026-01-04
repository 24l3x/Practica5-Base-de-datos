-- ==========================================================
-- PRÁCTICA 5: Edición de valores empleando DML
-- AUTOR: Alexander
-- TEMA: E-commerce (Tienda de Abarrotes "Don Mero")
-- ==========================================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS tienda_abarrotes;
USE tienda_abarrotes;

-- ==========================================================
-- 1. TABLA CATEGORIA (Independiente)
-- ==========================================================
CREATE TABLE Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único de la categoría',
    nombre VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nombre de la categoría, no se repite',
    descripcion TEXT NULL
);

-- ==========================================================
-- 2. TABLA CLIENTE (Independiente)
-- ==========================================================
CREATE TABLE Cliente (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único del cliente',
    nombre VARCHAR(150) NOT NULL COMMENT 'Nombre completo del cliente',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT 'Correo electrónico único para login',
    direccion TEXT NOT NULL COMMENT 'Dirección de envío',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de alta (Uso de DEFAULT)'
);

-- ==========================================================
-- 3. TABLA PRODUCTOS (Depende de Categoria)
-- ==========================================================
CREATE TABLE Productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0) COMMENT 'El precio debe ser positivo (Uso de CHECK)',
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0) COMMENT 'Inventario no puede ser negativo',
    id_categoria INT NOT NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) 
        REFERENCES Categoria(id_categoria) ON DELETE CASCADE
);

-- ==========================================================
-- 4. TABLA PEDIDO (Depende de Cliente)
-- ==========================================================
CREATE TABLE Pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    total DECIMAL(12, 2) DEFAULT 0.00,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_usuario) 
        REFERENCES Cliente(id_usuario) ON DELETE RESTRICT
);

-- ==========================================================
-- 5. TABLA DETALLE_PEDIDO (Depende de Pedido y Productos)
-- ==========================================================
CREATE TABLE Detalle_Pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL COMMENT 'Precio al momento de la compra',
    CONSTRAINT fk_detalle_pedido FOREIGN KEY (id_pedido) 
        REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (id_producto) 
        REFERENCES Productos(id_producto) ON DELETE RESTRICT
);

-- ==========================================================
-- 6. TABLA PAGOS (Depende de Pedido - Relación 1 a 1)
-- ==========================================================
CREATE TABLE Pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL UNIQUE COMMENT 'Un pedido tiene un solo pago (Relación 1:1)',
    metodo_pago VARCHAR(50) NOT NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(12, 2) NOT NULL,
    -- Validación de métodos de pago permitidos
    CONSTRAINT chk_metodo_pago CHECK (metodo_pago IN ('Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia')),
    CONSTRAINT fk_pago_pedido FOREIGN KEY (id_pedido) 
        REFERENCES Pedido(id_pedido) ON DELETE CASCADE
);