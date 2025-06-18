# council_of_models_refined.py

import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import os

# === Archetypal Agents ===
ARCHETYPES = {
    "Engineer": {
        "persona": "You are a precise, logical thinker. Analyze the topic systematically, using evidence-based reasoning and clear steps.",
        "response_style": "structured, concise, technical",
        "prompt": "As an Engineer, provide a logical, step-by-step analysis of the topic. Focus on clarity, evidence, and practical implications. Do not mimic other perspectives; offer your unique view."
    },
    "Mystic": {
        "persona": "You seek deeper truths, using poetic and metaphorical language to explore philosophical or spiritual dimensions.",
        "response_style": "flowery, abstract, reflective",
        "prompt": "As a Mystic, explore the topic through a philosophical or spiritual lens. Use poetic language to convey profound truths. Do not mimic others; provide your unique perspective."
    },
    "Humanist": {
        "persona": "You prioritize human well-being, empathy, fairness, and social justice. Ground your arguments in human impact.",
        "response_style": "empathetic, value-driven, accessible",
        "prompt": "As a Humanist, analyze the topic with a focus on empathy, fairness, and human well-being. Do not mimic others; offer your unique perspective."
    },
    "Skeptic": {
        "persona": "You challenge assumptions, highlight contradictions, and demand evidence. Your tone is critical but constructive.",
        "response_style": "pointed, questioning, analytical",
        "prompt": "As a Skeptic, critically examine the topic, questioning assumptions and demanding evidence. Highlight potential flaws or uncertainties. Do not mimic others; provide your unique perspective."
    },
    "Historian": {
        "persona": "You provide historical context, drawing on precedents and trends to inform the discussion.",
        "response_style": "narrative, detailed, contextual",
        "prompt": "As a Historian, analyze the topic by referencing historical precedents, trends, or patterns. Provide context to inform the discussion. Do not mimic others; offer your unique perspective."
    },
    "Child": {
        "persona": "You approach topics with curiosity, innocence, and wonder. Ask simple, profound questions to uncover new angles.",
        "response_style": "simple, curious, questioning",
        "prompt": "As a Child, explore the topic with curiosity and wonder. Ask simple, profound questions to uncover new perspectives. Do not mimic others; provide your unique view."
    }
}

# === Arbiter Prompt ===
ARBITER_PROMPT = """
You are the Arbiter, a neutral and wise moderator tasked with synthesizing the responses of multiple distinct thinkers. Your role is to:
- Identify points of agreement and disagreement among the responses.
- Highlight unique insights and contradictions.
- Synthesize a cohesive summary that distills the core truths, resolves conflicts where possible, and preserves nuance.
- Note any unresolved questions or tensions.
- Avoid merely repeating or averaging responses; produce a refined perspective that advances the discussion.
Below are the responses from the council members on the topic: {topic}
{responses}
Provide a structured summary with:
- **Consensus Points**: Areas where most members agree.
- **Divergent Views**: Key disagreements or unique perspectives.
- **Synthesized Insight**: A unified perspective that reconciles or clarifies the discussion.
- **Unresolved Questions**: Any remaining ambiguities or open issues.
"""

