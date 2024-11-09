import numpy as np

# Definir los rangos HSV para múltiples colores
COLOR_RANGES = {
    "yellow": {
        "lower_hsv": np.array([20, 80, 80], dtype=np.uint8),
        "upper_hsv": np.array([30, 255, 255], dtype=np.uint8),
        "rectangle_color": (0, 255, 255)  # Amarillo en BGR
    },
    "green": {
        "lower_hsv": np.array([40, 150, 130], dtype=np.uint8),
        "upper_hsv": np.array([70, 255, 255], dtype=np.uint8),
        "rectangle_color": (0, 255, 0)  # Verde en BGR
    },
    "red1": {  # Primer rango para rojo
        "lower_hsv": np.array([0, 150, 130], dtype=np.uint8),
        "upper_hsv": np.array([10, 255, 255], dtype=np.uint8),
        "rectangle_color": (0, 0, 255)  # Rojo en BGR
    },
    "red2": {  # Segundo rango para rojo (envolvimiento)
        "lower_hsv": np.array([170, 100, 100], dtype=np.uint8),
        "upper_hsv": np.array([180, 255, 255], dtype=np.uint8),
        "rectangle_color": (0, 0, 255)  # Rojo en BGR
    },
    "blue": {
        "lower_hsv": np.array([100, 100, 100], dtype=np.uint8),
        "upper_hsv": np.array([130, 255, 255], dtype=np.uint8),
        "rectangle_color": (255, 0, 0)  # Azul en BGR
    }
}


def get_color_limits(color_name):
    """
    Devuelve los rangos HSV y el color de rectángulo para el color especificado.

    Args:
        color_name (str): Nombre del color (e.g., 'yellow', 'green', 'red', 'blue').

    Returns:
        list of dict: Lista de diccionarios con 'lower_hsv', 'upper_hsv' y 'rectangle_color'.
    """
    if color_name.lower() == "red":
        # Rojo tiene dos rangos debido al envolvimiento del matiz
        return [COLOR_RANGES["red1"], COLOR_RANGES["red2"]]
    elif color_name.lower() in COLOR_RANGES:
        return [COLOR_RANGES[color_name.lower()]]
    else:
        raise ValueError(f"Color '{color_name}' no está definido en COLOR_RANGES.")


def get_all_color_limits():
    """
    Devuelve todos los rangos HSV y colores de rectángulo definidos.

    Returns:
        list of dict: Lista de diccionarios con 'name', 'lower_hsv', 'upper_hsv' y 'rectangle_color'.
    """
    all_colors = []
    processed_colors = set()
    for color_key, color_info in COLOR_RANGES.items():
        if color_key.startswith("red"):
            color_name = "Red"
            if color_name in processed_colors:
                continue  # Evitar duplicados
            processed_colors.add(color_name)
        else:
            color_name = color_key.capitalize()
            if color_name in processed_colors:
                continue  # Evitar duplicados
            processed_colors.add(color_name)
        # Recolectar todos los rangos correspondientes a cada color
        if color_name.lower() == "red":
            # Añadir ambos rangos para el rojo
            all_colors.extend([
                {
                    "name": color_name,
                    "lower_hsv": COLOR_RANGES["red1"]["lower_hsv"],
                    "upper_hsv": COLOR_RANGES["red1"]["upper_hsv"],
                    "rectangle_color": COLOR_RANGES["red1"]["rectangle_color"]
                },
                {
                    "name": color_name,
                    "lower_hsv": COLOR_RANGES["red2"]["lower_hsv"],
                    "upper_hsv": COLOR_RANGES["red2"]["upper_hsv"],
                    "rectangle_color": COLOR_RANGES["red2"]["rectangle_color"]
                }
            ])
        else:
            all_colors.append({
                "name": color_name,
                "lower_hsv": color_info["lower_hsv"],
                "upper_hsv": color_info["upper_hsv"],
                "rectangle_color": color_info["rectangle_color"]
            })
    return all_colors