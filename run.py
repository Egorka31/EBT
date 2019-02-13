from parsing import Parser
from planning_task.task import Task

if __name__ == '__main__':
    with open('domain.pddl', 'r') as domain_file, open('problem.pddl', 'r') as problem_file:
        domain = domain_file.read()
        problem = problem_file.read()
        p = Parser(domain, problem)
        p.parse()
        t = Task.from_parser(p)
        print(t.domain_name)
        print(t.problem_name)
        print(t.objects)
        print(t.predicates)
        print(t.init)
        print(t.goal)
