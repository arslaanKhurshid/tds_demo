# backend/app/services/groq_service.py
from groq import Groq
from app.models.rule import Rule
from app.models.alert import Alert
from typing import List
import yaml
import uuid
from datetime import datetime
import logging
import re
from app.models.log import Log

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.client = Groq(api_key="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")  # Replace with your real key

    async def generate_rule(self, log_samples: List[dict]) -> Rule:
        prompt = f"""
        Given the following sample logs:
        {yaml.dump(log_samples, default_flow_style=False)}

        Generate a detection rule to identify potential threats. The rule must include:
        - name: A descriptive string (e.g., "Suspicious Login Rule")
        - query: A condition to match logs (e.g., "event_type == 'login' AND user == 'unknown'")
        - exclusion_list: A list of strings to filter out benign events (e.g., ["192.168.1.1"])

        Return the rule in plain YAML format with no Markdown, code blocks (e.g., ```yaml or ```), or extra text. Use this exact structure:
        name: <rule_name>
        query: <condition>
        exclusion_list: <list_of_strings>

        Example:
        name: Suspicious Login Rule
        query: event_type == 'login' AND user == 'unknown'
        exclusion_list: ['192.168.1.1']
        """
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            rule_yaml = response.choices[0].message.content
            logger.debug(f"Raw Groq response: {rule_yaml}")

            # Clean the response
            cleaned_yaml = rule_yaml.strip()
            # Remove Markdown code blocks and language identifiers
            cleaned_yaml = re.sub(r'```(?:yaml|)\n?', '', cleaned_yaml)
            cleaned_yaml = re.sub(r'```$', '', cleaned_yaml).strip()
            # Remove any leading/trailing non-YAML text
            cleaned_yaml = re.sub(r'^[^\n{]*\n', '', cleaned_yaml)
            cleaned_yaml = re.sub(r'\n[^\n}]*$', '', cleaned_yaml)

            logger.debug(f"Cleaned YAML: {cleaned_yaml}")

            if not cleaned_yaml:
                logger.error("Empty YAML after cleaning")
                raise ValueError("Empty response after cleaning")

            rule_dict = yaml.safe_load(cleaned_yaml)
            if not isinstance(rule_dict, dict):
                logger.error(f"Parsed YAML is not a dictionary: {rule_dict}")
                raise ValueError("Invalid YAML structure")

            # Validate required fields
            if not rule_dict.get("name") or not rule_dict.get("query"):
                logger.error(f"Missing required fields in rule: {rule_dict}")
                raise ValueError("Rule missing name or query")

            return Rule(
                id=str(uuid.uuid4()),
                name=rule_dict["name"],
                query=rule_dict["query"],
                exclusion_list=rule_dict.get("exclusion_list", []),
                enabled=True
            )

        except Exception as e:
            logger.error(f"Error generating rule: {e}, raw response: {rule_yaml}")
            return Rule(
                id=str(uuid.uuid4()),
                name="Fallback Rule",
                query="event_type == 'error'",  # Provide a basic default query
                exclusion_list=[],
                enabled=True
            )

    async def detect_threats(self, logs: List[Log], rule: Rule) -> List[Alert]:
        alerts = []
        for log in logs:
            prompt = f"""
            Given the following log:
            {yaml.dump(log.dict(), default_flow_style=False)}
            And the detection rule:
            Name: {rule.name}
            Query: {rule.query}
            Exclusion List: {', '.join(rule.exclusion_list)}

            Determine if this log represents a threat. Return a JSON object with:
            - severity: A string ("low", "medium", "high")
            - details: An object with a "reason" field explaining the threat

            Return the result in plain JSON format with no Markdown or code blocks (e.g., ```json or ```).
            Example:
            {{
                "severity": "medium",
                "details": {{"reason": "Suspicious login attempt"}}
            }}
            If no threat, return "null".
            """
            try:
                response = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                result_json = response.choices[0].message.content
                logger.debug(f"Raw Groq response for threat detection: {result_json}")

                # Clean the response
                cleaned_result = result_json.strip()
                cleaned_result = re.sub(r'```(?:json|)\n?', '', cleaned_result)
                cleaned_result = re.sub(r'```$', '', cleaned_result).strip()

                logger.debug(f"Cleaned result: {cleaned_result}")

                result = yaml.safe_load(cleaned_result)  # Using YAML parser for consistency
                if result and result != "null":
                    alerts.append(Alert(
                        id=str(uuid.uuid4()),
                        rule_id=rule.id,
                        severity=result.get("severity", "medium"),
                        details={"log_id": log.id, **result.get("details", {})},
                        timestamp=datetime.utcnow()
                    ))
            except Exception as e:
                logger.error(f"Error in threat detection: {e}, raw response: {result_json}")
                continue  # Skip this log and continue with the next

        return alerts