import customtkinter as ctk
import tkinter as tk
from PIL import Image
import database as db
from tkinter import messagebox,ttk
from category import Categorization
from encryption import Credentials
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from generate_receipt_pdf import Receipt
import webbrowser
import os
import pandas as pd
from datetime import datetime, timedelta, time
from matplotlib import dates as mdates
from SalesPrediction import Predict
import json

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = db.Database()
        self.a = db.Business_Details()
        self.b = db.Customer_Details()
        self.c = db.Products()
        self.d = Categorization()
        self.f = Credentials()
        self.e = Receipt()
        self.g = db.Orders()
        self.p = Predict()

        settings = self.load_settings_fn()
        
        self.width = settings["width"]
        self.height = settings["height"]
        self.currency = settings["currency"]

        self.find_center()
        self.title ("AI - Powered Shop Manager")
        self.minsize(1366, 768)        
        self.geometry(f"{self.width}x{self.height}+{self.c_x}+{self.c_y}")
        self.resizable(False, False)
        self.b_name = None
        self.check_login_credentials()

    def handle_btncolor_fn(self, btn, *args):
        pass
    
    def find_center(self):
        
        width = self.winfo_screenwidth() 
        height = self.winfo_screenheight()
                
        self.c_x = int(width/2 - self.width/2)
        self.c_y = int(height/2 - self.height/2)
    
    def align_text(self, text):
        max_len = 15
        text_len = max_len - len(text)

        return text + " " * text_len
    
    def check_login_credentials(self):
        result = self.f.load_decrypted_credentials()
        
        if result:
            result2 = self.a.login_business(result[0], result[1], self.db)
            if result2:
                self.b_name = self.a.get_business_name(result[0], result[1], self.db)
                self.mainpage()
        else:
            self.login_page()
    
    def save_settings_fn(self, default_setting):

        with open ("data/Settings/settings.json", "w") as f:
            json.dump(default_setting, f, indent=4)
    
    def load_settings_fn(self):
        file_path = "data/Settings/settings.json"

        default_setting = {
            "width" : 1366,
            "height" : 768,
            "currency": "PKR",
        }

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        else:
            return default_setting
            
    def process_login(self, email, password, check_var):
        result = self.a.login_business(email, password, self.db)

        default_setting = {
            "width" : 1366,
            "height" : 768,
            "currency": "PKR",
        }
        
        if result:
            self.b_name = self.a.get_business_name(email, password, self.db)
            if check_var:
                self.f.store_encrypted_credentials(email, password)
                self.save_settings_fn(default_setting)
            messagebox.showinfo("Success", "Login Successful")
            self.mainpage()
        else:
            messagebox.showerror("Error" , "Email or Password is  wrong")

    def process_register(self, name, email, password, phone):
        if name == "" or email == "" or password == "" or phone == "":
            messagebox.showerror("Error" , "Some Fields are Empty")
        else:
            if self.a.business_exist(self.db, email):
                messagebox.showerror("Error", "Email is Already Registered")
            else:
                result = self.a.register_business(self.db, name, email, password, phone)
                if result:
                    messagebox.showinfo("Success", "Business registered Successfully")
                    self.login_page()
                else:
                    messagebox.showerror("Failure", "Something Wrong occured")

    def login_page(self):

        if hasattr(self, 'register_frame') and isinstance(self.register_frame, ctk.CTkFrame):
            self.register_frame.destroy()
        
        self.login_frame = ctk.CTkFrame(self, fg_color="#c4d5e1")
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.login_bg_image = ctk.CTkImage(light_image=(Image.open("data/images/login_bg.jpg")), size=(self.width, self.height))
        
        self.login_bg_image_lbl = ctk.CTkLabel(self.login_frame, text="", image=self.login_bg_image)
        self.login_bg_image_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.login_window_log = ctk.CTkFrame(self.login_frame, fg_color="#ffffff", corner_radius=0)
        self.login_window_log.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.login_window_left = ctk.CTkFrame(self.login_window_log, fg_color="#ffffff", corner_radius=0)
        self.login_window_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.login_window_right = ctk.CTkFrame(self.login_window_log, fg_color="#34D1DC", corner_radius=0)
        self.login_window_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        temp = Image.open("data/images/login_head_pic.png")
        self.login_image = ctk.CTkImage(light_image=temp, size=(500, 355))
        self.login_image_label = ctk.CTkLabel(self.login_window_right, text="", image=self.login_image)
        self.login_image_label.place(relx=0.05, rely=0)

        self.login_heading_label = ctk.CTkLabel(
            self.login_window_right,
            text="WELCOME",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=30, weight="bold"),
        )
        self.login_heading_label.place(relx=0.2, rely=0.7)

        self.login_slogan_label = ctk.CTkLabel(
            self.login_window_right,
            text="Your Shop, Our Smarts – Strange Solutions Inside",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
        )
        self.login_slogan_label.place(relx=0.2, rely=0.76)

        self.heading_account = ctk.CTkLabel(
            self.login_window_left,
            text="Hello! Welcome Back",
            text_color="#15B4BF",
            fg_color="#ffffff",
            font=("Roboto", 30, "bold"),
        )
        self.heading_account.place(relx=0.25, rely=0.1)

        self.email_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Email", corner_radius=20)
        self.email_entry.place(relx=0.15, rely=0.3, relwidth=0.7, relheight=0.08)

        self.password_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Password", 
                                           corner_radius=20, show="*")
        self.password_entry.place(relx=0.15, rely=0.42, relwidth=0.7, relheight=0.08)
        
        check_var = ctk.BooleanVar()

        self.remember_pass = ctk.CTkCheckBox(
            self.login_window_left, 
            text="Remember me",
            variable=check_var
            )
        self.remember_pass.place(relx=0.16, rely=0.54, relwidth=0.7, relheight=0.05)

        self.login_button = ctk.CTkButton(
            self.login_window_left,
            text="LOGIN",
            fg_color="#15B4BF",
            text_color="#ffffff",
            hover=False,
            cursor="hand2",
            corner_radius=40,
            font=("Roboto", 20, "bold"),
            command=lambda : self.process_login(self.email_entry.get(), self.password_entry.get(), check_var.get())
        )
        self.login_button.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.08)
        
        self.line_frame = ctk.CTkFrame(self.login_window_left, corner_radius=0, fg_color="#ffffff")
        self.line_frame.place(relx=0, rely=0.765, relwidth=1, relheight=0.006)
        
        self.canvas1 = tk.Canvas(self.line_frame, highlightthickness=0)
        self.canvas1.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        width = self.line_frame.winfo_width()
        height = self.line_frame.winfo_height()
        
        self.canvas1.create_line(0.1*width, 0.002*height, 0.5*width, 0.002*height, fill="#a9abad", width=1)
        
        self.create_account_label = ctk.CTkLabel(self.login_window_left, text="Dont Have an account?", text_color="#000000")
        self.create_account_label.place(relx=0.3, rely=0.775,relheight=0.1)
        
        self.create_button = ctk.CTkButton(
            self.login_window_left,
            text="Create Account",
            fg_color="#ffffff",
            text_color="#15B4BF",
            hover=False,
            cursor="hand2",
            corner_radius=30,
            command=self.register_page
        )
        self.create_button.place(relx=0.54, rely=0.775, relheight=0.1)
    
    def register_page(self):

        if hasattr(self, 'login_frame') and isinstance(self.login_frame, ctk.CTkFrame):
            self.login_frame.destroy()
        
        self.register_frame = ctk.CTkFrame(self, fg_color="#c4d5e1")
        self.register_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        login_bg_image = ctk.CTkImage(light_image=(Image.open("data/images/login_bg.jpg")), size=(self.width, self.height))
        
        self.login_bg_image_lbl = ctk.CTkLabel(self.register_frame, text="", image=login_bg_image)
        self.login_bg_image_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.login_window_reg = ctk.CTkFrame(self.register_frame, fg_color="#ffffff", corner_radius=0)
        self.login_window_reg.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.login_window_left = ctk.CTkFrame(self.login_window_reg, bg_color="#c4d5e1", fg_color="#ffffff", corner_radius=0)
        self.login_window_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.login_window_right = ctk.CTkFrame(self.login_window_reg, bg_color="#c4d5e1", fg_color="#34D1DC", corner_radius=0)
        self.login_window_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        temp = Image.open("data/images/login_head_pic.png")
        login_head_image = ctk.CTkImage(light_image=temp, size=(500, 355))
        self.login_image_label = ctk.CTkLabel(self.login_window_right, text="", image=login_head_image)
        self.login_image_label.place(relx=0.05, rely=0)

        self.login_heading_label = ctk.CTkLabel(
            self.login_window_right,
            text="WELCOME",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=30, weight="bold"),
        )
        self.login_heading_label.place(relx=0.2, rely=0.7)

        self.login_slogan_label = ctk.CTkLabel(
            self.login_window_right,
            text="Your Shop, Our Smarts – Strange Solutions Inside",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
        )
        self.login_slogan_label.place(relx=0.2, rely=0.76)

        self.heading_account = ctk.CTkLabel(
            self.login_window_left,
            text="Hello! Stranger",
            text_color="#15B4BF",
            fg_color="#ffffff",
            font=("Roboto", 30, "bold"),
        )
        self.heading_account.place(relx=0.25, rely=0.1)
        
        self.name_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Name", 
                                           corner_radius=20)
        self.name_entry.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.08)

        self.email_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Email", corner_radius=20)
        self.email_entry.place(relx=0.15, rely=0.37, relwidth=0.7, relheight=0.08)

        self.password_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Password", 
                                           corner_radius=20)
        self.password_entry.place(relx=0.15, rely=0.49, relwidth=0.7, relheight=0.08)
        
        self.phone_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Phone Number", 
                                           corner_radius=20)
        self.phone_entry.place(relx=0.15, rely=0.61, relwidth=0.7, relheight=0.08)
        
        self.register_button = ctk.CTkButton(
            self.login_window_left,
            text="Register",
            fg_color="#15B4BF",
            text_color="#ffffff",
            hover=False,
            cursor="hand2",
            corner_radius=40,
            font=("Roboto", 20, "bold"),
            command=lambda : self.process_register(self.name_entry.get(), self.email_entry.get(), self.password_entry.get(), self.phone_entry.get())
        )
        self.register_button.place(relx=0.25, rely=0.75, relwidth=0.5, relheight=0.08)
        
        self.line_frame = ctk.CTkFrame(self.login_window_left, corner_radius=0, fg_color="#ffffff")
        self.line_frame.place(relx=0, rely=0.85, relwidth=1, relheight=0.006)
        
        self.canvas = tk.Canvas(self.line_frame, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        width = self.line_frame.winfo_width()
        height = self.line_frame.winfo_height()

        license_text = "All Rights Reserved by Strange Solutions Private Limited.\nUnauthorized copying or modification is strictly prohibited"
        
        self.reserved_label = ctk.CTkLabel(self.login_window_left, text=license_text, text_color="#888888",
                                           font=("Roboto Italic", 10))
        self.reserved_label.place(relx=0.25, rely=0.88,relheight=0.1)
    
    def mainpage(self):
        if hasattr(self,"login_frame") and hasattr(self, "register_frame") and isinstance(self.login_frame, ctk.CTkFrame) and isinstance(self.register_frame, ctk.CTkFrame):
            self.login_frame.destroy()
            self.register_frame.destroy()

        self.main_frame = ctk.CTkFrame(self, fg_color="#d7fff5",corner_radius=0)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.side_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=10)
        self.side_frame.place(relx=0.01, rely=0.02, relwidth=0.2, relheight=0.95)

        temp = Image.open("data/images/side_header.png")
        head_image = ctk.CTkImage(light_image=temp, size=(300, 250))
        self.side_head_label = ctk.CTkLabel(self.side_frame, text="", image=head_image)
        self.side_head_label.place(relx=0, rely=0, relwidth=1)

        self.main_center_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=10)
        self.main_center_frame.place(relx=0.22, rely=0.02, relwidth=0.77, relheight=0.95)

        self.shop_head_label = ctk.CTkLabel(self.side_frame, text=f"{self.b_name}", text_color="#1185c7",
                                            fg_color="#ffffff",font=("Arial", 26, "bold"))
        self.shop_head_label.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.05)

        manageprod_image = ctk.CTkImage(light_image=Image.open("data/images/manage_prod.png"), size=(20, 20))

        self.manage_prod = ctk.CTkButton(self.side_frame, text=self.align_text("Manage Products"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=manageprod_image, compound="left",
                                         command=self.manage_products_fn
                                         )
        self.manage_prod.place(relx=0, rely=0.25, relwidth=1, relheight=0.05)

        sale_image = ctk.CTkImage(light_image=Image.open("data/images/manage_sale.png"), size=(20, 20))

        self.manage_sale = ctk.CTkButton(self.side_frame, text=self.align_text("Manage Sales"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=sale_image, compound="left",command=self.manage_sales_fn
                                         )
        self.manage_sale.place(relx=0, rely=0.32, relwidth=1, relheight=0.05)

        cus_image = ctk.CTkImage(light_image=Image.open("data/images/view_customer.png"), size=(20, 20))

        self.view_cus = ctk.CTkButton(self.side_frame, text=self.align_text("Manage Customers"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=cus_image, compound="left",
                                         command=self.manage_customers_fn
                                         )
        self.view_cus.place(relx=0, rely=0.39, relwidth=1, relheight=0.05)

        prod_image = ctk.CTkImage(light_image=Image.open("data/images/view_product.png"), size=(20, 20))

        self.menu_prod = ctk.CTkButton(self.side_frame, text=self.align_text("Products Menu"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=prod_image, compound="left",
                                         command=self.product_menu_fn
                                         )
        self.menu_prod.place(relx=0, rely=0.46, relwidth=1, relheight=0.05)

        scan_image = ctk.CTkImage(light_image=Image.open("data/images/scan_id.png"), size=(20, 20))

        # self.scan_id = ctk.CTkButton(self.side_frame, text=self.align_text("Scan ID"), text_color="#000000", corner_radius=0,
        #                                  fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
        #                                  image=scan_image, compound="left"
        #                                  )
        # self.scan_id.place(relx=0, rely=0.44, relwidth=1, relheight=0.05)

        # chatbot_image = ctk.CTkImage(light_image=Image.open("data/images/chatbot.png"), size=(20, 20))

        # self.chat_bot = ctk.CTkButton(self.side_frame, text=self.align_text("Chatbot"), text_color="#000000", corner_radius=0,
        #                                  fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
        #                                  image=chatbot_image, compound="left"
        #                                  )
        # self.chat_bot.place(relx=0, rely=0.50, relwidth=1, relheight=0.05)

        about_image = ctk.CTkImage(light_image=Image.open("data/images/about us.png"), size=(20, 20))

        self.about_us = ctk.CTkButton(self.side_frame, text=self.align_text("About us"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=about_image, compound="left",command=self.about_us_fn
                                         )
        self.about_us.place(relx=0, rely=0.53, relwidth=1, relheight=0.05)
        
        self.canvas2 = tk.Canvas(self.side_frame, highlightthickness=0)
        self.canvas2.place(relx=0, rely=0.67, relwidth=1, relheight=0.008)
                
        self.canvas2.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        email_image = ctk.CTkImage(light_image=Image.open("data/images/email.png"), size=(20, 20))
        
        self.email_support = ctk.CTkButton(self.side_frame, text=self.align_text("Email Support"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=email_image, compound="left", command=self.open_email_fn
                                         )
        self.email_support.place(relx=0, rely=0.72, relwidth=1, relheight=0.05)

        setting_image = ctk.CTkImage(light_image=Image.open("data/images/settings.png"), size=(20, 20))

        self.settings = ctk.CTkButton(self.side_frame, text=self.align_text("Settings"), text_color="#000000", corner_radius=0,
                                         fg_color="#ffffff", font=("Consolas", 16, "bold"), cursor="hand2", hover_color="#193c8a",
                                         image=setting_image, compound="left", command=self.settings_page
                                         )
        self.settings.place(relx=0, rely=0.79, relwidth=1, relheight=0.05)

        logout_image = ctk.CTkImage(light_image=Image.open("data/images/logout.png"), size=(20, 20))

        self.logout = ctk.CTkButton(self.side_frame, text=self.align_text("Log out"), image=logout_image, compound="left", text_color="#000000", 
                                         corner_radius=0, fg_color="#ffffff", font=("Consolas", 16, "bold"),
                                          cursor="hand2", hover_color="#193c8a", command=self.log_out_fn
                                         )
        self.logout.place(relx=0, rely=0.86, relwidth=1, relheight=0.05)

        self.manage_products_fn()
    
    def reset_window_fn(self):
        if hasattr (self, 'add_window'):
            self.add_window.destroy()
            # self.add_window = None
            # self.add_window_check = None

    def process_add_entity_fn(self, check, *args):
        if check == 0:
            if any(arg.strip() == "" for arg in args) :
                self.add_window.attributes('-topmost', False)
                messagebox.showerror("Fill Details", "Please Fill in All Boxes")
                self.add_window.attributes('-topmost', True)
            else:
                result = self.d.Run_Model([args[0]])
                a = self.c.get_category_details(self.db, "id", result[0]) 
                b = self.c.add_product(self.db, args[0], args[1], args[2], a[0][0])
                if b:
                    self.add_window.destroy()
                    messagebox.showinfo("Success", "Product Added Successfully")
                    self.manage_products_fn()
                else:
                    self.add_window.attributes('-topmost', False)
                    messagebox.showerror("Error", "Something Wrong has happened")
                    self.add_window.attributes('-topmost', True)
        else:
            if any(arg.strip() == "" for arg in args) :
                self.add_cus_window.attributes('-topmost', False)
                messagebox.showerror("Fill Details", "Please Fill in All Boxes")
                self.add_cus_window.attributes('-topmost', True)
            else:
                b = self.b.register_customer(self.db, args[0], args[1], args[2], args[3])
                if b:
                    self.add_cus_window.destroy()
                    messagebox.showinfo("Success", "Customer Registered Successfully")
                    self.manage_customers_fn()
                else:
                    self.add_cus_window.attributes('-topmost', False)
                    messagebox.showerror("Error", "Something Wrong has happened")
                    self.add_cus_window.attributes('-topmost', True)

    def Add_product_fn(self):
        if hasattr(self, 'add_window') and self.add_window.winfo_exists() :
            self.add_window.focus()
            return

        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title(f"Add Product")
        self.add_window.configure(fg_color="#ffffff")
        self.add_window.resizable(False, False)
        self.add_window.lift()
        self.add_window.attributes('-topmost', True)

        c_x = int(self.width / 2 - 500 / 2)
        c_y = int(self.height / 2 - 350 / 2)
        self.add_window.geometry(f"500x350+{c_x}+{c_y}")

        # self.add_window.protocol('WM_DELETE_WINDOW', self.reset_window_fn)

        head_label = ctk.CTkLabel(self.add_window, text=f"Add Product", text_color="#000000", fg_color="#ffffff",
                                    font=("Arial", 24, "bold"))
        head_label.place(relx=0.35, rely=0.05)

        name_entry = ctk.CTkEntry(self.add_window, placeholder_text="Product Name",corner_radius=10)
        name_entry.place(relx=0.3, rely=0.19, relwidth=0.4, relheight=0.1)

        price_entry = ctk.CTkEntry(self.add_window, placeholder_text="Product Price",corner_radius=10)
        price_entry.place(relx=0.3, rely=0.34, relwidth=0.4, relheight=0.1)

        stock_entry = ctk.CTkEntry(self.add_window, placeholder_text="Product Stock",corner_radius=10)
        stock_entry.place(relx=0.3, rely=0.49, relwidth=0.4, relheight=0.1)

        ok_btn = ctk.CTkButton(self.add_window, text="OK", text_color="#ffffff", fg_color="#037ade",
                                        cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                        command=lambda : self.process_add_entity_fn(0, name_entry.get(), price_entry.get(), stock_entry.get()))
        ok_btn.place(relx=0.38, rely=0.67, relwidth=0.25, relheight=0.08)

        footer = "The product ID will be generated automatically, and the category will be intelligently assigned using AI."
        footer_label = ctk.CTkLabel(self.add_window, text=footer, text_color="#888888",
                                        font=("Roboto Italic", 10))
        footer_label.place(relx=0.02, rely=0.88,relheight=0.1)
        
    def context_menu_fn(self, event):
        self.row_id = self.tree.identify_row(event.y)

        if self.row_id:
            self.context_menu.post(event.x_root, event.y_root)

    def delete_row(self, check=0):
        if self.row_id:
            value = self.tree.item(self.row_id, "values")
            if check == 0:
                result = self.c.delete_product(self.db, value[0])
            else:
                result = self.b.delete_customer(self.db, value[0])
            self.tree.delete(self.row_id)
            if result:
                messagebox.showinfo("Success", "Operation Successful")
    
    def process_Entity_alter_fn(self, check, *args):
        if self.row_id:
            value = self.tree.item(self.row_id, "values")
        
        if check == 0:
            check_id = value[0]
            value = value[1:4]
        else:
            check_id = value[0]
            value = value[1:]

        if value == args:
            self.alter_window.destroy()

        if check == 0:
            result = self.c.alter_product(self.db, check_id, name=args[0], price=args[1], stocklevel=args[2])
            if result:
                self.alter_window.destroy()
                messagebox.showinfo("Success", "Product Info Edited Successfully")
                self.manage_products_fn()
        else:
            result = self.b.alter_customer_info(self.db, check_id, name=args[0], cnic=value[1], 
                                                email=args[2], phone=args[3], reg_date=args[4]
                                                )
            if result:
                self.alter_window.destroy()
                messagebox.showinfo("Success", "Customer Info Edited Successfully")
                self.manage_customers_fn()

    def alter_row(self, check):
        if hasattr(self, "alter_window") and self.alter_window.winfo_exists():
            self.alter_window.focus()
            return

        self.alter_window = ctk.CTkToplevel(self)
        self.alter_window.title("Edit Product")
        self.alter_window.configure(fg_color="#ffffff")
        self.alter_window.resizable(False, False)
        self.alter_window.lift()

        c_x = int(self.width/2 - 500/2)
        c_y = int(self.height/2 - 350/2)

        self.alter_window.geometry(f"500x350+{c_x}+{c_y}")

        if check == 0:

            head_label = ctk.CTkLabel(self.alter_window, text="Edit Product", text_color="#000000", fg_color="#ffffff",
                                    font=("Arial", 24, "bold"))
            head_label.place(relx=0.35, rely=0.05)

            name_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Product Name",corner_radius=10)
            name_entry.place(relx=0.08, rely=0.19, relwidth=0.4, relheight=0.1)

            price_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Product Price",corner_radius=10)
            price_entry.place(relx=0.08, rely=0.32, relwidth=0.4, relheight=0.1)

            stock_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Product Stock",corner_radius=10)
            stock_entry.place(relx=0.08, rely=0.45, relwidth=0.4, relheight=0.1)

            photo_label = ctk.CTkLabel(self.alter_window, text="", corner_radius=10, fg_color="#000000")
            photo_label.place(relx=0.6, rely=0.19, relwidth=0.25, relheight=0.3)

            add_image = ctk.CTkButton(self.alter_window, text="Add Image", text_color="#ffffff", fg_color="#000000", bg_color="#000000",
                                         cursor="hand2", hover=False, corner_radius=0, font=("Roboto", 10, "bold")
                                         )
            add_image.place(relx=0.63, rely=0.28, relwidth=0.2, relheight=0.1)

            ok_rely = 0.63
        else:
            head_label = ctk.CTkLabel(self.alter_window, text="Edit Customer Details", text_color="#000000", fg_color="#ffffff",
                                    font=("Arial", 24, "bold"))
            head_label.place(relx=0.29, rely=0.05)

            name_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Customer Name",corner_radius=10)
            name_entry.place(relx=0.33, rely=0.19, relwidth=0.4, relheight=0.1)

            cnic_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Customer CNIC", corner_radius=10)
            cnic_entry.place(relx=0.33, rely=0.32, relwidth=0.4, relheight=0.1)

            email_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Customer Email", corner_radius=10)
            email_entry.place(relx=0.33, rely=0.45, relwidth=0.4, relheight=0.1)

            phone_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Phone Number", corner_radius=10)
            phone_entry.place(relx=0.33, rely=0.58, relwidth=0.4, relheight=0.1)

            date_entry = ctk.CTkEntry(self.alter_window, placeholder_text="Registration Date", corner_radius=10)
            date_entry.place(relx=0.33, rely=0.71, relwidth=0.4, relheight=0.1)

            ok_rely = 0.83

        if self.row_id:
            value = self.tree.item(self.row_id, "values")

        if check == 0:
            value = value[0:4]
        else:
            value = value[0:]
        

        for widget, data in zip(self.alter_window.winfo_children(), value):
            if isinstance(widget, ctk.CTkEntry):
                widget.insert(0, data)
               
        ok_btn = ctk.CTkButton(self.alter_window, text="OK", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold")
                                          )
        if check == 0:
            ok_btn.configure(command = lambda : self.process_Entity_alter_fn(check,
                                                                             name_entry.get(), 
                                                                             price_entry.get(), 
                                                                             stock_entry.get()
                                                                             ))
        else:
            ok_btn.configure(command = lambda : self.process_Entity_alter_fn(check,
                                                                             name_entry.get(), 
                                                                             cnic_entry.get(), 
                                                                             email_entry.get(),
                                                                             phone_entry.get(),
                                                                             date_entry.get()
                                                                             ))
        ok_btn.place(relx=0.42, rely=ok_rely, relwidth=0.25, relheight=0.08)

    def ViewEdit_Entity_fn(self, data, columns, frame, delValue=0):

        if hasattr(self, "tree"):
            self.tree.destroy()

        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=50)
        style = ttk.Style()

        style.configure("Treeview.Heading",font=("Arial Black", 12, "bold"))

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, anchor="center", width=int(0.05 * self.width))
            else:
                self.tree.column(col, anchor="center", width=int(0.1 * self.width))

        if data:
            for row in data:
                self.tree.insert("", "end", values=row)
        
        self.tree.pack(fill="both", expand=True)

        self.context_menu = tk.Menu(frame, tearoff=0)
        if delValue == 0 or delValue == 1:
            self.context_menu.add_command(label="Alter", command= lambda : self.alter_row(delValue))
            self.context_menu.add_command(label="Delete", command=lambda : self.delete_row(delValue))
            self.tree.bind("<Button-3>", self.context_menu_fn)
    
    def handle_search_fn(self, data, columns, frame, entry, delValue=0, event=None):

        search_content = entry.get()

        if not search_content:
            self.ViewEdit_Entity_fn(data, columns, frame, delValue)
        else:
            return

    def search_Entity_fn(self, id, columns, frame, choice=0, event=None):
        if choice == 0:
            result = self.c.get_product_details(self.db, id)
        elif choice == 1:
            result = self.b.get_customer_details(self.db, id)
        else:
            if self.two_button.get().strip() == "Orders":
                result = self.g.get_order_details(self.db, id, 0, 1)
            else:
                result = self.g.get_order_details(self.db, id, 1, 1)

        if result:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.ViewEdit_Entity_fn(result, columns, frame, choice)
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def manage_products_fn(self):

        if hasattr(self, "product_frame"):
            self.product_frame.destroy()

        columns = ["ID", "Product Name", f"Product Price({self.currency})", "Stock Level", "Product Category"]

        self.product_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.product_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.product_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Products", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        self.add_product_btn = ctk.CTkButton(upper_frame, text="Add Product", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=self.Add_product_fn
                                         )
        self.add_product_btn.place(relx=0.85, rely=0.05, relwidth=0.13, relheight=0.15)

        self.canvas3 = tk.Canvas(self.product_frame, highlightthickness=0)
        self.canvas3.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        self.canvas3.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        self.search_entry = ctk.CTkEntry(self.product_frame, placeholder_text="Search Product",corner_radius=10)
        self.search_entry.place(relx=0.65, rely=0.13, relwidth=0.3, relheight=0.05)

        search_icon = ctk.CTkImage(light_image=Image.open("data/images/search_icon.png"), size=(20, 20))

        self.search_btn = ctk.CTkButton(self.product_frame, text="", image=search_icon, cursor="hand2",
                                         hover=False, fg_color=self.search_entry.cget("fg_color"),
                                         command=lambda:self.search_Entity_fn(self.search_entry.get(), columns, self.product_display_frame))
        self.search_btn.place(relx=0.9, relwidth=0.04, relheight=0.04, rely=0.135)

        self.search_entry.bind("<Return>", 
                               lambda event : self.search_Entity_fn(self.search_entry.get(), columns, self.product_display_frame))

        self.product_display_frame = ctk.CTkScrollableFrame(self.product_frame, fg_color="#ffffff", corner_radius=0)
        self.product_display_frame.place(relx=0, rely=0.21, relwidth=1, relheight=0.7)

        data = self.c.get_product_details(self.db, 0)

        self.search_entry.bind("<KeyRelease>", 
                               lambda event : self.handle_search_fn(data, 
                                                                    columns, 
                                                                    self.product_display_frame,
                                                                    self.search_entry)
                               )

        self.ViewEdit_Entity_fn(data, columns, self.product_display_frame, 0)
    
    def filter_data_fn(self, g_type, df):
        
        df["ord_date"] = pd.to_datetime(df["ord_date"])
        
        today = datetime.now().date()
        X_label, Y_label, quan, top_prod = None, None, None, None

        if g_type == "Today":
            filter = df["ord_date"].dt.date == today
            X_label = df.loc[filter, "ord_time"]
            Y_label = df.loc[filter, "total_sales"]
            quan = df.loc[filter, "quantity_sold"]
            
            if not quan.empty:
                a = quan.idxmax()
                top_prod = df.loc[a, "p_id"]
            else:
                top_prod = None

        elif g_type == "Last 7 Days":
            start_date = today - timedelta(days=7)
            filter = ((df["ord_date"].dt.date >= start_date) & (df["ord_date"].dt.date < today))
            filtered_df = df.loc[filter]

            if not filtered_df.empty:
                X_label = filtered_df["ord_date"].dt.date.unique()
                Y_label = filtered_df.groupby(filtered_df["ord_date"].dt.date)["total_sales"].sum()
                quan = filtered_df.groupby(filtered_df["ord_date"].dt.date)["quantity_sold"].sum()
                top_prod = filtered_df.loc[filtered_df["quantity_sold"].idxmax(), "p_id"]

        elif g_type == "Last 30 Days":
            start_date = today - timedelta(days=30)
            filter = ((df["ord_date"].dt.date >= start_date) & (df["ord_date"].dt.date < today))
            filtered_df = df.loc[filter]

            if not filtered_df.empty:
                X_label = filtered_df["ord_date"].dt.date.unique()
                Y_label = filtered_df.groupby(filtered_df["ord_date"].dt.date)["total_sales"].sum()
                quan = filtered_df.groupby(filtered_df["ord_date"].dt.date)["quantity_sold"].sum()
                top_prod = filtered_df.loc[filtered_df["quantity_sold"].idxmax(), "p_id"]
        
        else:
            X_label = df["ord_date"]
            Y_label = df["total_sales"]
            quan = df["quantity_sold"]

            if not quan.empty:
                top_prod = df.loc[df["quantity_sold"].idxmax(), "p_id"]
        
        return X_label, Y_label, quan, top_prod

    def plot_graph_fn(self, g_type):
        df = pd.read_csv("data/Sales Data/sales_data.csv")
        if hasattr(self, "ax"):
            self.ax.clear()

        X_label, Y_label, quan, top_prod= self.filter_data_fn(g_type, df)
        
        val = sum(i for i in Y_label)
        quan = sum(i for i in quan)

        self.revenue_lbl.configure(text = f"Total Revenue : {val/1000}k")
        self.item_sold_lbl.configure(text = f"Product Sold : {quan}")
        self.topproduct_lbl.configure(text = f"Top Product : {top_prod}")

        if hasattr(self, "anal_sale_frame") and self.anal_sale_frame.winfo_exists():
            self.anal_sale_frame.update_idletasks()

        self.ax.plot(X_label, Y_label, marker="o", color="b", label="Sales")

        self.ax.set_title("Sales Analysis")

        if g_type == "All-Time":
            first_date = X_label.values[0]
            middle_date = X_label.values[len(X_label) // 2]
            last_date = X_label.values[-1]

            custom_tick = [first_date, middle_date, last_date]

            custom_label = [datetime.fromisoformat(str(d)).strftime("%d-%b") for d in custom_tick]

            plt.xticks(ticks=custom_tick, labels=custom_label)
        
        elif g_type == "Last 7 Days":
            custom_label = [datetime.fromisoformat(str(d)).strftime("%d-%b") for d in X_label]

            plt.xticks(ticks=X_label, labels=custom_label)

        elif g_type == "Last 30 Days":
            X_label = pd.Series(X_label)
            first_date = X_label.values[0]
            left_date = X_label.values[len(X_label) // 4]
            right_date = X_label.values[len(X_label) // 3]
            middle_date = X_label.values[len(X_label) // 2]
 
            last_date = X_label.values[-1]

            custom_tick = [first_date, left_date, right_date, middle_date, last_date]
        
            custom_label = [datetime.fromisoformat(str(d)).strftime("%d-%b") for d in custom_tick]

            plt.xticks(ticks=custom_tick, labels=custom_label)

        else:
            X_label = X_label.unique()
            start_time = X_label[0]
            mid_time = X_label[len(X_label) // 2]
            end_time = X_label[-1]

            custom_ticks = [start_time, mid_time, end_time]

            custom_labels = [datetime.strptime(str(d), "%I : %M : %S %p").strftime("%I : %M %p") for d in custom_ticks]

            plt.xticks(ticks=custom_ticks, labels=custom_labels)

            # self.ax.set_xticks([])
            # self.ax.set_yticks([])
        plt.grid(True)
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.legend()

        self.canvas_graph.draw()

    def Segment_btn_fn(self, selected_value):
        
        Order_col = ["Order ID", "Customer ID", "Order Date", "Order Time", "Total Amount"]
        Order_detail_col = ["ID", "Order ID", "Product ID", "Quantity"]

        Order_data = self.g.get_order_details(self.db, 0, 0, 0)
        Order_detail_data = self.g.get_order_details(self.db, 0, 1, 0)

        if selected_value == "Orders":
            self.ViewEdit_Entity_fn(Order_data, Order_col, self.ord_disply_frame, 2)
        else:
            self.ViewEdit_Entity_fn(Order_detail_data, Order_detail_col, self.ord_disply_frame, 2)
    
    def Two_Search_fn(self, id, event=None):
        Order_col = ["Order ID", "Customer ID", "Order Date", "Order Time", "Total Amount"]
        Order_detail_col = ["ID", "Order ID", "Product ID", "Quantity"]

        if self.two_button.get().strip() == "Orders":
            self.search_Entity_fn(id, Order_col, self.ord_disply_frame, 2)
        else:
            self.search_Entity_fn(id, Order_detail_col, self.ord_disply_frame, 2)
    
    def Two_Search_Handle_fn(self, entry, event=None):
        Order_col = ["Order ID", "Customer ID", "Order Date", "Order Time", "Total Amount"]
        Order_detail_col = ["ID", "Order ID", "Product ID", "Quantity"]

        Order_data = self.g.get_order_details(self.db, 0, 0, 0)
        Order_detail_data = self.g.get_order_details(self.db, 0, 1, 0)

        if self.two_button.get().strip() == "Orders":
            self.handle_search_fn(Order_data, Order_col, self.ord_disply_frame, entry, 2)
        else:
            self.handle_search_fn(Order_detail_data, Order_detail_col, self.ord_disply_frame, entry, 2)
    
    def plot_pred_graph_fn(self, gtype):

        X_label, Y_label = self.p.get_future_sales_fn(gtype)
        print(X_label, Y_label)
        print(gtype)

        if hasattr(self, "ax1"):
            self.ax1.clear()
        
        self.ax1.set_title("Sales Prediction")
        self.ax1.plot(X_label, Y_label, marker="o", color="b", label="Sales")

        if gtype == "Next 7 Days":
            custom_label = [datetime.fromisoformat(str(d)).strftime("%d-%b") for d in X_label]

            plt.xticks(ticks=X_label, labels=custom_label)
            
        elif gtype == "Next 30 Days":
            X_label = pd.Series(X_label)
            first_date = X_label.values[0]
            left_date = X_label.values[len(X_label) // 4]
            right_date = X_label.values[len(X_label) // 3]
            middle_date = X_label.values[len(X_label) // 2]
 
            last_date = X_label.values[-1]

            custom_tick = [first_date, left_date, right_date, middle_date, last_date]
        
            custom_label = [datetime.fromisoformat(str(d)).strftime("%d-%b") for d in custom_tick]

            plt.xticks(ticks=custom_tick, labels=custom_label)

        plt.grid(True)
        self.ax1.set_xlabel("")
        self.ax1.set_ylabel("")
        self.ax1.legend()

        self.canvas_graph1.draw()
    
    def go_back_fn(self, event, function):
        function()
        
    def predict_sales_fn(self):
        if hasattr(self, "pred_sale_frame") and self.pred_sale_frame.winfo_exists():
            self.pred_sale_frame.destroy()
        
        if hasattr(self, "g_widget"):
            self.g_widget.destroy()
                    
        self.pred_sale_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=0)
        self.pred_sale_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.pred_sale_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Predict Sales", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        canvas = tk.Canvas(self.pred_sale_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        options = ["Next 7 Days", "Next 30 Days"]

        self.pred_selected_option = ctk.StringVar(master=self.pred_sale_frame, value=options[0])

        self.pred_graph_range_menu = ctk.CTkOptionMenu(self.pred_sale_frame, variable=self.pred_selected_option, values=options,
                                                  fg_color="#193c8a", text_color="#ffffff", font=("Arial", 12, "bold"),
                                                  dropdown_fg_color="#193c8a", dropdown_text_color="#ffffff", hover=False,
                                                  cursor="hand2", dropdown_hover_color="#171f24",
                                                  command=self.plot_pred_graph_fn)
        self.pred_graph_range_menu.place(relx=0.1, rely=0.13)

        self.bind("<Escape>", lambda event : self.go_back_fn(event, self.analyze_sales_fn))
    
        self.pred_sales_graph_frame = ctk.CTkFrame(self.pred_sale_frame, fg_color="#ffffff", corner_radius=0)
        self.pred_sales_graph_frame.place(relx=0.15, rely=0.17, relwidth=0.7, relheight=0.7)

        width = self.pred_sale_frame.winfo_width()
        height = self.pred_sale_frame.winfo_height()

        graph_width = width * 0.8
        graph_height = height * 0.8

        self.fig1, self.ax1 = plt.subplots(figsize=(graph_width / 100, graph_height / 100))
        self.canvas_graph1 = FigureCanvasTkAgg(self.fig1, master=self.pred_sales_graph_frame)
        self.g_widget1 = self.canvas_graph1.get_tk_widget()
        self.g_widget1.pack()

        self.plot_pred_graph_fn(options[0])

    def analyze_sales_fn(self):

        if hasattr(self, "anal_sale_frame") and self.anal_sale_frame.winfo_exists():
            self.anal_sale_frame.destroy()
        
        if hasattr(self, "pred_sale_frame") and self.pred_sale_frame.winfo_exists():
            self.pred_sale_frame.destroy()
            if hasattr(self, "g_widget1"):
                self.g_widget1.destroy()
            
        self.anal_sale_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=0)
        self.anal_sale_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.anal_sale_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Analyze Sales", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)
        
        self.pred_sale_btn = ctk.CTkButton(upper_frame, text="Predict Sales", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=self.predict_sales_fn
                                         )
        self.pred_sale_btn.place(relx=0.85, rely=0.05, relwidth=0.13, relheight=0.15)

        canvas = tk.Canvas(self.anal_sale_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        options = ["Today", "Last 7 Days", "Last 30 Days", "All-Time"]

        self.selected_option = ctk.StringVar(master=self.sales_frame, value=options[0])

        self.graph_range_menu = ctk.CTkOptionMenu(self.anal_sale_frame, variable=self.selected_option, values=options,
                                                  fg_color="#193c8a", text_color="#ffffff", font=("Arial", 12, "bold"),
                                                  dropdown_fg_color="#193c8a", dropdown_text_color="#ffffff", hover=False,
                                                  cursor="hand2", dropdown_hover_color="#171f24",
                                                  command=self.plot_graph_fn)
        self.graph_range_menu.place(relx=0.1, rely=0.13)

        self.bind("<Escape>", lambda event : self.go_back_fn(event, self.manage_sales_fn))

        self.sales_graph_frame = ctk.CTkFrame(self.anal_sale_frame, fg_color="#ffffff", corner_radius=0)
        self.sales_graph_frame.place(relx=0.15, rely=0.17, relwidth=0.7, relheight=0.7)

        self.revenue_lbl = ctk.CTkLabel(self.anal_sale_frame, text="Total Revenue : ", text_color="#ffffff", fg_color="#193c8a",
                                        font=("Arial", 16, "bold"), corner_radius=20)
        self.revenue_lbl.place(relx=0.08, rely=0.87, relwidth=0.2, relheight=0.05)

        self.item_sold_lbl = ctk.CTkLabel(self.anal_sale_frame, text="Products Sold : ", text_color="#ffffff", fg_color="#193c8a",
                                        font=("Arial", 16, "bold"), corner_radius=20)
        self.item_sold_lbl.place(relx=0.4, rely=0.87, relwidth=0.2, relheight=0.05)

        self.topproduct_lbl = ctk.CTkLabel(self.anal_sale_frame, text="Top Product : ", text_color="#ffffff", fg_color="#193c8a",
                                        font=("Arial", 16, "bold"), corner_radius=20)
        self.topproduct_lbl.place(relx=0.7, rely=0.87, relwidth=0.2, relheight=0.05)

        width = self.anal_sale_frame.winfo_width()
        height = self.anal_sale_frame.winfo_height()

        graph_width = width * 0.7
        graph_height = height * 0.7
        
        self.fig, self.ax = plt.subplots(figsize=(graph_width / 100, graph_height / 100))
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self.sales_graph_frame)
        self.g_widget = self.canvas_graph.get_tk_widget()
        self.g_widget.pack()
        
        self.plot_graph_fn(options[0])

    def manage_sales_fn(self):
        if hasattr(self, "sales_frame") and self.sales_frame.winfo_exists():
            self.sales_frame.destroy()
        
        if hasattr(self, "anal_sale_frame") and self.anal_sale_frame.winfo_exists():
            self.anal_sale_frame.destroy()
            if hasattr(self, "g_widget"):
                self.g_widget.destroy()

        self.sales_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.sales_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.sales_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Sales", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        self.view_sale_btn = ctk.CTkButton(upper_frame, text="Analyze Sales", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=self.analyze_sales_fn
                                         )
        self.view_sale_btn.place(relx=0.85, rely=0.05, relwidth=0.13, relheight=0.15)

        canvas = tk.Canvas(self.sales_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        self.under_sale_frame = ctk.CTkFrame(self.sales_frame, fg_color="#ffffff", corner_radius=0)
        self.under_sale_frame.place(relx=0, rely=0.13, relwidth=1, relheight=1)
        
        self.two_button = ctk.CTkSegmentedButton(self.under_sale_frame, values=["Orders", "Detail"], text_color="#000000",
                                                 corner_radius=0, font=("Consolas", 12, "bold"), selected_hover_color="#037ade",
                                                 unselected_color="#ffffff", border_width=2,
                                                 command=self.Segment_btn_fn)
        self.two_button.place(relx=0.05, rely=0.02)

        self.two_button.set("Orders")

        self.search_order_entry = ctk.CTkEntry(self.under_sale_frame, placeholder_text="Search",corner_radius=10)
        self.search_order_entry.place(relx=0.65, rely=0.02, relwidth=0.3, relheight=0.05)

        search_icon = ctk.CTkImage(light_image=Image.open("data/images/search_icon.png"), size=(20, 20))
        self.search_ord_btn = ctk.CTkButton(self.under_sale_frame, text="", image=search_icon, cursor="hand2",
                                         hover=False, fg_color=self.search_order_entry.cget("fg_color"),
                                         command=lambda:self.Two_Search_fn(self.search_order_entry.get()))
        self.search_ord_btn.place(relx=0.9, relwidth=0.04, relheight=0.04, rely=0.023)


        self.ord_disply_frame = ctk.CTkScrollableFrame(self.under_sale_frame, fg_color="#ffffff", corner_radius=0)
        self.ord_disply_frame.place(relx=0, rely=0.09, relwidth=1, relheight=0.7)

        self.search_order_entry.bind("<Return>", 
                               lambda event : self.Two_Search_fn(self.search_order_entry.get()))
        
        self.Segment_btn_fn(self.two_button.get())

        self.search_order_entry.bind("<KeyRelease>", 
                               lambda event : self.Two_Search_Handle_fn(self.search_order_entry)
                               )
    
    def add_customer_fn(self):
        if hasattr(self, 'add_cus_window') and self.add_cus_window.winfo_exists() :
            self.add_cus_window.focus()
            return

        self.add_cus_window = ctk.CTkToplevel(self)
        self.add_cus_window.title(f"Add Customer")
        self.add_cus_window.configure(fg_color="#ffffff")
        self.add_cus_window.resizable(False, False)
        self.add_cus_window.lift()
        self.add_cus_window.attributes('-topmost', True)

        c_x = int(self.width / 2 - 500 / 2)
        c_y = int(self.height / 2 - 350 / 2)
        self.add_cus_window.geometry(f"500x350+{c_x}+{c_y}")

        # self.add_window.protocol('WM_DELETE_WINDOW', self.reset_window_fn)

        head_label = ctk.CTkLabel(self.add_cus_window, text=f"Add Customer", text_color="#000000", fg_color="#ffffff",
                                    font=("Arial", 24, "bold"))
        head_label.place(relx=0.35, rely=0.05)

        name_entry = ctk.CTkEntry(self.add_cus_window, placeholder_text="Customer Name",corner_radius=10)
        name_entry.place(relx=0.33, rely=0.19, relwidth=0.4, relheight=0.1)

        cnic_entry = ctk.CTkEntry(self.add_cus_window, placeholder_text="Customer CNIC", corner_radius=10)
        cnic_entry.place(relx=0.33, rely=0.32, relwidth=0.4, relheight=0.1)

        email_entry = ctk.CTkEntry(self.add_cus_window, placeholder_text="Customer Email", corner_radius=10)
        email_entry.place(relx=0.33, rely=0.45, relwidth=0.4, relheight=0.1)

        phone_entry = ctk.CTkEntry(self.add_cus_window, placeholder_text="Phone Number", corner_radius=10)
        phone_entry.place(relx=0.33, rely=0.58, relwidth=0.4, relheight=0.1)


        ok_btn = ctk.CTkButton(self.add_cus_window, text="OK", text_color="#ffffff", fg_color="#037ade",
                                        cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                        command=lambda : self.process_add_entity_fn(1, name_entry.get(), 
                                                                                    cnic_entry.get(), 
                                                                                    email_entry.get(), 
                                                                                    phone_entry.get()
                                                                                    ))
        ok_btn.place(relx=0.42, rely=0.78, relwidth=0.25, relheight=0.08)

    def manage_customers_fn(self):
        if hasattr(self, "cus_frame") and self.cus_frame.winfo_exists():
            self.cus_frame.destroy()
        
        columns = ["Customer ID", "Name", "CNIC", "Email", "Phone", "Reg Date"]

        self.cus_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.cus_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.cus_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Customers", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        self.add_customer_btn = ctk.CTkButton(upper_frame, text="Add Customer", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=self.add_customer_fn)
        self.add_customer_btn.place(relx=0.85, rely=0.05, relwidth=0.13, relheight=0.15)

        canvas = tk.Canvas(self.cus_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        self.search_entry_cus = ctk.CTkEntry(self.cus_frame, placeholder_text="Search Customer",corner_radius=10)
        self.search_entry_cus.place(relx=0.65, rely=0.13, relwidth=0.3, relheight=0.05)

        search_icon = ctk.CTkImage(light_image=Image.open("data/images/search_icon.png"), size=(20, 20))

        self.search_btn_cus = ctk.CTkButton(self.cus_frame, text="", image=search_icon, cursor="hand2",
                                         hover=False, fg_color=self.search_entry_cus.cget("fg_color"),
                                         command=lambda:self.search_Entity_fn(self.search_entry_cus.get(), columns, self.cus_display_frame, 1))
        self.search_btn_cus.place(relx=0.9, relwidth=0.04, relheight=0.04, rely=0.135)

        self.search_entry_cus.bind("<Return>", 
                                   lambda event : self.search_Entity_fn(
                                       self.search_entry_cus.get(), 
                                       columns, 
                                       self.cus_display_frame,
                                       1))

        self.cus_display_frame = ctk.CTkScrollableFrame(self.cus_frame, fg_color="#ffffff", corner_radius=0)
        self.cus_display_frame.place(relx=0, rely=0.21, relwidth=1, relheight=0.7)

        data = self.b.get_customer_details(self.db, 0)

        self.search_entry_cus.bind("<KeyRelease>", 
                                   lambda event : self.handle_search_fn(data, 
                                                                        columns, 
                                                                        self.cus_display_frame, 
                                                                        self.search_entry_cus,
                                                                        1
                                                                        )
                                   )

        self.ViewEdit_Entity_fn(data, columns, self.cus_display_frame, 1)
    
    def add_to_cart_fn(self, data):
        data = list(data)
        data.pop()
        data.pop()

        quan_check = self.g.check_stocks_fn(self.db, data[0], 1)

        if quan_check:
            data.append(1)
        else:
            messagebox.showwarning("Error" , "No Stock Available")
            return
            
        data = tuple(data)

        if data in self.cart_list:
            return
        
        self.total_Price += data[2]
        self.cart_list.append(data)
        self.display_cart_fn()
        
        self.totalPrice_lbl.configure(text=f"Total Price : {self.total_Price}")

    def show_suggestions(self, event=None):
        value = self.search_entry_ProdMenu_var.get().lower()
        
        if self.is_id_searching:
            return
        
        if value and not value.isdigit():
            
            if self.suggestion_lst_frame.winfo_children():
                for widget in self.suggestion_lst_frame.winfo_children():
                    widget.destroy()
            
            result = self.c.get_product_details(self.db)
            
            suggestions = [
                prod for prod in result if prod[1].lower().startswith(value)
            ]

            if suggestions:
                self.suggestion_lst_frame.place(relx=0.65, rely=0.180, relwidth=0.3 )

                for product in suggestions:
                    suggest_label = ctk.CTkButton(self.suggestion_lst_frame, 
                                                text=f"{product[0]} - {product[1]}",
                                                text_color="#000000",
                                                fg_color=self.search_entry_ProdMenu.cget("fg_color"),
                                                corner_radius=0,
                                                anchor="w",
                                                hover=False,
                                                command=lambda idx = product: self.add_to_cart_fn(idx))
                    suggest_label.pack(fill="x", padx=5)
            else:
                if not isinstance(value, int):
                    self.suggestion_lst_frame.place_forget()
        else:
            if not value.isdigit():
                self.suggestion_lst_frame.place_forget()
    
    def search_id_fn(self, id, event=None):

        self.is_id_searching = None
        if id.isdigit():
            if isinstance(int(id), int):
                result = self.c.get_product_details(self.db, id)

                if result:
                    self.suggestion_lst_frame.place(relx=0.65, rely=0.180, relwidth=0.3)

                    if self.suggestion_lst_frame.winfo_children():
                        for widget in self.suggestion_lst_frame.winfo_children():
                            widget.destroy()

                    self.searched_id_btn = ctk.CTkButton(self.suggestion_lst_frame, 
                                                    text=f"{result[0][0]} - {result[0][1]}",
                                                    text_color="#000000",
                                                    fg_color=self.search_entry_ProdMenu.cget("fg_color"),
                                                    corner_radius=0,
                                                    anchor="w",
                                                    hover=False,
                                                    command=lambda : self.add_to_cart_fn(result[0]))
                    self.searched_id_btn.pack(fill="x", padx=5)

            else:
                self.suggestion_lst_frame.place_forget()
            
            self.is_id_searching = False
    
    def context_menu_cart_fn(self, event):
        self.cart_row_id = self.cart_tree.identify_row(event.y)
        if self.cart_row_id:
            self.cart_context_menu.post(event.x_root, event.y_root)

    def delete_cart_item(self):
        if self.cart_row_id:
            value = self.cart_tree.item(self.cart_row_id, "values")
            self.total_Price -= float(value[2]) * int(value[3])

            value = list(value)
            value[0] = float(value[0])
            value[2] = float(value[2])
            value[3] = float(value[3])
            value = tuple(value)
   
            self.cart_list.remove(value)
            self.totalPrice_lbl.configure(text=f"Total Price : {self.total_Price}")
            self.cart_tree.delete(self.cart_row_id)
    
    def get_cart_tree_rowId(self, event):
        self.cart_row_quan_id = self.cart_tree.identify_row(event.y)

    def display_cart_fn(self):
        if hasattr(self, 'cart_tree'):
            self.cart_tree.destroy()
        
        columns = ["ID", "Name", "Price", "Quantity"]

        self.cart_tree = ttk.Treeview(self.cart_frame, columns=columns, show="headings", height=50)

        style = ttk.Style()

        style.configure("Treeview.Heading",font=("Arial Black", 12, "bold"))
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            if col == "ID":
                self.cart_tree.column(col, anchor="center", width=int(0.05 * self.width))
            else:
                self.cart_tree.column(col, anchor="center", width=int(0.1 * self.width))
        
        if self.cart_list:
            for row in self.cart_list:
                self.cart_tree.insert("", "end", values=row)
                
        self.cart_tree.pack(fill="both", expand=True)
        
        self.cart_context_menu = tk.Menu(self.cart_frame, tearoff=0)
        self.cart_context_menu.add_command(label="Delete", command=self.delete_cart_item)

        self.cart_tree.bind("<ButtonRelease-1>", self.get_cart_tree_rowId)
        self.cart_tree.bind("<Button-3>", self.context_menu_cart_fn)
    
    def get_customer_id_fn(self):
        result = self.b.get_customer_details(self.db)

        cus_names_lst = []
        if result:
            for i in result:
                cus_names_lst.append(str(i[0]))
        
        return cus_names_lst
    
    def search_cus_id_fn(self, event):
        value = event.widget.get()
        customer_ids = self.get_customer_id_fn()
        customer_ids = [str(i) for i in customer_ids]

        if value == '' :
            self.cus_combo.configure(values=customer_ids)
        
        elif value not in customer_ids:
            self.cus_combo.configure(values=[])

        else:
            print(value)
            if value in customer_ids:
                self.cus_combo.configure(values=[value])
    
    def spin_value_fn(self, event=None):
        value = self.quan_box.get()
        
        temp_row = self.cart_tree.item(self.cart_row_quan_id, "values")
        
        quan_check = self.g.check_stocks_fn(self.db, int(temp_row[0]) , int(value))

        if not quan_check:
            messagebox.showwarning("Sorry", "Low Stock : Cannot Add More")
            return
        
        if self.cart_row_quan_id:
            rowValues = self.cart_tree.item(self.cart_row_quan_id, "values")
            rowValues = list(rowValues)
            rowValues[0] = int(rowValues[0])
            rowValues[2] = float(rowValues[2])
            rowValues[3] = int(rowValues[3])
            rowValues = tuple(rowValues)
            
            for index, data in enumerate(self.cart_list):
                if data == rowValues:
                    self.total_Price -= data[2] * data[3]
                    data_t = list(data)
                    data_t[3] = int(value)
                    self.cart_list[index] = tuple(data_t)
                    self.total_Price += data_t[2] * data_t[3]
                    self.totalPrice_lbl.configure(text=f"Total Price : {self.total_Price}")
                    

            self.display_cart_fn()
        else:
            pass

    def generate_receipt_fn(self):
        cus_id = self.cus_combo.get()
        
        result = self.g.place_order(self.db, cus_id, self.total_Price)
        if result:
            for i in self.cart_list:
                self.g.place_orderDetails(self.db, cus_id, i[0], i[3], self.total_Price)
                self.g.update_stocks_fn(self.db, int(i[0]), int(i[3]))

            data = self.b.get_customer_details(self.db, int(cus_id))
            
            self.e.generate_receipt([data[0][1], data[0][2]], self.cart_list, f"{self.total_Price} {self.currency}", self.b_name)

            messagebox.showinfo("Sucess", "Receipt Saved To Output Folder")
            
            A = self.g.Model_Sales_Data_fn(self.db)

            self.product_menu_fn()
        
    def product_menu_fn(self):
        if hasattr(self, "prod_menu_frame") and self.prod_menu_frame.winfo_exists():
            self.prod_menu_frame.destroy()
        
        self.is_id_searching = None
        self.cart_list = []
        self.total_Price = 0.0
        
        self.prod_menu_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.prod_menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.prod_menu_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Products Menu", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        canvas = tk.Canvas(self.prod_menu_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)
        
        self.search_entry_ProdMenu_var = ctk.StringVar()
        self.search_entry_ProdMenu = ctk.CTkEntry(self.prod_menu_frame, textvariable=self.search_entry_ProdMenu_var,
                                                  placeholder_text="Search Product", border_color="#a2a1a1", border_width=2, 
                                                  placeholder_text_color="#000000",
                                                  corner_radius=0)
        self.search_entry_ProdMenu.place(relx=0.65, rely=0.13, relwidth=0.3, relheight=0.05)

        self.search_entry_ProdMenu.bind('<KeyRelease>', self.show_suggestions)
        self.search_entry_ProdMenu.bind('<Return>', lambda event : self.search_id_fn(self.search_entry_ProdMenu.get()))

        self.suggestion_lst_frame = ctk.CTkScrollableFrame(self.prod_menu_frame, fg_color=self.search_entry_ProdMenu.cget("fg_color"), 
                                                           corner_radius=0, border_color="#a2a1a1",
                                                           border_width=2)

        search_icon = ctk.CTkImage(light_image=Image.open("data/images/search_icon.png"), size=(20, 20))

        self.search_btn_cus_ProdMenu = ctk.CTkButton(self.prod_menu_frame, text="", image=search_icon, cursor="hand2",
                                         hover=False, fg_color=self.search_entry_ProdMenu.cget("fg_color"),
                                         command= lambda : self.search_id_fn(self.search_entry_ProdMenu.get())
                                         )
        self.search_btn_cus_ProdMenu.place(relx=0.9, relwidth=0.04, relheight=0.04, rely=0.135)

        cart_label = ctk.CTkLabel(self.prod_menu_frame, text="Cart", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 24, "bold"))
        cart_label.place(relx=0.06, rely=0.15)

        self.cart_frame = ctk.CTkScrollableFrame(self.prod_menu_frame, fg_color="#ffffff", corner_radius=0, 
                                                 border_color="#000000", border_width=2)
        self.cart_frame.place(relx=0.05, rely=0.19, relwidth=0.5, relheight=0.4)

        self.totalPrice_lbl = ctk.CTkLabel(self.prod_menu_frame, text="Total Price : ", text_color="#ffffff", fg_color="#193c8a",
                                        font=("Arial", 16, "bold"), corner_radius=10)
        self.totalPrice_lbl.place(relx=0.08, rely=0.62, relwidth=0.2, relheight=0.05)

        self.cus_combo = ctk.CTkComboBox(self.prod_menu_frame, values=self.get_customer_id_fn(), fg_color="#ffffff", 
                                         text_color="#000000", font=("Arial", 14, "bold"))
        self.cus_combo.set("Select Customer")
        self.cus_combo.place(relx=0.08, rely=0.72, relwidth=0.25, relheight=0.05)

        self.cus_combo.bind('<KeyRelease>', self.search_cus_id_fn)

        self.quan_box = tk.Spinbox(self.prod_menu_frame, from_=1, to=100, font=("Arial", 14, "bold"),
                                   command=self.spin_value_fn)
        self.quan_box.place(relx=0.45, rely=0.62, relwidth=0.1, relheight=0.05)
        self.quan_box.bind("<Return>", self.spin_value_fn)

        self.gen_rec_btn = ctk.CTkButton(self.prod_menu_frame, text="Generate Receipt", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=self.generate_receipt_fn)
        self.gen_rec_btn.place(relx=0.4, rely=0.8, relheight=0.05)
    
    def about_us_fn(self):
        if hasattr(self, "about_us_frame") and self.about_us_frame.winfo_exists():
            self.about_us_frame.destroy()

        self.about_us_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.about_us_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.about_us_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.15)

        top_label = ctk.CTkLabel(upper_frame, text="AI Powered Shop Manager", text_color="#000000", 
                                fg_color="#ffffff", font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        subheading_label = ctk.CTkLabel(self.about_us_frame, 
                                        text="Streamline your shop management with AI-driven solutions.", 
                                        text_color="#000000", 
                                        fg_color="#ffffff", 
                                        font=("Roboto", 18, "bold"))
        subheading_label.place(relx=0.03, rely=0.1)

        canvas = tk.Canvas(self.about_us_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.15, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)
        
        quote_label = ctk.CTkLabel(
            self.about_us_frame, 
            text=(
                "\"Producing ten leaders is better than making thousand slaves\"\n"
                "\t\t\t\t~Mr. Irfan Malik"
            ),
            text_color="#000000", 
            fg_color="#ffffff", 
            font=("Roboto", 16, "bold"), 
            justify="center",
            wraplength=800 
        )
        quote_label.place(relx=0.03, rely=0.2, relwidth=0.94)

        
        main_content_heading = ctk.CTkLabel(self.about_us_frame, 
                                            text="Project Overview:", 
                                            text_color="#000000", 
                                            fg_color="#ffffff", 
                                            font=("Roboto", 16, "bold"))
        main_content_heading.place(relx=0.03, rely=0.3)

        about_text = (
            "The AI Powered Shop Manager is designed to streamline shop management tasks, "
            "such as managing products, analyzing sales trends, predicting future sales using "
            "machine learning models, and providing customer management features. The application "
            "ensures data security with encryption techniques and uses an intuitive graphical user interface for ease of use."
        )
        about_label = ctk.CTkLabel(self.about_us_frame, 
                                text=about_text, 
                                text_color="#000000", 
                                fg_color="#ffffff", 
                                wraplength=900, 
                                justify="left", 
                                font=("Roboto", 14))
        about_label.place(relx=0.03, rely=0.35)

        credits_heading = ctk.CTkLabel(self.about_us_frame, 
                                    text="Credits:", 
                                    text_color="#000000", 
                                    fg_color="#ffffff", 
                                    font=("Roboto", 16, "bold"))
        credits_heading.place(relx=0.03, rely=0.45)

        credits_label = ctk.CTkLabel(self.about_us_frame, 
                                    text="• Images provided by Flaticon.\n"
                                        "• AI models and data courtesy of Ahmad Malik.\n"
                                        "• Documentation by Muhammad Abdullah.\n"
                                        "• Requirements analysis assisted by ChatGPT.", 
                                    text_color="#000000", 
                                    fg_color="#ffffff", 
                                    justify="left", 
                                    font=("Roboto", 14))
        credits_label.place(relx=0.03, rely=0.5)

        footer_label = ctk.CTkLabel(
            self.about_us_frame, 
            text="Developed and Designed by Strange Solutions Pvt. Limited", 
            text_color="#000000", 
            fg_color="#ffffff", 
            font=("Roboto", 12, "italic"), 
            justify="center"
        )
        footer_label.place(relx=0.45, rely=0.95, anchor="center")


    def open_email_fn(self):
        gmail_url = "https://mail.google.com/mail/u/0/#inbox?compose=GTvVlcSMTSCNFKrRsHbxbnvJcPpmcPLfsFrPwVDDSbDCJwfDRCChLRDwxxnBMWxqCwsmTfHttxVrS"
        webbrowser.open(gmail_url)
    
    def save_apply_fn(self, name_entry, old_p, new_p, con_P):
        curr = self.currency_combo.get().split(" - ")[0]
        scr = self.scr_res_combo.get().split("x")

        setting = self.load_settings_fn()
        setting["width"] = int(scr[0])
        setting["height"] = int(scr[1])
        setting["currency"] = curr

        res = self.f.load_decrypted_credentials()
        if old_p == "" and new_p == "" and con_P == "":
            if res:
                if not name_entry  == " ":
                    a = self.a.update_name_fn(self.db, name_entry, res[0], res[1])
                    self.save_settings_fn(setting)
                    messagebox.showinfo("Saved", "Please Restart the Application")
        else:
            if old_p == "" or new_p == "" or con_P == "":
                messagebox.showwarning("Empty", "Some Fields are Empty")
            else:
                result = self.a.login_business(res[0], old_p, self.db)
                if result:
                    file_path = "data/credentials/credentials.enc"
                    if os.path.exists(file_path):
                        if new_p == con_P:
                            a = self.a.update_name_fn(self.db, name_entry, res[0], res[1])
                            b = self.a.update_password_fn(self.db, new_p, res[0], res[1])
                            self.f.store_encrypted_credentials(res[0], new_p)
                            messagebox.showinfo("Saved", "Please Restart the Application")
                        else:    
                            messagebox.showwarning("MisMatch", "New and Confirm Password Does not Match")
                else:
                    messagebox.showerror("Wrong Password", "Please Enter Correct Password")
                    
    def settings_page(self):
    
        self.setting_frame = ctk.CTkFrame(self.main_center_frame, fg_color="#ffffff", corner_radius=10)
        self.setting_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        upper_frame = ctk.CTkFrame(self.setting_frame, fg_color="#ffffff", corner_radius=0)
        upper_frame.place(relx=0, rely=0.02, relwidth=1, relheight=0.2)

        top_label = ctk.CTkLabel(upper_frame, text="Settings", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 28, "bold"))
        top_label.place(relx=0.03, rely=0)

        canvas = tk.Canvas(self.setting_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        bus_label = ctk.CTkLabel(self.setting_frame, text="Business Information", text_color="#07058e", fg_color="#ffffff",
                                      font=("Roboto", 22, "bold"))
        bus_label.place(relx=0.03, rely=0.15)

        canvas = tk.Canvas(self.setting_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.19, relwidth=0.3, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        name_label = ctk.CTkLabel(self.setting_frame, text="Update Name", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 18, "bold"))
        name_label.place(relx=0.05, rely=0.22, relwidth=0.2, relheight=0.08)

        res = self.f.load_decrypted_credentials()
        res1 = self.a.get_business_name(res[0], res[1], self.db)
        # settings = self.load_settings_fn()

        name_entry = ctk.CTkEntry(self.setting_frame, placeholder_text="",corner_radius=10)
        name_entry.place(relx=0.28, rely=0.2350, relwidth=0.2, relheight=0.05)

        name_entry.insert(0, str(res1))

        currency_label = ctk.CTkLabel(self.setting_frame, text="Update Currency", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 20, "bold"))
        currency_label.place(relx=0.09, rely=0.3)

        currencies = [
            "PKR - Pakistani Rupee",
            "USD - United States Dollar",
            "EUR - Euro",
            "GBP - British Pound",
            "JPY - Japanese Yen",
            "AUD - Australian Dollar",
            "CAD - Canadian Dollar",
            "CHF - Swiss Franc",
            "CNY - Chinese Yuan",
            "INR - Indian Rupee"
        ]

        self.currency_combo = ctk.CTkComboBox(self.setting_frame, values=currencies, fg_color="#ffffff", 
                                         text_color="#000000", font=("Arial", 14, "bold"))
        self.currency_combo.set(currencies[0])
        self.currency_combo.place(relx=0.28, rely=0.3, relwidth=0.22, relheight=0.05)

        dis_label = ctk.CTkLabel(self.setting_frame, text="Display Information", text_color="#07058e", fg_color="#ffffff",
                                      font=("Roboto", 22, "bold"))
        dis_label.place(relx=0.03, rely=0.36)

        canvas = tk.Canvas(self.setting_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.4, relwidth=0.3, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        scr_res_label = ctk.CTkLabel(self.setting_frame, text="Change Resolution", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 20, "bold"))
        scr_res_label.place(relx=0.09, rely=0.45)

        options = ["1366x768", "1440x900", "1600x900", "1920x1080"]
        
        self.scr_res_combo = ctk.CTkComboBox(self.setting_frame, values=options, fg_color="#ffffff", 
                                         text_color="#000000", font=("Arial", 14, "bold"))
        self.scr_res_combo.set(options[0])
        self.scr_res_combo.place(relx=0.28, rely=0.45, relwidth=0.15, relheight=0.05)

        dis1_label = ctk.CTkLabel(self.setting_frame, text="Change Password", text_color="#07058e", fg_color="#ffffff",
                                      font=("Roboto", 22, "bold"))
        dis1_label.place(relx=0.03, rely=0.51)
        
        canvas = tk.Canvas(self.setting_frame, highlightthickness=0)
        canvas.place(relx=0, rely=0.55, relwidth=0.3, relheight=0.004)

        canvas.create_line(0, 0, 1, 1, fill="#d7fff5", width=1)

        old_p_label = ctk.CTkLabel(self.setting_frame, text="Old Password", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 18, "bold"))
        old_p_label.place(relx=0.059, rely=0.59, relwidth=0.2, relheight=0.08)

        old_p_entry = ctk.CTkEntry(self.setting_frame, placeholder_text="",corner_radius=10)
        old_p_entry.place(relx=0.28, rely=0.61, relwidth=0.2, relheight=0.05)

        new_p_label = ctk.CTkLabel(self.setting_frame, text="New Password", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 18, "bold"))
        new_p_label.place(relx=0.059, rely=0.66, relwidth=0.2, relheight=0.08)

        new_p_entry = ctk.CTkEntry(self.setting_frame, placeholder_text="",corner_radius=10)
        new_p_entry.place(relx=0.28, rely=0.6750, relwidth=0.2, relheight=0.05)

        confirm_p_label = ctk.CTkLabel(self.setting_frame, text="Repeat Password", text_color="#000000", fg_color="#ffffff",
                                      font=("Roboto", 18, "bold"))
        confirm_p_label.place(relx=0.07, rely=0.73, relwidth=0.2, relheight=0.08)

        confirm_p_entry = ctk.CTkEntry(self.setting_frame, placeholder_text="",corner_radius=10)
        confirm_p_entry.place(relx=0.28, rely=0.7450, relwidth=0.2, relheight=0.05)

        self.apply_btn = ctk.CTkButton(self.setting_frame, text="Save & Apply", text_color="#ffffff", fg_color="#037ade",
                                         cursor="hand2", hover=False, corner_radius=10, font=("Roboto", 14, "bold"),
                                         command=lambda : self.save_apply_fn(name_entry.get(), 
                                                                             old_p_entry.get(), 
                                                                             new_p_entry.get(),
                                                                             confirm_p_entry.get())
                                         
                                         )
        self.apply_btn.place(relx=0.4, rely=0.85, relwidth=0.15, relheight=0.05)

    def log_out_fn(self):
        response = messagebox.askokcancel("Logout", "Are You Sure")
        if response:
            if hasattr(self, "main_frame"):
                file_path = "data/credentials/credentials.enc"
                self.main_frame.destroy()
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.login_page()


