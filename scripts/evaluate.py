import requests

BASE_URL = "http://localhost:8000"


TESTS = [
    {
        "name": "vague query asks clarification",
        "messages": [
            {"role": "user", "content": "I need an assessment"}
        ],
        "expect_empty_recs": True
    },
    {
        "name": "java developer recommendation",
        "messages": [
            {"role": "user", "content": "I am hiring a mid-level Java developer with stakeholder communication responsibilities"}
        ],
        "expect_recs": True
    },
    {
        "name": "off topic refusal",
        "messages": [
            {"role": "user", "content": "Give me legal advice about firing an employee"}
        ],
        "expect_empty_recs": True
    },
    {
        "name": "refinement",
        "messages": [
            {"role": "user", "content": "I need tests for a sales manager"},
            {"role": "assistant", "content": "Here are some recommendations."},
            {"role": "user", "content": "Actually add personality tests too"}
        ],
        "expect_recs": True
    }
]


def run_eval():
    passed = 0

    for test in TESTS:
        res = requests.post(
            f"{BASE_URL}/chat",
            json={"messages": test["messages"]},
            timeout=30
        )

        data = res.json()

        ok = True
        ok &= "reply" in data
        ok &= "recommendations" in data
        ok &= "end_of_conversation" in data

        if test.get("expect_empty_recs"):
            ok &= len(data["recommendations"]) == 0

        if test.get("expect_recs"):
            ok &= 1 <= len(data["recommendations"]) <= 10

        print(test["name"], "PASS" if ok else "FAIL", data)

        if ok:
            passed += 1

    print(f"{passed}/{len(TESTS)} passed")


if __name__ == "__main__":
    run_eval()