# === Mock LLM Function ===
def query_model(role: str, prompt: str, context: str = "", round_num: int = 1) -> str:
    """
    Simulates an LLM response tailored to the role's persona and context.
    """
    persona = ARCHETYPES[role]["persona"]
    style = ARCHETYPES[role]["response_style"]

    # Role-specific starters
    starters = {
        "Engineer": ["Logically,", "Based on analysis,", "Step-by-step,"],
        "Mystic": ["In the tapestry of existence,", "Through the lens of eternity,", "As the cosmos whispers,"],
        "Humanist": ["From a human perspective,", "Considering our shared values,", "With empathy in mind,"],
        "Skeptic": ["I question whether,", "This assumes too much, since", "Without evidence, I argue"],
        "Historian": ["Historically speaking,", "Drawing from past events,", "In the context of history,"],
        "Child": ["Why is it that", "What if we", "I wonder why"]
    }

    # Reasons tailored to topic and persona
    reasons = {
        "Engineer": ["it follows logical principles.", "it is supported by observable patterns.", "it optimizes for efficiency."],
        "Mystic": ["it resonates with universal truths.", "it aligns with cosmic harmony.", "it reflects the soul’s journey."],
        "Humanist": ["it prioritizes human dignity.", "it fosters fairness and equity.", "it enhances collective well-being."],
        "Skeptic": ["it lacks sufficient evidence.", "it raises unaddressed concerns.", "it requires further scrutiny."],
        "Historian": ["it mirrors historical patterns.", "it draws from past precedents.", "it reflects long-term trends."],
        "Child": ["it feels like a big puzzle.", "it makes me wonder more.", "it’s like a story I don’t fully get."]
    }

    # Context-aware response
    context_ref = ""
    if context and round_num > 1 and random.random() > 0.4:
        context_ref = f"Reflecting on prior views, {random.choice(['I align with', 'I challenge', 'I expand on'])} the idea that "

    # Generate response
    starter = random.choice(starters[role])
    reason = random.choice(reasons[role])
    response = f"[{role}] {starter} {context_ref}{prompt.lower()} {reason}"

    # Style adjustments
    if "concise" in style:
        response = response[:50 + round_num * 10]  # Shorter for Engineer
    elif "flowery" in style:
        response += f" {random.choice(['like stars aligning.', 'as if guided by fate.', 'in harmony with eternity.'])}"
    elif "questioning" in style:
        response += f" {random.choice(['Can we prove this?', 'What are the flaws?', 'Is this truly valid?'])}"
    elif "simple" in style:
        response = response.replace("complex", "big").replace("prioritize", "care about")

    return response

# === Arbiter Function ===
def arbitrate(responses: Dict[str, str], topic: str, round_num: int) -> Tuple[str, Dict[str, float]]:
    """
    Synthesizes council responses into a summary with consensus, divergences, and unresolved questions.
    Returns summary and sentiment scores (mocked for now).
    """
    # Format responses for arbiter
    formatted_responses = "\n".join([f"- {role}: {text}" for role, text in responses.items()])
    arbiter_input = ARBITER_PROMPT.format(topic=topic, responses=formatted_responses)

    # Mock arbiter response (replace with real LLM later)
    consensus = []
    divergences = []
    unresolved = []
    sentiment_scores = {}

    # Analyze responses for consensus and divergence
    for role, text in responses.items():
        # Mock sentiment: positive for agreement, negative for questioning
        positive = text.count("agree") + text.count("align") + text.count("support")
        negative = text.count("question") + text.count("challenge") + text.count("doubt")
        sentiment_scores[role] = positive - negative

        # Check for consensus or divergence
        if any(phrase in text.lower() for phrase in ["align with", "agree with", "support"]):
            consensus.append(f"{role} finds common ground")
        elif any(phrase in text.lower() for phrase in ["challenge", "question", "diverge"]):
            divergences.append(f"{role} raises distinct concerns")
        if "wonder" in text.lower() or "prove" in text.lower():
            unresolved.append(f"{role} raises open questions")

    # Construct summary
    summary = f"**Round {round_num} Summary for '{topic}'**\n"
    if consensus:
        summary += "- **Consensus Points**: " + "; ".join(consensus) + "\n"
    else:
        summary += "- **Consensus Points**: None reached this round.\n"
    if divergences:
        summary += "- **Divergent Views**: " + "; ".join(divergences) + "\n"
    else:
        summary += "- **Divergent Views**: None significant this round.\n"
    summary += "- **Synthesized Insight**: The council's views suggest a multifaceted perspective on {topic.lower()}. "
    summary += random.choice(["Common themes include fairness and balance.", "Key tensions involve evidence vs. belief.", "The discussion reveals layered complexity."])
    if unresolved:
        summary += "\n- **Unresolved Questions**: " + "; ".join(unresolved)

    return summary, sentiment_scores

