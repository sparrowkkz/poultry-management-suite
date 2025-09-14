import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import sqlite3

class PoultryManagementSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("JD INVESTMENTS LTD - Poultry Management Suite")
        self.root.geometry("800x600")
        self.conn = sqlite3.connect('poultry_data.db')
        self.create_tables()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        self.add_weight_calculator_tab()
        self.add_fcr_calculator_tab()
        self.add_egg_production_tracker_tab()
        self.add_vaccination_scheduler_tab()
        self.add_financial_profit_calculator_tab()
        self.add_flock_health_monitor_tab()
        self.add_incubation_hatch_calculator_tab()
        self.add_coop_environment_monitor_tab()
        self.add_expense_sales_tracker_tab()
        self.add_customer_info_tab()
        self.add_medication_tracker_tab()
        self.add_inventory_tracker_tab()
        self.add_report_generator_tab()
        self.add_dashboard_tab()
        self.add_supplier_management_tab()
        self.add_task_scheduler_tab()
        self.add_sustainability_tracker_tab()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS egg_production (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            flock_size INTEGER,
                            eggs_collected INTEGER,
                            average_egg_weight REAL
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS vaccinations (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            vaccine_type TEXT,
                            flock_size INTEGER,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS health_logs (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            mortality INTEGER,
                            symptoms TEXT,
                            treatments TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS incubation (
                            id INTEGER PRIMARY KEY,
                            set_date TEXT,
                            eggs_set INTEGER,
                            hatched INTEGER,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS environment_logs (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            temperature REAL,
                            humidity REAL,
                            ventilation REAL,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            category TEXT,
                            amount REAL,
                            description TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            product TEXT,
                            quantity INTEGER,
                            amount REAL
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            contact TEXT,
                            address TEXT,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS medications (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            medication_type TEXT,
                            dosage REAL,
                            flock_size INTEGER,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                            id INTEGER PRIMARY KEY,
                            item_name TEXT,
                            quantity REAL,
                            unit TEXT,
                            last_updated TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            contact TEXT,
                            address TEXT,
                            notes TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            task_description TEXT,
                            status TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sustainability (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            water_usage REAL,
                            energy_usage REAL,
                            waste REAL,
                            notes TEXT
                          )''')
        self.conn.commit()

    def add_weight_calculator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Weight Calculator")
        self.weights_brown = []
        self.weights_white = []
        self.current_bird = 0
        self.current_color = "brown"
        self.sample_brown = 0
        self.sample_white = 0
        self.brown_standards = {1: 75, 2: 130, 3: 195, 4: 273, 5: 366, 6: 469, 7: 573, 8: 677, 9: 777, 10: 873}
        self.white_standards = {1: 75, 2: 125, 3: 187, 4: 257, 5: 338, 6: 432, 7: 530, 8: 627, 9: 722, 10: 814}
        tk.Label(tab, text="Age of birds (weeks):").pack(pady=5)
        self.age_entry = tk.Entry(tab)
        self.age_entry.pack(pady=5)
        tk.Label(tab, text="Number of brown birds:").pack(pady=5)
        self.brown_entry = tk.Entry(tab)
        self.brown_entry.pack(pady=5)
        tk.Label(tab, text="Number of white birds:").pack(pady=5)
        self.white_entry = tk.Entry(tab)
        self.white_entry.pack(pady=5)
        tk.Button(tab, text="Start Weight Collection", command=self.start_weight_collection).pack(pady=20)
        self.weight_label = tk.Label(tab, text="")
        self.weight_label.pack(pady=5)
        self.weight_entry = tk.Entry(tab)
        self.weight_entry.pack(pady=5)
        tk.Button(tab, text="Submit Weight", command=self.submit_weight).pack(pady=10)
        tk.Button(tab, text="Export Weights to CSV", command=self.export_weights).pack(pady=10)

    def start_weight_collection(self):
        try:
            self.age = int(self.age_entry.get())
            num_brown = int(self.brown_entry.get())
            num_white = int(self.white_entry.get())
            if self.age < 1 or num_brown < 0 or num_white < 0:
                messagebox.showerror("Error", "Invalid input. Age must be positive, and bird counts non-negative.")
                return
            self.sample_brown = max(1, round(0.1 * num_brown))
            self.sample_white = max(1, round(0.1 * num_white))
            self.weights_brown = []
            self.weights_white = []
            self.current_bird = 0
            self.current_color = "brown"
            self.update_weight_label()
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def update_weight_label(self):
        if self.current_color == "brown" and self.current_bird < self.sample_brown:
            self.weight_label.config(text=f"Enter weight for brown bird {self.current_bird + 1} of {self.sample_brown}")
        elif self.current_color == "white" and self.current_bird < self.sample_white:
            self.weight_label.config(text=f"Enter weight for white bird {self.current_bird + 1} of {self.sample_white}")
        else:
            self.show_weight_results()

    def submit_weight(self):
        try:
            weight = float(self.weight_entry.get())
            if weight <= 0:
                messagebox.showerror("Error", "Weight must be positive.")
                return
            if self.current_color == "brown":
                self.weights_brown.append(weight)
                self.current_bird += 1
                if self.current_bird >= self.sample_brown:
                    self.current_color = "white"
                    self.current_bird = 0
            else:
                self.weights_white.append(weight)
                self.current_bird += 1
            self.weight_entry.delete(0, tk.END)
            self.update_weight_label()
        except ValueError:
            messagebox.showerror("Error", "Invalid weight.")

    def get_metrics(self, weights, color):
        if not weights:
            return 0, 0, 0, 0, "N/A"
        total = sum(weights)
        avg = total / len(weights)
        lower = avg * 0.9
        upper = avg * 1.1
        in_range = sum(lower <= w <= upper for w in weights)
        uniformity = (in_range / len(weights)) * 100
        standards = self.brown_standards if color == "brown" else self.white_standards
        target = standards.get(self.age, max(standards.values()))
        verdict = "On Target" if 0.95 * target <= avg <= 1.05 * target else "Off Target"
        return total, avg, uniformity, in_range, verdict

    def show_weight_results(self):
        brown_total, brown_avg, brown_uniformity, brown_in_range, brown_verdict = self.get_metrics(self.weights_brown, "brown")
        white_total, white_avg, white_uniformity, white_in_range, white_verdict = self.get_metrics(self.weights_white, "white")
        result_str = (f"Brown Birds:\nSample: {self.sample_brown}\nTotal Weight: {brown_total:.2f} g\n"
                      f"Average Weight: {brown_avg:.2f} g\nUniformity: {brown_uniformity:.2f}%\n"
                      f"In Range (+/-10%): {brown_in_range}\nVerdict: {brown_verdict}\n\n"
                      f"White Birds:\nSample: {self.sample_white}\nTotal Weight: {white_total:.2f} g\n"
                      f"Average Weight: {white_avg:.2f} g\nUniformity: {white_uniformity:.2f}%\n"
                      f"In Range (+/-10%): {white_in_range}\nVerdict: {white_verdict}")
        messagebox.showinfo("Weight Results", result_str)

    def export_weights(self):
        brown_total, brown_avg, brown_uniformity, brown_in_range, brown_verdict = self.get_metrics(self.weights_brown, "brown")
        white_total, white_avg, white_uniformity, white_in_range, white_verdict = self.get_metrics(self.weights_white, "white")
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["JD INVESTMENTS LTD - Weight Calculator"])
                writer.writerow(["Age (weeks)", self.age])
                writer.writerow([])
                writer.writerow(["Brown Birds"])
                writer.writerow(["Sample Size", self.sample_brown])
                writer.writerow(["Total Weight (grams)", f"{brown_total:.2f}"])
                writer.writerow(["Average Weight (grams)", f"{brown_avg:.2f}"])
                writer.writerow(["Uniformity (%)", f"{brown_uniformity:.2f}"])
                writer.writerow(["Birds in Range (+/-10%)", brown_in_range])
                writer.writerow(["Weight Verdict", brown_verdict])
                writer.writerow(["Individual Weights (grams)"] + [f"{w:.2f}" for w in self.weights_brown])
                writer.writerow([])
                writer.writerow(["White Birds"])
                writer.writerow(["Sample Size", self.sample_white])
                writer.writerow(["Total Weight (grams)", f"{white_total:.2f}"])
                writer.writerow(["Average Weight (grams)", f"{white_avg:.2f}"])
                writer.writerow(["Uniformity (%)", f"{white_uniformity:.2f}"])
                writer.writerow(["Birds in Range (+/-10%)", white_in_range])
                writer.writerow(["Weight Verdict", white_verdict])
                writer.writerow(["Individual Weights (grams)"] + [f"{w:.2f}" for w in self.weights_white])
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_fcr_calculator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="FCR Calculator")
        tk.Label(tab, text="Bird Type (Brown/White):").pack(pady=5)
        self.fcr_bird_type = tk.Entry(tab)
        self.fcr_bird_type.pack(pady=5)
        tk.Label(tab, text="Total Feed Consumed (kg):").pack(pady=5)
        self.fcr_feed = tk.Entry(tab)
        self.fcr_feed.pack(pady=5)
        tk.Label(tab, text="Total Weight Gain or Egg Weight (kg):").pack(pady=5)
        self.fcr_output = tk.Entry(tab)
        self.fcr_output.pack(pady=5)
        tk.Button(tab, text="Calculate FCR", command=self.calculate_fcr).pack(pady=20)
        self.fcr_result = tk.Label(tab, text="")
        self.fcr_result.pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_fcr).pack(pady=10)

    def calculate_fcr(self):
        try:
            bird_type = self.fcr_bird_type.get().capitalize()
            feed = float(self.fcr_feed.get())
            output = float(self.fcr_output.get())
            if feed <= 0 or output <= 0:
                messagebox.showerror("Error", "Inputs must be positive.")
                return
            fcr = feed / output
            standards = {"Brown": 2.0, "White": 2.2}
            standard = standards.get(bird_type, 2.0)
            verdict = "Optimal" if fcr <= standard else "Suboptimal"
            self.fcr_value = fcr
            self.fcr_verdict = verdict
            self.fcr_result.config(text=f"FCR: {fcr:.2f} - Verdict: {verdict}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def export_fcr(self):
        if not hasattr(self, 'fcr_value'):
            messagebox.showerror("Error", "Calculate FCR first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["JD INVESTMENTS LTD - FCR Calculator"])
                writer.writerow(["Bird Type", self.fcr_bird_type.get()])
                writer.writerow(["FCR", f"{self.fcr_value:.2f}"])
                writer.writerow(["Verdict", self.fcr_verdict])
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_egg_production_tracker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Egg Production Tracker")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.egg_date = tk.Entry(tab)
        self.egg_date.pack(pady=5)
        tk.Label(tab, text="Flock Size:").pack(pady=5)
        self.egg_flock_size = tk.Entry(tab)
        self.egg_flock_size.pack(pady=5)
        tk.Label(tab, text="Eggs Collected:").pack(pady=5)
        self.egg_collected = tk.Entry(tab)
        self.egg_collected.pack(pady=5)
        tk.Label(tab, text="Average Egg Weight (grams):").pack(pady=5)
        self.egg_weight = tk.Entry(tab)
        self.egg_weight.pack(pady=5)
        tk.Button(tab, text="Log Production", command=self.log_egg_production).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_egg_logs).pack(pady=5)
        tk.Button(tab, text="Export Logs to CSV", command=self.export_egg_logs).pack(pady=5)

    def log_egg_production(self):
        try:
            date = self.egg_date.get()
            flock_size = int(self.egg_flock_size.get())
            eggs = int(self.egg_collected.get())
            weight = float(self.egg_weight.get())
            if flock_size <= 0 or eggs < 0 or weight <= 0:
                messagebox.showerror("Error", "Invalid input. Ensure positive values.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO egg_production (date, flock_size, eggs_collected, average_egg_weight) VALUES (?, ?, ?, ?)",
                           (date, flock_size, eggs, weight))
            self.conn.commit()
            messagebox.showinfo("Success", "Production logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_egg_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM egg_production")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Flock: {log[2]}, Eggs: {log[3]}, Avg Weight: {log[4]}" for log in logs])
        messagebox.showinfo("Egg Production Logs", log_str or "No logs.")

    def export_egg_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM egg_production")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Flock Size", "Eggs Collected", "Average Egg Weight"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_vaccination_scheduler_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Vaccination Scheduler")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.vac_date = tk.Entry(tab)
        self.vac_date.pack(pady=5)
        tk.Label(tab, text="Vaccine Type:").pack(pady=5)
        self.vac_type = tk.Entry(tab)
        self.vac_type.pack(pady=5)
        tk.Label(tab, text="Flock Size:").pack(pady=5)
        self.vac_flock_size = tk.Entry(tab)
        self.vac_flock_size.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.vac_notes = tk.Entry(tab)
        self.vac_notes.pack(pady=5)
        tk.Button(tab, text="Log Vaccination", command=self.log_vaccination).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_vaccination_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_vaccination_logs).pack(pady=5)

    def log_vaccination(self):
        try:
            date = self.vac_date.get()
            vac_type = self.vac_type.get()
            flock_size = int(self.vac_flock_size.get())
            notes = self.vac_notes.get()
            if not date or not vac_type or flock_size <= 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date, type, and positive flock size.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO vaccinations (date, vaccine_type, flock_size, notes) VALUES (?, ?, ?, ?)",
                           (date, vac_type, flock_size, notes))
            self.conn.commit()
            messagebox.showinfo("Success", "Vaccination logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_vaccination_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vaccinations")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Type: {log[2]}, Flock: {log[3]}, Notes: {log[4]}" for log in logs])
        messagebox.showinfo("Vaccination Logs", log_str or "No logs.")

    def export_vaccination_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vaccinations")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Vaccine Type", "Flock Size", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_financial_profit_calculator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Financial Calculator")
        tk.Label(tab, text="Total Revenue:").pack(pady=5)
        self.fin_revenue = tk.Entry(tab)
        self.fin_revenue.pack(pady=5)
        tk.Label(tab, text="Total Expenses:").pack(pady=5)
        self.fin_expenses = tk.Entry(tab)
        self.fin_expenses.pack(pady=5)
        tk.Button(tab, text="Calculate Profit", command=self.calculate_profit).pack(pady=20)
        self.profit_result = tk.Label(tab, text="")
        self.profit_result.pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_profit).pack(pady=10)

    def calculate_profit(self):
        try:
            revenue = float(self.fin_revenue.get())
            expenses = float(self.fin_expenses.get())
            if revenue < 0 or expenses < 0:
                messagebox.showerror("Error", "Inputs must be non-negative.")
                return
            profit = revenue - expenses
            self.profit_value = profit
            self.profit_result.config(text=f"Profit: {profit:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def export_profit(self):
        if not hasattr(self, 'profit_value'):
            messagebox.showerror("Error", "Calculate profit first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["JD INVESTMENTS LTD - Financial Calculator"])
                writer.writerow(["Total Revenue", f"{self.fin_revenue.get()}"])
                writer.writerow(["Total Expenses", f"{self.fin_expenses.get()}"])
                writer.writerow(["Profit", f"{self.profit_value:.2f}"])
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_flock_health_monitor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Health Monitor")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.health_date = tk.Entry(tab)
        self.health_date.pack(pady=5)
        tk.Label(tab, text="Mortality:").pack(pady=5)
        self.health_mortality = tk.Entry(tab)
        self.health_mortality.pack(pady=5)
        tk.Label(tab, text="Symptoms:").pack(pady=5)
        self.health_symptoms = tk.Entry(tab)
        self.health_symptoms.pack(pady=5)
        tk.Label(tab, text="Treatments:").pack(pady=5)
        self.health_treatments = tk.Entry(tab)
        self.health_treatments.pack(pady=5)
        tk.Button(tab, text="Log Health", command=self.log_health).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_health_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_health_logs).pack(pady=5)

    def log_health(self):
        try:
            date = self.health_date.get()
            mortality = int(self.health_mortality.get())
            symptoms = self.health_symptoms.get()
            treatments = self.health_treatments.get()
            if not date or mortality < 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date and non-negative mortality.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO health_logs (date, mortality, symptoms, treatments) VALUES (?, ?, ?, ?)",
                           (date, mortality, symptoms, treatments))
            self.conn.commit()
            messagebox.showinfo("Success", "Health logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_health_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM health_logs")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Mortality: {log[2]}, Symptoms: {log[3]}, Treatments: {log[4]}" for log in logs])
        messagebox.showinfo("Health Logs", log_str or "No logs.")

    def export_health_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM health_logs")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Mortality", "Symptoms", "Treatments"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_incubation_hatch_calculator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Incubation Calculator")
        tk.Label(tab, text="Set Date (YYYY-MM-DD):").pack(pady=5)
        self.inc_set_date = tk.Entry(tab)
        self.inc_set_date.pack(pady=5)
        tk.Label(tab, text="Eggs Set:").pack(pady=5)
        self.inc_eggs_set = tk.Entry(tab)
        self.inc_eggs_set.pack(pady=5)
        tk.Label(tab, text="Hatched:").pack(pady=5)
        self.inc_hatched = tk.Entry(tab)
        self.inc_hatched.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.inc_notes = tk.Entry(tab)
        self.inc_notes.pack(pady=5)
        tk.Button(tab, text="Log Incubation", command=self.log_incubation).pack(pady=10)
        tk.Button(tab, text="Calculate Hatch Rate", command=self.calculate_hatch_rate).pack(pady=5)
        tk.Button(tab, text="View Logs", command=self.view_incubation_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_incubation_logs).pack(pady=5)

    def log_incubation(self):
        try:
            set_date = self.inc_set_date.get()
            eggs_set = int(self.inc_eggs_set.get())
            hatched = int(self.inc_hatched.get())
            notes = self.inc_notes.get()
            if not set_date or eggs_set <= 0 or hatched < 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date and non-negative values.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO incubation (set_date, eggs_set, hatched, notes) VALUES (?, ?, ?, ?)",
                           (set_date, eggs_set, hatched, notes))
            self.conn.commit()
            messagebox.showinfo("Success", "Incubation logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def calculate_hatch_rate(self):
        try:
            eggs_set = int(self.inc_eggs_set.get())
            hatched = int(self.inc_hatched.get())
            if eggs_set <= 0 or hatched < 0:
                messagebox.showerror("Error", "Invalid input. Ensure positive eggs set and non-negative hatched.")
                return
            rate = (hatched / eggs_set) * 100 if eggs_set > 0 else 0
            messagebox.showinfo("Hatch Rate", f"Hatch Rate: {rate:.2f}%")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_incubation_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM incubation")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Set Date: {log[1]}, Eggs Set: {log[2]}, Hatched: {log[3]}, Notes: {log[4]}" for log in logs])
        messagebox.showinfo("Incubation Logs", log_str or "No logs.")

    def export_incubation_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM incubation")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Set Date", "Eggs Set", "Hatched", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_coop_environment_monitor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Environment Monitor")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.env_date = tk.Entry(tab)
        self.env_date.pack(pady=5)
        tk.Label(tab, text="Temperature (C):").pack(pady=5)
        self.env_temp = tk.Entry(tab)
        self.env_temp.pack(pady=5)
        tk.Label(tab, text="Humidity (%):").pack(pady=5)
        self.env_hum = tk.Entry(tab)
        self.env_hum.pack(pady=5)
        tk.Label(tab, text="Ventilation (rate):").pack(pady=5)
        self.env_vent = tk.Entry(tab)
        self.env_vent.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.env_notes = tk.Entry(tab)
        self.env_notes.pack(pady=5)
        tk.Button(tab, text="Log Environment", command=self.log_environment).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_environment_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_environment_logs).pack(pady=5)

    def log_environment(self):
        try:
            date = self.env_date.get()
            temp = float(self.env_temp.get())
            hum = float(self.env_hum.get())
            vent = float(self.env_vent.get())
            notes = self.env_notes.get()
            if not date or temp < 0 or hum < 0 or vent < 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date and non-negative values.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO environment_logs (date, temperature, humidity, ventilation, notes) VALUES (?, ?, ?, ?, ?)",
                           (date, temp, hum, vent, notes))
            self.conn.commit()
            messagebox.showinfo("Success", "Environment logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_environment_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM environment_logs")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Temp: {log[2]}, Humidity: {log[3]}, Ventilation: {log[4]}, Notes: {log[5]}" for log in logs])
        messagebox.showinfo("Environment Logs", log_str or "No logs.")

    def export_environment_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM environment_logs")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Temperature", "Humidity", "Ventilation", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_expense_sales_tracker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Expense/Sales Tracker")
        tk.Label(tab, text="Log Expense", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(tab, text="Expense Date (YYYY-MM-DD):").pack(pady=5)
        self.exp_date = tk.Entry(tab)
        self.exp_date.pack(pady=5)
        tk.Label(tab, text="Category (e.g., Feed, Labor):").pack(pady=5)
        self.exp_category = tk.Entry(tab)
        self.exp_category.pack(pady=5)
        tk.Label(tab, text="Amount:").pack(pady=5)
        self.exp_amount = tk.Entry(tab)
        self.exp_amount.pack(pady=5)
        tk.Label(tab, text="Description:").pack(pady=5)
        self.exp_desc = tk.Entry(tab)
        self.exp_desc.pack(pady=5)
        tk.Button(tab, text="Log Expense", command=self.log_expense).pack(pady=10)
        tk.Label(tab, text="Log Sale", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(tab, text="Sale Date (YYYY-MM-DD):").pack(pady=5)
        self.sale_date = tk.Entry(tab)
        self.sale_date.pack(pady=5)
        tk.Label(tab, text="Product (e.g., Eggs, Broilers):").pack(pady=5)
        self.sale_product = tk.Entry(tab)
        self.sale_product.pack(pady=5)
        tk.Label(tab, text="Quantity:").pack(pady=5)
        self.sale_qty = tk.Entry(tab)
        self.sale_qty.pack(pady=5)
        tk.Label(tab, text="Amount:").pack(pady=5)
        self.sale_amount = tk.Entry(tab)
        self.sale_amount.pack(pady=5)
        tk.Button(tab, text="Log Sale", command=self.log_sale).pack(pady=10)
        tk.Button(tab, text="View Expenses", command=self.view_expenses).pack(pady=5)
        tk.Button(tab, text="View Sales", command=self.view_sales).pack(pady=5)
        tk.Button(tab, text="Export Expenses to CSV", command=self.export_expenses).pack(pady=5)
        tk.Button(tab, text="Export Sales to CSV", command=self.export_sales).pack(pady=5)

    def log_expense(self):
        try:
            date = self.exp_date.get()
            category = self.exp_category.get()
            amount = float(self.exp_amount.get())
            desc = self.exp_desc.get()
            if not date or not category or amount <= 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date, category, and positive amount.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                           (date, category, amount, desc))
            self.conn.commit()
            messagebox.showinfo("Success", "Expense logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def log_sale(self):
        try:
            date = self.sale_date.get()
            product = self.sale_product.get()
            quantity = int(self.sale_qty.get())
            amount = float(self.sale_amount.get())
            if not date or not product or quantity <= 0 or amount <= 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date, product, and positive quantity/amount.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO sales (date, product, quantity, amount) VALUES (?, ?, ?, ?)",
                           (date, product, quantity, amount))
            self.conn.commit()
            messagebox.showinfo("Success", "Sale logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_expenses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Category: {log[2]}, Amount: {log[3]}, Description: {log[4]}" for log in logs])
        messagebox.showinfo("Expenses", log_str or "No logs.")

    def view_sales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sales")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Product: {log[2]}, Quantity: {log[3]}, Amount: {log[4]}" for log in logs])
        messagebox.showinfo("Sales", log_str or "No logs.")

    def export_expenses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def export_sales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sales")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Product", "Quantity", "Amount"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_customer_info_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Customer Info")
        tk.Label(tab, text="Name:").pack(pady=5)
        self.cust_name = tk.Entry(tab)
        self.cust_name.pack(pady=5)
        tk.Label(tab, text="Contact:").pack(pady=5)
        self.cust_contact = tk.Entry(tab)
        self.cust_contact.pack(pady=5)
        tk.Label(tab, text="Address:").pack(pady=5)
        self.cust_address = tk.Entry(tab)
        self.cust_address.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.cust_notes = tk.Entry(tab)
        self.cust_notes.pack(pady=5)
        tk.Button(tab, text="Add Customer", command=self.add_customer).pack(pady=10)
        tk.Button(tab, text="View Customers", command=self.view_customers).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_customers).pack(pady=5)

    def add_customer(self):
        name = self.cust_name.get()
        contact = self.cust_contact.get()
        address = self.cust_address.get()
        notes = self.cust_notes.get()
        if not name:
            messagebox.showerror("Error", "Customer name is required.")
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO customers (name, contact, address, notes) VALUES (?, ?, ?, ?)",
                       (name, contact, address, notes))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer added.")

    def view_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Name: {log[1]}, Contact: {log[2]}, Address: {log[3]}, Notes: {log[4]}" for log in logs])
        messagebox.showinfo("Customers", log_str or "No customers.")

    def export_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Contact", "Address", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_medication_tracker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Medication Tracker")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.med_date = tk.Entry(tab)
        self.med_date.pack(pady=5)
        tk.Label(tab, text="Medication Type:").pack(pady=5)
        self.med_type = tk.Entry(tab)
        self.med_type.pack(pady=5)
        tk.Label(tab, text="Dosage:").pack(pady=5)
        self.med_dosage = tk.Entry(tab)
        self.med_dosage.pack(pady=5)
        tk.Label(tab, text="Flock Size:").pack(pady=5)
        self.med_flock_size = tk.Entry(tab)
        self.med_flock_size.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.med_notes = tk.Entry(tab)
        self.med_notes.pack(pady=5)
        tk.Button(tab, text="Log Medication", command=self.log_medication).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_medication_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_medication_logs).pack(pady=5)

    def log_medication(self):
        try:
            date = self.med_date.get()
            med_type = self.med_type.get()
            dosage = float(self.med_dosage.get())
            flock_size = int(self.med_flock_size.get())
            notes = self.med_notes.get()
            if not date or not med_type or dosage <= 0 or flock_size <= 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date, type, and positive dosage/flock size.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO medications (date, medication_type, dosage, flock_size, notes) VALUES (?, ?, ?, ?, ?)",
                           (date, med_type, dosage, flock_size, notes))
            self.conn.commit()
            messagebox.showinfo("Success", "Medication logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_medication_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM medications")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Type: {log[2]}, Dosage: {log[3]}, Flock: {log[4]}, Notes: {log[5]}" for log in logs])
        messagebox.showinfo("Medication Logs", log_str or "No logs.")

    def export_medication_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM medications")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Medication Type", "Dosage", "Flock Size", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_inventory_tracker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Inventory Tracker")
        tk.Label(tab, text="Item Name:").pack(pady=5)
        self.inv_item = tk.Entry(tab)
        self.inv_item.pack(pady=5)
        tk.Label(tab, text="Quantity:").pack(pady=5)
        self.inv_quantity = tk.Entry(tab)
        self.inv_quantity.pack(pady=5)
        tk.Label(tab, text="Unit (e.g., kg, liters):").pack(pady=5)
        self.inv_unit = tk.Entry(tab)
        self.inv_unit.pack(pady=5)
        tk.Label(tab, text="Last Updated (YYYY-MM-DD):").pack(pady=5)
        self.inv_updated = tk.Entry(tab)
        self.inv_updated.pack(pady=5)
        tk.Button(tab, text="Log Inventory", command=self.log_inventory).pack(pady=10)
        tk.Button(tab, text="View Inventory", command=self.view_inventory).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_inventory).pack(pady=5)

    def log_inventory(self):
        try:
            item = self.inv_item.get()
            quantity = float(self.inv_quantity.get())
            unit = self.inv_unit.get()
            updated = self.inv_updated.get()
            if not item or quantity < 0 or not unit or not updated:
                messagebox.showerror("Error", "Invalid input. Ensure valid item, unit, date, and non-negative quantity.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO inventory (item_name, quantity, unit, last_updated) VALUES (?, ?, ?, ?)",
                           (item, quantity, unit, updated))
            self.conn.commit()
            messagebox.showinfo("Success", "Inventory logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_inventory(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Item: {log[1]}, Quantity: {log[2]}, Unit: {log[3]}, Updated: {log[4]}" for log in logs])
        messagebox.showinfo("Inventory", log_str or "No inventory.")

    def export_inventory(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Item Name", "Quantity", "Unit", "Last Updated"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_report_generator_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Report Generator")
        tk.Label(tab, text="Select Report Type:").pack(pady=5)
        self.report_type = tk.StringVar()
        report_types = ["Egg Production", "Vaccinations", "Health Logs", "Incubation", "Environment", "Expenses", "Sales", "Customers", "Medications", "Inventory", "Suppliers", "Tasks", "Sustainability"]
        tk.OptionMenu(tab, self.report_type, *report_types).pack(pady=5)
        tk.Button(tab, text="Generate Report (CSV)", command=self.generate_report).pack(pady=10)

    def generate_report(self):
        report_type = self.report_type.get()
        table_map = {
            "Egg Production": "egg_production",
            "Vaccinations": "vaccinations",
            "Health Logs": "health_logs",
            "Incubation": "incubation",
            "Environment": "environment_logs",
            "Expenses": "expenses",
            "Sales": "sales",
            "Customers": "customers",
            "Medications": "medications",
            "Inventory": "inventory",
            "Suppliers": "suppliers",
            "Tasks": "tasks",
            "Sustainability": "sustainability"
        }
        headers_map = {
            "Egg Production": ["ID", "Date", "Flock Size", "Eggs Collected", "Average Egg Weight"],
            "Vaccinations": ["ID", "Date", "Vaccine Type", "Flock Size", "Notes"],
            "Health Logs": ["ID", "Date", "Mortality", "Symptoms", "Treatments"],
            "Incubation": ["ID", "Set Date", "Eggs Set", "Hatched", "Notes"],
            "Environment": ["ID", "Date", "Temperature", "Humidity", "Ventilation", "Notes"],
            "Expenses": ["ID", "Date", "Category", "Amount", "Description"],
            "Sales": ["ID", "Date", "Product", "Quantity", "Amount"],
            "Customers": ["ID", "Name", "Contact", "Address", "Notes"],
            "Medications": ["ID", "Date", "Medication Type", "Dosage", "Flock Size", "Notes"],
            "Inventory": ["ID", "Item Name", "Quantity", "Unit", "Last Updated"],
            "Suppliers": ["ID", "Name", "Contact", "Address", "Notes"],
            "Tasks": ["ID", "Date", "Task Description", "Status"],
            "Sustainability": ["ID", "Date", "Water Usage", "Energy Usage", "Waste", "Notes"]
        }
        if not report_type:
            messagebox.showerror("Error", "Select a report type.")
            return
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_map[report_type]}")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([f"JD INVESTMENTS LTD - {report_type} Report"])
                writer.writerow(headers_map[report_type])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Report saved to {file_path}")

    def add_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dashboard")
        tk.Label(tab, text="Dashboard Overview", font=("Arial", 14, "bold")).pack(pady=10)
        self.dashboard_text = tk.Label(tab, text="Click 'Refresh' to update metrics.")
        self.dashboard_text.pack(pady=10)
        tk.Button(tab, text="Refresh Dashboard", command=self.refresh_dashboard).pack(pady=10)

    def refresh_dashboard(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM sales")
        total_sales = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(eggs_collected) FROM egg_production")
        total_eggs = cursor.fetchone()[0] or 0
        cursor.execute("SELECT AVG(average_egg_weight) FROM egg_production")
        avg_egg_weight = cursor.fetchone()[0] or 0
        dashboard_str = (f"Total Expenses: {total_expenses:.2f}\n"
                         f"Total Sales: {total_sales:.2f}\n"
                         f"Total Eggs Collected: {total_eggs}\n"
                         f"Average Egg Weight: {avg_egg_weight:.2f} g")
        self.dashboard_text.config(text=dashboard_str)

    def add_supplier_management_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Supplier Management")
        tk.Label(tab, text="Name:").pack(pady=5)
        self.sup_name = tk.Entry(tab)
        self.sup_name.pack(pady=5)
        tk.Label(tab, text="Contact:").pack(pady=5)
        self.sup_contact = tk.Entry(tab)
        self.sup_contact.pack(pady=5)
        tk.Label(tab, text="Address:").pack(pady=5)
        self.sup_address = tk.Entry(tab)
        self.sup_address.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.sup_notes = tk.Entry(tab)
        self.sup_notes.pack(pady=5)
        tk.Button(tab, text="Add Supplier", command=self.add_supplier).pack(pady=10)
        tk.Button(tab, text="View Suppliers", command=self.view_suppliers).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_suppliers).pack(pady=5)

    def add_supplier(self):
        name = self.sup_name.get()
        contact = self.sup_contact.get()
        address = self.sup_address.get()
        notes = self.sup_notes.get()
        if not name:
            messagebox.showerror("Error", "Supplier name is required.")
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO suppliers (name, contact, address, notes) VALUES (?, ?, ?, ?)",
                       (name, contact, address, notes))
        self.conn.commit()
        messagebox.showinfo("Success", "Supplier added.")

    def view_suppliers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM suppliers")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Name: {log[1]}, Contact: {log[2]}, Address: {log[3]}, Notes: {log[4]}" for log in logs])
        messagebox.showinfo("Suppliers", log_str or "No suppliers.")

    def export_suppliers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM suppliers")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Contact", "Address", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_task_scheduler_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Task Scheduler")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.task_date = tk.Entry(tab)
        self.task_date.pack(pady=5)
        tk.Label(tab, text="Task Description:").pack(pady=5)
        self.task_desc = tk.Entry(tab)
        self.task_desc.pack(pady=5)
        tk.Label(tab, text="Status (e.g., Pending, Completed):").pack(pady=5)
        self.task_status = tk.Entry(tab)
        self.task_status.pack(pady=5)
        tk.Button(tab, text="Add Task", command=self.add_task).pack(pady=10)
        tk.Button(tab, text="View Tasks", command=self.view_tasks).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_tasks).pack(pady=5)

    def add_task(self):
        date = self.task_date.get()
        desc = self.task_desc.get()
        status = self.task_status.get()
        if not date or not desc or not status:
            messagebox.showerror("Error", "Invalid input. Ensure valid date, description, and status.")
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (date, task_description, status) VALUES (?, ?, ?)",
                       (date, desc, status))
        self.conn.commit()
        messagebox.showinfo("Success", "Task added.")

    def view_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Description: {log[2]}, Status: {log[3]}" for log in logs])
        messagebox.showinfo("Tasks", log_str or "No tasks.")

    def export_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Task Description", "Status"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def add_sustainability_tracker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sustainability Tracker")
        tk.Label(tab, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.sus_date = tk.Entry(tab)
        self.sus_date.pack(pady=5)
        tk.Label(tab, text="Water Usage (liters):").pack(pady=5)
        self.sus_water = tk.Entry(tab)
        self.sus_water.pack(pady=5)
        tk.Label(tab, text="Energy Usage (kWh):").pack(pady=5)
        self.sus_energy = tk.Entry(tab)
        self.sus_energy.pack(pady=5)
        tk.Label(tab, text="Waste (kg):").pack(pady=5)
        self.sus_waste = tk.Entry(tab)
        self.sus_waste.pack(pady=5)
        tk.Label(tab, text="Notes:").pack(pady=5)
        self.sus_notes = tk.Entry(tab)
        self.sus_notes.pack(pady=5)
        tk.Button(tab, text="Log Sustainability", command=self.log_sustainability).pack(pady=10)
        tk.Button(tab, text="View Logs", command=self.view_sustainability_logs).pack(pady=5)
        tk.Button(tab, text="Export to CSV", command=self.export_sustainability_logs).pack(pady=5)

    def log_sustainability(self):
        try:
            date = self.sus_date.get()
            water = float(self.sus_water.get())
            energy = float(self.sus_energy.get())
            waste = float(self.sus_waste.get())
            notes = self.sus_notes.get()
            if not date or water < 0 or energy < 0 or waste < 0:
                messagebox.showerror("Error", "Invalid input. Ensure valid date and non-negative values.")
                return
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO sustainability (date, water_usage, energy_usage, waste, notes) VALUES (?, ?, ?, ?, ?)",
                           (date, water, energy, waste, notes))
            self.conn.commit()
            messagebox.showinfo("Success", "Sustainability data logged.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def view_sustainability_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sustainability")
        logs = cursor.fetchall()
        log_str = "\n".join([f"ID: {log[0]}, Date: {log[1]}, Water: {log[2]}, Energy: {log[3]}, Waste: {log[4]}, Notes: {log[5]}" for log in logs])
        messagebox.showinfo("Sustainability Logs", log_str or "No logs.")

    def export_sustainability_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sustainability")
        logs = cursor.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Water Usage", "Energy Usage", "Waste", "Notes"])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"Saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PoultryManagementSuite(root)
    root.mainloop()