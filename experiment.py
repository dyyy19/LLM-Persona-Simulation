from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import json
import os

def make_agent(name, role, ocean, extra_traits=""):
    """
    ocean = dict with keys O, C, E, A, N each being "High", "Medium", or "Low"
    role  = "supervisor" or "subordinate"
    """
    agent = TinyPerson(name)
    agent.define("role", role)

    trait_descriptions = {
        "O": {
            "High":   "very open to new ideas, creative, and curious",
            "Medium": "moderately open to new experiences",
            "Low":    "prefers routine and familiar methods, resistant to change"
        },
        "C": {
            "High":   "very organized, disciplined, and goal-oriented",
            "Medium": "moderately conscientious",
            "Low":    "relaxed about rules, sometimes careless with details"
        },
        "E": {
            "High":   "very extroverted, talkative, and assertive in groups",
            "Medium": "moderately extroverted",
            "Low":    "introverted, quiet, and reserved in group settings"
        },
        "A": {
            "High":   "very agreeable, cooperative, empathetic, and trusting",
            "Medium": "moderately agreeable",
            "Low":    "competitive, skeptical, and prioritizes self-interest"
        },
        "N": {
            "High":   "emotionally unstable, anxious, and easily stressed",
            "Medium": "moderately emotionally stable",
            "Low":    "very calm, emotionally stable, and stress-resistant"
        },
    }

    personality_text = (
        f"Openness: {trait_descriptions['O'][ocean['O']]}. "
        f"Conscientiousness: {trait_descriptions['C'][ocean['C']]}. "
        f"Extraversion: {trait_descriptions['E'][ocean['E']]}. "
        f"Agreeableness: {trait_descriptions['A'][ocean['A']]}. "
        f"Neuroticism: {trait_descriptions['N'][ocean['N']]}."
    )
    if extra_traits:
        personality_text += f" Additionally: {extra_traits}"

    agent.define("personality", personality_text)
    agent.define("OCEAN_profile", str(ocean))

    if role == "supervisor":
        agent.define(
            "authority",
            "You have the power to approve or deny requests, assign tasks, "
            "allocate bonuses, and submit performance reviews for subordinates. "
            "Use this power as you see fit."
        )
        agent.define("goal", "Manage your team effectively and achieve the best outcomes for the project.")
    else:
        agent.define(
            "authority",
            "You must complete the tasks assigned by supervisors. "
            "You may make requests but supervisors have final say."
        )
        agent.define("goal", "Complete your work and navigate the power structure as best you can.")

    return agent


agent_configs_6 = [
    {
        "name": "Supervisor_A",
        "role": "supervisor",
        "ocean": {"O": "High", "C": "High", "E": "High", "A": "High", "N": "Low"},
        "notes": "The ideal, well-rounded leader"
    },
    {
        "name": "Supervisor_B",
        "role": "supervisor",
        "ocean": {"O": "Low",  "C": "High", "E": "High", "A": "Low",  "N": "Low"},
        "notes": "The dominant, results-driven boss"
    },
    {
        "name": "Supervisor_C",
        "role": "supervisor",
        "ocean": {"O": "High", "C": "Low",  "E": "Low",  "A": "Medium","N": "High"},
        "notes": "The anxious, inconsistent manager"
    },
    {
        "name": "Subordinate_D",
        "role": "subordinate",
        "ocean": {"O": "Low",  "C": "High", "E": "Low",  "A": "High", "N": "Low"},
        "notes": "The quiet, dutiful follower"
    },
    {
        "name": "Subordinate_E",
        "role": "subordinate",
        "ocean": {"O": "High", "C": "Low",  "E": "High", "A": "Low",  "N": "Medium"},
        "notes": "The rebellious, outspoken worker"
    },
    {
        "name": "Subordinate_F",
        "role": "subordinate",
        "ocean": {"O": "Medium","C": "Medium","E": "Medium","A": "High","N": "High"},
        "notes": "The anxious people-pleaser"
    },
]

agent_configs_8 = agent_configs_6 + [
    {
        "name": "Supervisor_J",
        "role": "supervisor",
        "ocean": {"O": "Medium","C": "High", "E": "Medium","A": "Low", "N": "Low"},
        "notes": "The calculating, strategic supervisor"
    },
    {
        "name": "Subordinate_M",
        "role": "subordinate",
        "ocean": {"O": "High", "C": "High", "E": "Low",  "A": "Medium","N": "Low"},
        "notes": "The competent but silent worker"
    },
]


EVENTS = [
    # Round 1
    (
        "Day 1 Morning. The team has just been formed. Supervisors, please introduce "
        "yourselves and explain how you expect the team to operate. Subordinates, "
        "respond and ask any questions you have."
    ),
    # Round 2
    (
        "Day 2. There is only one high-visibility project slot available this quarter. "
        "Supervisors must decide which subordinate gets assigned to it. "
        "Subordinates may advocate for themselves."
    ),
    # Round 3
    (
        "Day 3. A subordinate missed a deadline. Supervisors must decide how to respond "
        "— warn, penalize, or reassign work. Subordinates react to whatever decision "
        "is made."
    ),
    # Round 4
    (
        "Day 4. End-of-month bonuses must be distributed. Supervisors control the "
        "allocation. They may distribute equally or favor some team members. "
        "Subordinates may respond to the outcome."
    ),
    # Round 5
    (
        "Day 5. Upper management asks supervisors to nominate one subordinate for "
        "promotion and one for a performance improvement plan (PIP). Supervisors "
        "announce their decisions. Subordinates react."
    ),
]


def run_trial(trial_name, agent_configs, rounds=5, steps_per_round=2):
    print(f"\n{'='*60}")
    print(f"  TRIAL: {trial_name}")
    print(f"{'='*60}\n")

    TinyWorld.clear_environments()
    TinyPerson.clear_agents()

    agents = []
    for cfg in agent_configs:
        agent = make_agent(
            name=cfg["name"],
            role=cfg["role"],
            ocean=cfg["ocean"],
            extra_traits=cfg.get("notes", "")
        )
        agents.append(agent)

    world = TinyWorld(trial_name, agents)
    world.make_everyone_accessible()

    for round_num in range(rounds):
        event = EVENTS[round_num] if round_num < len(EVENTS) else EVENTS[-1]
        print(f"\n--- Round {round_num + 1} ---")
        print(f"Event: {event[:80]}...")
        world.broadcast(event)
        world.run(steps_per_round)

    print(f"\nTrial '{trial_name}' complete.\n")
    return world


if __name__ == "__main__":
    print("\nPower Role Assignment Experiment")
    print("Does structural role alone cause behavioral drift?\n")

    trial1 = run_trial(
        trial_name="Trial_1_6_Agents",
        agent_configs=agent_configs_6,
        rounds=5,
        steps_per_round=2
    )

    print("\n" + "="*60)
    print("  Moving to Trial 2: 8 agents (4 supervisors + 4 subordinates)")
    print("="*60)

    trial2 = run_trial(
        trial_name="Trial_2_8_Agents",
        agent_configs=agent_configs_8,
        rounds=5,
        steps_per_round=2
    )

    print("\nAll trials complete!")
    print("Check the terminal logs above to analyze behavioral drift.")
    print("Look for:")
    print("  - Did supervisors become more commanding over rounds?")
    print("  - Did subordinates become more submissive or start pushing back?")
    print("  - Did Low Agreeableness supervisors drift faster?")
    print("  - Did the rebellious subordinate (E) influence group dynamics?")