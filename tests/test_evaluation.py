import pytest
from src.evaluation.evaluation_utils import calculate_similarity

def test_exact_match_score():
    inference = {
        "throughput": "1000 requests/second",
        "max_latency": "50ms",
        "security_protocols": ["TLS 1.2", "OAuth2"]
    }
    target = {
        "criteria": {
            "throughput": "1000 requests/second",
            "max_latency": "50ms",
            "security_protocols": ["TLS 1.2", "OAuth2"]
        }
    }
    score = calculate_similarity(inference, target)
    assert score == 1.0, "Expected full match score of 1.0"

def test_partial_match_score():
    inference = {
        "throughput": "900 requests/second",
        "max_latency": "100ms",
        "security_protocols": ["TLS 1.2"]
    }
    target = {
        "criteria": {
            "throughput": "1000 requests/second",
            "max_latency": "50ms",
            "security_protocols": ["TLS 1.2", "OAuth2"]
        }
    }
    score = calculate_similarity(inference, target)
    assert 0 < score < 1.0, "Expected partial score between 0 and 1"

def test_no_match_score():
    inference = {
        "throughput": "100 requests/second",
        "max_latency": "500ms",
        "security_protocols": ["None"]
    }
    target = {
        "criteria": {
            "throughput": "1000 requests/second",
            "max_latency": "50ms",
            "security_protocols": ["TLS 1.2", "OAuth2"]
        }
    }
    score = calculate_similarity(inference, target)
    assert score == 0.0, "Expected score of 0.0 for no match"

def test_empty_input():
    inference = {}
    target = {
        "criteria": {
            "throughput": "1000 requests/second"
        }
    }
    score = calculate_similarity(inference, target)
    assert score == 0.0, "Empty inference should score 0.0"
