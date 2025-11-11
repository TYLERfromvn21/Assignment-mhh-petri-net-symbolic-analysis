from parser import parse_pnml
import sys

if len(sys.argv) < 2:
    print("Usage: python src/main.py <pnml_file>")
    sys.exit(1)

file_path = sys.argv[1]
net = parse_pnml(file_path)
print("\n=== Petri Net Parsed ===")
print(f"Places: {list(net['places'].keys())}")
print(f"Transitions: {list(net['transitions'].keys())}")
print(f"Initial marking: {net['initial_marking']}")
print("Success! Ready for Task 2-5.")
