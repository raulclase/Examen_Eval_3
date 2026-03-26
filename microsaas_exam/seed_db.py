import sqlite3
DB = "saas.db"
conn = sqlite3.connect(DB); c = conn.cursor()
# Usuarios
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
# Clientes
c.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    email TEXT
)
""")
# Productos
c.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio REAL
)
""")
# Pedidos
c.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    fecha TEXT,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")
# Líneas de pedido (estructura preparada)
c.execute("""
CREATE TABLE IF NOT EXISTS lineas_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")

# Datos si están vacíos
c.execute("SELECT COUNT(*) FROM usuarios")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO usuarios (username,password) VALUES (?,?)", ("raul","1234"))

c.execute("SELECT COUNT(*) FROM clientes")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO clientes (nombre,email) VALUES (?,?)", [
        ("Acme SL", "ventas@acme.test"),
        ("ValenSoft", "info@valensoft.test"),
        ("Naranjas Premium", "contacto@naranjas.test")
    ])

c.execute("SELECT COUNT(*) FROM productos")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO productos (nombre,precio) VALUES (?,?)", [
        ("Suscripción Básica", 9.90),
        ("Suscripción Pro", 29.90),
        ("Soporte Premium", 49.00)
    ])

c.execute("SELECT COUNT(*) FROM pedidos")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO pedidos (cliente_id,fecha) VALUES (?,?)", [
        (1, "2026-02-21"),
        (2, "2026-02-22")
    ])
    c.executemany("INSERT INTO lineas_pedido (pedido_id,producto_id,cantidad) VALUES (?,?,?)", [
        (1,1,1), (1,2,1), (2,3,2)
    ])

conn.commit(); conn.close()
print("✔ saas.db lista con datos de ejemplo")
