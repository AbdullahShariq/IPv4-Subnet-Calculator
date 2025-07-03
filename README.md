# IPv4 Subnet Calculator

## Overview
The IPv4 Subnet Calculator is a web-based application designed to perform subnet calculations for IPv4 addresses. It allows users to input an IP address and select a subnet mask to calculate network details such as the **network address**, **usable host IP range**, **broadcast address**, **total and usable hosts**, **subnet mask**, **wildcard mask**, **binary subnet mask**, and **IP class**. The application generates downloadable `CSV` and `PDF` reports for the calculated results.

---

## Features
- **IP Address Validation**: Validates the input IPv4 address format.
- **Subnet Selection**: Supports a wide range of subnet masks from /8 to /30.
- **Network Details Calculation**: Computes key subnetting details, including:
  - Network Address
  - Usable Host IP Range
  - Broadcast Address
  - Total Number of Hosts
  - Number of Usable Hosts
  - Subnet Mask with CIDR Notation
  - Wildcard Mask
  - Binary Subnet Mask
  - IP Class (A, B, C, or Invalid)
- **Export Options**: Generates downloadable CSV and PDF files containing the calculation results.
- **User-Friendly Interface**: Clean and responsive web interface built with HTML, CSS, and Flask templates.

---

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Jinja2 templating
- **Libraries**:
  - `pandas` for CSV generation
  - `reportlab` for PDF generation
- **Deployment**: Runs as a Flask web application

---

## 📁 Folder Structure
```
├── app.py                      # The main Flask application (backend logic, IP validation, etc.)
├── templates/
│   └── index.html             # Frontend template for the user interface (Jinja2)
├── static/                    # Directory for storing generated CSV and PDF files
├── requirements.txt           # Lists the required Python packages
└── README.md
```

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AbdullahShariq/IPv4-Subnet-Calculator.git
   cd IPv4-Subnet-Calculator
   ```
   
2. **Install Dependencies**:
   Ensure you have Python 3.6+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will start in debug mode and be accessible at `http://127.0.0.1:5000`.

---

## Usage
1. Open the application in a web browser (`http://127.0.0.1:5000`).
2. Select a network class (Any, A, B, or C) or leave it as "Any".
3. Choose a subnet mask from the dropdown menu (e.g., 255.255.255.0 /24).
4. Enter a valid IPv4 address (e.g., 192.168.1.100).
5. Click "Calculate" to view the subnet details.
6. Download the results as a CSV or PDF file using the provided links.
7. Click "Clear" to reset the form.

---


## Notes
- Ensure the `static` directory exists before running the application, as it is used to store generated files.
- The application validates IP addresses to ensure they follow the correct format (four octets, each between 0 and 255).
- Subnet masks must include the CIDR notation (e.g., 255.255.255.0/24).
- Generated files are timestamped to avoid overwrites and are stored in the `static` directory.

