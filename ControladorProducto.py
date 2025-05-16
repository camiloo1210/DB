import pyodbc
import json
from Producto import Producto


def establecer_conexion():
    try:
        # Recupera config con JSON
        with open('config.json', 'r') as archivo_config:
            config = json.load(archivo_config)

        # Recuperar variables de conexión
        name_server = config['name_server']
        database = config['database']
        username = config['username']
        password = config['password']
        controlador_odbc = config['controlador_odbc']

        # Crear Cadena de Conexión (con login SQL)
        connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'

        # Establece la conexión
        conexion = pyodbc.connect(connection_string)
        print("Conexión Exitosa:")
        return conexion
        
    except Exception as e:
        print("\n\tOcurrió un error al conectar a SQL Server: \n", e)
        return None

# Función para consultar todos los productos
def consultar_productos(conexion):
    try:
        # Consulta SQL usando procedimiento almacenado
        SQL_QUERY = "{CALL sp_ConsultarProductos}"
        cursor = conexion.cursor()
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()
        print("\n\t{:<5} {:<30} {:<10} {:<10}".format("ID", "NOMBRE", "PRECIO", "STOCK"))
        print("\t" + "-" * 60)
        for r in records:
            print(f"\t{r.IDProducto:<5} {r.NombreProducto:<30} ${r.PrecioProducto:<9.2f} {r.StockProducto:<10}")
    
    except Exception as e:
        print("\n\tOcurrió un error al conectar a SQL Server: \n", e)
    
    finally:
        print("Consulta Finalizada")


# Función para insertar un nuevo producto
def insertar_producto(conexion):
    try:
        with conexion.cursor() as cursor:
            # Consulta SQL usando procedimiento almacenado
            SQL_STATEMENT = "{CALL sp_InsertarProducto(?, ?, ?)}"
            
            # Ingreso de información
            print("\n\t-- NUEVO PRODUCTO --")
            l_NombreProducto = input("\tIngrese Nombre del Producto: \t")
            l_PrecioProducto = float(input("\tIngrese Precio del Producto: \t"))
            l_StockProducto = int(input("\tIngrese Stock del Producto: \t"))
            
            # Crear objeto Producto
            nuevo_producto = Producto(None, l_NombreProducto, l_PrecioProducto, l_StockProducto)
            
            # Ejecutar procedimiento almacenado
            cursor.execute(SQL_STATEMENT, 
                          (nuevo_producto.NombreProducto, 
                           nuevo_producto.PrecioProducto, 
                           nuevo_producto.StockProducto))
            
            # Obtener el ID generado
            row = cursor.fetchone()
            if row:
                print(f"\n\t✓ Producto registrado con ID: {row.IDProducto}")
            
            conexion.commit()
    except Exception as e:
        print("\n\tOcurrió un error al insertar en SQL Server: \n\tError:", e)


# Función para actualizar un producto
def actualizar_producto(conexion):
    try:
        with conexion.cursor() as cursor:
            # Consulta SQL usando procedimiento almacenado
            SQL_STATEMENT = "{CALL sp_ActualizarProducto(?, ?, ?, ?)}"
            
            # Ingreso de información
            print("\n\t-- ACTUALIZAR PRODUCTO --")
            l_IDProducto = int(input("\tIngrese ID del Producto a actualizar: \t"))
            
            # Primero consultamos el producto para mostrar sus datos actuales
            cursor.execute("{CALL sp_ConsultarProductoPorID(?)}", (l_IDProducto,))
            producto_actual = cursor.fetchone()
            
            if not producto_actual:
                print(f"\n\t✗ No se encontró producto con ID: {l_IDProducto}")
                return
                
            print(f"\n\tProducto actual: {producto_actual.NombreProducto}, Precio: ${producto_actual.PrecioProducto}, Stock: {producto_actual.StockProducto}")
            
            # Solicitar nuevos datos
            l_NombreProducto = input("\tIngrese nuevo Nombre (dejar vacío para mantener): \t")
            l_PrecioStr = input("\tIngrese nuevo Precio (dejar vacío para mantener): \t")
            l_StockStr = input("\tIngrese nuevo Stock (dejar vacío para mantener): \t")
            
            # Usar valores actuales si no se ingresan nuevos
            l_NombreProducto = l_NombreProducto if l_NombreProducto else producto_actual.NombreProducto
            l_PrecioProducto = float(l_PrecioStr) if l_PrecioStr else producto_actual.PrecioProducto
            l_StockProducto = int(l_StockStr) if l_StockStr else producto_actual.StockProducto
            
            # Ejecutar procedimiento almacenado
            cursor.execute(SQL_STATEMENT, 
                          (l_IDProducto, l_NombreProducto, l_PrecioProducto, l_StockProducto))
            
            # Verificar resultado
            row = cursor.fetchone()
            if row and row.FilasAfectadas > 0:
                print(f"\n\t✓ Producto actualizado correctamente")
            else:
                print(f"\n\t✗ No se pudo actualizar el producto")
            
            conexion.commit()
    except Exception as e:
        print("\n\tOcurrió un error al actualizar en SQL Server: \n\tError:", e)


