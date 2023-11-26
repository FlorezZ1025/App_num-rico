import tkinter as tk
import numpy as np
from tkinter import ttk
import sympy as sp
from modulos import rutinas as r
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ventana_principal = tk.Tk()
ventana_principal.title("Aplicación de Análisis Numérico")

ttk.Label(
    ventana_principal, text="¡Bienvenido a la Aplicación de Análisis Numérico!"
).grid(row=0, column=1, columnspan=3, pady=10)

ttk.Label(ventana_principal, text="Seleccione un tema:").grid(
    row=1, column=2, columnspan=2, padx=10, pady=5, sticky="w"
)


def tema_taylor():
    ventana_tema_1 = tk.Toplevel(ventana_principal)
    ventana_tema_1.title("Taylor")
    ventana_tema_1.geometry("800x700")

    valores_parametros = []
    entry_widgets = []

    ttk.Label(ventana_tema_1, text="Ingrese la función:").grid(
        row=1, column=0, padx=10, pady=5, sticky="w"
    )
    entry_funcion = ttk.Entry(ventana_tema_1)
    entry_funcion.grid(row=1, column=1, padx=10, pady=5)

    etq1 = ttk.Label(ventana_tema_1, text="Ingrese x0:")
    etq1.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    entry_parametro = ttk.Entry(ventana_tema_1)
    entry_parametro.grid(row=2, column=1, columnspan=3, padx=10, pady=5)
    valores_parametros.append(entry_parametro)

    etq2 = ttk.Label(ventana_tema_1, text="Ingrese n:")
    etq2.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    entry_parametro = ttk.Entry(ventana_tema_1)
    entry_parametro.grid(row=3, column=1, columnspan=3, padx=10, pady=5)
    valores_parametros.append(entry_parametro)

    def ejecutar_taylor():
        try:
            p_i = [eval(param.get()) for param in valores_parametros]

            x = sp.symbols("x")
            funcion = eval(entry_funcion.get())
            polinomio = r.taylor(funcion, p_i[0], p_i[1])

            funcion = sp.lambdify(x, funcion)

            resultado_label.config(text=f"El polinomio de taylor es: {polinomio}")
            polinomio = sp.lambdify(x, polinomio)

            mostrar_grafica(funcion, polinomio, p_i[0], p_i[0] + 4, ventana_tema_1)
        except Exception as e:
            resultado_label.config(text=f"Error ==> {e}")

    def mostrar_grafica(funcion, polinomio, a, b, ventana):
        x_vals = np.linspace(a, b, 100)
        y_vals = [funcion(x) for x in x_vals]

        figura, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="Función")
        ax.plot(x_vals, polinomio(x_vals), label="Polinomio")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

        canvas = FigureCanvasTkAgg(figura, master=ventana)
        canvas_widget = canvas.get_tk_widget()
        entry_widgets.append(canvas_widget)
        canvas_widget.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    ttk.Button(
        ventana_tema_1,
        text="Crear Polinomio",
        command=lambda: ejecutar_taylor(),
    ).grid(row=9, column=1, columnspan=2, pady=10)

    resultado_label = ttk.Label(ventana_tema_1, text="")
    resultado_label.grid(row=8, column=1, columnspan=4, pady=10)


