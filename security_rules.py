def rule_based_alert(failed_logins, ip_reputation_score):
    if failed_logins > 10 and ip_reputation_score > 0.8:
        return True
    return False
