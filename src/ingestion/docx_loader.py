import docx
import zipfile
from io import BytesIO
from llm.azure_openai import AzureLLM

llm_helper = AzureLLM()

def parse_docx_stream(file_stream: BytesIO):
    """
    Parses DOCX for Text and Images (converted to text descriptions).
    """
    doc = docx.Document(file_stream)
    full_text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            full_text += para.text + "\n"

    file_stream.seek(0)

    try:
        with zipfile.ZipFile(file_stream) as z:

            image_files = [f for f in z.namelist() if f.startswith("word/media/") and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if image_files:
                full_text += "\n--- Extracted Images from Document ---\n"

                for img_path in image_files:

                    image_bytes = z.read(img_path)

                    if len(image_bytes) < 5 * 1024:
                        continue

                    print(f"   -> Captioning DOCX image: {img_path}...")
                    caption = llm_helper.describe_image(image_bytes)
                    full_text += f"\n[IMAGE DESCRIPTION ({img_path}): {caption}]\n"

    except Exception as e:
        print(f"Error extracting images from DOCX: {e}")


    return full_text