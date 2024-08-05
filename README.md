# Monitor de Humor

Este é um programa em Python destinado a monitorar o humor dos usuários. O programa permite que os usuários registrem seu humor em diferentes momentos do dia, clicando em emojis que representam seus sentimentos. Após um período de tempo, é possível gerar relatórios que mostram como estava o humor do usuário.

## Funcionalidades

- **Registro de Humor:** Os usuários podem clicar em emojis correspondentes ao seu humor atual.
- **Execução Contínua:** O programa fica em execução contínua, permitindo registros em qualquer momento.
- **Relatórios:** Geração de relatórios diários, semanais ou mensais para análise do humor.

## Requisitos

- Python 3.x
- Bibliotecas:
  - pandas
  - matplotlib
  - seaborn
  - sqlite3
  - tkinter
  - pillow

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd seu-repositorio
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o programa:
   ```bash
   python App.Humor.py
   ```
2. Utilize a interface gráfica para clicar no emoji que representa seu humor atual.
3. Para gerar um relatório, selecione o período desejado (diário, semanal, mensal) e visualize os resultados.

## Gerando Relatórios

Os relatórios podem ser gerados executando a função `generate_report` no script `analysis.py`. Por exemplo:

```python
from analysis import generate_report

generate_report(period='diário')  # ou 'semanal' ou 'mensal'
```

## Estrutura do Projeto

- `App.Humor.py`: Código principal que executa o monitor de humor.
- `analysis.py`: Funções para gerar relatórios baseados nos dados de humor coletados.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.
