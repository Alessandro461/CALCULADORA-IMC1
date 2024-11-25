import flet as ft
from numpy import size


def calcular_imc(talla, peso):
    return peso / (talla**2)


def obtener_categoria_imc(imc):
    """
    Determine la categoría de IMC correspondiente a un valor dado.

    Parameters:
    imc (float): El índice de masa corporal a evaluar.

    Returns:
    str: La categoría de IMC correspondiente al valor dado.
         - 'Bajo peso' si el IMC es menor a 18.5.
         - 'Peso normal' si el IMC está entre 18.5 y 25.
         - 'Sobrepeso' si el IMC está entre 25 y 30.
         - 'Obesidad' si el IMC es mayor a 30.
    """
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"



def cargar_datos_desde_txt(archivo):
    """
    Carga datos de un archivo de texto y calcula el IMC y la categoría de cada persona.

    Parameters:
    archivo (str): La ruta del archivo de texto que contiene los datos de las personas.

    Returns:
    personas (list): Una lista de tuplas, donde cada tupla representa a una persona y contiene:
        - Talla (float)
        - Peso (float)
        - IMC (float)
        - Categoría (str)

    Raises:
    FileNotFoundError: Si el archivo no se encuentra en la ruta especificada.
    """
    personas = []
    try:
        with open(archivo, "r") as file:
            lineas = file.readlines()
            for linea in lineas:
                talla, peso = map(float, linea.strip().split("\t"))
                imc = calcular_imc(talla, peso)
                categoria = obtener_categoria_imc(imc)
                personas.append((talla, peso, imc, categoria))
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo}")
    return personas



def guardar_datos_en_txt(archivo, personas):
    with open(archivo, "w") as file:
        for talla, peso, *_ in personas:
            file.write(f"{talla}\t{peso}\n")


def crear_menu_lateral(on_menu_click, page):
    # Colores de resaltado para temas claros y oscuros
    color_hover_claro = "#d7e3f7"
    color_hover_oscuro = "#3b4858"

    def crear_item_menu(icon, label, menu_id):
        def on_hover(e):
            e.control.bgcolor = (
                color_hover_claro
                if page.theme_mode == ft.ThemeMode.LIGHT
                else color_hover_oscuro
            )
            if e.data == "false":
                e.control.bgcolor = None
            e.control.update()

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=30),
                    ft.Text(label, size=20),  ######################## tamaño
                ],
            ),
            padding=10,
            on_click=lambda e: on_menu_click(menu_id),
            on_hover=on_hover,
            data=menu_id,
            bgcolor=None,
            border_radius=8,
        )

    return ft.Container(
        width=200,
        padding=ft.padding.only(top=10),
        content=ft.Column(
            controls=[
                # Header del menú
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(
                                src="EEI.png",
                                width=70,
                                height=70,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("IMC", weight=ft.FontWeight.BOLD, size=24),
                                    ft.Text("Calculadora", size=20),  #########
                                ],
                            ),
                        ],
                    ),
                    padding=10,
                ),
                ft.Divider(height=5, color="transparent"),
                crear_item_menu(ft.icons.CREATE, "Ingresar Datos", "ingresar"),
                crear_item_menu(ft.icons.TABLE_CHART, "Procesar Datos", "procesar"),
                crear_item_menu(ft.icons.BRIGHTNESS_4, "Cambiar Tema", "tema"),
                crear_item_menu(ft.icons.EXIT_TO_APP, "Salir", "salir"),
            ],
        ),
    )


