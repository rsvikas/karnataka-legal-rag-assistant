# Karnataka Legal Research Offline RAG Assistant

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rsvikas/karnataka-legal-rag-assistant/blob/main/karnataka_legal_rag.ipynb)

An offline, hallucination-guarded Legal Research AI Assistant designed to run directly inside **Google Colab** to query Karnataka property laws (KAOA, KAOR, KOFA, RERA, KCSA, TOPA, RDPR, IGR).

---

## 🚀 Quickstart Guide

Click the **Open in Colab** badge above to launch the notebook directly in Google Colab, or run the steps manually below.

### Step 1: Install Ollama & Models
```python
!apt-get update -qq && apt-get install -y zstd
!curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
!pip install faiss-cpu rank_bm25 numpy requests

import subprocess, time
subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

!ollama pull nomic-embed-text
!ollama pull qwen2.5:7b
```

### Step 2: Launch Application
```python
!git clone [https://github.com/rsvikas/karnataka-legal-rag-assistant.git](https://github.com/rsvikas/karnataka-legal-rag-assistant.git)
%cd karnataka-legal-rag-assistant
!python scripts/legal_rag_app.py
```