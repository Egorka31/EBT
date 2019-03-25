from parsing import parse_domain
from task import HierarchicalTaskNetwork


if __name__ == '__main__':
    with open('domain.pddl', 'r') as domain_file:
        domain_str = domain_file.read()

        domain = parse_domain(domain_str)
        htn = HierarchicalTaskNetwork(domain)
        htn.construct_tree()

        for action_def in domain.action_defs:
            grounded = htn.ground_action(action_def)
            grounded_str = list(map(str, grounded))
            print(f"Grounding of action '{action_def.action_functor}': {grounded_str}")
