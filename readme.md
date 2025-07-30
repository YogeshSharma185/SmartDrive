# SmartDrive: Where Manual Thrill meets AI Skill 

## Overview
This project is a custom 2D driving game environment with **two modes**:
1. **Manual Mode** – Player controls the car using keyboard inputs.
2. **AI (Reinforcement Learning) Mode** – A trained RL agent drives autonomously.

We built a fully custom OpenAI Gym-compatible environment (without using Gym directly) and trained a **PPO agent for 300K steps** using Stable-Baselines3. The agent is optimized to avoid obstacles, collect coins, and refuel for extended survival.  

The project combines **real-time rendering, AI-based gameplay, and manual interaction** into a single robust system.

---

## Key Features
- **Dual Game Modes**
  - **Manual Mode:** Drive using keyboard controls for acceleration, braking, and steering.
  - **AI Mode:** Watch the RL agent make decisions in real-time.
- **Custom RL Environment:** Built from scratch to be compatible with Stable-Baselines3’s PPO.
- **Reward Design:** Rewards agent for:
  - Avoiding obstacles  
  - Collecting coins  
  - Refueling when necessary  
- **Training:** PPO agent trained for **300,000 steps**, resulting in smooth and optimized gameplay.
---


## Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YogeshSharma185/SmartDrive.git
cd SmartDrive
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv env
source env/bin/activate   # For Windows: env\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
pygame
stable-baselines3
torch
gym
numpy

---

## How to Play

### Manual Mode
```bash
python start.py
```
**Controls:**
- ⬅️ / ➡️: Steering left/right  
- ⬆️: Accelerate  
- ⬇️: Brake  
- `R`: Restart after game over  
- `Q`: Quit the game  


### AI (RL) Mode
```bash
python start.py
```
The PPO-trained agent will take control and navigate the environment autonomously.

---

## Training the Agent
To retrain the agent from scratch:
```bash
python train_agent.py
```
- Uses PPO algorithm from Stable-Baselines3.  
- Trains for **300,000 steps** by default (can be modified in `train_agent.py`).  
- Saves the trained model as `ppo_speak2steer.zip`.
