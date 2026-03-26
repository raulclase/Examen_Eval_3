from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey_change_me"
DB = "saas.db"

# --- helpers ---
def get_db():
    conn = sqlite3.connect(DB)
    return conn

def require_login():
    return "user" in session

# --- auth ---
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username","" ).strip()
    password = request.form.get("password","" )
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id FROM usuarios WHERE username=? AND password=?", (username, password))
    ok = c.fetchone()
    conn.close()
    if ok:
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="Credenciales incorrectas")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- dashboard ---
@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# --- CLIENTES ---
@app.route("/clientes")
def clientes():
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id,nombre,email FROM clientes ORDER BY id")
    data = c.fetchall(); conn.close()
    return render_template("clientes.html", clientes=data)

@app.route("/clientes/add", methods=["GET","POST"])
def cliente_add():
    if not require_login():
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form.get("nombre").strip()
        email = request.form.get("email").strip()
        conn = get_db(); c = conn.cursor()
        c.execute("INSERT INTO clientes (nombre,email) VALUES (?,?)", (nombre,email))
        conn.commit(); conn.close()
        return redirect(url_for("clientes"))
    return render_template("cliente_form.html", cliente=None)

@app.route("/clientes/edit/<int:id>", methods=["GET","POST"])
def cliente_edit(id):
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre").strip()
        email = request.form.get("email").strip()
        c.execute("UPDATE clientes SET nombre=?, email=? WHERE id=?", (nombre,email,id))
        conn.commit(); conn.close()
        return redirect(url_for("clientes"))
    c.execute("SELECT id,nombre,email FROM clientes WHERE id=?", (id,))
    cliente = c.fetchone(); conn.close()
    return render_template("cliente_form.html", cliente=cliente)

@app.route("/clientes/delete/<int:id>")
def cliente_delete(id):
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit(); conn.close()
    return redirect(url_for("clientes"))

# --- PRODUCTOS ---
@app.route("/productos")
def productos():
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id,nombre,precio FROM productos ORDER BY id")
    data = c.fetchall(); conn.close()
    return render_template("productos.html", productos=data)

@app.route("/productos/add", methods=["GET","POST"])
def producto_add():
    if not require_login():
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form.get("nombre").strip()
        precio = float(request.form.get("precio", 0))
        conn = get_db(); c = conn.cursor()
        c.execute("INSERT INTO productos (nombre,precio) VALUES (?,?)", (nombre,precio))
        conn.commit(); conn.close()
        return redirect(url_for("productos"))
    return render_template("producto_form.html", producto=None)

@app.route("/productos/edit/<int:id>", methods=["GET","POST"])
def producto_edit(id):
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre").strip()
        precio = float(request.form.get("precio", 0))
        c.execute("UPDATE productos SET nombre=?, precio=? WHERE id=?", (nombre,precio,id))
        conn.commit(); conn.close()
        return redirect(url_for("productos"))
    c.execute("SELECT id,nombre,precio FROM productos WHERE id=?", (id,))
    producto = c.fetchone(); conn.close()
    return render_template("producto_form.html", producto=producto)

@app.route("/productos/delete/<int:id>")
def producto_delete(id):
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit(); conn.close()
    return redirect(url_for("productos"))

# --- PEDIDOS (sin líneas) ---
@app.route("/pedidos")
def pedidos():
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("""
        SELECT pedidos.id, clientes.nombre, pedidos.fecha
        FROM pedidos JOIN clientes ON clientes.id = pedidos.cliente_id
        ORDER BY pedidos.id
    """)
    data = c.fetchall(); conn.close()
    return render_template("pedidos.html", pedidos=data)

@app.route("/pedidos/add", methods=["GET","POST"])
def pedido_add():
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    if request.method == "POST":
        cliente_id = int(request.form.get("cliente_id"))
        fecha = request.form.get("fecha")
        c.execute("INSERT INTO pedidos (cliente_id, fecha) VALUES (?,?)", (cliente_id, fecha))
        conn.commit(); conn.close()
        return redirect(url_for("pedidos"))
    c.execute("SELECT id,nombre FROM clientes ORDER BY nombre")
    clientes = c.fetchall(); conn.close()
    return render_template("pedido_form.html", clientes=clientes)

@app.route("/pedidos/delete/<int:id>")
def pedido_delete(id):
    if not require_login():
        return redirect(url_for("login"))
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM lineas_pedido WHERE pedido_id=?", (id,))
    c.execute("DELETE FROM pedidos WHERE id=?", (id,))
    conn.commit(); conn.close()
    return redirect(url_for("pedidos"))

if __name__ == "__main__":
    app.run(debug=True)
