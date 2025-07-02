from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

app = Flask(__name__)

def validate_ip(ip):
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    return all(int(octet) >= 0 and int(octet) <= 255 and octet == str(int(octet)) for octet in octets)

def get_network_details(ip, subnet):
    # Ensure subnet is in the correct format (e.g., "255.255.224.0/19")
    if '/' not in subnet:
        raise ValueError("Invalid subnet format. Expected format: '255.255.224.0/19'")
    subnet_mask, prefix = subnet.split('/')
    prefix = int(prefix)
    mask_octets = [int(octet) for octet in subnet_mask.split('.')]
    
    ip_octets = [int(octet) for octet in ip.split('.')]
    
    network_octets = [ip_octets[i] & mask_octets[i] for i in range(4)]
    network_address = '.'.join(map(str, network_octets))

    broadcast_octets = [network_octets[i] | (255 - mask_octets[i]) for i in range(4)]
    broadcast_address = '.'.join(map(str, broadcast_octets))

    host_min = network_octets.copy()
    host_min[3] = 1 if network_octets[3] == 255 else network_octets[3] + 1
    host_max = broadcast_octets.copy()
    host_max[3] = 254 if broadcast_octets[3] == 0 else broadcast_octets[3] - 1
    usable_range = f"{'.'.join(map(str, host_min))} - {'.'.join(map(str, host_max))}"

    total_hosts = 2 ** (32 - prefix)
    usable_hosts = total_hosts - 2

    wildcard_octets = [255 - octet for octet in mask_octets]
    wildcard_mask = '.'.join(map(str, wildcard_octets))

    binary_mask = ''.join(bin(octet)[2:].zfill(8) for octet in mask_octets)

    if 0 <= ip_octets[0] <= 127:
        ip_class = 'A'
    elif 128 <= ip_octets[0] <= 191:
        ip_class = 'B'
    elif 192 <= ip_octets[0] <= 223:
        ip_class = 'C'
    else:
        ip_class = 'Invalid'

    return {
        'network_address': network_address,
        'usable_range': usable_range,
        'broadcast_address': broadcast_address,
        'total_hosts': total_hosts,
        'usable_hosts': usable_hosts,
        'subnet_mask': subnet_mask + '/' + str(prefix),  # Return full subnet mask with CIDR
        'wildcard_mask': wildcard_mask,
        'binary_mask': binary_mask,
        'ip_class': ip_class
    }

def generate_csv(result, ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"subnet_result_{ip}_{timestamp}.csv"
    filepath = os.path.join("static", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    data = {
        'Field': ['IP Address', 'Network Address', 'Usable Host IP Range', 'Broadcast Address',
                  'Total Number of Hosts', 'Number of Usable Hosts', 'Subnet Mask',
                  'Wildcard Mask', 'Binary Subnet Mask', 'IP Class'],
        'Value': [ip, result['network_address'], result['usable_range'], result['broadcast_address'],
                  result['total_hosts'], result['usable_hosts'], result['subnet_mask'],
                  result['wildcard_mask'], result['binary_mask'], result['ip_class']]
    }
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    return filename

def generate_pdf(result, ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"subnet_result_{ip}_{timestamp}.pdf"
    pdf_filepath = os.path.join("static", pdf_filename)
    os.makedirs(os.path.dirname(pdf_filepath), exist_ok=True)

    c = canvas.Canvas(pdf_filepath, pagesize=letter)
    width, height = letter
    y_position = height - inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, y_position, "IPv4 Subnet Calculation Result")
    y_position -= 0.5 * inch

    c.setFont("Helvetica", 12)
    c.drawString(inch, y_position, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y_position -= inch

    c.setFont("Helvetica", 12)
    fields = [
        ("IP Address", ip),
        ("Network Address", result['network_address']),
        ("Usable Host IP Range", result['usable_range']),
        ("Broadcast Address", result['broadcast_address']),
        ("Total Number of Hosts", str(result['total_hosts'])),
        ("Number of Usable Hosts", str(result['usable_hosts'])),
        ("Subnet Mask", result['subnet_mask']),
        ("Wildcard Mask", result['wildcard_mask']),
        ("Binary Subnet Mask", result['binary_mask']),
        ("IP Class", result['ip_class'])
    ]

    for field, value in fields:
        c.drawString(inch, y_position, f"{field}: {value}")
        y_position -= 0.5 * inch
        if y_position < inch:
            c.showPage()
            y_position = height - inch

    c.showPage()
    c.save()
    return pdf_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    csv_file = None
    pdf_file = None

    if request.method == 'POST':
        ip = request.form.get('ipAddress', '').strip()
        subnet = request.form.get('subnet', '')
        network_class = request.form.get('networkClass', 'Any')

        if not validate_ip(ip):
            error = "Invalid IP address!"
        elif not subnet:
            error = "Please select a subnet!"
        else:
            try:
                result = get_network_details(ip, subnet)
                csv_file = generate_csv(result, ip)
                pdf_file = generate_pdf(result, ip)
            except ValueError as e:
                error = str(e)

    subnets = [
        ("255.0.0.0/8", "255.0.0.0 /8"),
        ("255.128.0.0/9", "255.128.0.0 /9"),
        ("255.192.0.0/10", "255.192.0.0 /10"),
        ("255.224.0.0/11", "255.224.0.0 /11"),
        ("255.240.0.0/12", "255.240.0.0 /12"),
        ("255.248.0.0/13", "255.248.0.0 /13"),
        ("255.252.0.0/14", "255.252.0.0 /14"),
        ("255.254.0.0/15", "255.254.0.0 /15"),
        ("255.255.0.0/16", "255.255.0.0 /16"),
        ("255.255.128.0/17", "255.255.128.0 /17"),
        ("255.255.192.0/18", "255.255.192.0 /18"),
        ("255.255.224.0/19", "255.255.224.0 /19"),
        ("255.255.240.0/20", "255.255.240.0 /20"),
        ("255.255.248.0/21", "255.255.248.0 /21"),
        ("255.255.252.0/22", "255.255.252.0 /22"),
        ("255.255.254.0/23", "255.255.254.0 /23"),
        ("255.255.255.0/24", "255.255.255.0 /24"),
        ("255.255.255.128/25", "255.255.255.128 /25"),
        ("255.255.255.192/26", "255.255.255.192 /26"),
        ("255.255.255.224/27", "255.255.255.224 /27"),
        ("255.255.255.240/28", "255.255.255.240 /28"),
        ("255.255.255.248/29", "255.255.255.248 /29"),
        ("255.255.255.252/30", "255.255.255.252 /30")
    ]

    return render_template('index.html', result=result, error=error, subnets=subnets, csv_file=csv_file, pdf_file=pdf_file)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join("static", filename), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)