def crear_vista_ingreso(content, page, file_picker):
    content.content = None

    # Campos de entrada
    talla_input = ft.TextField(
        label="Talla (m)",
        width=300,
        label_style=ft.TextStyle(size=18),
        hint_text="Ejemplo: 1.75",
    )
    peso_input = ft.TextField(
        label="Peso (kg)",
        width=300,
        label_style=ft.TextStyle(size=18),
        hint_text="Ejemplo: 70.5",
    )
    archivo_input = ft.TextField(
        label="Nombre del archivo",
        width=300,
        label_style=ft.TextStyle(size=18),
        hint_text="Ingrese nombre del archivo",
    )

    # Tabla de datos
    data_table = ft.Column(
        [
            ft.Row(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("#", size=16, weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Talla (m)", size=16, weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Peso (kg)", size=16, weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("IMC", size=16, weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Categoría", size=16, weight=ft.FontWeight.BOLD)),
                        ],
                        rows=[],
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    def mostrar_mensaje(mensaje, es_error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.ERROR if es_error else ft.colors.GREEN,
        )
        page.snack_bar.open = True
        page.update()

    def validar_entrada(talla, peso):
        try:
            t = float(talla)
            p = float(peso)
            if t <= 0 or p <= 0:
                return False, "Los valores deben ser mayores que 0"
            if t > 2.5 or p > 300:
                return False, "Valores fuera de rango normal"
            return True, ""
        except ValueError:
            return False, "Por favor ingrese valores numéricos válidos"

    def calcular_categoria(imc):
        if imc < 18.5:
            return "Bajo peso"
        elif 18.5 <= imc < 24.9:
            return "Normal"
        elif 25 <= imc < 29.9:
            return "Sobrepeso"
        else:
            return "Obesidad"

    def cargar_datos_desde_txt(nombre_archivo):
        personas = []
        with open(nombre_archivo, "r") as file:
            for linea in file:
                talla, peso = map(float, linea.strip().split("\t"))
                personas.append((talla, peso))
        return personas

    def on_ingresar(e):
        if not archivo_input.value:
            mostrar_mensaje("Por favor ingrese un nombre de archivo", True)
            return

        valido, mensaje = validar_entrada(talla_input.value, peso_input.value)
        if not valido:
            mostrar_mensaje(mensaje, True)
            return

        talla = float(talla_input.value)
        peso = float(peso_input.value)

        # Cálculo del IMC
        imc = peso / (talla ** 2)
        categoria = calcular_categoria(imc)

        archivo = f"{archivo_input.value}.txt"
        try:
            with open(archivo, "a") as file:
                file.write(f"{talla}\t{peso}\n")

            # Agregar los datos ingresados al DataTable
            data_table.controls[0].controls[0].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(len(data_table.controls[0].controls[0].rows) + 1))),
                        ft.DataCell(ft.Text(f"{talla:.2f}")),
                        ft.DataCell(ft.Text(f"{peso:.2f}")),
                        ft.DataCell(ft.Text(f"{imc:.2f}")),
                        ft.DataCell(ft.Text(categoria)),
                    ]
                )
            )

            talla_input.value = ""
            peso_input.value = ""
            mostrar_mensaje("Datos guardados correctamente")
        except Exception as e:
            mostrar_mensaje(f"Error al guardar los datos: {str(e)}", True)

        content.update()

    def on_mostrar(e):
        if not archivo_input.value:
            mostrar_mensaje("Por favor ingrese un nombre de archivo", True)
            return

        archivo = f"{archivo_input.value}.txt"
        try:
            personas = cargar_datos_desde_txt(archivo)
            data_table.controls[0].controls[0].rows.clear()
            for idx, (talla, peso) in enumerate(personas, start=1):
                imc = peso / (talla ** 2)
                categoria = calcular_categoria(imc)
                data_table.controls[0].controls[0].rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(idx))),
                            ft.DataCell(ft.Text(f"{talla:.2f}")),
                            ft.DataCell(ft.Text(f"{peso:.2f}")),
                            ft.DataCell(ft.Text(f"{imc:.2f}")),
                            ft.DataCell(ft.Text(categoria)),
                        ]
                    )
                )
            content.update()
        except Exception as e:
            mostrar_mensaje(f"Error al cargar los datos: {str(e)}", True)

    # Layout de la vista
    content.content = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    controls=[
                        ft.Text("Ingreso de Datos", size=32, weight=ft.FontWeight.BOLD),
                        talla_input,
                        peso_input,
                        archivo_input,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Ingresar Datos",
                                    icon=ft.icons.ADD,
                                    on_click=on_ingresar,
                                    height=50,
                                    width=200,
                                ),
                                ft.ElevatedButton(
                                    "Mostrar Datos",
                                    icon=ft.icons.VIEW_LIST,
                                    on_click=on_mostrar,
                                    height=50,
                                    width=200,
                                ),
                            ],
                            spacing=20,
                        ),
                    ],
                    spacing=20,
                ),
                ft.VerticalDivider(),
                ft.Column(
                    [
                        ft.Text("Datos Ingresados", size=24, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=data_table,
                            height=400,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=10,
                            padding=10,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        ),
        padding=20,
    )
    content.update()



def crear_vista_procesar(content, page, file_picker):
    content.content = None

    # Tabla original con columna para índice
    data_table_original = ft.Column(
        [
            ft.Row(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(
                                ft.Text("Índice", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("Talla (m)", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("Peso (kg)", size=16, weight=ft.FontWeight.BOLD)
                            ),
                        ],
                        rows=[],
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # Tabla procesada con columna para índice
    data_table_procesada = ft.Column(
        [
            ft.Row(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(
                                ft.Text("Índice", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("Talla (m)", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("Peso (kg)", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("IMC", size=16, weight=ft.FontWeight.BOLD)
                            ),
                            ft.DataColumn(
                                ft.Text("Categoría", size=16, weight=ft.FontWeight.BOLD)
                            ),
                        ],
                        rows=[],
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    procesar_btn = ft.ElevatedButton(
        "Procesar", icon=ft.icons.ANALYTICS, visible=False, height=50, width=200
    )

    guardar_btn = ft.ElevatedButton(
        "Guardar", icon=ft.icons.SAVE, visible=False, height=50, width=300
    )

    def mostrar_mensaje(mensaje, es_error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.colors.ERROR if es_error else ft.colors.GREEN,
        )
        page.snack_bar.open = True
        page.update()

    def on_file_selected(e: ft.FilePickerResultEvent):
        if not e.files or not e.files[0].path:
            return

        archivo = e.files[0].path
        personas = cargar_datos_desde_txt(archivo)

        # Limpiar las filas del DataTable original
        data_table_original.controls[0].controls[0].rows.clear()
        for idx, p in enumerate(personas, start=1):
            data_table_original.controls[0].controls[0].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{idx}")),  # Índice
                        ft.DataCell(ft.Text(f"{p[0]:.2f}")),  # Talla
                        ft.DataCell(ft.Text(f"{p[1]:.2f}")),  # Peso
                    ]
                )
            )

        procesar_btn.visible = True
        content.update()

        def on_procesar(e):
            # Limpiar las filas del DataTable procesada
            data_table_procesada.controls[0].controls[0].rows.clear()
            for idx, p in enumerate(personas, start=1):
                talla, peso = p[:2]
                imc = calcular_imc(talla, peso)
                categoria = obtener_categoria_imc(imc)
                data_table_procesada.controls[0].controls[0].rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{idx}")),  # Índice
                            ft.DataCell(ft.Text(f"{talla:.2f}")),  # Talla
                            ft.DataCell(ft.Text(f"{peso:.2f}")),  # Peso
                            ft.DataCell(ft.Text(f"{imc:.2f}")),  # IMC
                            ft.DataCell(ft.Text(categoria)),  # Categoría
                        ]
                    )
                )

            guardar_btn.visible = True
            content.update()

        def on_guardar(e):
            try:
                with open(archivo, "w") as file:
                    for row in data_table_procesada.controls[0].controls[0].rows:
                        talla = float(row.cells[1].content.value)  # Cambiado a cells[1]
                        peso = float(row.cells[2].content.value)  # Cambiado a cells[2]
                        imc = float(row.cells[3].content.value)
                        categoria = row.cells[4].content.value
                        file.write(f"{talla}\t{peso}\t{imc}\t{categoria}\n")
                mostrar_mensaje("Resultados guardados correctamente")
            except Exception as e:
                mostrar_mensaje(f"Error al guardar los resultados: {str(e)}", True)

        procesar_btn.on_click = on_procesar
        guardar_btn.on_click = on_guardar

    file_picker.on_result = on_file_selected

    # Layout de la vista
    content.content = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("CALCULAR IMC", size=48, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton(
                            "Escoger archivo",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: file_picker.pick_files(
                                allow_multiple=False, allowed_extensions=["txt"]
                            ),
                            height=50,
                            width=300,
                        ),
                        ft.Container(
                            content=data_table_original,
                            height=600,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=10,
                            padding=10,
                        ),
                    ],
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Column(
                    [
                        procesar_btn,
                        ft.Container(
                            content=data_table_procesada,
                            height=600,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=10,
                            padding=10,
                        ),
                        guardar_btn,
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        ),
        padding=20,
    )   
    content.update()



def main(page: ft.Page):
    """
    This function initializes the main window of the IMC calculator application.

    Parameters:
    page (ft.Page): The main window of the .

    Returns:application
    None
    """
    page.title = "Calculadora de IMC"
    page.window_width = 1920
    page.window_height = 1080
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # File picker setup
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # Main content container
    content = ft.Container(
        expand=True,
        content=ft.Container(
            content=ft.Text("Seleccione una opción del menú", size=20),
            padding=20,
        ),
    )

    def on_menu_click(menu_id):
        """
        This function handles the menu item click events.

        Parameters:
        menu_id (str): The ID of the clicked menu item.

        Returns:
        None
        """
        if menu_id == "ingresar":
            crear_vista_ingreso(content, page, file_picker)
        elif menu_id == "procesar":
            crear_vista_procesar(content, page, file_picker)
        elif menu_id == "tema":
            page.theme_mode = (
                ft.ThemeMode.LIGHT
                if page.theme_mode == ft.ThemeMode.DARK
                else ft.ThemeMode.DARK
            )
            page.update()
        elif menu_id == "salir":
            page.window_destroy()

    # Menu lateral
    menu = crear_menu_lateral(on_menu_click, page)

    # Layout principal
    page.add(
        ft.Row(
            controls=[
                menu,
                ft.VerticalDivider(width=1),
                content,
            ],
            expand=True,
        )
    )



if __name__ == "__main__":
    ft.app(target=main)
