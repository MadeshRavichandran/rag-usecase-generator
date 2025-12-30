def has_sufficient_evidence(results, threshold=0.2):
    valid = [r["score"] for r in results if r["score"] > 0.1]
    if not valid:
        return False
    avg_score = sum(valid) / len(valid)
    return avg_score >= threshold
