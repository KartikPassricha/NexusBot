# NexusBot

NexusBot is a feature-rich Discord bot built using **Python** and the **Discord API**, integrating moderation tools, interactive games, music functionality, and AI-powered text generation features.

---

## Overview

NexusBot was designed to enhance Discord server experiences through automation, entertainment, and intelligent interactions. The bot combines traditional moderation utilities with AI-based text generation and dynamic command handling.

It follows a modular architecture using Discord cogs for scalability and maintainability.

---

## Key Features

### Moderation System
- Role-based command access
- Server moderation utilities
- Automated command handling

### Interactive Games
- Truth & Dare command system
- Dynamic prompt generation
- Context-aware responses

### Music Functionality
- Integrated with YouTube API
- Dynamic music retrieval
- Stream-based playback support

### AI/ML Integration
- Implemented probabilistic text generation using **Markov chains**
- Built using Python’s **Markovify**
- Trained custom dataset for dynamic content generation
- Model training script included (`train_model_t&d.py`)

---

## Tech Stack

- **Language:** Python
- **Library:** discord.py
- **AI/ML:** Markovify (Markov Chain Text Generation)
- **APIs:** Discord API, YouTube API
- **Architecture:** Modular (Cogs-based)
- **Frontend:**
  - HTML
  - CSS
  - JavaScript

---

## Project Structure

```text
NexusBot/
│
├── cogs/                   
├── data/                   
├── dataset/               
├── models/                 
│
├── main.py                 
├── Nexus.py                
├── train_model_t&d.py     
│
├── index.html            
├── style.css
├── script.js
│
└── README.md
```

---

## Installation & Setup

```bash
git clone https://github.com/KartikPassricha/NexusBot.git
cd NexusBot
python -m venv venv
venv\Scripts\activate   # Windows
