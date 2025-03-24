from tkinter import Tk, Button, filedialog, messagebox, Toplevel, colorchooser, Label, Entry
from tkcalendar import Calendar  # Make sure to install tkcalendar
import data_import
import data_export
from datetime import datetime  # Add this import

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Data Import/Export Application")
        master.geometry("600x400")  # Set default window size

        self.import_button = Button(master, text="Import Data", command=self.import_data, width=20, height=2, bg="lightblue")
        self.import_button.pack(pady=5)
        
        # self.update_button = Button(master, text="Update Data", command=self.update_data)
        # self.update_button.pack()

        self.export_button = Button(master, text="Export Data", command=self.export_data, width=20, height=2, bg="lightgreen")
        self.export_button.pack(pady=5)
        
        self.calendar_label = Label(master, text="Select Date:")
        self.calendar_label.pack(pady=5)
        self.calendar = Calendar(master, selectmode='day')
        self.calendar.pack(pady=5)

        self.settings_button = Button(master, text="Settings", command=self.open_settings, width=20, height=2, bg="lightgray")
        self.settings_button.pack(pady=5)

    def run(self):
        self.master.mainloop()  # Add this method to start the Tkinter main loop

    def import_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.imported_data = data_import.import_data(file_path)
            required_columns = {'amount', 'account_number', 'branch_code', 'company_name', 'reference'}
            if not self.imported_data.empty:
                missing_columns = required_columns - set(self.imported_data.columns)
                if not missing_columns:
                    messagebox.showinfo("Success", "Data imported successfully!")
                else:
                    messagebox.showerror("Error", f"Missing columns in data_import: {', '.join(missing_columns)}")
            else:
                messagebox.showerror("Error", "Failed to import data. Please check the log for details.")

    # def update_data(self):
    #     data = data_import.import_data()
    #     if not data.empty:
    #         updated_data = self.perform_update(data)
    #         if not updated_data.empty:
    #             messagebox.showinfo("Success", "Data updated successfully!")
    #         else:
    #             messagebox.showerror("Error", "Failed to update data. Please check the log for details.")
    #     else:
    #         messagebox.showerror("Error", "Failed to import data for update. Please check the log for details.")

    # def perform_update(self, data):
    #     # Placeholder for the actual update logic
    #     # For now, just return the data as is
    #     return data

    def select_date(self):
        selected_date = self.calendar.get_date()  # Correctly get the selected date
        self.selected_date = datetime.strptime(selected_date, "%m/%d/%y")  # Convert to datetime object
        messagebox.showinfo("Selected Date", f"You selected: {selected_date}")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            if hasattr(self, 'imported_data') and self.imported_data is not None:
                if hasattr(self, 'selected_date'):
                    # Use self.selected_date as needed for exporting data
                    try:
                        success = data_export.export_data(self.imported_data, file_path, self.selected_date)
                        if success:
                            messagebox.showinfo("Success", "Data exported successfully!")
                        else:
                            messagebox.showerror("Error", "Failed to export data.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export data: {e}")
                else:
                    self.select_date()  # Prompt user to select a date if not already selected
                    if hasattr(self, 'selected_date'):
                        try:
                            success = data_export.export_data(self.imported_data, file_path, self.selected_date)
                            if success:
                                messagebox.showinfo("Success", "Data exported successfully!")
                            else:
                                messagebox.showerror("Error", "Failed to export data.")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to export data: {e}")
                    else:
                        messagebox.showerror("Error", "No date selected for export.")
            else:
                messagebox.showerror("Error", "No data imported to export.")

    def load_data(self, file_path):
        # Load the data from the specified file path
        return data_import.import_data(file_path)  # Adjust this line as needed

    def open_settings(self):
        settings_window = Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        def change_bg_color():
            color = colorchooser.askcolor()[1]
            if color:
                self.master.configure(bg=color)

        def change_window_size():
            width = width_entry.get()
            height = height_entry.get()
            if width.isdigit() and height.isdigit():
                self.master.geometry(f"{width}x{height}")

        bg_color_button = Button(settings_window, text="Change Background Color", command=change_bg_color)
        bg_color_button.pack(pady=10)

        width_label = Label(settings_window, text="Width:")
        width_label.pack()
        width_entry = Entry(settings_window)
        width_entry.pack()

        height_label = Label(settings_window, text="Height:")
        height_label.pack()
        height_entry = Entry(settings_window)
        height_entry.pack()

        size_button = Button(settings_window, text="Change Window Size", command=change_window_size)
        size_button.pack(pady=10)

def main():
    root = Tk()
    gui = GUI(root)
    gui.run()

if __name__ == "__main__":
    main()