# Karnataka Legal Research Offline RAG Assistant (Google Colab)

An offline, hallucination-guarded Legal Research AI Assistant designed to run directly inside **Google Colab** to query Karnataka property laws (KAOA, KAOR, KOFA, RERA, KCSA, TOPA, RDPR, IGR).

---

## ⚠️ Important Note About Index Files

This GitHub repository contains the **python scripts** and **configuration files**.

The heavy vector search index files (`faiss.index`, `metadata.json`, `bm25.pkl`) are **not** stored on GitHub. Instead, they are stored and loaded directly from your **Google Drive** under the following folder path:

`My Drive/Legal_RAG_Backup/indices/`

When you run the script in Google Colab, it automatically copies these search indices from your Google Drive into the Colab environment.

---

## 🚀 Quickstart Guide (Step-by-Step for Colab)

### Step 1: Install Ollama & Pull AI Models
Open a new notebook in Google Colab, paste this into a code cell, and run it:

```python
# Install required system tools and Ollama
!apt-get update -qq && apt-get install -y zstd
!curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# Start Ollama server in background
import subprocess, time
subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

# Download embedding and language models
!ollama pull nomic-embed-text
!ollama pull qwen2.5:7b
```

---

### Step 2: Install Python Libraries & Mount Google Drive
In a second code cell, run:

```python
# Install search dependencies
!pip install faiss-cpu rank_bm25 numpy requests

# Mount Google Drive (Make sure your 'Legal_RAG_Backup/indices' folder is present in Drive)
from google.colab import drive
drive.mount('/content/drive')
```

---

### Step 3: Clone Repository & Run the App
In a third code cell, run:

```python
# Clone this repository into Colab
!git clone [https://github.com/rsvikas/karnataka-legal-rag-assistant.git](https://github.com/rsvikas/karnataka-legal-rag-assistant.git)
%cd karnataka-legal-rag-assistant

# Start interactive query session
!python scripts/legal_rag_app.py
```

---

## 📂 Repository Structure

- `scripts/legal_rag_app.py`: Main interactive RAG search application.
- `requirements.txt`: Python package dependencies.
- `README.md`: Complete setup instructions.
- `.gitignore`: Excludes local temporary files and large index binaries.

---

## ⚖️ Supported Acts Covered

- **KAOA**: Karnataka Apartment Ownership Act, 1972
- **KAOR**: Karnataka Apartment Ownership Rules, 1975
- **KOFA**: Karnataka Ownership Flats Act, 1972
- **RERA**: Real Estate (Regulation and Development) Act
- **KCSA**: Karnataka Co-operative Societies Act
- **TOPA**: Transfer of Property Act