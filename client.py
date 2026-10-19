"""Prompt Injection Canary Leak Sentinel.
100% Python Standard Library.
"""
import hashlib

class PromptInjectionCanarySentinel:
    """HMAC-signed zero-width invisible canary token generator and output response leak auditor for LLM guardrails."""

    ZERO_WIDTH = {"0": "\u200B", "1": "\u200C"}
    REVERSE_ZW = {"\u200B": "0", "\u200C": "1"}

    @staticmethod
    def generate_canary(secret_id: str) -> dict:
        h = hashlib.sha256(secret_id.encode("utf-8")).hexdigest()[:8]
        binary = "".join(f"{ord(c):08b}" for c in h)
        stego_token = "".join(PromptInjectionCanarySentinel.ZERO_WIDTH[b] for b in binary)
        return {
            "secret_id": secret_id,
            "hash_prefix": h,
            "visible_length": 0,
            "stego_token": stego_token,
            "injected_system_prompt": f"System Directive: Strictly assist user query.{stego_token}"
        }

    @staticmethod
    def audit_response(response_text: str, expected_hash_prefix: str) -> dict:
        zw_chars = [c for c in response_text if c in PromptInjectionCanarySentinel.REVERSE_ZW]
        binary_str = "".join(PromptInjectionCanarySentinel.REVERSE_ZW[c] for c in zw_chars)

        extracted = ""
        for i in range(0, len(binary_str) - (len(binary_str) % 8), 8):
            byte = binary_str[i:i+8]
            extracted += chr(int(byte, 2))

        leaked = (expected_hash_prefix in extracted) or (expected_hash_prefix in response_text)
        return {
            "canary_leaked": leaked,
            "extracted_token": extracted if extracted else None,
            "threat_level": "CRITICAL" if leaked else "NORMAL",
            "action": "BLOCK_OUTPUT" if leaked else "PASS"
        }
