import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos PDF",
        filetypes=[("PDF arquivos", "*.pdf")]
    )
    if arquivos:
        lista_de_arquivos.set(arquivos)
        update_lista_pdfs(arquivos)

def update_lista_pdfs(arquivos):
    try:
        pdf_grid_lista.delete(0, tk.END)
        for pdf in arquivos:
            pdf_grid_lista.insert(tk.END, os.path.basename(pdf))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar arquivos PDF: {e}")

def salvar_arquivo():
    arquivo = filedialog.asksaveasfilename(
        title="Salvar PDF mesclado",
        defaultextension=".pdf",
        filetypes=[("PDF arquivos", "*.pdf")]
    )
    if arquivo:
        saida_path.set(arquivo)

def juntar_pdfs():
    arquivos = lista_de_arquivos.get()
    if not arquivos:
        messagebox.showerror("Erro", "Por favor, selecione os arquivos PDF.")
        return

    saida_arquivo = saida_path.get()
    if not saida_arquivo:
        messagebox.showerror("Erro", "Por favor, selecione o local para salvar o PDF final.")
        return

    try:
        merger = PyPDF2.PdfMerger()
        for file in arquivos:
            merger.append(file)

        merger.write(saida_arquivo)
        merger.close()

        messagebox.showinfo("Sucesso", f"PDF mesclado salvo em: {saida_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao mesclar PDFs: {e}")

# Configuração da janela principal
root = ThemedTk(theme="equilux")  # Define o tema escuro
root.title("Mesclador de PDFs")
root.geometry("400x500")
root.configure(bg="#2B2B2B")  # Fundo principal mais escuro

# Variáveis
lista_de_arquivos = tk.Variable()
saida_path = tk.StringVar()

# dark mode
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2B2B2B")
style.configure("TLabel", background="#2B2B2B", foreground="#E0E0E0", font=("Helvetica", 11))
style.configure("TButton", padding=6, relief="flat", background="#4A90E2", foreground="white", font=("Helvetica", 10))
style.map("TButton", background=[("active", "#377BB5")])
style.configure("TEntry", fieldbackground="#3E3E3E", foreground="#FFFFFF")

# Layout principal
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(1, weight=1)

# Mensagem header
ttk.Label(frame, text="Bem-vindo ao Merge_PDF!", font=("Helvetica", 14, "bold"), foreground="#4A90E2").grid(row=0, column=0, columnspan=3, pady=(0, 5))
ttk.Label(frame, text="Uma ferramenta simples e eficiente para unir arquivos PDF.", font=("Helvetica", 9), foreground="#FFFFFF").grid(row=1, column=0, columnspan=3, pady=(0, 10))

# Selecionar arquivos
ttk.Label(frame, text="Arquivos PDF:").grid(row=2, column=0, sticky=tk.W)
btn_browse_files = ttk.Button(frame, text="Procurar", command=selecionar_arquivos)
btn_browse_files.grid(row=2, column=1, sticky=tk.W)

# Lista de PDFs selecionados
ttk.Label(frame, text="Arquivos selecionados:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
pdf_grid_lista = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=15, bg="#3E3E3E", fg="#E0E0E0", selectbackground="#4A90E2", selectforeground="#FFFFFF", highlightthickness=0, font=("Helvetica", 10))
pdf_grid_lista.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

# Local de saída
ttk.Label(frame, text="Salvar como:").grid(row=5, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
entry_output = ttk.Entry(frame, textvariable=saida_path)
entry_output.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
btn_save_as = ttk.Button(frame, text="Procurar", command=salvar_arquivo)
btn_save_as.grid(row=5, column=2, sticky=tk.E)

# Botão para mesclar PDFs
btn_merge = ttk.Button(frame, text="Mesclar PDFs", command=juntar_pdfs)
btn_merge.grid(row=6, column=0, columnspan=3, pady=20)

# Rodapé
ttk.Label(root, text="Desenvolvido com Python e Tkinter", background="#2B2B2B", foreground="#888888", anchor="center", font=("Helvetica", 9)).grid(row=1, column=0, pady=(10, 0))

# Inicializar a interface
root.mainloop()
