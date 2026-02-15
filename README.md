# Tech Challenge -- Fase 4

## Sistema Multimodal para Detecção de Risco em Procedimentos Ginecológicos

------------------------------------------------------------------------

## 1. Visão Geral

Este projeto implementa um sistema multimodal de análise clínica capaz
de identificar situações de risco durante procedimentos ginecológicos,
combinando:

-   Visão computacional (detecção de sangramento em vídeo)
-   Processamento de áudio (análise de fala da paciente)
-   Fusão multimodal para classificação de risco
-   Integração com Azure Cognitive Services
-   Armazenamento seguro em Azure Blob Storage

O objetivo é simular um sistema de suporte à decisão clínica capaz de
detectar precocemente sinais de complicação, como hemorragia pós-parto
associada a sofrimento relatado pela paciente.

------------------------------------------------------------------------

## 2. Arquitetura

Arquitetura final do sistema:

Pipeline local (Python) ├── Módulo de vídeo (YOLO) ├── Módulo de áudio
(SpeechRecognition) ├── Fusão multimodal └── Cliente HTTP

        ↓ POST (JSON minimizado)

Azure Function (HTTP Trigger) ├── Azure AI Language (Healthcare
Entities) └── Azure Blob Storage (container privado "alerts")

O pipeline local executa a inferência e envia apenas um resumo
estruturado do alerta para a nuvem. Nenhum vídeo ou áudio bruto é
transmitido.

------------------------------------------------------------------------

## 3. Estrutura do Projeto

### Projeto principal (pipeline local)

tech-challenge-fase4/ │ ├── video/ ├── audio/ ├── fusion/ ├──
azure_integration/ ├── main.py ├── requirements.txt └── README.md

### Projeto Azure Function (separado)

ingest-alert-func/ │ ├── function_app.py ├── host.json ├──
requirements.txt └── local.settings.json

------------------------------------------------------------------------

## 4. Instalação -- Projeto Principal

### Criar ambiente virtual

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependências

``` bash
pip install -r requirements.txt
```

Bibliotecas principais:

-   opencv-python
-   ultralytics
-   torch
-   speechrecognition
-   moviepy
-   requests

------------------------------------------------------------------------

## 5. Configuração de Variáveis de Ambiente

``` bash
export VIDEO_INPUT="data/videos/pph_simulation_clip.mp4"
export VIDEO_MODEL="caminho/para/best.pt"
export VIDEO_CONF="0.35"
export AZURE_FUNCTION_URL="https://<app>.azurewebsites.net/api/ingest_alert?code=..."
```

------------------------------------------------------------------------

## 6. Execução

``` bash
python main.py
```

Saída esperada:

-   Número de eventos de vídeo
-   Número de eventos de áudio
-   Resultado da fusão multimodal
-   Resposta da Azure Function
-   Confirmação de upload no Blob Storage

------------------------------------------------------------------------

## 7. Fusão Multimodal

Exemplo de saída:

``` json
{
  "risk_level": "high",
  "reasons": ["bleeding", "patient_distress"],
  "action": "notify_medical_team"
}
```

------------------------------------------------------------------------

## 8. Integração com Azure

### Azure Function

-   Recebe alerta estruturado via HTTP
-   Enriquecimento com Azure AI Language
-   Persistência em Azure Blob Storage

### Azure AI Language

-   Extração de entidades clínicas
-   Identificação de relações médicas

### Azure Blob Storage

Container privado:

alerts

Formato dos arquivos:

alert_YYYYMMDDTHHMMSSZ.json

------------------------------------------------------------------------

## 9. Segurança e Privacidade

-   Não envio de mídia bruta
-   Transmissão apenas de resumo estruturado
-   Autenticação via Function Key
-   Armazenamento privado no Blob
-   Segredos via variáveis de ambiente

------------------------------------------------------------------------

## 10. Objetivo Acadêmico

Este projeto demonstra:

-   Aplicação prática de IA multimodal
-   Integração com serviços gerenciados em nuvem
-   Arquitetura distribuída baseada em microserviço
