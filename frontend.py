import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime, date, timedelta
from zipar import compactar
import os
import json
import google_backups

service = google_backups.autenticar()


def tela_envio_avancado():
    def selecionar_pasta():
        caminho = filedialog.askdirectory()
        if caminho:
            entry_caminho.delete(0, tk.END)
            entry_caminho.insert(0, caminho)

    def enviar_agora():
        hoje = date.today()
        nome = hoje.strftime("%d_%m_%Y")
        nome_zip = f'{nome}.zip'
        caminho = entry_caminho.get()
        arquivo_zip = compactar(nome, caminho)
        service = google_backups.autenticar()
        google_backups.criar_pasta_mensal(service, arquivo_zip, nome_zip, id_pasta_pai=None)
        print(f"Envio realizado em {hoje}")

    def programar_envio():
        data = data_envio.get()
        hora = hora_envio.get()
        intervalo = entry_intervalo.get()
        caminho = entry_caminho.get()

        dados = {
            "data": data,
            "hora": hora,
            "intervalo": intervalo,
            "caminho": caminho
        }

        with open("dados.json", "w") as arquivo:
            json.dump(dados, arquivo)

        messagebox.showinfo("Programado", f"Envio programado para {data} às {hora}, a cada {intervalo} dias.")

    def baixar_backup():
        data_usuario = entry_data_backup.get()
        data = data_usuario.replace("/", "_")
        base_nome = data
        destino_pasta = os.path.join(os.getcwd(), "downloads")
        os.makedirs(destino_pasta, exist_ok=True)

        contador = 0

        while True:
            if contador == 0:
                nome_arquivo = f"{base_nome}.zip"
            else:
                nome_arquivo = f"{base_nome}_{contador:02d}.zip"

            file_id = google_backups.buscar_arquivo_por_nome(service, nome_arquivo)
            if not file_id:
                if contador == 0:
                    print("❌ Arquivo principal não encontrado.")
                break

            destino_arquivo = os.path.join(destino_pasta, nome_arquivo)
            google_backups.baixar_arquivo(service, file_id, destino_arquivo)
            contador += 1

    def checagem_automatico():
        try:
            with open("dados.json", "r") as f:
                dados = json.load(f)

            data_str = dados.get("data")
            hora_str = dados.get("hora")
            intervalo_str = dados.get("intervalo", "1")  # padrão 1 dia se vazio

            if not data_str or not hora_str:
                # Dados incompletos, não faz nada
                janela.after(30000, checagem_automatico)  # checa de novo em 30s
                return

            # Converter data e hora do JSON para datetime
            data_envio_dt = datetime.strptime(data_str, "%d/%m/%Y")
            hora_envio_dt = datetime.strptime(hora_str, "%H:%M").time()
            intervalo = int(intervalo_str)

            agora = datetime.now()

            # Combinar data e hora para comparar
            data_hora_envio = datetime.combine(data_envio_dt, hora_envio_dt)

            # Checa se já passou ou bateu a hora programada (dentro do minuto)
            if agora >= data_hora_envio and agora < data_hora_envio + timedelta(minutes=1):
                print("Hora do envio automático! Executando enviar_agora()...")
                enviar_agora()

                # Atualiza a data no JSON somando o intervalo em dias
                nova_data_dt = data_envio_dt + timedelta(days=intervalo)
                nova_data_str = nova_data_dt.strftime("%d/%m/%Y")

                dados["data"] = nova_data_str
                with open("dados.json", "w") as f:
                    json.dump(dados, f)

                # Atualiza o campo da interface também
                data_envio.delete(0, tk.END)
                data_envio.insert(0, nova_data_str)

            # Reagenda a checagem para daqui 30 segundos
            janela.after(30000, checagem_automatico)

        except Exception as e:
            print(f"Erro na checagem automática: {e}")
            janela.after(30000, checagem_automatico)

    # --- Interface e widgets (igual ao código que te passei antes) ---
    # [Aqui vai todo o código para criação da janela, frames, labels, entries, botões, etc.]
    # Para manter o foco, vou colocar só o trecho principal da criação da janela e widgets (aqui você cola seu código completo)

    # Janela principal
    janela = tk.Tk()
    janela.title("Envio Avançado")
    janela.configure(bg="#e6f2ff")
    janela.resizable(False, False)

    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.7)
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    janela.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Topo
    top_frame = tk.Frame(janela, bg="#0052cc", height=int(window_height * 0.2))
    top_frame.pack(fill="x")

    titulo = tk.Label(top_frame, text="Envio de Arquivos", font=("Helvetica", 24, "bold"), fg="white", bg="#0052cc")
    titulo.place(relx=0.5, rely=0.5, anchor="center")

    # Área de conteúdo
    frame_conteudo = tk.Frame(janela, bg="#ffffff", padx=30, pady=30)
    frame_conteudo.place(relx=0.5, rely=0.55, anchor="center")

    # Caminho da Pasta
    tk.Label(frame_conteudo, text="Caminho da Pasta:", bg="white", font=("Helvetica", 12)).grid(row=0, column=0,
                                                                                                sticky="w", pady=5)

    frame_caminho_interno = tk.Frame(frame_conteudo, bg="white")
    frame_caminho_interno.grid(row=0, column=1, columnspan=2, sticky="w", pady=5)

    entry_caminho = tk.Entry(frame_caminho_interno, font=("Helvetica", 12), width=35)
    entry_caminho.pack(side="left", padx=(0, 5))

    btn_buscar = tk.Button(frame_caminho_interno, text="Buscar", command=selecionar_pasta)
    btn_buscar.pack(side="left")

    # Data e Hora
    tk.Label(frame_conteudo, text="Data do Envio (dd/mm/aaaa):", bg="white", font=("Helvetica", 12)).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          pady=5)
    data_envio = tk.Entry(frame_conteudo, font=("Helvetica", 12), width=25)
    data_envio.grid(row=1, column=1, pady=5, sticky="w")

    tk.Label(frame_conteudo, text="Hora do Envio (HH:MM):", bg="white", font=("Helvetica", 12)).grid(row=2, column=0,
                                                                                                     sticky="w", pady=5)
    hora_envio = tk.Entry(frame_conteudo, font=("Helvetica", 12), width=25)
    hora_envio.grid(row=2, column=1, pady=5, sticky="w")

    # Novo campo intervalo
    tk.Label(frame_conteudo, text="De quantos em quantos dias?", bg="white", font=("Helvetica", 12)).grid(row=3,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          pady=5)
    entry_intervalo = tk.Entry(frame_conteudo, font=("Helvetica", 12), width=25)
    entry_intervalo.grid(row=3, column=1, pady=5, sticky="w")

    # Tenta carregar dados iniciais do JSON
    try:
        with open("dados.json", "r") as f:
            valores_iniciais = json.load(f)
            data_envio.insert(0, valores_iniciais.get("data", ""))
            hora_envio.insert(0, valores_iniciais.get("hora", ""))
            entry_intervalo.insert(0, valores_iniciais.get("intervalo", ""))
            entry_caminho.insert(0, valores_iniciais.get("caminho", ""))
    except FileNotFoundError:
        pass

    # Botões
    frame_botoes = tk.Frame(frame_conteudo, bg="white")
    frame_botoes.grid(row=4, column=0, columnspan=3, pady=15)

    btn_enviar = tk.Button(frame_botoes, text="Enviar Agora", bg="#0052cc", fg="white", font=("Helvetica", 11, "bold"),
                           width=15, command=enviar_agora)
    btn_enviar.pack(side="left", padx=10)

    btn_programar = tk.Button(frame_botoes, text="Programar Envio", bg="#1a75ff", fg="white",
                              font=("Helvetica", 11, "bold"),
                              width=15, command=programar_envio)
    btn_programar.pack(side="left", padx=10)

    # Backup
    tk.Label(frame_conteudo, text="Baixar Backup (dd/mm/aaaa):", bg="white", font=("Helvetica", 12)).grid(row=5,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          pady=(20, 5))
    entry_data_backup = tk.Entry(frame_conteudo, font=("Helvetica", 12), width=25)
    entry_data_backup.grid(row=5, column=1, pady=(20, 5), sticky="w")

    btn_backup = tk.Button(frame_conteudo, text="Baixar backup já feito", font=("Helvetica", 11, "bold"), bg="#0066cc",
                           fg="white",
                           width=25, command=baixar_backup)
    btn_backup.grid(row=6, column=0, columnspan=2, pady=10)

    # Rodapé
    rodape = tk.Label(janela, text="© 2025 Felipe da Silva | Portfólio", bg="#e6f2ff", font=("Helvetica", 9))
    rodape.pack(side="bottom", pady=10)

    # Inicia a checagem automática
    janela.after(1000, checagem_automatico)

    janela.mainloop()


if __name__ == '__main__':
    tela_envio_avancado()
