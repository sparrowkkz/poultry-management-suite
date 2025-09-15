Poultry Management Suite

A Python/Tkinter desktop app for poultry farms, runs in VS Code. 17 tools: weight, FCR, eggs, vaccinations, profit, health, incubation, environment, expenses/sales, customers, meds, inventory, reports, dashboard, suppliers, tasks, sustainability. SQLite storage, CSV export, no external dependencies.
Features

Weight & Uniformity Calculator: Sample 10% of birds, calculate averages, uniformity (±10%), compare to Lohmann standards.
FCR Calculator: Feed Conversion Ratio with verdicts (Optimal/Suboptimal).
Egg Production Tracker: Log daily eggs, flock size, weights; view/export trends.
Health & Medication Tracker: Mortality, symptoms, treatments, vaccination schedules.
Financial Tools: Profit calculator, expense/sales tracker with CSV export.
Inventory & Supplier Management: Track feed, meds, vendors.
Environment Monitor: Log temperature, humidity, ventilation.
Reports & Dashboard: Generate CSV reports, view key metrics.
Sustainability Tracker: Water, energy, waste logging.
Incubation Calculator: Hatch rates, breeding logs.

Data is stored in a local SQLite database (poultry_data.db) for offline use.
Installation
Prerequisites

Python 3.6+ (tested with 3.13; includes Tkinter and SQLite3).
Visual Studio Code (or another Python IDE).
No external dependencies required.

Setup

Clone the repo:
git clone https://github.com/sparrowkkz/poultry-management-suite.git
cd poultry-management-suite


Open in VS Code:

Open VS Code, select File > Open Folder, choose the poultry-management-suite folder.
Select Python 3.13 interpreter (Ctrl+Shift+P, Python: Select Interpreter).


Run the script:

Open poultry_management_suite.py in VS Code.
Click "Run" (triangle icon) or press F5, or right-click and select "Run Python File in Terminal."



The GUI will launch with tabs for each tool.
Usage

Weight Calculator: Enter age/flock size, collect 10% weights, get uniformity and verdicts.
Expense/Sales Tracker: Log expenses and sales; export to CSV.
All Tools: Use "View Logs" for history, "Export to CSV" for reports.
Database: poultry_data.db auto-creates; backup regularly.

Contributing

Fork the repo.
Create a feature branch: git checkout -b feature/amazing-tool.
Commit changes: git commit -m "Add amazing tool".
Push: git push origin feature/amazing-tool.
Open a Pull Request.

See CONTRIBUTING.md for details.
License
This project is licensed under the MIT License - see LICENSE for details.
Acknowledgments

Built with Tkinter and SQLite3 (Python standard library).
Inspired by open-source poultry systems like TelelBirds.

For issues or support: Open an Issue.
