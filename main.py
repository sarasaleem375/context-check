"""Context Check v1: will this document fit in an AI model, and what will it cost?"""
import json
import sys

import requests


CHARS_PER_TOKEN = 4  # rule of thumb for English text
PRICE_PER_MILLION_TOKENS = 3.00  # illustrative USD rate per 1M input tokens

CONTEXT_TIERS = {
    "Small (8K)": 8_000,
    "Standard (128K)": 128_000,
    "Large (200K)": 200_000,
    "Extra-large (1M)": 1_000_000,
}


def estimate_tokens(text):
    """Roughly estimate how many tokens an AI model would see in this text."""
    return max(1, round(len(text) / CHARS_PER_TOKEN))


def estimate_cost(tokens):
    """Estimated input cost in US dollars at the illustrative rate."""
    return tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS


def check_tiers(tokens):
    """Return a dict of tier name -> True/False (does the text fit?)."""
    results = {}
    for name, limit in CONTEXT_TIERS.items():
        results[name] = tokens <= limit
    return results


def load_text(source):
    """Load text file from a web address (http/https) or from a local file."""
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=10)
        response.raise_for_status()     # truns 4xx / 5xx
        return response.text    
    with open(source, "r", encoding="utf-8") as file:
        return file.read()


def build_report(source, text):
    """Collec everything we know about the document in one dictionary."""
    tokens = estimate_tokens(text)
    return {
        "source": source,
        "characters": len(text),
        "words": len(text.split()),
        "estimated_tokens": tokens,
        "estimated_cost_usd": round(estimate_cost(tokens), 4),
        "fits": check_tiers(tokens),
    }


def save_report(report, path="report.json"):
    """Write the report to a JSOn file  that other programs can read"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def main():
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = input("File or web address to check: ").strip()
    
    try:
        text = load_text(source)
    except FileNotFoundError:
        print(f"Could not find {source}. Check the name and the folder you are in.")
        return
    except UnicodeDecodeError:
        print(f"{source} doesn't look like a plain text file.")
        return
    except requests.exceptions.RequestException as error:
        print(f"Could not download {source}")
        print(f"Reason: {error}")
        return
    if not text.strip():
        print(f"{source} is empty. There is nothing to check.")
        return

    report = build_report(source, text)

    print(f"Characters: {report['characters']:,}")
    print(f"Words: {report['words']:,}")
    print(f"Estimated tokens: {report['estimated_tokens']:,}")
    print(f"Estimated cost: ${report['estimated_cost_usd']:.4f}")
    for tier, fits in report["fits"].items():
        if fits:
            print(f"  {tier}: fits")
        else:
            print(f"  {tier}: TOO BIG")
    save_report(report)
    print("Saved report.json")

main()
