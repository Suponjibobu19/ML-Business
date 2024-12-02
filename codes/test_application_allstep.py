import tkinter as tk
from tkinter import messagebox, ttk
from main import (
    step_1_retrieve_emails,
    step_2_save_emails,
    step_3_classify_emails,
    step_4_send_emails,
)
import json

class EmailTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Automation Testing Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")

        # Variables for storing emails and results
        self.test_emails = []
        self.classification_results = []

        # UI setup
        self.create_section(root, "Step 1: Load Emails", self.load_emails, icon="📂")
        self.email_display = self.create_scrollable_section(root, "Loaded Emails", height=10)
        self.create_section(root, "Step 2: Save Emails", self.save_emails, icon="💾")
        self.create_section(root, "Step 3: Classify Emails", self.classify_emails, icon="📋")
        self.result_display = self.create_scrollable_section(root, "Classification Results", height=10)
        self.create_section(root, "Step 4: Send Emails", self.send_emails, icon="✉️")

    def create_section(self, root, label_text, command, icon=""):
        frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        frame.pack(pady=10, fill=tk.X)

        label = tk.Label(frame, text=f"{icon} {label_text}", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w")
        label.pack(side=tk.LEFT, padx=5)

        button = tk.Button(
            frame, text="Execute", command=command, bg="#007bff", fg="white", activebackground="#0056b3",
            activeforeground="white", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5
        )
        button.pack(side=tk.RIGHT, padx=5)

    def create_scrollable_section(self, root, title, height=10):
        frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        title_label = tk.Label(frame, text=title, bg="#ffffff", font=("Arial", 12, "bold"), anchor="w")
        title_label.pack(fill=tk.X, pady=(0, 5))

        text_widget = tk.Text(frame, height=height, wrap=tk.WORD, bg="#f9f9f9", bd=0, relief="flat")
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return text_widget

    def load_emails(self):
        """
        Step 1: Load emails using `step_1_retrieve_emails`.
        """
        try:
            self.test_emails = step_1_retrieve_emails()
            self.email_display.delete(1.0, tk.END)
            for email in self.test_emails:
                self.email_display.insert(
                    tk.END,
                    f"Email ID: {email['email_id']}\nFrom: {email['from']}\n"
                    f"Subject: {email['subject']}\nBody: {email['body']}\n\n"
                )
            messagebox.showinfo("Success", "Emails loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load emails: {e}")

    def save_emails(self):
        """
        Step 2: Save emails using `step_2_save_emails`.
        """
        try:
            if not self.test_emails:
                raise ValueError("No emails loaded to save.")
            step_2_save_emails(self.test_emails)
            messagebox.showinfo("Success", "Emails saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save emails: {e}")

    def classify_emails(self):
        """
        Step 3: Classify emails using `step_3_classify_emails`.
        """
        try:
            if not self.test_emails:
                raise ValueError("No emails loaded for classification.")
            self.classification_results = step_3_classify_emails(self.test_emails)
            self.result_display.delete(1.0, tk.END)
            for result in self.classification_results:
                self.result_display.insert(
                    tk.END,
                    f"Email ID: {result['email_id']}\n"
                    f"From: {result['from']}\n"
                    f"Subject: {result['email_subject']}\n"
                    f"Classified as: {result['classified_as']}\n"
                    f"Recipient: {result['recipient_email']}\n\n"
                )
            messagebox.showinfo("Success", "Emails classified successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to classify emails: {e}")

    def send_emails(self):
        """
        Step 4: Send emails using `step_4_send_emails`.
        """
        try:
            if not self.classification_results:
                raise ValueError("No classification results available for sending emails.")
            step_4_send_emails(self.classification_results)
            messagebox.showinfo("Success", "Emails sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send emails: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailTestApp(root)
    root.mainloop()
