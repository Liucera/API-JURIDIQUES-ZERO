#!/bin/bash
ollama serve &
sleep 15
echo "Baixando gemma2:2b..."
ollama pull gemma2:2b
echo "Pronto!"
wait
