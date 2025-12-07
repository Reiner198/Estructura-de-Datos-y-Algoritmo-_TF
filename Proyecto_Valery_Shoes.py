# presentador_sql_valery.py
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "tienda.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sucursal (
            CODIGO_SUCURSAL INTEGER PRIMARY KEY,
            SUCURSAL        TEXT NOT NULL UNIQUE,
            STOCK           INTEGER DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS marca (
            CODIGO_MARCA INTEGER PRIMARY KEY,
            MARCA        TEXT NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            CODIGO_PRODUCTO INTEGER PRIMARY KEY,
            DESCRIPCION     TEXT NOT NULL,
            PRECIO          REAL NOT NULL,
            CODIGO_SUCURSAL INTEGER NOT NULL,
            CODIGO_MARCA    INTEGER NOT NULL,
            FOREIGN KEY (CODIGO_SUCURSAL) REFERENCES sucursal (CODIGO_SUCURSAL),
            FOREIGN KEY (CODIGO_MARCA)    REFERENCES marca (CODIGO_MARCA)
        );
    """)

    cur.execute("SELECT COUNT(*) FROM sucursal;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO sucursal (CODIGO_SUCURSAL, SUCURSAL, STOCK) VALUES (?, ?, ?);",
            [
                (1, "Huaral", 150),
                (2, "Huacho", 150),
                (3, "Barranca", 120),
                (4, "Ventanilla", 180),
            ],
        )

    cur.execute("SELECT COUNT(*) FROM marca;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO marca (CODIGO_MARCA, MARCA) VALUES (?, ?);",
            [
                (1, "Valery"),
                (2, "Vizzano"),
                (3, "Beira Rio"),
                (4, "Zeta"),
                (5, "Stilo"),
            ],
        )

    cur.execute("SELECT COUNT(*) FROM producto;")
    if cur.fetchone()[0] == 0:
        productos = [
            (1001, "Sandalia taco medio nude", 119.90, 1, 1),
            (1002, "Ballerina negra clásica", 79.90, 1, 2),
            (1003, "Zapato taco aguja rojo", 149.90, 2, 2),
            (1004, "Zapatilla casual blanca", 129.90, 3, 1),
            (1005, "Sandalia plataforma dorada", 139.90, 4, 3),
            (1006, "Botín cuero corto marrón", 159.90, 1, 4),
            (1007, "Sandalia plana negra trenzada", 89.90, 2, 5),
            (1008, "Borcego urbano negro", 189.90, 3, 1),
            (1009, "Tacón block beige", 129.00, 4, 2),
            (1010, "Mocasin gamuza azul", 99.50, 1, 3),
            (1011, "Zapatilla running gris", 149.00, 2, 1),
            (1012, "Sandalia fiesta plateada", 169.90, 3, 2),
            (1013, "Ballerina con lazo coral", 79.00, 4, 5),
            (1014, "Zapato de novia blanco", 199.00, 1, 3),
            (1015, "Zapatilla lona baja", 69.90, 2, 4),
            (1016, "Sandalia con plataforma negra", 139.00, 3, 1),
            (1017, "Botín charol rojo", 179.90, 4, 2),
            (1018, "Mule animal print", 119.00, 1, 5),
            (1019, "Sandalia minimal nude", 109.90, 2, 1),
            (1020, "Bota trekking marrón", 229.90, 3, 4),
            (1021, "Zapato escolar negro", 89.90, 4, 3),
            (1022, "Sandalia deportiva azul", 99.00, 1, 1),
            (1023, "Ballerina estampada", 85.00, 2, 5),
            (1024, "Zapatilla plataforma alta", 159.90, 3, 2),
            (1025, "Zapato oxford cuero", 169.00, 4, 4),
            (1026, "Sandalia con hebilla", 95.50, 1, 3),
            (1027, "Mocasin sin cordones", 129.90, 2, 1),
            (1028, "Zapatilla slip-on", 119.90, 3, 4),
            (1029, "Sandalia con pedrería", 149.90, 4, 2),
            (1030, "Botín estilo militar", 199.90, 1, 5),
            (1031, "Tacón aguja negro", 189.90, 2, 1),
            (1032, "Zapatilla running color block", 159.90, 3, 4),
            (1033, "Sandalia esparto natural", 129.90, 4, 3),
        ]
        productos.extend(ejemplos)

        cur.executemany(
            """
            INSERT INTO producto (CODIGO_PRODUCTO, DESCRIPCION, PRECIO, CODIGO_SUCURSAL, CODIGO_MARCA)
            VALUES (?, ?, ?, ?, ?);
            """,
            productos,
        )

    conn.commit()
    conn.close()

def obtener_productos(sucursal_filtro=None, marca_filtro=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    query = """
        SELECT
            p.CODIGO_PRODUCTO,
            p.DESCRIPCION,
            p.PRECIO,
            s.SUCURSAL,
            m.MARCA,
            s.STOCK
        FROM producto p
        JOIN sucursal s ON p.CODIGO_SUCURSAL = s.CODIGO_SUCURSAL
        JOIN marca m    ON p.CODIGO_MARCA    = m.CODIGO_MARCA
        WHERE 1 = 1
    """
    params = []

    if sucursal_filtro:
        query += " AND s.SUCURSAL = ?"
        params.append(sucursal_filtro)

    if marca_filtro:
        query += " AND m.MARCA = ?"
        params.append(marca_filtro)

    query += " ORDER BY p.CODIGO_PRODUCTO;"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def obtener_sucursales():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT SUCURSAL FROM sucursal ORDER BY SUCURSAL;")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def obtener_marcas():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT MARCA FROM marca ORDER BY MARCA;")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def agregar_producto(codigo, descripcion, precio, sucursal_nombre, marca_nombre):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT CODIGO_SUCURSAL FROM sucursal WHERE SUCURSAL = ?;", (sucursal_nombre,))
        row_s = cur.fetchone()
        if not row_s:
            raise ValueError("Sucursal no encontrada.")
        codigo_sucursal = row_s[0]

        cur.execute("SELECT CODIGO_MARCA FROM marca WHERE MARCA = ?;", (marca_nombre,))
        row_m = cur.fetchone()
        if not row_m:
            raise ValueError("Marca no encontrada.")
        codigo_marca = row_m[0]

        cur.execute(
            "INSERT INTO producto (CODIGO_PRODUCTO, DESCRIPCION, PRECIO, CODIGO_SUCURSAL, CODIGO_MARCA) VALUES (?, ?, ?, ?, ?);",
            (codigo, descripcion, precio, codigo_sucursal, codigo_marca),
        )
        conn.commit()
    finally:
        conn.close()


def eliminar_producto(codigo_producto):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM producto WHERE CODIGO_PRODUCTO = ?;", (codigo_producto,))
    conn.commit()
    conn.close()


def actualizar_stock_sucursal_por_producto(codigo_producto, nuevo_stock):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.CODIGO_SUCURSAL
        FROM producto p
        JOIN sucursal s ON p.CODIGO_SUCURSAL = s.CODIGO_SUCURSAL
        WHERE p.CODIGO_PRODUCTO = ?;
        """,
        (codigo_producto,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        raise ValueError("Producto no encontrado")
    codigo_sucursal = row[0]
    cur.execute("UPDATE sucursal SET STOCK = ? WHERE CODIGO_SUCURSAL = ?;", (nuevo_stock, codigo_sucursal))
    conn.commit()
    conn.close()

def main():
    init_db()

    root = tk.Tk()
    root.title("Presentador de Consultas SQL - Valery Shoes")
    root.geometry("1000x600")

    frame_filtros = ttk.Frame(root, padding=8)
    frame_filtros.pack(fill="x")

    ttk.Label(frame_filtros, text="Sucursal:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
    sucursales = ["(Todas)"] + obtener_sucursales()
    combo_sucursal = ttk.Combobox(frame_filtros, values=sucursales, state="readonly", width=20)
    combo_sucursal.current(0)
    combo_sucursal.grid(row=0, column=1, padx=6, pady=6)

    ttk.Label(frame_filtros, text="Marca:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
    marcas = ["(Todas)"] + obtener_marcas()
    combo_marca = ttk.Combobox(frame_filtros, values=marcas, state="readonly", width=20)
    combo_marca.current(0)
    combo_marca.grid(row=0, column=3, padx=6, pady=6)

    def cargar_datos():
        sucursal_sel = combo_sucursal.get()
        marca_sel = combo_marca.get()

        sucursal_filtro = None if sucursal_sel == "(Todas)" else sucursal_sel
        marca_filtro = None if marca_sel == "(Todas)" else marca_sel

        try:
            rows = obtener_productos(sucursal_filtro, marca_filtro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar la base de datos:\n{e}")
            return

        # Limpiar tabla
        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

    boton_cargar = ttk.Button(frame_filtros, text="Cargar datos", command=cargar_datos)
    boton_cargar.grid(row=0, column=4, padx=8, pady=6)

    frame_gestion = ttk.Labelframe(root, text="Gestión de productos", padding=8)
    frame_gestion.pack(fill="x", padx=8, pady=6)

    ttk.Label(frame_gestion, text="Código producto:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    entry_codigo = ttk.Entry(frame_gestion, width=10)
    entry_codigo.grid(row=0, column=1, sticky="w", padx=6, pady=4)

    ttk.Label(frame_gestion, text="Descripción:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
    entry_desc = ttk.Entry(frame_gestion, width=40)
    entry_desc.grid(row=0, column=3, sticky="w", padx=6, pady=4)

    ttk.Label(frame_gestion, text="Marca:").grid(row=1, column=2, sticky="w", padx=6, pady=4)
    combo_marca_g = ttk.Combobox(frame_gestion, values=obtener_marcas(), state="readonly", width=25)
    combo_marca_g.grid(row=1, column=3, sticky="w", padx=6, pady=4)
    if combo_marca_g['values']:
        combo_marca_g.current(0)

    ttk.Label(frame_gestion, text="Precio:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    entry_precio = ttk.Entry(frame_gestion, width=12)
    entry_precio.grid(row=1, column=1, sticky="w", padx=6, pady=4)

    ttk.Label(frame_gestion, text="Sucursal:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
    combo_sucursal_g = ttk.Combobox(frame_gestion, values=obtener_sucursales(), state="readonly", width=20)
    combo_sucursal_g.grid(row=0, column=5, sticky="w", padx=6, pady=4)
    if combo_sucursal_g['values']:
        combo_sucursal_g.current(0)

    boton_agregar = ttk.Button(frame_gestion, text="Agregar producto")
    boton_agregar.grid(row=1, column=5, padx=6, pady=4)

    boton_eliminar = ttk.Button(frame_gestion, text="Eliminar producto seleccionado")
    boton_eliminar.grid(row=2, column=0, padx=6, pady=6)

    ttk.Label(frame_gestion, text="Nuevo stock para sucursal del producto seleccionado:").grid(row=2, column=2, sticky="w", padx=6, pady=6)
    entry_nuevo_stock = ttk.Entry(frame_gestion, width=10)
    entry_nuevo_stock.grid(row=2, column=3, sticky="w", padx=6, pady=6)

    boton_actualizar_stock = ttk.Button(frame_gestion, text="Actualizar stock sucursal")
    boton_actualizar_stock.grid(row=2, column=5, padx=6, pady=6)

    frame_tabla = ttk.Frame(root, padding=6)
    frame_tabla.pack(fill="both", expand=True, padx=8, pady=4)

    columnas = ("CODIGO_PRODUCTO", "DESCRIPCION", "PRECIO", "SUCURSAL", "MARCA", "STOCK")
    global tree
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

    for col in columnas:
        tree.heading(col, text=col)
        if col in ("CODIGO_PRODUCTO", "PRECIO", "STOCK"):
            tree.column(col, width=110, anchor="center")
        elif col in ("SUCURSAL", "MARCA"):
            tree.column(col, width=160, anchor="center")
        else:
            tree.column(col, width=380, anchor="w")

    # Scrollbars
    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True, side="left")

    def on_agregar():
        codigo_text = entry_codigo.get().strip()
        desc = entry_desc.get().strip()
        precio_text = entry_precio.get().strip()
        suc = combo_sucursal_g.get().strip()
        marca = combo_marca_g.get().strip()

        if not (codigo_text and desc and precio_text and suc and marca):
            messagebox.showwarning("Datos incompletos", "Debe completar todos los campos para agregar.")
            return

        try:
            codigo = int(codigo_text)
            precio = float(precio_text)
        except ValueError:
            messagebox.showerror("Error", "Código debe ser entero y Precio numérico.")
            return

        try:
            agregar_producto(codigo, desc, precio, suc, marca)
            messagebox.showinfo("OK", "Producto agregado correctamente.")
            cargar_datos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un producto con ese código.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto:\n{e}")

    def on_eliminar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Seleccione un producto en la tabla para eliminar.")
            return
        item = tree.item(sel[0])
        codigo = item['values'][0]
        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar el producto {codigo}?")
        if not respuesta:
            return
        try:
            eliminar_producto(codigo)
            messagebox.showinfo("OK", "Producto eliminado.")
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def on_actualizar_stock():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Seleccione un producto en la tabla para actualizar stock.")
            return
        nuevo = entry_nuevo_stock.get().strip()
        if not nuevo:
            messagebox.showwarning("Dato faltante", "Ingrese el nuevo stock (valor entero).")
            return
        try:
            nuevo_stock = int(nuevo)
        except ValueError:
            messagebox.showerror("Error", "Stock debe ser un número entero.")
            return
        item = tree.item(sel[0])
        codigo = item['values'][0]
        try:
            actualizar_stock_sucursal_por_producto(codigo, nuevo_stock)
            messagebox.showinfo("OK", "Stock actualizado en la sucursal asociada.")
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar stock:\n{e}")

    boton_agregar.config(command=on_agregar)
    boton_eliminar.config(command=on_eliminar)
    boton_actualizar_stock.config(command=on_actualizar_stock)

    def on_row_double_click(event):
        sel = tree.selection()
        if not sel:
            return
        item = tree.item(sel[0])
        codigo, desc, precio, suc, marca, stock = item['values']
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, str(codigo))
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, desc)
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, str(precio))
        try:
            combo_sucursal_g.set(suc)
        except Exception:
            pass
        try:
            combo_marca_g.set(marca)
        except Exception:
            pass
        entry_nuevo_stock.delete(0, tk.END)
        entry_nuevo_stock.insert(0, str(stock))

    tree.bind("<Double-1>", on_row_double_click)

    cargar_datos()

    root.mainloop()


if __name__ == "__main__":
    main()
