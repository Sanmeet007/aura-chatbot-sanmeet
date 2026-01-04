import json
from .farm_context import farm_ctx_builder
from .symptom_detector import SymptomDetector
from .llm import llm


class DiagnosticRuleEngine:
    def __init__(self, rules_path: str):
        with open(rules_path, "r") as f:
            self.rules = json.load(f)["diagnostic_rules"]

    def _condition_met(self, condition, value, threshold):
        if condition == "below_min":
            return value < threshold
        if condition == "above_max":
            return value > threshold
        if condition == "outside_range":
            return value < threshold["min"] or value > threshold["max"]
        return False

    def evaluate(self, crop: str, symptom: str, sensors: dict) -> list[dict]:
        crop_rules = self.rules.get(crop, {})
        issue_rules = crop_rules.get("issues", {}).get(symptom, {})
        checks = issue_rules.get("diagnostic_checks", [])

        findings = []

        for check in checks:
            param = check["parameter"]
            value = sensors.get(param)

            if value is None:
                continue

            condition = check["condition"]
            threshold = check["threshold"]

            if self._condition_met(condition, value, threshold):
                findings.append(
                    {
                        "parameter": param,
                        "value": value,
                        "severity": check["severity"],
                        "cause": check["cause"],
                        "explanation": check["explanation"],
                        "impact": check["impact"],
                        "action": check["action"],
                        "recovery_time": check["recovery_time"],
                    }
                )

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        findings.sort(key=lambda x: severity_order.get(x["severity"], 99))

        return findings[:3]


def format_rule_diagnosis(findings: list[dict]) -> str:
    if not findings:
        return "No critical issues detected by diagnostic rules."

    text = "RULE-BASED DIAGNOSIS:\n"

    for idx, f in enumerate(findings, 1):
        text += f"""
{idx}. Cause: {f['cause']}
   - Severity: {f['severity']}
   - Sensor: {f['parameter']} = {f['value']}
   - Explanation: {f['explanation']}
   - Impact: {f['impact']}
   - Recommended Action: {f['action']}
   - Recovery Time: {f['recovery_time']}
"""
    return text.strip()


rule_engine = DiagnosticRuleEngine("./data/diagnostic_rules.json")
sympot_detector = SymptomDetector(llm)


def build_rule_context(inputs):
    farm_id = inputs.get("farm_id")
    question = inputs.get("question")

    if not farm_id:
        return "No rule-based diagnosis available."

    farm = farm_ctx_builder.get_farm(farm_id)

    detected_symptom = sympot_detector.detect_symptom_llm(question)

    rule_findings = rule_engine.evaluate(
        crop=farm["currentCrop"],
        symptom=detected_symptom,
        sensors=farm["sensors"],
    )

    return format_rule_diagnosis(rule_findings)
