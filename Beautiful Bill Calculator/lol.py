from flask import Flask, request

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
        rule = "Post-2026 (.90 deduction limit)"
    else:
        max_deductible = min(winnings, losses)
        rule = "Pre-2026 (full deduction)"

    taxable_income = max(winnings - max_deductible, 0)
    tax_owed = calculate_tax_with_brackets(taxable_income)
    phantom_income = taxable_income if losses >= winnings and taxable_income > 0 else 0

    return {
        "winnings": round(winnings, 2),
        "losses": round(losses, 2),
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
                body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 1rem; }
                label { display: block; margin-top: 1rem; }
                input, select { width: 100%; padding: 0.5rem; box-sizing: border-box; }
                .section { border: 1px solid #ccc; padding: 1rem; margin-top: 1rem; }
                .result { background-color: #f0f0f0; padding: 1rem; margin-top: 1rem; }
                .error { color: red; margin-top: 1rem; }
                button { padding: 0.7rem 1rem; margin-top: 1rem; }
            </style>
        </head>
        <body>
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
                    <input type="number" name="winnings" step="0.01">
                    <label>Total Losses ($):</label>
                    <input type="number" name="losses" step="0.01">
                </div>

                <div id="roi" class="section" style="display:none;">
                    <label>Total Profit ($):</label>
                    <input type="number" name="profit" step="0.01">
                    <label>ROI (%):</label>
                    <input type="number" name="roi" step="0.01" placeholder="e.g., -5 for -5%">
                </div>

                <button type="submit">Calculate Tax</button>
            </form>

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

        return f'''
        <h1>🧾 Results</h1>
        <p><strong>Rule Applied:</strong> {result["rule_applied"]}</p>
        <p><strong>Winnings:</strong> ${result["winnings"]}</p>
        <p><strong>Losses:</strong> ${result["losses"]}</p>
        <p><strong>Taxable Income:</strong> ${result["taxable_income"]}</p>
        <p><strong>Phantom Income:</strong> ${result["phantom_income"]}</p>
        <p><strong>Tax Owed:</strong> ${result["tax_owed"]}</p>
        <a href="/">Calculate Again</a>
        '''

    except Exception as e:
        return f'<h1>Error</h1><p style="color:red;">{str(e)}</p><a href="/">Back</a>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)