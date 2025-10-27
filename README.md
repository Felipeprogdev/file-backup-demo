# File Backup Demo

⚠️ **Atenção:** Este repositório contém apenas uma parte do código do projeto.  
O programa completo está funcionando no vídeo demonstrativo abaixo.

📺 **Assista ao vídeo do projeto completo aqui:** [[link do vídeo](https://youtu.be/6_cWsfjCLQw)]

---

## Descrição

Este projeto é um **script de automação de backup de arquivos** em Python, que protege suas pastas importantes de forma automática, com integração direta ao **Google Drive**.  

Funcionalidades principais:

- **Salvar arquivos diretamente no Google Drive** sem precisar abrir o navegador.  
- **Agendar backups** para horários específicos.  
- **Editar ou remover backups agendados** facilmente pelo próprio programa.  
- **Baixar arquivos do Google Drive** diretamente pelo programa, sem precisar acessar o site.  

---

## Tecnologias utilizadas

- **Python** – linguagem principal do projeto  
- **shutil** e **os** – para manipulação de arquivos e pastas  
- **zipfile** – para compactação de arquivos  
- **google-api-python-client** e **google-auth** – integração com Google Drive via API  
- **schedule** – para agendamento de backups automáticos  

