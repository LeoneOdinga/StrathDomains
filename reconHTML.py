import json
from collections import Counter
import qrcode

# Common elearning sites
common_elearning_sites = [
    "elearning.strathmore.edu",
    "sbselearning.strathmore.edu",
    "shsselearning.strathmore.edu",
    "executivelearning.strathmore.edu",
    "cpelearning.strathmore.edu"
]

def generate_html_table(data):
    html_table = "<html><head><style>"
    
    # CSS styles
    html_table += """
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
    
    .table-container {
        overflow-y: auto;
        max-height: 400px;
        font-family: 'Quicksand', sans-serif;
        font-size: 14px;
    }

    table {
        border-collapse: collapse;
        width: 100%;
    }

    th, td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 10px;
    }

    th {
        background-color: #f2f2f2;
    }

    a {
        text-decoration: none;
        color: #1E90FF;
    }

    h1 {
        text-align: center;
        font-family: 'Quicksand', sans-serif;
        font-size: 32px;
        margin-bottom: 10px;
    }

    h2 {
        text-align: center;
        font-family: 'Quicksand', sans-serif;
        font-size: 20px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .summary {
        margin-top: 30px;
        padding: 10px;
        background-color: #f2f2f2;
    }

    .summary-table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 10px;
    }

    .summary-table th, .summary-table td {
        border: 1px solid #dddddd;
        padding: 8px;
        text-align: center;
    }

    .summary-table th {
        background-color: #1E90FF;
        color: white;
    }
    """
    
    html_table += "</style></head><body><div class='table-container'><h1>Strathmore University Domains</h1>"
    html_table += "<h2>Explore Strathmore Domains To Find Out Various Services</h2>"
    html_table += "<table>\n"
    
    # Create table headers
    headers = data[0].keys()
    html_table += "<thead><tr>"
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += "<th>QR Code</th>"  # New column for QR codes
    html_table += "</tr></thead>\n"
    
    # Create table body
    html_table += "<tbody>"
    for row in data:
        html_table += "<tr>"
        for key, value in row.items():
            if key == "hostName":
                html_table += f"<td><a href='http://{value}'>{value}</a></td>"
            else:
                html_table += f"<td>{value}</td>"
        qr = generate_qr_code(f"http://{row['hostName']}")
        html_table += f"<td>{qr}</td>"  # Add QR code in its own column
        html_table += "</tr>\n"
    html_table += "</tbody></table></div><div class='summary'>"
    
    # Generate summary
    summary = generate_summary(data)
    html_table += summary
    
    # Generate eLearning summary
    elearning_summary = generate_elearning_summary(data)
    html_table += elearning_summary
	
	# Generate WHOIS summary
    whois_summary = generate_whois_summary(data)
    html_table += whois_summary
    
    html_table += "</div></body></html>"
    return html_table

	
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_base64 = qr_img.resize((100, 100)).save("qr_temp.png", format="PNG")
    return f'<img src="qr_temp.png">'


def generate_summary(data):
    ip_addresses = [row['IPAddress'] for row in data]
    ip_counter = Counter(ip_addresses)
    total_sites = len(data)
    
    summary = "<h2>Server Efficiency Summary</h2>"
    
    summary += "<table class='summary-table'>"
    summary += "<tr><th>Server</th><th>Sites Supported</th><th>Percentage</th></tr>"
    
    for ip, count in ip_counter.items():
        percentage = (count / total_sites) * 100
        summary += f"<tr><td>{ip}</td><td>{count}</td><td>{percentage:.2f}%</td></tr>"
    
    summary += "</table>"
    
    most_common_ip = ip_counter.most_common(1)[0][0]
    summary += f"<p><strong>Most Efficient Server: {most_common_ip}</strong></p>"
    
    return summary

def generate_elearning_summary(data):
    elearning_servers = {}
    
    for row in data:
        if row['hostName'] in common_elearning_sites:
            server = row['IPAddress']
            site = row['hostName']
            if server not in elearning_servers:
                elearning_servers[server] = []
            elearning_servers[server].append(site)
    
    elearning_summary = "<h2>eLearning Platforms and Their Servers</h2>"
    
    elearning_summary += "<table class='summary-table'>"
    elearning_summary += "<tr><th>Server</th><th>eLearning Sites</th></tr>"
    
    for server, sites in elearning_servers.items():
        sites_str = ", ".join(sites)
        elearning_summary += f"<tr><td>{server}</td><td>{sites_str}</td></tr>"
    
    elearning_summary += "</table>"
    
    return elearning_summary
	
def generate_whois_summary(data):
    whois_summary = "<h2>WHOIS Lookup Summary</h2>"
    
    whois_summary += "<table class='summary-table'>"
    whois_summary += "<tr><th>Server</th><th>Domain</th><th>Registrar</th><th>Creation Date</th></tr>"
    
    for row in data:
        domain = row['hostName']
        whois_info = perform_whois_lookup(domain)
        
        if whois_info:
            registrar = whois_info.registrar[0] if isinstance(whois_info.registrar, list) else whois_info.registrar
            creation_date = whois_info.creation_date.strftime("%Y-%m-%d") if whois_info.creation_date else "N/A"
            
            whois_summary += f"<tr><td>{row['IPAddress']}</td><td>{domain}</td><td>{registrar}</td><td>{creation_date}</td></tr>"
        else:
            whois_summary += f"<tr><td>{row['IPAddress']}</td><td>{domain}</td><td>N/A</td><td>N/A</td></tr>"
    
    whois_summary += "</table>"
    
    return whois_summary

	
def perform_whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        print(f"Failed to perform WHOIS lookup for {domain}: {e}")
        return None
		

def main():
    with open("recondata.json", "r") as json_file:
        data = json.load(json_file)
    
    html_table = generate_html_table(data)
    
    with open("output.html", "w") as html_file:
        html_file.write(html_table)
        print("HTML table generated and saved to output.html")

if __name__ == "__main__":
    main()
