import os
from PyPDF2 import PdfReader
from PIL import Image
import io

# Directorio donde se encuentran los archivos PDF
pdf_directory = 'D:/Tarjetaspdf'

# Directorio donde guardar las imágenes extraídas
output_directory = 'D:/ImagenesPDF'

# Crear el directorio de salida si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Función para extraer imágenes de un archivo PDF


def extract_images_from_pdf(pdf_path, output_folder):
    pdf = PdfReader(pdf_path)

    # Iterar sobre todas las páginas del PDF
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]

        resources = page.get("/Resources")
        if resources:
            resources = resources.get_object()

            if '/XObject' in resources:
                xObject = resources['/XObject'].get_object()

                # Iterar sobre todos los objetos en la página
                for obj in xObject:
                    if xObject[obj].get("/Subtype", "") == '/Image':
                        # Obtener la imagen como un objeto PIL
                        image_data = xObject[obj]._data
                        image = Image.open(io.BytesIO(image_data))
                        # Construir un nombre de archivo único
                        # Obtener el nombre del archivo PDF sin extensión
                        file_name = os.path.splitext(
                            os.path.basename(pdf_path))[0]
                        image_path = os.path.join(output_folder, f"{file_name}_page{
                                                  page_num+1}_{obj[1:]}.png")
                        # Guardar la imagen en el directorio de salida
                        image.save(image_path)


# Iterar sobre todos los archivos PDF en el directorio
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        print(f"Extracting images from {pdf_path}...")
        extract_images_from_pdf(pdf_path, output_directory)

print("Extracción de imágenes completa.")
