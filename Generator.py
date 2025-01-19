import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

# Funções definidas anteriormente
def GenLine(data, Error):
    for y in data.index:
        if data[y] != 0:
            t = random.uniform(-Error, Error)
            data[y] += t
    return data

def GenLine_error(data, Error):
    for y in data.index:
        if data[y] != 0:
            t = random.uniform(0, Error / 10)
            data[y] = t
    return data

def CreateDataframe(N_Obs, Error, df, year_range=(1992, 2016)):
    elementos = list(df.columns)
    elementos_error = [col + ' Error' for col in df.columns]
    elementos_combinados = [item for pair in zip(elementos, elementos_error) for item in pair]
    df_gen = pd.DataFrame(columns=elementos_combinados + ['Year'], index=range(N_Obs))
    for i in range(N_Obs):
        e = random.choice(df.index)
        generated_data = GenLine(df.loc[e, :].copy(), Error)
        df_gen.loc[i, elementos] = generated_data

        df_gen.loc[i, 'Year'] = random.choice(range(*year_range))

        generated_data_error = GenLine_error(df.loc[e, :].copy(), Error)
        df_gen.loc[i, elementos_error] = list(generated_data_error)

        df_gen.loc[i, elementos] = df_gen.loc[i, elementos].div(df_gen.loc[i, elementos].sum(axis=0), axis=0).multiply(100)
    return df_gen

def salvar_df_gen(df_gen):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df_gen.to_excel(file_path, index=False)
        messagebox.showinfo("Sucesso", f"Arquivo salvo em {file_path}")
        root.destroy()  # Fecha a janela principal

# Função para gerar o DataFrame
def gerar_dataframe():
    try:
        N_Obs = int(entry_n_obs.get())
        Error = float(entry_error.get())
        year_start = int(entry_year_start.get())
        year_end = int(entry_year_end.get())

        df_gen = CreateDataframe(N_Obs, Error, df, year_range=(year_start, year_end))
        salvar_df_gen(df_gen)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Gerador de DataFrame")

# Labels e entradas
label_n_obs = tk.Label(root, text="Número de Observações:")
label_n_obs.grid(row=0, column=0, padx=10, pady=5)
entry_n_obs = tk.Entry(root)
entry_n_obs.grid(row=0, column=1, padx=10, pady=5)

label_error = tk.Label(root, text="Erro (Error):")
label_error.grid(row=1, column=0, padx=10, pady=5)
entry_error = tk.Entry(root)
entry_error.grid(row=1, column=1, padx=10, pady=5)

label_year_start = tk.Label(root, text="Ano Inicial:")
label_year_start.grid(row=2, column=0, padx=10, pady=5)
entry_year_start = tk.Entry(root)
entry_year_start.grid(row=2, column=1, padx=10, pady=5)

label_year_end = tk.Label(root, text="Ano Final:")
label_year_end.grid(row=3, column=0, padx=10, pady=5)
entry_year_end = tk.Entry(root)
entry_year_end.grid(row=3, column=1, padx=10, pady=5)

# Botão para gerar o DataFrame
button_generate = tk.Button(root, text="Gerar DataFrame", command=gerar_dataframe)
button_generate.grid(row=4, column=0, columnspan=2, pady=20)

# Executar a interface
def iniciar_interface():
    global df
    df = pd.read_excel('moedas.xlsx', index_col='Moeda')
    root.mainloop()

# Inicialização
iniciar_interface()
