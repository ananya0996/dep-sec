import json

def generate_html_report(json_file, output_html="vulnerability_report.html"):
    with open(json_file, "r") as f:
        data = json.load(f)

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background-color: #000000;
                color: #ffffff;
                margin: 2rem;
            }
            .vulnerability-table {
                width: 100%;
                border-collapse: collapse;
                font-family: 'Courier New', monospace;
                margin: 20px 0;
            }
            .vulnerability-table th,
            .vulnerability-table td {
                padding: 12px;
                text-align: left;
                border: 1px solid #00ff00;
            }
            .vulnerability-table th {
                background-color: #1a1a1a;
                color: #00ff00;
                border-bottom: 2px solid #00ff00;
            }
            .parent-package {
                color: #808080;
                font-style: italic;
            }
            .vulnerable-package {
                font-weight: bold;
                color: #ffffff;
            }
            .severity-HIGH {
                background-color: #330000;
                color: #ff0000;
                font-weight: bold;
            }
            .severity-MED {
                background-color: #333300;
                color: #ffff00;
            }
            .severity-LOW {
                background-color: #003300;
                color: #00ff00;
            }
            h2 {
                color: #00ff00;
                border-bottom: 2px solid #00ff00;
                padding-bottom: 0.5rem;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <h2>VULNERABILITY REPORT</h2>
        <table class="vulnerability-table">
            <thead>
                <tr>
                    <th>S. No.</th>
                    <th>Package</th>
                    <th>Vulnerable Version</th>
                    <th>Vulnerability ID</th>
                    <th>Vulnerability Type</th>
                    <th>Severity</th>
                    <th>Patched Version</th>
                </tr>
            </thead>
            <tbody>
    """

    for entry in data:
        num_vulns = len(entry["vulnerabilities"])
        package_parts = entry["package_hierarchy"].split(" > ")

        # First row with rowspan
        html_content += f"""
        <tr>
            <td rowspan="{num_vulns}">{entry["s_no"]}</td>
            <td rowspan="{num_vulns}">
                {"<span class='parent-package'>" + " > ".join(package_parts[:-1]) + "</span> > " if len(package_parts) > 1 else ""}
                <span class='vulnerable-package'>{package_parts[-1]}</span>
            </td>
            <td>{entry["vulnerable_versions"][0]}</td>
            <td>{entry["vulnerabilities"][0]["vulnerability_id"]}</td>
            <td>{entry["vulnerabilities"][0]["vulnerability_type"]}</td>
            <td class="severity-{entry["vulnerabilities"][0]["severity"]}">{entry["vulnerabilities"][0]["severity"]}</td>
            <td>{entry["vulnerabilities"][0]["patched_version"]}</td>
        </tr>
        """

        # Subsequent rows
        for i in range(1, num_vulns):
            html_content += f"""
            <tr>
                <td>{entry["vulnerable_versions"][i]}</td>
                <td>{entry["vulnerabilities"][i]["vulnerability_id"]}</td>
                <td>{entry["vulnerabilities"][i]["vulnerability_type"]}</td>
                <td class="severity-{entry["vulnerabilities"][i]["severity"]}">{entry["vulnerabilities"][i]["severity"]}</td>
                <td>{entry["vulnerabilities"][i]["patched_version"]}</td>
            </tr>
            """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(output_html, "w") as f:
        f.write(html_content)

# Same test data
json_input = '''
[
    {
        "s_no": 1,
        "package_hierarchy": "Package A > Package B > Package C",
        "vulnerable_versions": ["1.2", "1.2"],
        "vulnerabilities": [
            {
                "vulnerability_id": "CVE-12345",
                "vulnerability_type": "SQL Injection",
                "severity": "HIGH",
                "patched_version": "1.5"
            },
            {
                "vulnerability_id": "CVE-45678",
                "vulnerability_type": "Null Pointer Deref",
                "severity": "MED",
                "patched_version": "1.4"
            }
        ]
    },
    {
        "s_no": 2,
        "package_hierarchy": "Package X",
        "vulnerable_versions": ["4.5"],
        "vulnerabilities": [
            {
                "vulnerability_id": "CVE-54321",
                "vulnerability_type": "Hardcoded Credentials",
                "severity": "LOW",
                "patched_version": "4.9"
            }
        ]
    }
]
'''

with open("vulnerabilities.json", "w") as f:
    f.write(json_input)

generate_html_report("vulnerabilities.json")

