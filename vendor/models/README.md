# vendor/models

Coloque aqui o checkpoint do modelo Whisper `base.pt`, usado para rodar a
transcrição sem precisar baixar nada na primeira execução.

Para gerar o arquivo:

```bash
python -c "import whisper; whisper.load_model('base', download_root='vendor/models')"
```

Em desenvolvimento (`python app.py`), se este arquivo não existir o Whisper
baixa o modelo automaticamente para `~/.cache/whisper` na primeira execução.
