import cv2
import pytesseract
import re
import json
from PIL import Image

# Set up Tesseract executable path (adjust according to your system)
pytesseract.pytesseract.tesseract_cmd = "venv/Scripts/pytesseract.exe"


class IDCardProcessor:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def preprocess_image(self, image_path):
        """
        Preprocess the image for better OCR performance.
        Converts to grayscale, applies thresholding, and saves the processed image.
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # Save and return the preprocessed image
        processed_image_path = "processed_image.png"
        cv2.imwrite(processed_image_path, thresh)
        return processed_image_path

    def extract_text(self, image_path):
        """
        Extracts text from the preprocessed image using Tesseract OCR.
        """
        processed_image_path = self.preprocess_image(image_path)
        text = pytesseract.image_to_string(processed_image_path, lang="eng")
        return text

    def parse_details(self, extracted_text):
        """
        Parse the extracted text to retrieve specific details like Name, ID Number, and DOB.
        """
        details = {}
        # Adjust regex patterns to match your ID card format
        name_match = re.search(r"Name:\s*(.*)", extracted_text, re.IGNORECASE)
        id_match = re.search(r"ID:\s*(\d+)", extracted_text, re.IGNORECASE)
        dob_match = re.search(r"DOB:\s*(\d{2}/\d{2}/\d{4})", extracted_text, re.IGNORECASE)

        if name_match:
            details['Name'] = name_match.group(1).strip()
        if id_match:
            details['ID Number'] = id_match.group(1).strip()
        if dob_match:
            details['Date of Birth'] = dob_match.group(1).strip()

        return details

    def save_details(self, details, filename="details.json"):
        """
        Save the parsed details to a JSON file.
        """
        with open(filename, "w") as f:
            json.dump(details, f, indent=4)

    def process_id_card(self, image_path):
        """
        Full pipeline: preprocess image, extract text, parse details, and save to a file.
        """
        print("Processing ID card...")
        extracted_text = self.extract_text(image_path)
        details = self.parse_details(extracted_text)
        if details:
            print("Details extracted successfully:")
            print(details)
            self.save_details(details)
            print(f"Details saved to details.json")
        else:
            print("No details could be extracted. Please check the image quality and format.")


# Usage Example
if __name__ == "__main__":
    id_card_path = "sample.jpg"  # Replace with your image path
    processor = IDCardProcessor()
    processor.process_id_card(id_card_path)

          
    

