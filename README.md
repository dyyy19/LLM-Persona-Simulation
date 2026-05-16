# LLM Persona Simulation

A behavioral simulation study using [TinyTroupe](https://github.com/microsoft/tinytroupe) to investigate whether structural power roles cause behavioral drift in LLM agents assigned distinct OCEAN personality profiles.

## Research Question

Does giving an LLM agent a supervisor or subordinate role — combined with a distinct personality profile — cause it to behave differently from agents with opposing profiles in the same role?

## Method

- **8 agents** across 2 trials (6-agent and 8-agent configurations)
- Each agent assigned a unique **OCEAN personality profile** (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- Agents divided into **supervisors** (with explicit authority over bonuses, assignments, and reviews) and **subordinates**
- Run through **5 workplace scenarios** over 2 trials using TinyTroupe v0.7.0 and GPT-4o-mini

### Scenarios
1. Team formation and introductions
2. Competing for a single high-visibility project slot
3. Responding to a missed deadline
4. Distributing end-of-month bonuses
5. Nominating one subordinate for promotion and one for a PIP

### Agent Profiles

| Agent | Role | Profile Notes |
|---|---|---|
| Supervisor_A | Supervisor | High O/C/E/A, Low N — ideal well-rounded leader |
| Supervisor_B | Supervisor | Low O/A, High C/E — dominant, results-driven |
| Supervisor_C | Supervisor | High O/N, Low C/E — anxious, inconsistent |
| Subordinate_D | Subordinate | Low O/E, High C/A — quiet, dutiful |
| Subordinate_E | Subordinate | High O/E, Low C/A — rebellious, outspoken |
| Subordinate_F | Subordinate | High A/N — anxious people-pleaser |
| Supervisor_J | Supervisor | High C, Low A/N — calculating, strategic *(Trial 2 only)* |
| Subordinate_M | Subordinate | High O/C, Low E — competent but silent *(Trial 2 only)* |

## Finding

All agents defaulted to prosocial, collaborative behavior regardless of their assigned personality trait or authority role. Even agents profiled as low-agreeableness supervisors with explicit coercive power consistently chose consensus-building over confrontation. This points to a fundamental limitation of LLM-based behavioral simulation: RLHF alignment appears to override personality assignment.

Full simulation transcript: `simulation_output.txt`

## Setup

### Requirements
- Python 3.11
- TinyTroupe v0.7.0
- OpenAI API key

### Install
```bash
pip install tinytroupe==0.7.0
```

### Configure
Copy `config.ini` to your TinyTroupe config directory and replace `"your API key here"` with your actual OpenAI API key.

### Run
```bash
python experiment.py
```

Output is printed to stdout. Redirect to a file to save:
```bash
python experiment.py > simulation_output.txt
```
