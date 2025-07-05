from flask import Flask, render_template, request
app = Flask(__name__)

# ===== Tax Bracket Calculation =====
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

# ===== Helper: Convert Profit + ROI to Winnings/Losses =====
def derive_winnings_losses(profit, roi):
    if roi == 0:
        raise ValueError("ROI cannot be zero.")
    losses = profit / roi
    winnings = profit + losses
    if winnings < -1e-6 or losses < -1e-6:
        raise ValueError("Invalid combination of profit and ROI.")
    return round(winnings, 2), round(losses, 2)

# ===== Core Calculator =====
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

# ===== Routes =====
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
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
                roi = float(roi_raw) / 100  # ROI entered as %
                result = calculate_gambling_tax(year, profit=profit, roi=roi)

            else:
                raise ValueError("Invalid method selected.")

        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001)