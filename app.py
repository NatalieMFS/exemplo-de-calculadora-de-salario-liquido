"""Criar uma aplicação Flask com formulário de entrada de dados do salário
bruto e número de dependentes. A aplicação deve calcular e exibir o salário líquido com base
nas seguintes regras:
• O INSS será descontado com uma alíquota fixa de 8% sobre o salário bruto.
• O Imposto de Renda (IR) deve ser descontado apenas se o salário bruto for superior a
R$ 2.500,00, com uma alíquota de 15% sobre o valor total.
Público3
• Para cada dependente informado, será concedido um desconto fixo de R$ 200,00, que
será adicionado ao salário líquido (ou seja, representa uma dedução da base de
descontos).
• O resultado final deve ser exibido como salário líquido, isto é: salário bruto menos o
valor do INSS menos o valor do IR (se aplicável) mais o valor referente aos
dependentes.
• A aplicação deve tratar casos de erro, como:
o Salário negativo
o Número de dependentes negativo
o Entradas não numéricas""" #para lembrar o que a aplicação deve fazer


from flask import Flask, render_template, request

app = Flask(__name__)

VALOR_DEPENDENTE = 200  # dedução por dependente (ajuste se o enunciado pedir outro valor)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/resultado', methods=['POST'])
def resultado():
    try:
        salario = float(request.form['salario'].strip().replace(',', '.'))
        dependentes = int(request.form['dependentes'])
    except (ValueError, KeyError):
        return "Erro: insira valores numéricos válidos.", 400

    if salario < 0 or dependentes < 0:
        return "Erro: os valores não podem ser negativos.", 400

    # 1) INSS: 8% do salário bruto
    inss = salario * 0.08

    # 2) Dedução dos dependentes (reduz a base do IR)
    deducao_dependentes = dependentes * VALOR_DEPENDENTE

    # 3) IR: 15% se o salário bruto for maior que R$ 2.500
    if salario > 2500:
        base_ir = max(salario - inss - deducao_dependentes, 0)
        ir = base_ir * 0.15
    else:
        ir = 0

    # 4) Salário líquido
    salario_liquido = salario - inss - ir

    return f"""
    <h1>Resultado do cálculo</h1>
    <h2>Salário líquido: R$ {salario_liquido:.2f}</h2>
    <a href="/">Voltar</a>
    """


if __name__ == '__main__':
    app.run(debug=True)