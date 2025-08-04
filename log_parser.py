import re
import json
from pathlib import Path

def parse_log_line(line):
    pattern = re.compile(
        r"\[(\d+ns)\]\s+(ERROR|WARNING|INFO):\s+\[(.*?)\]?\s*(.*?)(?:\s+in\s+(.*?)\.sv\s+line\s+(\d+))?$"
    )
    match = pattern.match(line.strip())
    if match:
        timestamp, level, module, message, file, line_no = match.groups()
        return {
            "timestamp": timestamp,
            "level": level,
            "module": module or "unknown",
            "message": message.strip(),
            "file": file + ".sv" if file else "unknown",
            "line": int(line_no) if line_no else None
        }
    return None

def parse_log_file(log_path):
    results = []
    with open(log_path, "r") as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                results.append(parsed)
    return results

if __name__ == "__main__":
    input_path = Path("logs/sample_log_1.txt")  # ✅ CORRECTED: looks in 'logs' folder
    output_path = Path("output/parsed_log.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = parse_log_file(input_path)

    with open(output_path, "w") as out_file:
        json.dump(results, out_file, indent=4)

    print(f"[✓] Parsed log written to: {output_path}")
