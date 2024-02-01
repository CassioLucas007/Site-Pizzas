from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, send_from_directory

import pandas as pd

app = Flask(__name__)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Definindo o nome da planilha Excel onde os pedidos serão salvos
excel_file = r'C:\Users\cassio.lucas.DOMINIO\OneDrive\Cássio Lucas - Pessoal\Cássio\Projeto Pedidos Pizzas Centro\pedidos.xlsx'

# Rota principal para exibir o formulário de pedido
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Coletando os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        quantidade = request.form['quantidade']
        valorapagar = request.form['valor']
        pago = request.form.get('pago', 'Não')
        entregue = request.form.get('entregue', 'Não')
        responsavel = request.form['responsavel']
        
        # Carregando os pedidos existentes se o arquivo existir
        if excel_exists():
            df = pd.read_excel(excel_file)
        else:
            df = pd.DataFrame(columns=['Nome Completo', 'Endereço', 'Número da Casa', 'Complemento', 'Quantidade','Valor Total', 'Pago?', 'Entregue?','Responsável'])

        # Adicionando uma nova linha com os dados do formulário
        new_entry = pd.DataFrame({
            'Nome Completo': [nome],
            'Endereço': [endereco],
            'Número da Casa': [numero],
            'Complemento': [complemento],
            'Quantidade': [quantidade],
            'Pago?': [pago],
            'Entregue?': [entregue],
            'Responsável':[responsavel],
            'Valor Total':[valorapagar]

        })

        # Anexando os dados ao final do DataFrame
        df = pd.concat([df, new_entry], ignore_index=True)

        # Escrevendo os dados de volta para o arquivo Excel
        df.to_excel(excel_file, index=False)

        return redirect(url_for('index'))

    return render_template('index.html')

# Rota para exibir os pedidos existentes e permitir a edição e exclusão
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    if request.method == 'POST':
        # Verifica se a ação é de exclusão
        if request.form.get('action') == 'excluir':
            # Excluindo a entrada selecionada
            indice = int(request.form['indice'])
            df = pd.read_excel(excel_file)
            df = df.drop(index=indice)
            df.to_excel(excel_file, index=False)

    # Carregando os pedidos existentes
    pedidos = pd.read_excel(excel_file) if excel_exists() else None
    return render_template('pedidos.html', pedidos=pedidos)

# Rota para edição de pedido
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def pedido(index):
    # Carregar os dados do arquivo Excel
    if excel_exists():
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=['Nome Completo', 'Endereço', 'Número da Casa', 'Complemento', 'Quantidade','Valor Total', 'Pago?','Entregue?','Responsável'])

    # Se o método for POST, processar os dados do formulário
    if request.method == 'POST':
        # Obter os dados do formulário
        responsavel = request.form['responsavel']
        nome = request.form['nome']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        quantidade = request.form['quantidade']
        valorapagar = request.form['valor']
        pago = request.form.get('pago', 'Não')  # Se não for enviado, assume "Não" por padrão
        entregue = request.form.get('entregue', 'Não')
        

        # Atualizar os dados do pedido no DataFrame
        if index < len(df):
            df.at[index, 'Responsável'] = responsavel
            df.at[index, 'Nome Completo'] = nome
            df.at[index, 'Endereço'] = endereco
            df.at[index, 'Número da Casa'] = int(numero)
            df.at[index, 'Complemento'] = complemento
            df.at[index, 'Quantidade'] = int(quantidade)
            df.at[index, 'Valor Total'] = float(valorapagar)
            df.at[index, 'Pago?'] = pago
            df.at[index, 'Entregue?'] = entregue
            

            

            # Escrever os dados de volta para o arquivo Excel
            df.to_excel(excel_file, index=False)

            # Redirecionar para a página de pedidos ou exibir uma mensagem de sucesso
            return redirect(url_for('pedidos'))
        else:
            return 'Pedido não encontrado'

    # Se o método for GET, renderizar o formulário com os dados do pedido
    if index < len(df):
        pedido = df.iloc[index]
        return render_template('editar.html', pedido=pedido, index=index)
    else:
        return 'Pedido não encontrado'

# Função auxiliar para verificar se o arquivo Excel já existe
def excel_exists():
    try:
        pd.read_excel(excel_file)
        return True
    except FileNotFoundError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Exemplo de configuração para ouvir em todas as interfaces



