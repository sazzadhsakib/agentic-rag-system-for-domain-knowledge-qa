import fitz
from io import BytesIO
from llm.azure_openai import AzureLLM

llm_helper = AzureLLM()

def parse_pdf_stream(file_stream: BytesIO):
    """
    Parses PDF for both Text and Images (converted to text descriptions).
    """
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    full_text = ""

    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
        image_list = page.get_images(full=True)

        if image_list:
            print(f"Found {len(image_list)} images on page {page_num + 1}...")

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                if len(image_bytes) < 5 * 1024:
                    continue

                print(f"   -> Captioning image {img_index}...")
                caption = llm_helper.describe_image(image_bytes)

                full_text += f"\n[IMAGE DESCRIPTION on Page {page_num+1}: {caption}]\n"

    return full_text