import sys
import subprocess

# Auto-install missing dependencies if faiss is not present
try:
    import faiss
except ImportError:
    print("📦 Missing dependencies detected. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu", "rank_bm25", "numpy", "requests", "-q"])
    import faiss

import os
import time
import json
import pickle
import numpy as np
import requests
import re
import shutil

# --- INDEX RESOLUTION LOGIC ---
INDEX_DIR = './indices'
DRIVE_BACKUP = '/content/drive/MyDrive/Legal_RAG_Backup/indices'
RELEASE_URL = 'https://github.com/rsvikas/karnataka-legal-rag-assistant/releases/download/v1.0.0/indices.zip'

if not os.path.exists(INDEX_DIR):
    if os.path.exists(DRIVE_BACKUP):
        print('✅ Restoring vector indices from Google Drive...')
        shutil.copytree(DRIVE_BACKUP, INDEX_DIR, dirs_exist_ok=True)
    else:
        print('📥 Downloading vector indices from GitHub Release (v1.0.0)...')
        r = requests.get(RELEASE_URL, stream=True)
        if r.status_code == 200:
            with open('indices.zip', 'wb') as f:
                f.write(r.content)
            subprocess.run(['unzip', '-q', '-o', 'indices.zip'], check=True)
            print('✅ Indices downloaded and extracted successfully!')
        else:
            raise FileNotFoundError(
                "❌ Could not download indices.zip from GitHub Release. "
                "Ensure v1.0.0 release is published."
            )
else:
    print('✅ Local vector indices detected.')

FAISS_INDEX = f'{INDEX_DIR}/faiss.index'
META_FILE = f'{INDEX_DIR}/metadata.json'
BM25_FILE = f'{INDEX_DIR}/bm25.pkl'

OLLAMA_EMBED_URL = 'http://localhost:11434/api/embeddings'
OLLAMA_CHAT_URL = 'http://localhost:11434/api/generate'

EMBED_MODEL = 'nomic-embed-text'
CHAT_MODEL = 'qwen2.5:7b'

ACRONYMS = {
    'kaoa': 'Karnataka Apartment Ownership Act',
    'kaor': 'Karnataka Apartment Ownership Rules',
    'kofa': 'Karnataka Ownership Flats Act',
    'rera': 'Real Estate Regulatory Authority',
    'kcsa': 'Karnataka Co-operative Societies Act',
    'topa': 'Transfer of Property Act',
    'rdpr': 'Rural Development and Panchayat Raj',
    'igr': 'Inspector General of Registration'
}

def expand_query(query):
    expanded = query
    for acronym, full_name in ACRONYMS.items():
        expanded = re.sub(rf'\b{acronym}\b', full_name, expanded, flags=re.IGNORECASE)
    return expanded

def embed_query(text):
    r = requests.post(OLLAMA_EMBED_URL, json={'model': EMBED_MODEL, 'prompt': text}, timeout=60)
    r.raise_for_status()
    return np.array(r.json()['embedding'], dtype='float32').reshape(1, -1)

def hybrid_search(query, index, meta, bm25, top_k=3):
    query_vec = embed_query(query)
    _, faiss_ids = index.search(query_vec, top_k)
    faiss_results = [meta[i] for i in faiss_ids[0]]

    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_top_indices = np.argsort(bm25_scores)[::-1][:top_k]
    bm25_results = [meta[i] for i in bm25_top_indices]

    combined = {}
    for item in faiss_results + bm25_results:
        combined[item['chunk_id']] = item['text']
    return list(combined.values())[:5]

def ask_llm(context, question):
    prompt = f'''
Role: You are a strict Legal AI Assistant.
Objective: Answer the question ONLY using the provided legal text.
If the answer is not explicitly stated in the text, reply EXACTLY: "Not found in provided documents."
When answering, explicitly cite the Source (Act name) provided in the text.

----------------------------------------
LEGAL TEXT:
{context}

----------------------------------------
QUESTION:
{question}

ANSWER:
'''
    r = requests.post(OLLAMA_CHAT_URL, json={'model': CHAT_MODEL, 'prompt': prompt, 'stream': False, 'options': {'temperature': 0.0}}, timeout=120)
    r.raise_for_status()
    return r.json()['response'].strip()

print('Loading Hybrid Index (FAISS + BM25)...')
index = faiss.read_index(FAISS_INDEX)
with open(META_FILE, 'r', encoding='utf-8') as f:
    meta = json.load(f)
with open(BM25_FILE, 'rb') as f:
    bm25 = pickle.load(f)

print('✅ Robust Legal RAG ready!')
last_question = ''

while True:
    raw_question = input('\nAsk a legal question: ').strip()
    if raw_question.lower() == 'exit' or not raw_question:
        print('Exiting...')
        break
    if len(raw_question.split()) < 4 and last_question:
        question_to_use = f'{last_question} under {raw_question}'
    else:
        question_to_use = raw_question
        last_question = raw_question
    question = expand_query(question_to_use)
    contexts = hybrid_search(question, index, meta, bm25)
    combined_context = '\n\n---\n\n'.join(contexts)
    answer = ask_llm(combined_context, question)
    print('\n================ ANSWER ================\n')
    print(answer)
    print('\n========================================\n')
