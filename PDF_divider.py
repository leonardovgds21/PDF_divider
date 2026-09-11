import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


# ============================================================
# ORDEM FIXA DE NOMES
# A primeira página recebe o primeiro nome, a segunda o segundo,
# e assim por diante.
# ============================================================

NOMES_PAGINAS = [
    "Carteira de Trabalho - Lado único",
    "Certificado NR 33 - Frente",
    "Certificado NR 33 - Verso",
    "Certificado NR 35 - Lado único",
    "CNH - Frente",
    "CNH - Verso",
    "Comprovante de Escolaridade - Lado único",
    "Comprovante de Residência - Lado único",
    "Diploma Técnico em Segurança do Trabalho - Frente",
    "Diploma Técnico em Segurança do Trabalho - Verso",
    "Ficha cadastral GAP - Lado único",
    "Foto de Rosto - Lado único",
    "Registro Profissional (MTE) - Lado único",
    "Reservista - Lado único",
    "RG - Frente",
    "RG - Verso",
    "Título de Eleitor - Frente",
    "Título de Eleitor - Verso",
]


def nome_unico(pasta, nome):
    """Evita sobrescrever arquivos existentes."""
    caminho = os.path.join(pasta, nome + ".pdf")
    contador = 2

    while os.path.exists(caminho):
        caminho = os.path.join(pasta, f"{nome}_{contador}.pdf")
        contador += 1

    return caminho


def dividir_pdf(arquivo, pasta_saida, status_var, barra):
    if fitz is None:
        raise RuntimeError(
            "A biblioteca PyMuPDF não está instalada.\n\n"
            "No CMD, execute:\n"
            "pip install pymupdf"
        )

    doc = fitz.open(arquivo)
    total = len(doc)

    if total == 0:
        doc.close()
        raise RuntimeError("O PDF não possui páginas.")

    for i in range(total):
        if i < len(NOMES_PAGINAS):
            nome = NOMES_PAGINAS[i]
        else:
            nome = f"Página {i + 1}"

        caminho = nome_unico(pasta_saida, nome)

        # Cria um novo PDF contendo somente a página atual.
        novo = fitz.open()
        novo.insert_pdf(doc, from_page=i, to_page=i)
        novo.save(caminho)
        novo.close()

        progresso = int((i + 1) / total * 100)
        barra["value"] = progresso
        status_var.set(
            f"Página {i + 1} de {total}  |  {nome}.pdf"
        )
        janela.update_idletasks()

    doc.close()


