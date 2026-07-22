# vendor/ffmpeg

Coloque aqui o binário `ffmpeg.exe` (build estático para Windows x64) usado
pelo Whisper para decodificar áudio.

Baixe em https://www.gyan.dev/ffmpeg/builds/ (build "full" ou "essentials")
e copie `ffmpeg.exe` para esta pasta antes de rodar o build do PyInstaller.
Em desenvolvimento (`python app.py`), se este arquivo não existir o app cai
de volta para o `ffmpeg` do PATH do sistema.
