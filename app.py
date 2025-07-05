from flask import Flask, request
import os

app = Flask(__name__)

def calculate_tax_with_brackets(taxable_income):
    brackets = [
        (0, 11000, 0.10),
        (11000, 44725, 0.12),
        (44725, 95375, 0.22),
        (95375, 182100, 0.24),
        (182100, 231250, 0.32),
        (231250, 578125, 0.35),
        (578125, float('inf'), 0.37)
    ]
    tax = 0.0
    for lower, upper, rate in brackets:
        if taxable_income > lower:
            taxed_amount = min(taxable_income, upper) - lower
            tax += taxed_amount * rate
        else:
            break
    return round(tax, 2)

def derive_winnings_losses(profit, roi):
    if roi == 0:
        raise ValueError("ROI cannot be zero.")
    losses = profit / roi
    winnings = profit + losses
    if winnings < -1e-6 or losses < -1e-6:
        raise ValueError("Invalid combination of profit and ROI.")
    return round(winnings, 2), round(losses, 2)

def calculate_gambling_tax(year, winnings=None, losses=None, profit=None, roi=None):
    if winnings is None or losses is None:
        if profit is not None and roi is not None:
            winnings, losses = derive_winnings_losses(profit, roi)
        else:
            raise ValueError("Provide either (winnings & losses) or (profit & ROI).")

    if year >= 2026:
        max_deductible = min(winnings, losses * 0.90)
        rule = "Post-2026 (90% deduction limit)"
    else:
        max_deductible = min(winnings, losses)
        rule = "Pre-2026 (full deduction)"

    taxable_income = max(winnings - max_deductible, 0)
    tax_owed = calculate_tax_with_brackets(taxable_income)
    phantom_income = taxable_income if losses >= winnings and taxable_income > 0 else 0

    return {
        "winnings": round(winnings, 2),
        "losses": round(losses, 2),
        "max_deductible": round(max_deductible, 2),
        "taxable_income": round(taxable_income, 2),
        "phantom_income": round(phantom_income, 2),
        "tax_owed": tax_owed,
        "rule_applied": rule
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Beautiful Bill Tax Calculator</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 700px; 
                    margin: auto; 
                    padding: 2rem; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }
                h1 { 
                    color: #333; 
                    text-align: center; 
                    margin-bottom: 2rem;
                    font-size: 2.5rem;
                }
                label { 
                    display: block; 
                    margin-top: 1.5rem; 
                    font-weight: 600;
                    color: #555;
                }
                input, select { 
                    width: 100%; 
                    padding: 0.75rem; 
                    box-sizing: border-box; 
                    border: 2px solid #e1e5e9;
                    border-radius: 8px;
                    font-size: 1rem;
                    transition: border-color 0.3s ease;
                }
                input:focus, select:focus {
                    outline: none;
                    border-color: #667eea;
                }
                .section { 
                    border: 2px solid #e1e5e9; 
                    padding: 1.5rem; 
                    margin-top: 1.5rem; 
                    border-radius: 12px;
                    background: #f8f9fa;
                }
                .result { 
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 2rem; 
                    margin-top: 2rem; 
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
                }
                .result h2 {
                    margin-top: 0;
                    font-size: 1.8rem;
                }
                .result p {
                    margin: 0.8rem 0;
                    font-size: 1.1rem;
                }
                .error { 
                    color: #e74c3c; 
                    background: #fdf2f2;
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                    border-left: 4px solid #e74c3c;
                }
                button { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 1rem 2rem; 
                    margin-top: 2rem; 
                    border-radius: 8px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                    transition: transform 0.2s ease;
                }
                button:hover {
                    transform: translateY(-2px);
                }
                .breakdown {
                    background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎲 Beautiful Bill Tax Calculator</h1>
                
                <form method="POST" action="/">
                    <label>Tax Year:</label>
                    <input type="number" name="year" value="2026" required>

                    <label>Choose input method:</label>
                    <select name="method" required onchange="toggleSections(this.value)">
                        <option value="basic">Winnings & Losses</option>
                        <option value="roi">Profit & ROI</option>
                    </select>

                    <div id="basic" class="section">
                        <label>Total Winnings ($):</label>
                        <input type="number" name="winnings" step="0.01" placeholder="e.g., 200000">
                        <label>Total Losses ($):</label>
                        <input type="number" name="losses" step="0.01" placeholder="e.g., 210000">
                    </div>

                    <div id="roi" class="section" style="display:none;">
                        <label>Total Profit ($):</label>
                        <input type="number" name="profit" step="0.01">
                        <label>ROI (%):</label>
                        <input type="number" name="roi" step="0.01" placeholder="e.g., -5 for -5%">
                    </div>

                    <button type="submit">Calculate Tax</button>
                </form>
            </div>

            <script>
                function toggleSections(method) {
                    document.getElementById('basic').style.display = method === 'basic' ? 'block' : 'none';
                    document.getElementById('roi').style.display = method === 'roi' ? 'block' : 'none';
                }
            </script>
        </body>
        </html>
        '''
    
    # Handle POST request
    try:
        method = request.form.get('method')
        year = request.form.get('year')
        if not year:
            raise ValueError("Year is required.")
        year = int(year)

        if method == 'basic':
            winnings_raw = request.form.get('winnings')
            losses_raw = request.form.get('losses')
            if not winnings_raw or not losses_raw:
                raise ValueError("Please enter both winnings and losses.")
            winnings = float(winnings_raw)
            losses = float(losses_raw)
            result = calculate_gambling_tax(year, winnings=winnings, losses=losses)

        elif method == 'roi':
            profit_raw = request.form.get('profit')
            roi_raw = request.form.get('roi')
            if not profit_raw or not roi_raw:
                raise ValueError("Please enter both profit and ROI.")
            profit = float(profit_raw)
            roi = float(roi_raw) / 100
            result = calculate_gambling_tax(year, profit=profit, roi=roi)
        else:
            raise ValueError("Invalid method selected.")

        max_deductible = result['winnings'] if result['rule_applied'] == "Pre-2026 (full deduction)" else min(result['winnings'], result['losses'] * 0.90)
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Beautiful Bill Tax Calculator - Results</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 700px; 
                    margin: auto; 
                    padding: 2rem; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333; 
                    text-align: center; 
                    margin-bottom: 2rem;
                    font-size: 2.5rem;
                }}
                .result {{ 
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 2rem; 
                    margin-top: 2rem; 
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
                }}
                .result h2 {{
                    margin-top: 0;
                    font-size: 1.8rem;
                }}
                .result p {{
                    margin: 0.8rem 0;
                    font-size: 1.1rem;
                }}
                .breakdown {{
                    background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                }}
                .back-link {{
                    display: inline-block;
                    margin-top: 2rem;
                    padding: 1rem 2rem;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    transition: transform 0.2s ease;
                }}
                .back-link:hover {{
                    transform: translateY(-2px);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧾 Tax Calculation Results</h1>
                <div class="result">
                    <h2>Tax Calculation Results</h2>
                    <p><strong>Rule Applied:</strong> {result["rule_applied"]}</p>
                    <p><strong>Winnings:</strong> ${result["winnings"]:,.2f}</p>
                    <p><strong>Losses:</strong> ${result["losses"]:,.2f}</p>
                    <div class="breakdown">
                        <p><strong>Maximum Deductible Losses:</strong> ${max_deductible:,.2f}</p>
                        <p><strong>Taxable Income:</strong> ${result["taxable_income"]:,.2f}</p>
                        <p><strong>Phantom Income:</strong> ${result["phantom_income"]:,.2f}</p>
                        <p><strong>Tax Owed:</strong> ${result["tax_owed"]:,.2f}</p>
                    </div>
                </div>
                <a href="/" class="back-link">Calculate Again</a>
            </div>
        </body>
        </html>
        '''

    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Beautiful Bill Tax Calculator - Error</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 700px; margin: auto; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                .container {{ background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; margin-bottom: 2rem; font-size: 2.5rem; }}
                .error {{ color: #e74c3c; background: #fdf2f2; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #e74c3c; }}
                .back-link {{ display: inline-block; margin-top: 2rem; padding: 1rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Error</h1>
                <div class="error"><strong>Error:</strong> {str(e)}</div>
                <a href="/" class="back-link">Back to Calculator</a>
            </div>
        </body>
        </html>
        '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)