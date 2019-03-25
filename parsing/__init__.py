from parsing.domains import domain


def parse_domain(domain_str: str):
    result = domain.parseString(domain_str).asList()
    return result[0]
