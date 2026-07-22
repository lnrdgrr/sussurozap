# SussuroZap

Transcritor de áudio local usando o [Whisper](https://github.com/openai/whisper)
da OpenAI (modelo rodando 100% na máquina, sem enviar áudio pra nuvem).

- Interface desktop nativa (pywebview) com **drag-and-drop** de arquivos
- Formatos aceitos: `.ogg`, `.mp3`, `.aiff` / `.aif`
- Histórico de transcrições em SQLite, agrupado por dia
- Instalador Windows standalone (não exige Python, ffmpeg nem Whisper
  pré-instalados na máquina de destino)

## Download

Não precisa instalar nada antes: baixe o instalador pronto na página de
releases e rode.

**[⬇ Baixar SussuroZap-Setup.exe (última versão)](https://github.com/lnrdgrr/sussurozap/releases/latest/download/SussuroZap-Setup.exe)**

## Dependências

Para **rodar a partir do código-fonte** (não se aplica a quem só usa o
`SussuroZap-Setup.exe` já gerado, que é standalone):

| Dependência | Versão usada | Observação |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.11.x | PyTorch/Whisper ainda não suportam Python 3.12+ na prática |
| [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) | 8.1 (full build) | Precisa estar no PATH do sistema em modo dev, ou vendorizado em `vendor/ffmpeg/` |
| [openai-whisper](https://pypi.org/project/openai-whisper/) | 20250625 | Motor de transcrição (instalado via `requirements.txt`) |
| [pywebview](https://pypi.org/project/pywebview/) | 6.2.1 | Janela desktop nativa (instalado via `requirements.txt`) |
| torch | 2.13.0 | Dependência transitiva do whisper — pacote grande (~600MB), puxado automaticamente |
| numpy | 2.4.6 | Dependência transitiva |
| tiktoken | 0.13.0 | Dependência transitiva (tokenizer do whisper) |
| numba | 0.66.0 | Dependência transitiva |

As dependências Python inteiras estão em `requirements.txt` — `torch`,
`numpy`, `tiktoken`, `numba` etc. são instaladas automaticamente como
dependências do `openai-whisper`, não precisam ser listadas à parte no
`pip install`.

Para **gerar o instalador** (`.exe`), some a isso:

| Ferramenta | Uso |
|---|---|
| [PyInstaller](https://pyinstaller.org) | Empacota o app + Python + dependências num bundle standalone |
| [Inno Setup](https://jrsoftware.org/isinfo.php) 6.x | Compila o bundle num instalador `.exe` com atalhos e desinstalador |

## Estrutura

```
app.py             janela pywebview + ponte JS <-> Python
transcriber.py      motor de transcrição (Whisper local)
history_db.py       histórico em SQLite, agrupado por dia
paths.py            resolução de caminhos (dev vs. build empacotado)
ui/                 interface (HTML/CSS/JS)
vendor/             ffmpeg.exe e modelo Whisper embutidos no build final
installer.iss       script do instalador (Inno Setup)
```

## Rodando a partir do código-fonte

Requer Python 3.11 (PyTorch/Whisper ainda não suportam versões mais novas)
e [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) no PATH.

```bash
py -3.11 -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python app.py
```

## Gerando o instalador Windows

1. Baixe `ffmpeg.exe` para `vendor/ffmpeg/` e o modelo Whisper `base.pt`
   para `vendor/models/` (veja o README de cada pasta).
2. Instale o [PyInstaller](https://pyinstaller.org) no venv:
   `pip install pyinstaller`
3. Gere o bundle:

   ```bash
   pyinstaller --noconfirm --windowed --name SussuroZap ^
     --add-data "ui;ui" ^
     --add-data "venv/Lib/site-packages/whisper/assets;whisper/assets" ^
     --add-data "vendor/ffmpeg;vendor/ffmpeg" ^
     --add-data "vendor/models;vendor/models" ^
     --collect-all torch ^
     --collect-all whisper ^
     --collect-all webview ^
     --collect-all clr_loader ^
     --collect-all pythonnet ^
     app.py
   ```

4. Instale o [Inno Setup](https://jrsoftware.org/isinfo.php) e compile:

   ```bash
   ISCC.exe installer.iss
   ```

   O instalador final fica em `installer_output/SussuroZap-Setup.exe`.

## Notas

- O histórico de transcrições (`data/history.db`) é local e não é versionado.
- `ffmpeg.exe` e o modelo Whisper não são versionados no repositório (são
  binários grandes); veja `vendor/ffmpeg/README.md` e `vendor/models/README.md`
  para obtê-los.
