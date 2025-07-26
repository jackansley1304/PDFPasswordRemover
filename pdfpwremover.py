import PyPDF2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def remove_pdf_password():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for the PDF file
    input_path = filedialog.askopenfilename(title="Select a password-protected PDF",
                                            filetypes=[("PDF Files", "*.pdf")])
    if not input_path:
        messagebox.showinfo("Cancelled", "No file selected.")
        return

    # Ask for the password
    password = simpledialog.askstring("Enter Password", "Enter the PDF password:", show='*')
    if password is None:
        messagebox.showinfo("Cancelled", "No password entered.")
        return

    try:
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            if reader.is_encrypted:
                if not reader.decrypt(password):
                    messagebox.showerror("Error", "Incorrect password!")
                    return
            else:
                messagebox.showinfo("Info", "The selected PDF is not encrypted.")
                return

            # Ask where to save the decrypted file
            output_path = filedialog.asksaveasfilename(title="Save Decrypted PDF As",
                                                       defaultextension=".pdf",
                                                       filetypes=[("PDF Files", "*.pdf")])
            if not output_path:
                messagebox.showinfo("Cancelled", "No save location selected.")
                return

            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            messagebox.showinfo("Success", f"Password removed!\nSaved as:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    remove_pdf_password()
