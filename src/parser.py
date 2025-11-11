import lxml.etree as ET
import sys
import networkx as nx

def parse_pnml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}
        
        net = root.find('pnml:net', ns)
        if net is None:
            raise ValueError("No <net> found")
        
        places, transitions, arcs = {}, {}, []
        id_set = set()

        for place in net.iterfind('.//pnml:place', ns):
            pid = place.get('id')
            if pid in id_set: raise ValueError(f"Duplicate id: {pid}")
            id_set.add(pid)
            marking = int(place.find('pnml:initialMarking/pnml:text', ns).text or 0) if place.find('pnml:initialMarking', ns) is not None else 0
            if marking > 1: raise ValueError(f"Not 1-safe: {pid} has {marking} tokens")
            places[pid] = {'initial': marking}

        for trans in net.iterfind('.//pnml:transition', ns):
            tid = trans.get('id')
            if tid in id_set: raise ValueError(f"Duplicate id: {tid}")
            id_set.add(tid)
            transitions[tid] = {}

        for arc in net.iterfind('.//pnml:arc', ns):
            aid = arc.get('id')
            source, target = arc.get('source'), arc.get('target')
            if source not in id_set or target not in id_set:
                raise ValueError(f"Missing node in arc {aid}")
            weight = int(arc.find('pnml:inscription/pnml:text', ns).text or 1) if arc.find('pnml:inscription', ns) is not None else 1
            arcs.append((source, target, weight))

        G = nx.DiGraph()
        for p in places: G.add_node(p, type='place', marking=places[p]['initial'])
        for t in transitions: G.add_node(t, type='transition')
        for s, t, w in arcs: G.add_edge(s, t, weight=w)

        return {
            'places': places,
            'transitions': transitions,
            'arcs': arcs,
            'graph': G,
            'initial_marking': {p: places[p]['initial'] for p in places}
        }
    except Exception as e:
        raise ValueError(f"Parse error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/parser.py <pnml_file>")
        sys.exit(1)
    net = parse_pnml(sys.argv[1])
    print("Parsed successfully!")
    print(f"Places: {list(net['places'].keys())}")
    print(f"Transitions: {list(net['transitions'].keys())}")
    print(f"Initial marking: {net['initial_marking']}")