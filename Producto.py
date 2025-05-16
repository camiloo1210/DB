class Producto:
    def __init__(self, IDProducto=None, NombreProducto=None, PrecioProducto=None, StockProducto=None):
        self.IDProducto=IDProducto
        self.NombreProducto=NombreProducto
        self.PrecioProducto=PrecioProducto
        self.StockProducto=StockProducto
        
        
    def tostr(self):
        return f"ID:{self.IDProducto},Nombre: {self.NombreProducto},Precio:{self.PrecioProducto},Stock:{self.StockProducto}"