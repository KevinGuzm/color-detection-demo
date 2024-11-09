import gradio as gr
import cv2
import numpy as np
from gradio_webrtc import WebRTC
from utils import get_all_color_limits

def detection(image, sensibilidad=0.01):
    # Convertir la imagen de BGR a HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calcular el área mínima en función de la sensibilidad y el tamaño de la imagen
    frame_height, frame_width = hsv_image.shape[:2]
    min_area = frame_height * frame_width * sensibilidad

    # Obtener todos los colores definidos con sus rangos HSV y colores de rectángulo
    colors = get_all_color_limits()

    for color in colors:
        # Crear una máscara para detectar áreas que estén dentro del rango del color actual
        mask = cv2.inRange(hsv_image, color["lower_hsv"], color["upper_hsv"])

        # Encontrar los contornos de las áreas detectadas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar un rectángulo alrededor de las detecciones que superen el área mínima
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:  # Aplicar el umbral de área mínima
                x, y, w, h = cv2.boundingRect(contour)
                image = cv2.rectangle(
                    image,
                    (x, y),
                    (x + w, y + h),
                    color["rectangle_color"],
                    2  # Grosor del rectángulo reducido a 2
                )
                # Añadir el nombre del color detectado
                cv2.putText(
                    image,
                    color["name"],
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color["rectangle_color"],
                    2
                )

    # Redimensionar la imagen para la salida de Gradio
    return cv2.resize(image, (1000, 1000))

# Configuración CSS para la interfaz de Gradio
css = """
.my-group {max-width: 600px !important; max-height: 600 !important;}
.my-column {display: flex !important; justify-content: center !important; align-items: center !important;}
"""

with gr.Blocks(css=css) as demo:
    gr.HTML(
        """
    <h1 style='text-align: center'>
    Color Detection Webcam Stream (Powered by WebRTC ⚡️)
    </h1>
    """
    )
    gr.HTML(
        """
        <h3 style='text-align: center'>
        Detect Multiple Colors in Real-Time (yellow/green/red/blue)
        </h3>
        """
    )
    with gr.Column(elem_classes=["my-column"]):
        with gr.Group(elem_classes=["my-group"]):
            image = WebRTC(label="Stream", rtc_configuration=None)
            sensibilidad = gr.Slider(
                label="Sensibilidad (área mínima de detección)",
                minimum=0.0,
                maximum=0.1,
                step=0.005,
                value=0.01,
            )

        image.stream(
            fn=detection, inputs=[image, sensibilidad], outputs=[image], time_limit=60
        )

if __name__ == "__main__":
    demo.launch(share=True)