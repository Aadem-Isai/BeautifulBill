🎲 Gambling Tax Calculator
With the "One Big Beautiful Bill" proposed by President Donald Trump, this is a comprehensive web application for calculating gambling tax liability based on winnings, losses, and changing tax regulations.
🌟 Features

Dual Input Methods: Calculate taxes using either:

Direct winnings and losses
Net profit and ROI percentage


Multi-Year Support: Handles tax calculations for different years with varying deduction rules
Pre/Post-2026 Rules: Automatically applies the correct tax deduction limits
Phantom Income Detection: Identifies and calculates phantom income scenarios
Responsive Design: Works seamlessly on desktop and mobile devices
Real-time Calculations: Instant tax liability calculations

📊 Tax Rules Implemented
Pre-2026 Rules

Full deduction of losses up to winnings amount
Standard federal tax brackets apply

Post-2026 Rules (90% Deduction Limit)

Maximum deductible losses = 90% of total losses
Potential phantom income on net losing years
Updated tax calculations reflecting new regulations

🚀 Live Demo
Visit the calculator at: [Your Website URL]
🛠️ Installation & Setup
Prerequisites

Python 3.7+
pip package manager

Local Development

Clone the repository
bashgit clone https://github.com/aademisai/gambling-tax-calculator.git
cd gambling-tax-calculator

Install dependencies
bashpip install -r requirements.txt

Run the application
bashpython app.py

Open in browser
http://localhost:5000


📁 Project Structure
gambling-tax-calculator/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── static/            # Static files (if any)
🔧 Technical Details
Core Functions

calculate_tax_with_brackets(): Applies federal tax brackets to taxable income
derive_winnings_losses(): Converts profit/ROI to winnings/losses
calculate_gambling_tax(): Main calculation engine with year-specific rules

Tax Brackets (2024)

10%: $0 - $11,000
12%: $11,001 - $44,725
22%: $44,726 - $95,375
24%: $95,376 - $182,100
32%: $182,101 - $231,250
35%: $231,251 - $578,125
37%: $578,126+

📋 Usage Examples
Example 1: Basic Calculation

Winnings: $50,000
Losses: $40,000
Year: 2024
Result: Taxable income of $10,000

Example 2: ROI Method

Profit: -$5,000
ROI: -10%
Year: 2026
Result: Potential phantom income due to 90% deduction limit

Example 3: Phantom Income Scenario

Winnings: $100,000
Losses: $110,000
Year: 2026
Result: $11,000 phantom income due to 90% deduction limit

🔒 Security & Privacy

No user data is stored or transmitted
All calculations performed client-side and server-side without persistence
HTTPS encryption when deployed
No tracking or analytics by default

⚖️ Legal Disclaimer
This calculator is for educational and informational purposes only. Tax laws are complex and subject to change. Always consult with a qualified tax professional for advice specific to your situation.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🐛 Bug Reports & Feature Requests
Please use the GitHub Issues page to report bugs or request features.
📞 Support
For support, please open an issue on GitHub or contact [isai.aadem05@gmail.com].
🔄 Version History
v1.0.0

Initial release
Basic tax calculation functionality
Support for pre-2026 and post-2026 rules
Responsive web interface
Dual input methods (winnings/losses and profit/ROI)

🙏 Acknowledgments

Federal tax bracket information from IRS publications
Flask framework for web application structure
Bootstrap CSS framework for responsive design

📊 Performance

Load Time: < 2 seconds
Calculation Speed: Instant
Mobile Responsive: Yes
Browser Support: All modern browsers

🔮 Future Enhancements

 State tax calculations
 Historical tax bracket data
 PDF report generation
 Multiple tax scenarios comparison
 Advanced deduction strategies
 Integration with tax software APIs


Made with ❤️
Remember: This tool is for educational purposes. Always consult with a tax professional for official tax advice.