def selecionar_pdf():
    arquivo = filedialog.askopenfilename(
        title="Selecione o PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if arquivo:
        entrada_var.set(arquivo)
        status_var.set("PDF selecionado. Pronto para dividir.")


def selecionar_pasta():
    pasta = filedialog.askdirectory(
        title="Escolha a pasta de saída"
    )

    if pasta:
        saida_var.set(pasta)
        status_var.set("Pasta de saída selecionada.")


def limpar():
    """
    Limpa a seleção do PDF, pasta de saída, barra e status.
    Não apaga os PDFs que já foram gerados.
    """
    entrada_var.set("")
    saida_var.set("")
    barra["value"] = 0
    status_var.set("Tudo limpo. Selecione um novo PDF.")


def executar():
    arquivo = entrada_var.get().strip()
    pasta = saida_var.get().strip()

    if not arquivo:
        messagebox.showwarning(
            "Atenção",
            "Selecione o PDF que deseja dividir."
        )
        return

    if not os.path.isfile(arquivo):
        messagebox.showerror(
            "Erro",
            "O arquivo PDF selecionado não existe."
        )
        return

    # Verifica quantas páginas o PDF possui antes de dividir
    if fitz is None:
        messagebox.showerror(
            "Erro",
            "A biblioteca PyMuPDF não está instalada.\n\n"
            "No CMD, execute:\n"
            "pip install pymupdf"
        )
        return

    try:
        doc_temp = fitz.open(arquivo)
        total_paginas = len(doc_temp)
        doc_temp.close()
    except Exception as e:
        messagebox.showerror(
            "Erro",
            f"Não foi possível abrir o PDF:\n\n{e}"
        )
        return

    quantidade_nomes = len(NOMES_PAGINAS)

    # --------------------------------------------------------
    # PDF COM MENOS PÁGINAS QUE A SEQUÊNCIA
    # --------------------------------------------------------
    if total_paginas < quantidade_nomes:

        resposta = messagebox.askyesno(
            "Quantidade de páginas diferente",
            f"O PDF selecionado possui {total_paginas} páginas.\n\n"
            f"A sequência cadastrada possui {quantidade_nomes} nomes.\n\n"
            f"Isso significa que pelo menos um documento ficará "
            f"com um nome diferente do esperado.\n\n"
            f"Você poderá corrigir os nomes manualmente depois.\n\n"
            f"Deseja dividir mesmo assim?"
        )

        if not resposta:
            status_var.set(
                "Divisão cancelada. Nenhum arquivo foi criado."
            )
            return

    # --------------------------------------------------------
    # PDF COM MAIS PÁGINAS QUE A SEQUÊNCIA
    # --------------------------------------------------------
    elif total_paginas > quantidade_nomes:

        resposta = messagebox.askyesno(
            "Quantidade de páginas diferente",
            f"O PDF selecionado possui {total_paginas} páginas.\n\n"
            f"A sequência cadastrada possui apenas "
            f"{quantidade_nomes} nomes.\n\n"
            f"As páginas que ultrapassarem a sequência receberão "
            f"nomes automáticos como 'Página 19', 'Página 20', etc.\n\n"
            f"Deseja dividir mesmo assim?"
        )

        if not resposta:
            status_var.set(
                "Divisão cancelada. Nenhum arquivo foi criado."
            )
            return

    # Se não escolher uma pasta, cria automaticamente
    # uma pasta "_dividido" ao lado do PDF original.
    if not pasta:
        pasta = os.path.splitext(arquivo)[0] + "_dividido"
        saida_var.set(pasta)

    os.makedirs(pasta, exist_ok=True)

    botao_dividir.config(state="disabled")
    botao_limpar.config(state="disabled")
    barra["value"] = 0
    status_var.set("Iniciando divisão...")
    janela.update_idletasks()

    try:
        dividir_pdf(
            arquivo,
            pasta,
            status_var,
            barra
        )

        messagebox.showinfo(
            "Concluído",
            f"PDF dividido com sucesso!\n\n"
            f"{total_paginas} arquivos foram criados em:\n"
            f"{pasta}"
        )

        status_var.set(
            f"Concluído! {total_paginas} PDFs criados."
        )

    except Exception as e:
        messagebox.showerror(
            "Erro",
            str(e)
        )

        status_var.set(
            "Não foi possível concluir a divisão."
        )

        barra["value"] = 0

    finally:
        botao_dividir.config(state="normal")
        botao_limpar.config(state="normal")


# ============================================================
# INTERFACE
# ============================================================

janela = tk.Tk()
janela.title("Divisor de PDF - Documentos")
janela.geometry("820x430")
janela.minsize(820, 430)
janela.resizable(False, False)

entrada_var = tk.StringVar()
saida_var = tk.StringVar()
status_var = tk.StringVar(
    value="Selecione um PDF para começar."
)

frame = ttk.Frame(janela, padding=22)
frame.pack(fill="both", expand=True)

ttk.Label(
    frame,
    text="Divisor de PDF",
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", pady=(0, 5))

ttk.Label(
    frame,
    text=(
        "Divide o PDF página por página usando a sequência "
        "fixa de nomes cadastrada."
    )
).pack(anchor="w", pady=(0, 18))


# PDF de entrada
linha1 = ttk.Frame(frame)
linha1.pack(fill="x", pady=5)

ttk.Label(
    linha1,
    text="PDF de origem:",
    width=17
).pack(side="left")

ttk.Entry(
    linha1,
    textvariable=entrada_var
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)

ttk.Button(
    linha1,
    text="Selecionar...",
    command=selecionar_pdf
).pack(side="right")


# Pasta de saída
linha2 = ttk.Frame(frame)
linha2.pack(fill="x", pady=5)

ttk.Label(
    linha2,
    text="Pasta de saída:",
    width=17
).pack(side="left")

ttk.Entry(
    linha2,
    textvariable=saida_var
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)

ttk.Button(
    linha2,
    text="Escolher...",
    command=selecionar_pasta
).pack(side="right")


# Informação da sequência
info = ttk.LabelFrame(
    frame,
    text="Sequência de documentos"
)
info.pack(
    fill="x",
    pady=(18, 10)
)

ttk.Label(
    info,
    text=(
        "1. Carteira de Trabalho   →   2. Certificado NR 33 Frente   →   "
        "3. NR 33 Verso   →   ...   →   18. Título de Eleitor Verso"
    )
).pack(
    padx=12,
    pady=10
)


# Barra de progresso
barra = ttk.Progressbar(
    frame,
    mode="determinate",
    maximum=100
)
barra.pack(
    fill="x",
    pady=(10, 5)
)

ttk.Label(
    frame,
    textvariable=status_var
).pack(
    anchor="w",
    pady=5
)


# Botões
botoes = ttk.Frame(frame)
botoes.pack(
    pady=15
)

botao_dividir = ttk.Button(
    botoes,
    text="DIVIDIR PDF",
    command=executar
)
botao_dividir.pack(
    side="left",
    ipadx=25,
    ipady=7,
    padx=8
)

botao_limpar = ttk.Button(
    botoes,
    text="CLEAN",
    command=limpar
)
botao_limpar.pack(
    side="left",
    ipadx=25,
    ipady=7,
    padx=8
)

janela.mainloop()