def tema_ceros():
    ventana_tema_2 = tk.Toplevel(ventana_principal)
    ventana_tema_2.title("Ceros")
    ventana_tema_2.geometry("800x700")
    combobox_var = tk.StringVar()
    combobox_var.set("----")

    temas_info = {
        "Biseccion": ["a", "b", "tol"],
        "Posicion falsa": ["a", "b", "tol"],
        "Newton": ["x0", "tol"],
        "Secante": ["x0", "x1", "tol"],
    }

    def on_combobox_select(event):
        for entry_widget in entry_widgets:
            entry_widget.destroy()
        resultado_label.config(text="")

        seleccion = combobox_var.get()
        parametros = temas_info.get(seleccion, [])

        ttk.Label(ventana_tema_2, text="Ingrese la función:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        entry_funcion = ttk.Entry(ventana_tema_2)
        entry_funcion.grid(row=1, column=1, padx=10, pady=5)

        valores_parametros = []

        for i, parametro in enumerate(parametros):
            etq = ttk.Label(ventana_tema_2, text=f"Ingrese {parametro}:")
            etq.grid(row=i + 2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            entry_parametro = ttk.Entry(ventana_tema_2)
            entry_parametro.grid(row=i + 2, column=1, columnspan=3, padx=10, pady=5)
            valores_parametros.append(entry_parametro)
            entry_widgets.append(entry_parametro)
            entry_widgets.append(etq)

        def ejecutar_analisis():
            parametros_ingresados = [param.get() for param in valores_parametros]

            try:
                if seleccion == "Biseccion":
                    funcion = lambda x: eval(entry_funcion.get())
                    p_i = [eval(p) for p in parametros_ingresados]

                    resultado = r.Biseccion(funcion, p_i[0], p_i[1], p_i[2])
                    mostrar_grafica(funcion, p_i[0], p_i[1], ventana_tema_2, resultado)
                    resultado_label.config(text=f"Resultado: {resultado}")

                elif seleccion == "Posicion falsa":
                    funcion = lambda x: eval(entry_funcion.get())
                    p_i = [eval(p) for p in parametros_ingresados]

                    resultado = r.Pos_falsa(funcion, p_i[0], p_i[1], p_i[2])
                    mostrar_grafica(funcion, p_i[0], p_i[1], ventana_tema_2, resultado)
                    resultado_label.config(text=f"Resultado: {resultado}")

                elif seleccion == "Secante":
                    funcion = lambda x: eval(entry_funcion.get())
                    p_i = [eval(p) for p in parametros_ingresados]

                    resultado = r.Secante(funcion, p_i[0], p_i[1], p_i[2])
                    mostrar_grafica(funcion, p_i[0], p_i[1], ventana_tema_2, resultado)
                    resultado_label.config(text=f"Resultado: {resultado}")

                elif seleccion == "Newton":
                    x = sp.symbols("x")
                    f = eval(entry_funcion.get())
                    print(f)
                    p_i = [eval(p) for p in parametros_ingresados]
                    funcion = lambda x: eval(entry_funcion.get())

                    resultado = r.Newton(f, p_i[0], p_i[1])
                    f = sp.lambdify(x, f)
                    mostrar_grafica(f, p_i[0], p_i[0] + 5, ventana_tema_2, resultado)
                    resultado_label.config(text=f"Resultado: {resultado}")

            except Exception as e:
                resultado_label.config(text=f"Error ==> {e}")

        def mostrar_grafica(funcion, a, b, ventana, resultado):
            x_vals = np.linspace(a, b, 100)
            y_vals = [funcion(x) for x in x_vals]

            figura, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="Función")

            punto_x = resultado
            punto_y = funcion(resultado)
            ax.scatter([punto_x], [punto_y], color="red", marker="D", label="Raíz")
            ax.axvline(
                x=float(resultado),
                color="purple",
                linestyle="--",
            )

            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()

            canvas = FigureCanvasTkAgg(figura, master=ventana)
            canvas_widget = canvas.get_tk_widget()
            entry_widgets.append(canvas_widget)
            canvas_widget.grid(
                row=len(parametros) + 3, column=0, columnspan=2, padx=10, pady=5
            )

        ttk.Button(
            ventana_tema_2,
            text="Solucionar",
            command=lambda: ejecutar_analisis(),
        ).grid(row=9, column=1, columnspan=2, pady=10)

    etiqueta_metodo = ttk.Label(ventana_tema_2, text="Selecciona el método:")
    etiqueta_metodo.grid(row=0, column=0, padx=5, pady=10)

    tema_combobox = ttk.Combobox(
        ventana_tema_2,
        values=[
            "Biseccion",
            "Posicion falsa",
            "Newton",
            "Secante",
        ],
        textvariable=combobox_var,
    )
    tema_combobox.grid(row=0, column=1, padx=10, pady=5)
    tema_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    entry_widgets = []

    resultado_label = ttk.Label(ventana_tema_2, text="Resultados aquí")
    resultado_label.grid(row=8, column=0, columnspan=4, pady=10)


def tema_interpolacion():
    ventana_tema_3 = tk.Toplevel(ventana_principal)
    ventana_tema_3.title("Interpolacion")
    ventana_tema_3.geometry("800x700")

    temas_info = {
        "Polinomio simple": ["xdata", "ydata"],
        "Lagrange": ["xdata", "ydata"],
    }

    etiqueta_metodo = ttk.Label(ventana_tema_3, text="Selecciona:")
    etiqueta_metodo.grid(row=0, column=0, padx=5, pady=10)

    combobox_var = tk.StringVar()
    combobox_var.set("----")

    def on_combobox_select(event):
        for entry_widget in entry_widgets:
            entry_widget.destroy()
        resultado_label.config(text="")

        seleccion = combobox_var.get()
        parametros = temas_info.get(seleccion, [])

        valores_parametros = []

        for i, parametro in enumerate(parametros):
            etq = ttk.Label(ventana_tema_3, text=f"Ingrese {parametro}:")
            etq.grid(row=i + 2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            entry_parametro = ttk.Entry(ventana_tema_3)
            entry_parametro.grid(row=i + 2, column=1, columnspan=3, padx=10, pady=5)
            valores_parametros.append(entry_parametro)
            entry_widgets.append(entry_parametro)
            entry_widgets.append(etq)

        def ejecutar_analisis():
            try:
                p_i = [param.get() for param in valores_parametros]
                xd = np.array([eval(x) for x in p_i[0].split(",")])
                yd = np.array([eval(y) for y in p_i[1].split(",")])
                if seleccion == "Polinomio simple":
                    x = sp.symbols("x")
                    polinomio = r.p_simple(xd, yd)
                    resultado_label.config(text=f"Polinomio: {polinomio}")

                    polinomio = sp.lambdify(x, polinomio)
                    mostrar_grafica(polinomio, xd, yd, ventana_tema_3)

                elif seleccion == "Lagrange":
                    x = sp.symbols("x")
                    p_lagrange = r.lagrange(xd, yd)
                    resultado_label.config(text=f"Polinomio: {p_lagrange}")

                    p_lagrange = sp.lambdify(x, p_lagrange)
                    mostrar_grafica(p_lagrange, xd, yd, ventana_tema_3)
            except Exception as e:
                resultado_label.config(text=f"Error ==> {e}")
                print(f"Error --> {e}")

        def mostrar_grafica(polinomio, xd, yd, ventana):
            x_vals = np.linspace(min(xd), max(xd), 500)
            y_vals = [polinomio(x) for x in x_vals]

            figura, ax = plt.subplots()
            ax.scatter(xd, yd, color="blue", marker="D", label="Puntos")
            ax.plot(x_vals, y_vals, label="Polinomio simple")

            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()

            canvas = FigureCanvasTkAgg(figura, master=ventana)
            canvas_widget = canvas.get_tk_widget()
            entry_widgets.append(canvas_widget)
            canvas_widget.grid(
                row=len(parametros) + 3, column=0, columnspan=2, padx=10, pady=5
            )

        ttk.Button(
            ventana_tema_3,
            text="Solucionar",
            command=lambda: ejecutar_analisis(),
        ).grid(row=9, column=1, columnspan=2, pady=10)

    tema_combobox = ttk.Combobox(
        ventana_tema_3,
        values=["Polinomio simple", "Lagrange"],
        textvariable=combobox_var,
    )
    tema_combobox.grid(row=0, column=1, padx=10, pady=5)
    tema_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    entry_widgets = []

    resultado_label = ttk.Label(ventana_tema_3, text="")
    resultado_label.grid(row=8, column=3, columnspan=4, pady=10)


def tema_ED():
    ventana_tema_4 = tk.Toplevel(ventana_principal)
    ventana_tema_4.title("E.D")
    ventana_tema_4.geometry("800x700")

    temas_info = {"Euler": ["a", "b", "h", "co"], "Runge Kuta": ["a", "b", "h", "co"]}
    etiqueta_metodo = ttk.Label(ventana_tema_4, text="Selecciona:")
    etiqueta_metodo.grid(row=0, column=0, padx=5, pady=10)

    combobox_var = tk.StringVar()
    combobox_var.set("----")

    def on_combobox_select(event):
        for entry_widget in entry_widgets:
            entry_widget.destroy()
        resultado_label.config(text="")

        seleccion = combobox_var.get()
        parametros = temas_info.get(seleccion, [])

        ttk.Label(ventana_tema_4, text="Ingrese la función:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        entry_funcion = ttk.Entry(ventana_tema_4)
        entry_funcion.grid(row=1, column=1, padx=10, pady=5)

        valores_parametros = []

        for i, parametro in enumerate(parametros):
            etq = ttk.Label(ventana_tema_4, text=f"Ingrese {parametro}:")
            etq.grid(row=i + 2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            entry_parametro = ttk.Entry(ventana_tema_4)
            entry_parametro.grid(row=i + 2, column=1, columnspan=3, padx=10, pady=5)
            valores_parametros.append(entry_parametro)
            entry_widgets.append(entry_parametro)
            entry_widgets.append(etq)

        def ejecutar_analisis():
            resultado_label.config(text="")
            try:
                p_i = [eval(p.get()) for p in valores_parametros]
                funcion = lambda t, y: eval(entry_funcion.get())

                if seleccion == "Euler":
                    t, e = r.Euler(funcion, p_i[0], p_i[1], p_i[2], p_i[3])
                    mostrar_grafica(t, e, ventana_tema_4)

                elif seleccion == "Runge Kuta":
                    t, k = r.Runge4(funcion, p_i[0], p_i[1], p_i[2], p_i[3])
                    mostrar_grafica(t, k, ventana_tema_4)

            except Exception as e:
                resultado_label.config(text=f"{e}")

        def mostrar_grafica(t, e, ventana):
            figura, ax = plt.subplots()

            ax.scatter(t, e, color="blue", marker="D", label="Puntos")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()

            canvas = FigureCanvasTkAgg(figura, master=ventana)
            canvas_widget = canvas.get_tk_widget()
            entry_widgets.append(canvas_widget)
            canvas_widget.grid(
                row=len(parametros) + 3, column=0, columnspan=2, padx=10, pady=5
            )

        ttk.Button(
            ventana_tema_4,
            text="Solucionar",
            command=lambda: ejecutar_analisis(),
        ).grid(row=9, column=1, columnspan=2, pady=10)

    etiqueta_metodo = ttk.Label(ventana_tema_4, text="Selecciona el método:")
    etiqueta_metodo.grid(row=0, column=0, padx=5, pady=10)

    tema_combobox = ttk.Combobox(
        ventana_tema_4,
        values=[
            "Euler",
            "Runge Kuta",
        ],
        textvariable=combobox_var,
    )
    tema_combobox.grid(row=0, column=1, padx=10, pady=5)
    tema_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    entry_widgets = []

    resultado_label = ttk.Label(ventana_tema_4, text="Resultados aquí")
    resultado_label.grid(row=8, column=0, columnspan=4, pady=10)


def tema_IN():
    ventana_tema_5 = tk.Toplevel(ventana_principal)
    ventana_tema_5.title("Integración numérica")
    ventana_tema_5.geometry("600x500")

    temas_info = {
        "Trapecio": ["a", "b", "n"],
        "Simpson 1/3": ["a", "b", "n (Par)"],
        "Simpson 3/8": ["a", "b", "n"],
    }

    etiqueta_metodo = ttk.Label(ventana_tema_5, text="Selecciona:")
    etiqueta_metodo.grid(row=0, column=0, padx=5, pady=10)

    combobox_var = tk.StringVar()
    combobox_var.set("----")

    def on_combobox_select(event):
        for entry_widget in entry_widgets:
            entry_widget.destroy()
        resultado_label.config(text="")

        seleccion = combobox_var.get()
        parametros = temas_info.get(seleccion, [])
        ttk.Label(ventana_tema_5, text="Ingrese la función:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        entry_funcion = ttk.Entry(ventana_tema_5)
        entry_funcion.grid(row=1, column=1, padx=10, pady=5)

        valores_parametros = []

        for i, parametro in enumerate(parametros):
            etq = ttk.Label(ventana_tema_5, text=f"Ingrese {parametro}:")
            etq.grid(row=i + 2, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            entry_parametro = ttk.Entry(ventana_tema_5)
            entry_parametro.grid(row=i + 2, column=1, columnspan=3, padx=10, pady=5)
            valores_parametros.append(entry_parametro)
            entry_widgets.append(entry_parametro)
            entry_widgets.append(etq)

        def ejecutar_analisis():
            try:
                p_i = [eval(p.get()) for p in valores_parametros]
                funcion = lambda x: eval(entry_funcion.get())

                if seleccion == "Trapecio":
                    resultado = r.Trapecio(funcion, p_i[0], p_i[1], p_i[2])
                    resultado_label.config(text=f"Resultado: {resultado}")

                elif seleccion == "Simpson 1/3":
                    resultado = r.simpson1_3(funcion, p_i[0], p_i[1], p_i[2])
                    resultado_label.config(text=f"Resultado: {resultado}")

                elif seleccion == "Simpson 3/8":
                    resultado = r.simpson3_8(funcion, p_i[0], p_i[1], p_i[2])
                    resultado_label.config(text=f"Resultado: {resultado}")

            except Exception as e:
                resultado_label.config(text=f"Error ==> {e}")
                print(f"Error --> {e}")

        ttk.Button(
            ventana_tema_5,
            text="Solucionar",
            command=lambda: ejecutar_analisis(),
        ).grid(row=9, column=1, columnspan=2, pady=10)

    tema_combobox = ttk.Combobox(
        ventana_tema_5,
        values=["Trapecio", "Simpson 1/3", "Simpson 3/8"],
        textvariable=combobox_var,
    )
    tema_combobox.grid(row=0, column=1, padx=10, pady=5)
    tema_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    entry_widgets = []

    resultado_label = ttk.Label(ventana_tema_5, text="")
    resultado_label.grid(row=8, column=1, columnspan=4, pady=10)


ttk.Button(ventana_principal, text="Taylor", command=tema_taylor).grid(
    row=3, column=0, pady=10
)
ttk.Button(ventana_principal, text="Ceros", command=tema_ceros).grid(
    row=3, column=1, pady=10
)
ttk.Button(ventana_principal, text="Interpolacion", command=tema_interpolacion).grid(
    row=3, column=2, pady=10
)
ttk.Button(ventana_principal, text="E.D", command=tema_ED).grid(
    row=3, column=3, pady=10
)
ttk.Button(ventana_principal, text="Integración numérica", command=tema_IN).grid(
    row=3, column=4, pady=10
)


ventana_principal.mainloop()