# Función para eliminar un producto
def eliminar_producto(conexion):
    try:
        with conexion.cursor() as cursor:
            # Consulta SQL usando procedimiento almacenado
            SQL_STATEMENT = "{CALL sp_EliminarProducto(?)}"
            
            # Ingreso de información
            print("\n\t-- ELIMINAR PRODUCTO --")
            l_IDProducto = int(input("\tIngrese ID del Producto a eliminar: \t"))
            
            # Primero consultamos el producto para confirmar
            cursor.execute("{CALL sp_ConsultarProductoPorID(?)}", (l_IDProducto,))
            producto = cursor.fetchone()
            
            if not producto:
                print(f"\n\t✗ No se encontró producto con ID: {l_IDProducto}")
                return
                
            print(f"\n\tProducto a eliminar: {producto.NombreProducto}, Precio: ${producto.PrecioProducto}, Stock: {producto.StockProducto}")
            confirmacion = input("\n\t¿Está seguro de eliminar este producto? (s/n): ")
            
            if confirmacion.lower() != 's':
                print("\n\tOperación cancelada")
                return
            
            # Ejecutar procedimiento almacenado
            cursor.execute(SQL_STATEMENT, (l_IDProducto,))
            
            # Verificar resultado
            row = cursor.fetchone()
            if row and row.FilasAfectadas > 0:
                print(f"\n\t✓ Producto eliminado correctamente")
            else:
                print(f"\n\t✗ No se pudo eliminar el producto")
            
            conexion.commit()
    except Exception as e:
        print("\n\tOcurrió un error al eliminar en SQL Server: \n\tError:", e)


# Función para listar opciones CRUD
def mostrar_opciones_crud():
    print("\n\t** SISTEMA CRUD DE PRODUCTOS ** \n")  
    print("\t***************************")  
    print("\tOpciones CRUD:\n")
    print("\t1. Crear producto")
    print("\t2. Consultar productos")
    print("\t3. Actualizar producto")
    print("\t4. Eliminar producto")
    print("\t5. Salir\n")


### Inicio Programa principal ########
if __name__ == "__main__":
    # Establecer conexión usando la función
    conexion = establecer_conexion()
    
    # Verificar si la conexión fue exitosa
    if conexion is None:
        print("No se pudo establecer la conexión. Saliendo del programa...")
        exit(1)

    mostrar_opciones_crud()
    opcion = input("Seleccione una opción 1-5:\t")

    while True:
        if opcion == '1':
            insertar_producto(conexion)
        elif opcion == '2':
            consultar_productos(conexion)
        elif opcion == '3':
            actualizar_producto(conexion)
        elif opcion == '4':
            eliminar_producto(conexion)
        elif opcion == '5':
            conexion.close()
            print("Conexión Finalizada")
            print("Saliendo del programa..\n")
            break
        else:
            print("Opción no válida.")
        
        # Mostrar opciones nuevamente
        print("\n")
        mostrar_opciones_crud()
        opcion = input("Seleccione una opción 1-5:\t")
    
    # Asegurar que se cierre la conexión
    if conexion:
        conexion.close()