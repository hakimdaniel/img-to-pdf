from tkinter import Tk, filedialog, Button, Label, Listbox, StringVar, messagebox, Frame, Menu  # Import Menu
from PIL import Image
import os, secrets

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.image_paths = []
        self.image_names = []  # Menyimpan nama fail imej
        self.output_label_text = StringVar()
        self.create_ui()

    def create_ui(self):
        # Menambah Menu Bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Menu Info
        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Info", command=self.show_info)

        menu_bar.add_cascade(label="Update", command=self.show_dev)

        # UI untuk arahan
        Label(self.root, text="PDF CVR", font=("Arial", 14)).pack(pady=10)

        # Butang untuk tambah imej
        Button(self.root, text="Add Images", command=self.add_images).pack(pady=5)

        # Senarai imej yang dimasukkan (hanya nama fail)
        self.image_listbox = Listbox(self.root, height=6, width=40)
        self.image_listbox.pack(pady=5)

        # Frame untuk butang Convert dan Remove supaya duduk bersebelahan
        button_frame = Frame(self.root)
        button_frame.pack(pady=5)

        # Butang untuk memulakan penukaran PDF
        convert_button = Button(button_frame, text="Convert", command=self.ask_confirm_convert)
        convert_button.pack(side="left", padx=5)

        # Butang untuk memadam imej yang dipilih
        remove_button = Button(button_frame, text="Remove", command=self.remove_image)
        remove_button.pack(side="left", padx=5)

        # Frame untuk butang "Move Up" dan "Move Down"
        frame = Frame(self.root)
        frame.pack(pady=5)

        # Butang untuk bawa imej ke atas
        move_up_button = Button(frame, text=" ↑ ", command=self.move_up)
        move_up_button.pack(side="left", padx=5)

        # Butang untuk bawa imej ke bawah
        move_down_button = Button(frame, text=" ↓ ", command=self.move_down)
        move_down_button.pack(side="left", padx=5)

        # Label untuk paparan nama fail PDF yang disimpan
        Label(self.root, textvariable=self.output_label_text, font=("Arial", 10), fg="green").pack(pady=10)

    def show_dev(self):
        info_message = "Coming Soon"
        messagebox.showinfo("update", info_message)

    def show_info(self):
        # Maklumat mengenai tool
        info_message = "Image to PDF Converter by Daniel Hakim\n\nThis tool allows users to convert images into a PDF file.\n\nVersion: 1.0"
        messagebox.showinfo("About", info_message)

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if files:
            for file in files:
                filename = os.path.basename(file)  # Dapatkan nama fail sahaja
                self.image_paths.append(file)
                self.image_names.append(filename)
                self.image_listbox.insert("end", filename)  # Papar nama fail dalam senarai
            messagebox.showinfo("Files Added", f"{len(files)} images added successfully!")

    def remove_image(self):
        selected_index = self.image_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select an image to remove.")
            return
        selected_index = selected_index[0]
        self.image_listbox.delete(selected_index)  # Padam imej dari senarai
        del self.image_paths[selected_index]
        del self.image_names[selected_index]
        messagebox.showinfo("Image Removed", "Selected image has been removed.")

    def move_up(self):
        selected_index = self.image_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        if selected_index > 0:
            # Tukar posisi imej dengan imej di atas
            self.image_paths[selected_index], self.image_paths[selected_index - 1] = self.image_paths[selected_index - 1], self.image_paths[selected_index]
            self.image_names[selected_index], self.image_names[selected_index - 1] = self.image_names[selected_index - 1], self.image_names[selected_index]
            # Kemas kini senarai
            self.update_image_list()
        else:
            messagebox.showwarning("Move Not Possible", "Image is already at the top.")

    def move_down(self):
        selected_index = self.image_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        if selected_index < len(self.image_paths) - 1:
            # Tukar posisi imej dengan imej di bawah
            self.image_paths[selected_index], self.image_paths[selected_index + 1] = self.image_paths[selected_index + 1], self.image_paths[selected_index]
            self.image_names[selected_index], self.image_names[selected_index + 1] = self.image_names[selected_index + 1], self.image_names[selected_index]
            # Kemas kini senarai
            self.update_image_list()
        else:
            messagebox.showwarning("Move Not Possible", "Image is already at the bottom.")

    def update_image_list(self):
        self.image_listbox.delete(0, "end")
        for name in self.image_names:
            self.image_listbox.insert("end", name)

    def ask_confirm_convert(self):
        if not self.image_paths:
            messagebox.showerror("No Images", "Please add images first!")
            return
        confirm = messagebox.askyesno("Confirm Conversion", "Are you sure you want to convert these images to PDF?")
        if confirm:
            self.ask_output_filename()

    def ask_output_filename(self):
        output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_filename:
            if os.path.exists(output_filename):
                messagebox.showerror("File Exists", "A file with that name already exists. Please choose another name.")
                self.ask_output_filename()  # Minta nama fail lagi
            else:
                self.convert_to_pdf(output_filename)

    def convert_to_pdf(self, output_filename):
        try:
            # Tukar imej kepada PDF
            first_image = Image.open(self.image_paths[0]).convert('RGB')
            image_list = [Image.open(img).convert('RGB') for img in self.image_paths[1:]]
            output_filepath = os.path.join(os.getcwd(), output_filename)  # Lokasi fail output PDF
            first_image.save(output_filepath, save_all=True, append_images=image_list)

            # Kemaskini label output dengan path fail PDF
            self.output_label_text.set(f"PDF saved as {output_filepath}")
            messagebox.showinfo("Success", f"PDF saved as {output_filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
        finally:
            self.image_paths.clear()
            self.image_names.clear()
            self.image_listbox.delete(0, "end")  # Kosongkan senarai imej

if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")  # Saiz tetingkap yang lebih besar
    app = ImageToPDFConverter(root)
    root.mainloop()
