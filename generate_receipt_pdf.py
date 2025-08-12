from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

class Receipt:
    def __init__(self):
        self.data = None
    
    def generate_receipt(self, customer_data, prod_data, total_price, b_name, address="Address Not Mentioned"):
        self.data = prod_data

        c = canvas.Canvas(filename=f"output/{customer_data[0]}.pdf", pagesize=letter)
        
        c.setFont("Helvetica-Bold", 24)
        c.drawString(200, 750, b_name)

        c.setFont("Helvetica-Bold", 8)
        c.drawString(220, 730, address)

        c.setFont("Helvetica-Bold", 24)
        c.drawString(200, 640, "CASH RECEIPT")
        
        c.line(0, 620, letter[0], 620)

        c.setFont("Helvetica-Bold", 12)
        
        c.drawString(50, 580, f"Customer Name : {customer_data[0]}")
        c.drawString(50, 560, f"Customer CNIC : {customer_data[1]}")

        c.line(0, 530, letter[0], 530)

        c.drawString(50, 510, "Product ID")
        c.drawString(150, 510, "Product Name")
        c.drawString(250, 510, "Product Price")
        c.drawString(350, 510, "Product Quantity")

        c.setFont("Helvetica", 12)

        y_pos = 490

        for i in prod_data:
            c.drawString(50, y_pos, str(i[0]))
            c.drawString(150, y_pos, str(i[1]))
            c.drawString(250, y_pos, str(i[2]))
            c.drawString(350, y_pos, str(i[3]))
            y_pos -= 20
        
        
        c.setFont("Helvetica-Bold", 12)
        c.line(0, y_pos - 20, letter[0], y_pos - 20)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos - 40, f"Total Price : {str(total_price)}")
        
        c.save()
