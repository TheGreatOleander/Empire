# Refiner's Fire: Recursive AI Council

A free, local-first tool for multi-agent AI debates on complex topics (coding, ethics, politics, religion). It runs a council of archetypal personas (Engineer, Mystic, Humanist, Skeptic, Historian, Child) that iteratively refine their views over a set duration, producing a detailed report of consensus, divergences, and unresolved questions.

## Features
- **Dual-Prompt System**: Separate prompts for council members and arbiter to ensure diverse, independent responses and meaningful synthesis.
- **Time-Based Iteration**: Runs for N hours, stopping early if consensus is reached.
- **Archetypal Diversity**: Six personas with distinct reasoning styles.
- **Final Report**: Markdown output with consensus points, divergent views, synthesized insights, and unresolved questions.
- **Free and Local**: Uses mock LLM responses; extensible to local models (Ollama) or free APIs (OpenRouter).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RefinersFire.git
   cd RefinersFire
