FROM ollama/ollama

# Inicie o servidor em background, espere, puxe o modelo e mate o processo
RUN ollama serve & sleep 20 && ollama pull orieg/gemma3-tools:1b && pkill ollama

EXPOSE 11434

ENTRYPOINT ["/usr/bin/ollama", "serve"]