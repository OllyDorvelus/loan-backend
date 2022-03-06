def format_date(date):
    return date.strftime("%d-%m-%y")


def format_money(amount):
    return f'R{amount:,.2f}'.replace(',', ' ').replace('.', ',')
