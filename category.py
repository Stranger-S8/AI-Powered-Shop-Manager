from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

class Categorization:
    product_names = [
    # Food & Beverages
    "Karachi Biryani", "Lahori Chargha", "Peshawari Chapli Kebab", "Faisalabad Sweets", 
    "Rawalpindi Chicken Karahi", "Multani Samosa", "Karachi Chicken Biryani", "Islamabad Mutton Seekh Kebab",
    "Quetta Pulao", "Sialkot Peshawari Naan", "Hyderabadi Chicken Handi", "Pakistani Mangoes",
    "Sahiwal Cattle Milk", "Cholistan Desert Dates", "Chana Chaat", "Pakistani Guava", 
    "Peshawari Ice Cream", "Dahi Bhalla", "Aloo Ke Parathe", "Pakistani Halwa", 
    "Chana Masala", "Gulab Jamun", "Lassi Drink", "Fried Fish", "Pakistani Tea", 
    "Spicy Prawns", "Balochi Sajji", "Pakistani Khoya", "Sindhi Biryani", "Peshawar Sweets", 
    "Peach Jam", "Mango Pickle", "Biryani Masala", "Dry Fruits Mix", "Pakistani Rose Water", 
    "Chili Garlic Sauce", "Pakistani Brown Rice", "Lahori Paratha", "Roti", "Shahi Tukra",
    "Pakistani Chicken Shawarma", "Pakistani Rice Flour", "Pakistani Lentils", "Peshawari Shawarma",
    "Karahi Gosht", "Sausage Roll", "Chapli Kebab",
    
    # Electronics
    "Samsung Galaxy S23", "Apple iPhone 15", "Huawei P40", "Oppo F21 Pro", "Xiaomi Mi 11", 
    "Sony Bravia 55 Inch TV", "LG OLED TV", "Dell Inspiron Laptop", "HP Pavilion Laptop", 
    "Asus ROG Gaming Laptop", "Apple MacBook Pro", "Bose QuietComfort Headphones", "JBL Flip 5 Speaker",
    "Logitech Wireless Mouse", "Microsoft Surface Pro", "Canon EOS 90D Camera", "Nikon D3500 Camera", 
    "GoPro Hero 11", "Fitbit Charge 5", "Samsung Galaxy Watch", "Acer Predator Monitor", "Xbox Series X", 
    "PlayStation 5", "Nintendo Switch", "Razer Gaming Keyboard", "Corsair RGB Gaming Mouse", "HP DeskJet Printer",
    "Apple iPad Air", "Sony WH-1000XM4", "LG UltraGear Monitor", "Samsung QLED TV", "Alienware Laptop", 
    "Dell XPS 13 Laptop", "Bose SoundLink Revolve", "Beats Studio3 Wireless", "Oculus Quest 2", "Apple Watch Ultra",
    "Logitech G Pro X Gaming Headset", "Razer Kraken V3", "Samsung T7 Portable SSD", "Huawei Watch GT3", "Acer Nitro 5 Laptop",
    "Lenovo ThinkPad X1", "Epson EcoTank Printer", "ViewSonic 4K Monitor", "BenQ 240Hz Gaming Monitor", "Philips Hue Smart Bulb",
    
    # Fashion
    "Khaadi Kurti", "Gul Ahmed Lawn Suit", "Junaid Jamshed Shirt", "Sapphire Cotton Dress", 
    "Bonanza Satrangi Top", "Bareeze Shawl", "ChenOne Linen Dress", "Maria B Bridal Dress", 
    "Sana Safinaz Maxi Dress", "Cross Stitch Tunic", "Outfitters Hoodie", "Pakistan Polo Shirt", 
    "Pakistani Silk Saree", "Pakistani Embroidered Suit", "Zara Shahjahan Lehenga", "Gul Ahmed Silk Scarf", 
    "Sapphire Frock", "Junaid Jamshed Sherwani", "Bonanza Satrangi Scarf", "Khaadi Dupatta", 
    "Bareeze Jacket", "Maria B Casual Dress", "Sana Safinaz Shawl", "Cross Stitch Jeans", 
    "Outfitters Sneakers", "Pakistan Traditional Dress", "Pakistani Woolen Sweater", 
    "Pakistani Cotton Kurta", "Bareeze Party Wear", "Khaadi Cardigan", "Sana Safinaz Formal Wear", 
    "Bonanza Satrangi Blouse", "Junaid Jamshed Kurta", "Sapphire Tunic", "Zara Shahjahan Wedding Dress", 
    "Cross Stitch Wool Sweater", "Bareeze Embroidered Shawl", "Outfitters Belt", "Sana Safinaz Pants", 
    "Bonanza Satrangi Casual Wear", "Khaadi Winter Collection", "Maria B Fancy Dress", "Gul Ahmed Nightwear", 
    "Sapphire Summer Dress", "Junaid Jamshed Casual Shirt", "Zara Shahjahan Designer Dress", "Pakistan Embroidered Jacket",
    
    # Home Appliances
    "Haier Refrigerator", "LG Air Conditioner", "Dawlance Washing Machine", "Kenwood Microwave", 
    "Orient Ceiling Fan", "Pel Water Heater", "Gree Air Conditioner", "Samsung Washing Machine", 
    "Haier Deep Freezer", "Ravi Water Purifier", "Super Asia Vacuum Cleaner", "Kenwood Blender", 
    "Dawlance Deep Freezer", "Rheem Water Heater", "Orient Washing Machine", "Haier LED TV", 
    "Panasonic Air Purifier", "Kenwood Rice Cooker", "Super Asia Washing Machine", "PEL LED TV", 
    "Gree Washing Machine", "Samsung Microwave Oven", "Dawlance LED TV", "Kenwood Air Conditioner", 
    "Haier Fan", "PEL Fan", "Ravi Refrigerator", "Super Asia Water Dispenser", "Panasonic Refrigerator", 
    "Dawlance Microwave Oven", "Kenwood Juicer", "Haier Vacuum Cleaner", "Gree Water Cooler", 
    "Orient Deep Freezer", "PEL Rice Cooker", "Panasonic Microwave", "Super Asia Air Cooler", 
    "Dawlance Fan", "Haier Water Dispenser", "Samsung Rice Cooker", "Gree Refrigerator", "Kenwood Fan", 
    "Pel Juicer", "Haier Water Cooler", "Orient Refrigerator", "Kenwood Water Dispenser", "PEL Washing Machine",
    
    # Beauty and Health
    "Safi Herbal Blood Purifier", "Hamdard Roghan Badam Shirin", "Pond's White Beauty Cream", "Garnier Skin Naturals",
    "Fair and Lovely Whitening Cream", "Sunsilk Shampoo", "L'Oréal Paris Hair Serum", "Olay Total Effects Cream",
    "Nivea Soft Cream", "Dove Body Lotion", "Himalaya Herbal Face Wash", "The Body Shop Vitamin E Moisture Cream",
    "Herbion Aloe Vera Gel", "Saaf Tonic", "Miracle Skin Care", "Qureshi's Skin Whitening Cream", "Garnier Men Oil Control Face Wash",
    "Fariha's Lip Care", "Sofy Super Dry Pads", "Medora Lipstick",
    "Pakistani Rose Water", "Nina Natural Herbal Shampoo", "Khaadi Herbal Bath Soap", "Bio Aqua Whitening Cream",
    "L'oreal Excellence Hair Color", "Jafferjees Hand Cream", "Hamama Ayurvedic Face Pack", "Mehndi (Henna) Powder",
    "Jovees Herbal Skin Care", "Pehle Aap Hair Oil", "Boro Plus Herbal Cream", "Indus Valley Natural Products",
    "Pond's Cold Cream", "Aloe Vera Gel by Al Haramain", "Cibelle Hair Removal Cream", "Faiza Beauty Cream",
    "Shahnaz Husain Shalmar Ayurvedic Cream", "Miracle Herb Face Mask", "Lush Cosmetics Bath Bombs", "Hamdard Mehrunnisa Soap",
    "Alharam Perfume", "Medora Nail Polish", "Pakistani Neem Face Pack", "Natural Skin Glow Cream",
    "Khadi Natural Foot Cream", "Ayurvedic Whitening Soap", "Pond's Pearl Powder",
    
    # Sports & Outdoors
    "Karachi Cricket Bat", "Lahore Football", "Peshawar Tennis Racket", "Islamabad Running Shoes", 
    "Multan Basketball", "Quetta Baseball Glove", "Sialkot Badminton Racket", "Faisalabad Hockey Stick", 
    "Rawalpindi Volleyball", "Lahore Sports Water Bottle", "Karachi Fitness Tracker", "Islamabad Yoga Mat", 
    "Peshawar Football Shoes", "Sialkot Gym Bag", "Faisalabad Tennis Ball", "Multan Bike Helmet", 
    "Quetta Running Shorts", "Rawalpindi Sports Watch", "Lahore Yoga Block", "Karachi Sports Gloves", 
    "Sialkot Baseball Bat", "Faisalabad Cycling Shorts", "Peshawar Hiking Boots", "Islamabad Exercise Bands", 
    "Quetta Soccer Jersey", "Rawalpindi Basketball Net", "Multan Sports T-shirt", "Sialkot Cricket Ball", 
    "Lahore Outdoor Tent", "Karachi Fitness Dumbbells", "Peshawar Sports Backpack", "Sialkot Protective Pads", 
    "Rawalpindi Fishing Rod", "Multan Gym Shoes", "Quetta Running Jacket", "Faisalabad Sports Socks", 
    "Karachi Outdoor Cooler", "Islamabad Skateboard", "Lahore Protective Helmet", "Rawalpindi Camping Stove", 
    "Sialkot Bike Pump", "Peshawar Sports Towel", "Faisalabad Sports Jacket", "Karachi Sports Visor", 
    "Multan Sports Shoes", "Sialkot Bike Lights", "Rawalpindi Soccer Cleats"
    ]

    categories = [
        # Food & Beverages
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        "Food & Beverages", "Food & Beverages", "Food & Beverages", "Food & Beverages",
        "Food & Beverages", "Food & Beverages", "Food & Beverages", 
        
        # Electronics
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics", 
        "Electronics", "Electronics",
        
        # Fashion
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", "Fashion", "Fashion", "Fashion", 
        "Fashion", "Fashion", 
            
        # Home Appliances
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", "Home Appliances", 
        "Home Appliances", "Home Appliances", "Home Appliances", 
        
        # Beauty and Health
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health", "Beauty & Health",
        "Beauty & Health", "Beauty & Health", "Beauty & Health",
        
        # Sports & Outdoors
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors", 
        "Sports & Outdoors", "Sports & Outdoors", "Sports & Outdoors"
    ]


    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def train_model(self):
        x = self.vectorizer.fit_transform(Categorization.product_names)
        y = Categorization.categories

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.Y_train)

        with open('AI Models/category_model.pkl','wb') as f:
            pickle.dump(self.model, f)

        with open('AI Models/category_vectorizer.pkl','wb') as g:
            pickle.dump(self.vectorizer, g)


    def accuracy_test(self):
        y_pred = self.model.predict(self.X_test)

        print("Accuraccy of Model is : ", accuracy_score(self.Y_test, y_pred))
        print("Classification Report : ", classification_report(self.Y_test, y_pred))

    def predict_model(self, product):
        new_product_vectorized = self.vectorizer.transform(product)
        predicted_category = self.model.predict(new_product_vectorized)
        return predicted_category
    
    def Run_Model(self, product):
        with open('AI Models/category_model.pkl','rb') as f:
            self.model = pickle.load(f)

        with open('AI Models/category_vectorizer.pkl','rb') as g:
            self.vectorizer = pickle.load(g)
        
        return self.predict_model(product)

# A = Categorization()
# # A.train_model()
# # A.accuracy_test()
# a = A.Run_Model(["Biryani"])

    
