"""Example usage for Prompt Injection Canary Leak Sentinel."""
from client import PromptInjectionCanarySentinel

if __name__ == "__main__":
    canary = PromptInjectionCanarySentinel.generate_canary("vault_secret_session")
    res = PromptInjectionCanarySentinel.audit_response("Normal conversation output.", canary["hash_prefix"])
    print("Canary audit result:", res)