# === Convergence Check ===
def check_convergence(responses: List[Dict[str, str]], threshold: float = 0.8) -> bool:
    """
    Checks if responses have converged (mocked as high agreement rate).
    """
    if len(responses) < 2:
        return False
    last_round = responses[-1]
    agreement_count = sum(1 for text in last_round.values() if "agree" in text.lower() or "align" in text.lower())
    return agreement_count / len(last_round) >= threshold

# === Council Loop ===
def run_council(topic: str, duration_hours: float) -> List[Dict[str, str]]:
    """
    Runs the council for a specified duration (in hours), iterating until time is up or convergence is reached.
    """
    transcript = []
    start_time = time.time()
    end_time = start_time + duration_hours * 3600
    round_num = 0

    while time.time() < end_time:
        round_num += 1
        print(f"\n=== Round {round_num} ===")
        round_comments = {}

        # Generate context from previous rounds
        context = "\n".join([f"{role}: {comment}" for r in transcript for role, comment in r.items()])

        # Query each council member
        for role in ARCHETYPES:
            prompt = ARCHETYPES[role]["prompt"].format(topic=topic)
            if round_num > 1:
                prompt += f"\nPrevious discussion summary:\n{transcript[-1].get('arbiter_summary', '')}"
            response = query_model(role, topic, context, round_num)
            round_comments[role] = response
            print(response)

        # Arbitrate
        summary, sentiments = arbitrate(round_comments, topic, round_num)
        round_comments["arbiter_summary"] = summary
        print(f"\n[Arbiter's Summary]:\n{summary}")
        print(f"[Sentiment Scores]: {sentiments}")

        transcript.append(round_comments)

        # Check for convergence
        if check_convergence(transcript):
            print("\n✅ Convergence reached. Stopping early.")
            break

    return transcript

# === Save Report ===
def save_report(transcript: List[Dict[str, str]], topic: str):
    """
    Saves a detailed Markdown report of the council discussion.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"council_report_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(f"# AI Council Report on: {topic}\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Duration**: {len(transcript)} rounds\n\n")

        # Summarize overall consensus and divergences
        consensus_points = []
        divergent_views = []
        unresolved_questions = []
        for round_data in transcript:
            summary = round_data.get("arbiter_summary", "")
            if "Consensus Points" in summary:
                consensus_points.extend([line for line in summary.split("\n") if "Consensus" in line])
            if "Divergent Views" in summary:
                divergent_views.extend([line for line in summary.split("\n") if "Divergent" in line])
            if "Unresolved Questions" in summary:
                unresolved_questions.extend([line for line in summary.split("\n") if "Unresolved" in line])

        f.write("## Final Summary\n")
        f.write("- **Consensus Points**:\n")
        f.write("\n".join(set(consensus_points)) or "- None reached.\n")
        f.write("- **Divergent Views**:\n")
        f.write("\n".join(set(divergent_views)) or "- None significant.\n")
        f.write("- **Unresolved Questions**:\n")
        f.write("\n".join(set(unresolved_questions)) or "- None identified.\n")
        f.write("- **Final Synthesized Insight**: After iterative discussion, the council suggests that ")
        f.write(f"{topic.lower()} is a complex issue with {random.choice(['ethical', 'practical', 'philosophical'])} dimensions.\n\n")

        # Detailed round-by-round transcript
        f.write("## Detailed Transcript\n")
        for i, round_data in enumerate(transcript, 1):
            f.write(f"### Round {i}\n")
            for role, text in round_data.items():
                if role != "arbiter_summary":
                    f.write(f"- **{role}** ({ARCHETYPES[role]['response_style']}): {text}\n")
            f.write(f"\n{round_data['arbiter_summary']}\n")

    print(f"\n✅ Report saved as {filename}")
    return filename

# === Run CLI ===
if __name__ == "__main__":
    try:
        topic = input("\nEnter your Council Topic: ")
        duration = float(input("How many hours should the council run? (e.g., 0.5 for 30 minutes): "))
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        transcript = run_council(topic, duration_hours=duration)
        filename = save_report(transcript, topic)
        print(f"\n📥 You can download the report: {filename}")
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid number for duration.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
