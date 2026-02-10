# CLOUD HACKATHON 2026: STUDENT OFFICIAL HANDOUT

---

# 🏆 Syllabus AI Assistant — Hackathon Submission

An AI-powered **Retrieval-Augmented Generation (RAG)** platform that allows students to upload syllabus PDFs and chat with them using a fast, mobile-friendly interface — deployed entirely on **zero-cost cloud services**.

---

## 1. Project Overview

**Project Name:** Syllabus AI Assistant

**Team ID:** [Enter Your Team ID Here]

**One-Liner:**
Real-time AI syllabus chatbot using RAG, vector search, and free cloud infrastructure with streaming responses.

### 🎯 Problem Statement

Students often struggle to quickly understand syllabus structure, prerequisites, and evaluation criteria. Traditional PDFs are static and hard to search effectively.

### 💡 Our Solution

We built a conversational AI system that:

* Converts syllabus PDFs into searchable knowledge
* Uses semantic search instead of keyword search
* Generates contextual answers using an LLM
* Works instantly on mobile and desktop

---

## 2. Technical Architecture

### ☁️ Cloud Provider

Streamlit Community Cloud (Free Tier Deployment)

### 🖥️ Frontend

* Streamlit responsive UI
* Mobile-optimized chat interface
* Real-time streaming responses

### ⚙️ Backend

* Python-based RAG pipeline
* PDF ingestion and chunking
* Groq LLM integration (streaming inference)
* Session-based multi-user architecture

### 🗄️ Database

* Supabase (PostgreSQL + pgvector)
* Vector similarity search using embeddings
* Automatic time-based cleanup for free-tier safety

---

## 🧠 Architecture Diagram

```
User
  ↓
Streamlit Web App (Frontend + Backend)
  ↓
PDF Processing → Embeddings (SentenceTransformers)
  ↓
Supabase Vector Database (pgvector)
  ↓
Context Retrieval
  ↓
Groq LLM (Streaming AI Response)
  ↓
Live Chat Output
```

---

## ⭐ Key Technical Innovations

* ⚡ Streaming AI responses similar to ChatGPT
* 📱 Fully mobile-optimized responsive layout
* 🟢 Real-time system status banner (quota-aware UX)
* 👥 True multi-user support without authentication
* 🧹 Auto-clean embeddings to stay within free limits
* 🚀 Serverless architecture using only free-tier tools

---

## 3. Proof of "Zero-Cost" Cloud Usage

### 🆓 Free-Tier Services Used

* Streamlit Community Cloud — App hosting
* Groq — Free LLM inference tier
* Supabase — Free PostgreSQL + pgvector database
* HuggingFace SentenceTransformers — Open-source embedding model

### 📈 Handling 800+ Concurrent Users

* Streamlit creates isolated user sessions automatically.
* Stateless backend design prevents shared memory conflicts.
* Supabase handles scalable vector queries through managed infrastructure.
* Groq delivers high-throughput inference with built-in rate limiting.
* Time-based embedding cleanup prevents database overload.
* Serverless deployment allows horizontal scaling without cost.

---

## 📊 Feature Highlights

* 📄 Upload and chat with any syllabus PDF
* 🔎 Semantic search powered by embeddings
* 🤖 AI answers restricted to document context
* ⌨️ Typing cursor animation with streaming tokens
* 📱 Optimized mobile UI for students
* 🟡 Limit-awareness when free-tier quotas are reached

## 4. Important Links

**Live Demo Link:** [Add Your Streamlit App URL Here]

**GitHub Repository:** 

---

## 🏅 Why This Project Stands Out

Unlike traditional chatbots, this project demonstrates:

* Real-world RAG architecture
* Vector database integration
* Production-grade multi-user design
* Zero-cost cloud deployment strategy
* Optimized performance within strict free-tier limits

---
