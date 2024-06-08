from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from ttkbootstrap import ttk
import datetime
import mysql.connector
import qrcode
#from tkinter import PhotoImage
#from tkinter import Label
#from tkinter import Canvas

class MedicineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Medicine App")
        # Adjust window size as needed
        self.geometry("600x650")

        # Initialize an empty list
        self.medicine_options = []  
        self.dosage_options = ["1-0-1", "0-1-0", "1-1-1"]

        self.selected_medicine = tk.StringVar()
        self.selected_dosage = tk.StringVar()

        self.load_medicine_data()
        self.create_widgets()

    def load_medicine_data(self):
        try:
            # Establish connection to MySQL database (Replace with your credentials)
            conn = mysql.connector.connect(host="localhost", user="root", password="Aravind123", database="nitte")
            cursor = conn.cursor()

            # Execute query to fetch medicine data (Modify query as needed)
            cursor.execute("SELECT drug FROM TBagents")

            # Fetch all rows and add medicine names to medicine_options list
            for row in cursor.fetchall():
                self.medicine_options.append(row[0])
            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_widgets(self):        
        frame1 = tk.Frame(self)
        medicine_label = ttk.Label(master = frame1, text="Select Medicine")
        medicine_label.pack(side = "left", padx = 10)
        medicine_combo = ttk.Combobox(master = frame1, textvariable=self.selected_medicine)
        medicine_combo['values'] = self.medicine_options
        medicine_combo.pack(side = "left", pady = 20)
        frame1.pack()

        frame2 = tk.Frame(self)
        dosage_label = ttk.Label(master = frame2, text="Select Dosage")
        dosage_label.pack(side = "left", padx = 10)
        dosage_combo = ttk.Combobox(master = frame2, textvariable=self.selected_dosage)
        dosage_combo['values'] = self.dosage_options
        dosage_combo.pack(side = "left", pady = 20)
        frame2.pack()

        # Generate QR button with styling
        generate_qr_button = ttk.Button(self, text="Generate QR Code", command=self.generate_qr)
        generate_qr_button.pack(pady=10)

        # Container for QR code image
        self.qr_image_container = tk.Label(self)  
        self.qr_image_container.pack()

        """ self.framePhoto = PhotoImage(file = "C:\\Users\\Aravind M\\Desktop\\Everything\\nitte\\test\\bg\\flower.png")
        # might use later
        self.background_canvas = Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg="lightblue")
        self.background_canvas.pack(fill="both", expand=True)
        self.resized_photo = self.framePhoto.subsample(self.canvas_background.winfo_width(), self.canvas_background.winfo_height())
        self.image_on_canvas = self.canvas_background.create_image(100, 50, image=self.resized_photo, anchor="nw")
       
        # change the bg image scale
        self.framePhoto = self.framePhoto.subsample(1, 1)
        self.frameLabel = Label(self, image = self.framePhoto)
        self.frameLabel.pack() """

    def generate_qr(self):
        medicine = self.selected_medicine.get()
        dosage = self.selected_dosage.get()

        if not medicine or not dosage:
                messagebox.showerror("Error", "Medicine name/Dosage field is empty!")
        
        elif medicine  or dosage:
            # Get timestamp
            current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            # Combine medicine name and timestamp
            filename = f"{medicine}_{current_time}.png" 

            try:
                # Calculate expiration time (placeholder for now)
                expiration_time = current_time

                # Include expiration time in QR code data
                qr_data = f"Medicine: {medicine}\nDosage: {dosage}\nThis QR Code will Expire on: {expiration_time}"
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(qr_data)
                qr.make()
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(filename)

                # Convert QR code image to Tkinter compatible format
                self.qr_image = ImageTk.PhotoImage(Image.open(filename))
                self.qr_image_container.config(image=self.qr_image)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate QR Code: {e}")
        else:
            messagebox.showerror("Unknown Error", "An unknown error has occured")

if __name__ == "__main__":
    app = MedicineApp()
    app.mainloop()