# Tech Challenge – Fase 4  
## Sistema Multimodal para Monitoramento Preventivo em Procedimentos Ginecológicos

### Pós-graduação em Inteligência Artificial

---

## Contexto

A integração da Inteligência Artificial aos processos médicos tem ampliado a capacidade de monitoramento, análise e apoio à decisão clínica. No contexto da saúde da mulher, especialmente em procedimentos ginecológicos, há desafios específicos relacionados à identificação precoce de complicações e à garantia da segurança da paciente.

Durante procedimentos clínicos, sinais de risco nem sempre são imediatamente evidentes por meios tradicionais, como sinais vitais. Mudanças sutis no comportamento vocal da paciente ou alterações visuais no procedimento podem indicar situações que demandam atenção imediata da equipe médica.

Este projeto propõe um sistema de monitoramento multimodal que combina **análise de vídeo** e **análise de áudio** para identificar **sinais precoces de risco**, atuando como um mecanismo adicional de apoio à segurança da paciente.

---

## Objetivo do Projeto

Desenvolver um sistema baseado em Inteligência Artificial capaz de:

- Detectar sinais visuais anômalos durante procedimentos ginecológicos  
- Identificar padrões vocais compatíveis com dor aguda ou sofrimento  
- Realizar a fusão multimodal de dados de vídeo e áudio  
- Gerar alertas preventivos para apoio à decisão clínica  
- Utilizar serviços em nuvem para processamento de dados sensíveis  

O sistema **não tem caráter diagnóstico**, atuando como um mecanismo de **monitoramento e alerta**, auxiliando a equipe médica na identificação de situações que merecem atenção imediata.

---

## Arquitetura Geral

O sistema é composto por quatro módulos principais:

Vídeo → Análise Visual (YOLOv8) → Evento Visual
Áudio → Análise Vocal (Speech + Features) → Evento de Áudio
Eventos → Fusão Multimodal → Avaliação de Risco
Avaliação → Geração de Alerta


---

## Análise de Vídeo

- Processamento de vídeos de procedimentos ginecológicos (cenários simulados)
- Utilização de modelo **YOLOv8 customizado**
- Detecção de:
  - Sangramento anômalo durante o procedimento

### Saída do módulo
- Bounding boxes
- Score de confiança
- Registro de evento visual

---

## Análise de Áudio

- Processamento de gravações de voz da paciente (cenários simulados)
- Utilização de **Speech-to-Text** para apoio à análise
- Extração de características acústicas:
  - Intensidade (energia)
  - Pitch
  - Pausas e interrupções
  - Vocalizações não linguísticas

### Objetivo
Identificar **padrões vocais compatíveis com dor aguda**, entendida como um sinal precoce de possível desconforto significativo durante o procedimento.

---

## Fusão Multimodal

A fusão multimodal combina eventos visuais e vocais para aumentar a confiabilidade dos alertas.

### Exemplo de regra:

Se (sangramento anômalo detectado)
E (vocalização compatível com dor)
→ alerta de risco elevado


Essa abordagem reduz falsos positivos e fortalece o caráter preventivo do sistema.

---

## Geração de Alertas

O módulo de alertas:
- Consolida os eventos multimodais
- Classifica o nível de risco
- Registra logs do evento
- Simula a notificação à equipe médica

---

## Uso de Serviços em Nuvem

O projeto utiliza serviços gerenciados em nuvem para ampliar a capacidade de processamento:

- Azure Speech-to-Text
- Azure Storage para armazenamento de vídeos e áudios

O uso de dados simulados respeita princípios éticos e de privacidade, evitando o uso de informações clínicas reais de pacientes.


---

## ⚠️ Considerações Éticas

Devido às restrições éticas e legais relacionadas ao uso de dados clínicos reais, este projeto utiliza **cenários simulados**. As vocalizações e eventos visuais foram construídos com base em características amplamente descritas na literatura médica, com o objetivo de validar o fluxo técnico e a arquitetura proposta.

---

## Próximos Passos

- Treinamento e ajuste fino do modelo YOLOv8
- Implementação completa do pipeline de áudio
- Integração final dos módulos
- Demonstração em vídeo do sistema em funcionamento
