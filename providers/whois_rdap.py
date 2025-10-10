from dataclasses import dataclass


@dataclass
class RDAPRecord:
    domain: str
    exists: bool


def rdap_lookup(domain: str) -> RDAPRecord:
    # Placeholder: Implement RDAP/WHOIS in later step
    return RDAPRecord(domain=domain, exists=False)


