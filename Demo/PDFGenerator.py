from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(self.filename, pagesize=letter)
        self.current_y = 800  # Iniciar posición Y para agregar contenido

    def add_title(self, title):
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(50, self.current_y, title)
        self.current_y -= 20  # Bajar la posición Y después del título

    def add_text(self, text):
        self.c.setFont("Helvetica", 12)
        lines = text.split("\n")
        for line in lines:
            self.c.drawString(50, self.current_y, line)
            self.current_y -= 15  # Bajar la posición Y después de cada línea de texto

    def add_image(self, image_path, width=400, height=300):
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width
            img_height = height
            img_width = int(img_height / aspect_ratio)
            self.c.drawImage(image_path, 50, self.current_y - img_height, width=img_width, height=img_height)
            self.current_y -= (img_height + 20)  # Bajar la posición Y después de cada imagen
        except Exception as e:
            print(f"Error al insertar imagen {image_path}: {str(e)}")

    def save(self):
        self.c.save()
        print(f"Reporte generado: {self.filename}")
