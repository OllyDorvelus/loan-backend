def format_date(date):
    return date.strftime("%d-%m-%y")


def apply_interest(amount, interest_rate=0.25):
    return (amount * interest_rate) + amount


def format_money(amount):
    return f'R{amount:,.2f}'.replace(',', ' ').replace('.', ',')
