import re
import json
import sys
from pathlib import Path

def parse_markdown(md_text):
    # Patterns for sections, choices, and rewards
    section_pat = re.compile(r'^##\s+(.+?)\s*\(([\w_]+)\)', re.MULTILINE)
    choice_pat = re.compile(r'- \[(.+?)\] *(?:→|->|→) *([\w_]+)(?: *\(REWARD: *([\w_]+)\))?', re.IGNORECASE)
    reward_pat = re.compile(r'\(REWARD: *([\w_]+)\)', re.IGNORECASE)
    flag_pat = re.compile(r'\(FLAG: *([\w_]+)\)', re.IGNORECASE)
    terminal_pat = re.compile(r'Terminal:\s*True', re.IGNORECASE)

    # Find all sections
    sections = [(m.start(), m.end(), m.group(1).strip(), m.group(2).strip()) for m in section_pat.finditer(md_text)]
    nodes = {}
    for idx, (start, end, title, node_id) in enumerate(sections):
        node_start = end
        node_end = sections[idx+1][0] if idx+1 < len(sections) else len(md_text)
        node_text = md_text[node_start:node_end].strip()

        # Prompt: first quoted or first paragraph
        prompt_match = re.search(r'["“](.+?)["”]', node_text, re.DOTALL)
        prompt = prompt_match.group(1).strip() if prompt_match else node_text.split('\n')[0].strip()

        # Choices
        choices = []
        for m in choice_pat.finditer(node_text):
            choice = {"text": m.group(1).strip()}
            if m.group(3):
                choice["reward"] = m.group(3).strip()
            choice["next_node"] = m.group(2).strip()
            choices.append(choice)

        # If no choices, treat as terminal/leaf node
        if not choices:
            # Try to find reward and outcome text
            reward = reward_pat.search(node_text)
            flag = flag_pat.search(node_text)
            terminal = bool(terminal_pat.search(node_text))
            outcome_text = node_text.strip()
            leaf = {"text": "END", "outcome_text": outcome_text}
            if reward:
                leaf["reward"] = reward.group(1)
            if flag:
                leaf["flag"] = flag.group(1)
            nodes[node_id] = {"prompt": prompt, "choices": [leaf]}
        else:
            nodes[node_id] = {"prompt": prompt, "choices": choices}

    return nodes

def build_room_json(md_path, room_name="Blue Room", description=None, completion_flag=None, exits=None):
    md_text = Path(md_path).read_text(encoding="utf-8")
    nodes = parse_markdown(md_text)
    # Use first section as description if not provided
    if not description:
        description = next(iter(nodes.values()))["prompt"]
    if not completion_flag:
        completion_flag = f"{room_name.lower().replace(' ', '_')}_complete"
    if not exits:
        exits = {"return": "hub"}
    return {
        "type": "story",
        "name": room_name,
        "description": description,
        "completion_flag": completion_flag,
        "story_nodes": nodes,
        "exits": exits
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python md_to_json.py <input_markdown.md> <output.json>")
        sys.exit(1)
    md_path, out_path = sys.argv[1], sys.argv[2]
    room_json = build_room_json(md_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(room_json, f, indent=4, ensure_ascii=False)
    print(f"Converted {md_path} to {out_path}")