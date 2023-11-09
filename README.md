## Practica 5: Login Flask

### Jinja
Jinja es una herramienta útil para utilizar un archivo base HTML, y se puede agregar código a partir del uso de bloques de código sustituible a modo de variables.

Al usar la estructura:

    {%block name%}
    {%endblock%}

Se puede heredar el código establecido y extender a partir de ahí en otro documento separado.

Por ejemplo, tener la estructura general de una página y agregar documentos varios que construyan distintos apartados de la página a partir de esta estética base.

    {%extends 'dirección'%}
    {%block name%}
        <codigo agregado>
    {%endblock%}

### Formulario

En esta práctica se debe generar una pantalla de login donde se deba ingresar las credenciales establecidas y entrar a otra página o mantenerse en la misma si no son aceptadas. Para ello se usa el método `POST`.

Se importan las librerías de `Flask`, `render_template`, `redirect` y `url_for`. El método `POST` se llama desde el HTML en la etiqueta `<form>`

Se le asignan los atributos `action="/login"` y `method="POST"` para indicar que se enviarán al servidor los elementos contenidos en el formulario. Lo que se envía son los inputs, y se debe tener en cuenta que el atributo `id` NO identifica el elemento enviado, sino que su atributo `name` lo hace, por lo que al manejar los parámetros enviados al servidor se deberá usar el nombre asignado en el atributo ´name´.

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            _user = request.form["username"]
            _pass = request.form["password"]
            print(_user)
            print(_pass)
            if _user == "admin" and _pass == "123":
                return redirect(url_for("home"))
            else:
                return render_template("auth/login.html")
        else:
            return render_template("auth/login.html")

Este es el código usado en el archivo `app.py`, a continuación se detalla el uso de partes importantes de este código.

    @app.route("/login", methods=["GET", "POST"])

Se define la ruta en /login y se indica que se espera que se usen los métodos GET y POST para enviar y recuperar información del servidor.

    if request.method == "POST":

Verifica que el tipo de método sea `POST`, lo que indica que se ha subido información al servidor.

    _user = request.form["username"]
    _pass = request.form["password"]

Desde los formularios, se toma los valores del `input` con el atributo `name` y se guardan en variables.

    return redirect(url_for("home"))
    return render_template("auth/login.html")

Regresa la página asignada a cada caso. `url_for("home")` ejecuta la función `home`, la que ingresa a la página de inicio cuando se cumplen las credenciales. `render_template("auth/login.html")` regresa a la página de login cuando las credenciales no se cumplan.