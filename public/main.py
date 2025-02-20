import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from deepface import DeepFace

class EmotionDetectorApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Detector de Emociones")

        # Elementos de la interfaz
        self.label = ttk.Label(window, text="Selecciona una opción:")
        self.label.pack(pady=10)

        self.camera_button = ttk.Button(window, text="Usar Cámara", command=self.open_camera)
        self.camera_button.pack(pady=5)

        self.upload_button = ttk.Button(window, text="Cargar Imagen", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.image_label = ttk.Label(window)
        self.image_label.pack(pady=10)

        self.emotion_label = ttk.Label(window, text="Emoción: N/A")
        self.emotion_label.pack(pady=10)

        self.cap = None  # Objeto de captura de video

    def analyze_face(self, img_path):
        try:
            result = DeepFace.analyze(img_path, actions=['emotion'], enforce_detection=False)
            dominant_emotion = result[0]['dominant_emotion']  # Acceder al primer rostro detectado
            return dominant_emotion
        except Exception as e:
            print(f"Error al analizar la imagen: {e}")
            return "No se pudo detectar"

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                img = Image.open(file_path)
                # Redimensionar la imagen
                img.thumbnail((400, 700))
                img = ImageTk.PhotoImage(img)
                self.image_label.config(image=img)
                self.image_label.image = img

                emotion = self.analyze_face(file_path)
                self.emotion_label.config(text=f"Emoción: {emotion}")
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                self.emotion_label.config(text="Error al cargar la imagen")

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.emotion_label.config(text="No se pudo abrir la cámara")
            return

        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                try:
                    s
                    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2_im)
                    img.thumbnail((800, 800))

                    # Guardar el frame temporalmente
                    temp_path = "temp_frame.jpg"
                    img.save(temp_path)

                    # Analizar el frame con DeepFace
                    emotion = self.analyze_face(temp_path)
                    self.emotion_label.config(text=f"Emoción: {emotion}")

                    # Mostrar el frame en la interfaz
                    img = ImageTk.PhotoImage(img)
                    self.image_label.config(image=img)
                    self.image_label.image = img
                except Exception as e:
                    print(f"Error al procesar el frame: {e}")
                    self.emotion_label.config(text="Error al procesar el frame")

            self.window.after(10, update_frame)  # Actualizar cada 10 ms

        update_frame()

    def close(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()


window = tk.Tk()
app = EmotionDetectorApp(window)
window.protocol("WM_DELETE_WINDOW", app.close) 
window.mainloop()
