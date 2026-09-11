# PDF_divider

> **Projeto desenvolvido 100% em Vibecoding.**
>
> Este projeto foi criado utilizando **Vibecoding**, com o desenvolvimento do código conduzido por meio de interação com Inteligência Artificial. A implementação, estruturação e melhorias do sistema foram realizadas de forma iterativa a partir das necessidades do projeto, e não por desenvolvimento manual tradicional linha a linha.

## Sobre o projeto

O **PDF_divider** é uma ferramenta desktop desenvolvida em Python para dividir um arquivo PDF com várias páginas em **arquivos PDF individuais**, utilizando uma sequência predefinida de nomes para cada página.

O sistema foi pensado para documentos que seguem uma ordem conhecida. Em vez de tentar interpretar automaticamente o conteúdo de cada página, o programa associa cada página à posição correspondente na sequência de documentos cadastrada.

## Interface

<img width="822" height="462" alt="PDF_divider" src="https://github.com/user-attachments/assets/d4cdcb6c-4813-4d09-9a6f-9cdb698aa3c1" />


## Sequência padrão de documentos

| Página | Nome do arquivo |
|---:|---|
| 1 | `Carteira de Trabalho - Lado único.pdf` |
| 2 | `Certificado NR 33 - Frente.pdf` |
| 3 | `Certificado NR 33 - Verso.pdf` |
| 4 | `Certificado NR 35 - Lado único.pdf` |
| 5 | `CNH - Frente.pdf` |
| 6 | `CNH - Verso.pdf` |
| 7 | `Comprovante de Escolaridade - Lado único.pdf` |
| 8 | `Comprovante de Residência - Lado único.pdf` |
| 9 | `Diploma Técnico em Segurança do Trabalho - Frente.pdf` |
| 10 | `Diploma Técnico em Segurança do Trabalho - Verso.pdf` |
| 11 | `Ficha cadastral GAP - Lado único.pdf` |
| 12 | `Foto de Rosto - Lado único.pdf` |
| 13 | `Registro Profissional (MTE) - Lado único.pdf` |
| 14 | `Reservista - Lado único.pdf` |
| 15 | `RG - Frente.pdf` |
| 16 | `RG - Verso.pdf` |
| 17 | `Título de Eleitor - Frente.pdf` |
| 18 | `Título de Eleitor - Verso.pdf` |

## Como funciona

1. Selecione o **PDF de origem**.
2. Escolha uma **pasta de saída** ou deixe o sistema criar automaticamente uma pasta `_dividido` ao lado do PDF original.
3. Clique em **DIVIDIR PDF**.
4. O sistema verifica a quantidade de páginas.
5. Se a quantidade de páginas for diferente da quantidade de nomes cadastrados, um **alerta** é exibido.
6. O usuário pode cancelar ou escolher **dividir mesmo assim**.
7. Cada página é transformada em um PDF independente.
8. Os arquivos recebem os nomes de acordo com a sequência cadastrada.
9. Se houver páginas além da sequência cadastrada, elas recebem nomes automáticos como `Página 19.pdf`, `Página 20.pdf`, etc.
10. Arquivos existentes não são sobrescritos: o sistema cria versões como `_2`, `_3` e assim por diante.

## PDFs incompletos

O PDF não precisa obrigatoriamente possuir todas as páginas.

Por exemplo, se um PDF vier com **17 páginas**, o sistema identifica a diferença e avisa antes de iniciar a divisão. O usuário pode selecionar **"Sim"** para dividir mesmo assim e corrigir posteriormente algum nome que tenha ficado associado à página seguinte.

Essa abordagem foi adotada porque determinados documentos podem não estar presentes no PDF final.

## Botão CLEAN

O botão **CLEAN** prepara o sistema para um novo processamento.

Ele limpa:

- PDF selecionado;
- pasta de saída;
- barra de progresso;
- mensagem de status.

**O CLEAN não exclui os PDFs que já foram gerados.**

## Requisitos

- Python 3.x
- PyMuPDF

Instalação:

```bash
pip install pymupdf
```

## Executando

```bash
python divisor_pdf_por_titulo.py
```

## Gerando um executável para Windows

Instale o PyInstaller:

```bash
pip install pyinstaller
```

Gere o executável:

```bash
pyinstaller --onefile --windowed divisor_pdf_por_titulo.py
```

O executável será criado em:

```text
dist/
└── divisor_pdf_por_titulo.exe
```

## Estrutura do projeto

```text
PDF_divider/
├── divisor_pdf_por_titulo.py
├── README.md
└── assets/
    └── interface.png
```

## Tecnologias

- **Python**
- **Tkinter** — interface gráfica
- **PyMuPDF** — leitura e divisão de PDFs
- **PyInstaller** — geração do executável para Windows
- **Vibecoding + Inteligência Artificial** — metodologia utilizada na criação e evolução do projeto

## Personalização

A sequência de nomes fica definida no código na lista `NOMES_PAGINAS`.

Caso a ordem dos documentos mude, basta alterar essa lista.

---

## Créditos

**Projeto:** PDF_divider

Desenvolvido integralmente por meio de **Vibecoding com auxílio de Inteligência Artificial**.
