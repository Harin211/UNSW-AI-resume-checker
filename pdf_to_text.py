import pdfplumber
import sys
import os

# Check if at least one PDF is provided
if len(sys.argv) < 2:
    print("Usage: python pdf_to_text.py <pdf_file1> [<pdf_file2> ...]")
    sys.exit(1)

# Get the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to outputs folder
output_dir = os.path.join(script_dir, "outputs")

# Create outputs folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop over all PDF files passed as arguments
for pdf_path in sys.argv[1:]:
    if not os.path.isfile(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist. Skipping.")
        continue

    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"

    # Save text file in the outputs folder
    txt_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    txt_path = os.path.join(output_dir, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(all_text)

    print(f"Text extracted to '{txt_path}'")



