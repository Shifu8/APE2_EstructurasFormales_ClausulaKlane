from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------- FUNCIONES --------

def generar_cadenas(alfabeto, max_len):
    resultado = [""]
    for _ in range(max_len):
        nuevas = []
        for cadena in resultado:
            for simbolo in alfabeto:
                nuevas.append(cadena + simbolo)
        resultado.extend(nuevas)
    return list(set(resultado))


def pertenece(cadena, lenguaje):
    return cadena in lenguaje


def union(L1, L2):
    return list(set(L1) | set(L2))


def concatenacion(L1, L2):
    return [x + y for x in L1 for y in L2]


def kleene_star(L, max_iter):
    resultado = [""]
    actual = [""]

    for _ in range(max_iter):
        nuevo = []
        for x in actual:
            for y in L:
                nuevo.append(x + y)

        resultado.extend(nuevo)
        actual = nuevo

    return list(set(resultado))


def kleene_plus(L, max_iter):
    return [x for x in kleene_star(L, max_iter) if x != ""]


def analizar_crecimiento(L, max_iter):
    resultado = []
    for i in range(1, max_iter + 1):
        cantidad = len(kleene_star(L, i))
        resultado.append(f"Iteración {i}: {cantidad} cadenas")
    return resultado


# -------- RUTAS --------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.json
    opcion = data["opcion"]

    if opcion == "generar":
        alfabeto = data["alfabeto"].split(",")
        n = int(data["n"])
        res = generar_cadenas(alfabeto, n)

    elif opcion == "pertenece":
        cadena = data["cadena"]
        lenguaje = data["lenguaje"].split(",")
        res = pertenece(cadena, lenguaje)

    elif opcion == "union":
        L1 = data["L1"].split(",")
        L2 = data["L2"].split(",")
        res = union(L1, L2)

    elif opcion == "concatenacion":
        L1 = data["L1"].split(",")
        L2 = data["L2"].split(",")
        res = concatenacion(L1, L2)

    elif opcion == "kleene":
        L = data["L"].split(",")
        n = int(data["n"])
        res = kleene_star(L, n)

    elif opcion == "kleene_plus":
        L = data["L"].split(",")
        n = int(data["n"])
        res = kleene_plus(L, n)

    elif opcion == "crecimiento":
        L = data["L"].split(",")
        n = int(data["n"])
        res = analizar_crecimiento(L, n)

    else:
        res = "Opción no válida"

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
