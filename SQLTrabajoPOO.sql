CREATE DATABASE TRABAJODB
GO

USE TRABAJODB
GO

CREATE LOGIN [pythonconsultor] WITH PASSWORD='UDLA', 
DEFAULT_DATABASE=[TRABAJODB] 
GO

CREATE TABLE Productos (
    IDProducto INT IDENTITY(1,1),
    NombreProducto NVARCHAR(100) NOT NULL,
    PrecioProducto DECIMAL(10,2) NOT NULL,
    StockProducto INT NOT NULL
);

ALTER TABLE Productos ADD CONSTRAINT PK_Productos PRIMARY KEY (IDProducto);

CREATE INDEX IX_Productos_Nombre ON Productos(NombreProducto);

CREATE PROCEDURE sp_InsertarProducto
    @NombreProducto NVARCHAR(100),
    @PrecioProducto DECIMAL(10,2),
    @StockProducto INT
AS
BEGIN
    INSERT INTO Productos (NombreProducto, PrecioProducto, StockProducto)
    VALUES (@NombreProducto, @PrecioProducto, @StockProducto);
    
    -- Devolver el ID del producto insertado
    SELECT SCOPE_IDENTITY() AS IDProducto;
END;

CREATE PROCEDURE sp_ConsultarProductos
AS
BEGIN
    SELECT IDProducto, NombreProducto, PrecioProducto, StockProducto
    FROM Productos
    ORDER BY NombreProducto;
END;

CREATE PROCEDURE sp_ConsultarProductoPorID
    @IDProducto INT
AS
BEGIN
    SELECT IDProducto, NombreProducto, PrecioProducto, StockProducto
    FROM Productos
    WHERE IDProducto = @IDProducto;
END;

CREATE PROCEDURE sp_ActualizarProducto
    @IDProducto INT,
    @NombreProducto NVARCHAR(100),
    @PrecioProducto DECIMAL(10,2),
    @StockProducto INT
AS
BEGIN
    UPDATE Productos
    SET NombreProducto = @NombreProducto,
        PrecioProducto = @PrecioProducto,
        StockProducto = @StockProducto
    WHERE IDProducto = @IDProducto;
    
    -- Devolver 1 si se actualizó correctamente, 0 si no se encontró el producto
    SELECT @@ROWCOUNT AS FilasAfectadas;
END;

CREATE PROCEDURE sp_EliminarProducto
    @IDProducto INT
AS
BEGIN
    DELETE FROM Productos
    WHERE IDProducto = @IDProducto;
    
    -- Devolver 1 si se eliminó correctamente, 0 si no se encontró el producto
    SELECT @@ROWCOUNT AS FilasAfectadas;
END;

USE [TRABAJODB]
GO

CREATE USER [pythonconsultor] FOR LOGIN [pythonconsultor]
GO

GRANT EXECUTE TO [pythonconsultor]
GO

EXEC sp_InsertarProducto 
    @NombreProducto = N'Camisa',
    @PrecioProducto = 29.99,
    @StockProducto = 100;



EXEC sp_InsertarProducto 
    @NombreProducto = N'Celular',
    @PrecioProducto = 10.99,
    @StockProducto = 21;

EXEC sp_ConsultarProductos;
GO

EXEC sp_ConsultarProductoPorID @IDProducto = 1;
GO

EXEC sp_ActualizarProducto 
    @IDProducto = 1,
    @NombreProducto = N'Camisa Actualizada',
    @PrecioProducto = 34.99,
    @StockProducto = 120;
GO

EXEC sp_EliminarProducto @IDProducto = 2;
GO