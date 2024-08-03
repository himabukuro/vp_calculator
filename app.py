from flask import Flask, render_template, request

app = Flask(__name__)

def find_min_cost_for_vp(desired_quantity, current_quantity):
    items = [
        (610, 500),
        (1340, 1150),
        (2440, 2150),
        (4900, 4400),
        (5980, 5500),
        (11000, 10500)
    ]

    additional_quantity = desired_quantity - current_quantity

    if additional_quantity <= 0:
        return "既に必要な数量を持っています。追加購入の必要はありません。", None

    from math import inf

    max_quantity = additional_quantity * 2
    dp = [inf] * (additional_quantity + max_quantity + 1)
    dp[0] = 0
    choices = [-1] * (additional_quantity + max_quantity + 1)

    for price, quantity in items:
        for i in range(quantity, additional_quantity + max_quantity + 1):
            if dp[i - quantity] != inf:
                if dp[i] > dp[i - quantity] + price:
                    dp[i] = dp[i - quantity] + price
                    choices[i] = quantity

    min_price = min(dp[additional_quantity:])
    min_index = dp.index(min_price)

    best_combination = []
    while min_index > 0:
        if choices[min_index] == -1:
            break
        quantity = choices[min_index]
        for price, q in items:
            if q == quantity:
                best_combination.append((price, quantity))
                min_index -= quantity
                break

    result = f"追加で必要な{additional_quantity}VPを購入するのに最も安い価格は{min_price}YENです。\n"
    result += "最適な購入組み合わせは次の通りです：\n"
    result += str(best_combination)
    return result, min_price

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        try:
            desired_quantity = int(request.form['desired_quantity'])
            current_quantity = int(request.form['current_quantity'])
            result, min_price = find_min_cost_for_vp(desired_quantity, current_quantity)
        except ValueError:
            result = "有効な数値を入力してください。"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
