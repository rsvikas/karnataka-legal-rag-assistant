# Karnataka Legal Research Offline RAG Assistant (Google Colab)

An offline, hallucination-guarded Legal Research AI Assistant designed to run directly inside **Google Colab** to query Karnataka property laws (KAOA, KAOR, KOFA, RERA, KCSA, TOPA, RDPR, IGR).

---

## 🚀 Quickstart Guide (For New Users)

### Step 1: Install Ollama & Download Models
Run this in a Google Colab code cell:

```python
# Install dependencies & Ollama
!apt-get update -qq && apt-get install -y zstd
!curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
!pip install faiss-cpu rank_bm25 numpy requests

# Start Ollama background service
import subprocess, time
subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

# Pull required AI models
!ollama pull nomic-embed-text
!ollama pull qwen2.5:7b
```

---

### Step 2: Clone Repository & Run Application
Run this in a second code cell:

```python
# Clone repository and navigate to folder
!git clone [https://github.com/rsvikas/karnataka-legal-rag-assistant.git](https://github.com/rsvikas/karnataka-legal-rag-assistant.git)
%cd karnataka-legal-rag-assistant

# Launch legal assistant (Index files download automatically)
!python scripts/legal_rag_app.py
```

---

## 📂 Repository Structure

- `scripts/legal_rag_app.py`: Interactive RAG script with automatic release index downloader.
- `requirements.txt`: Required Python dependencies.
- `README.md`: Setup instructions.
- `.gitignore`: Excludes binary files and index directories.

---

## ⚖️ Supported Acts Covered

- **KAOA**: Karnataka Apartment Ownership Act, 1972
- **KAOR**: Karnataka Apartment Ownership Rules, 1975
- **KOFA**: Karnataka Ownership Flats Act, 1972
- **RERA**: Real Estate (Regulation and Development) Act
- **KCSA**: Karnataka Co-operative Societies Act
- **TOPA**: Transfer of Property Act