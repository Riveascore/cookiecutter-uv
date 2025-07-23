"""
Conditional prompts for Azure DevOps options when publish_python_package is "azure_artifacts".

{% if cookiecutter.publish_python_package == "azure_artifacts" %}
Azure DevOps Configuration Required
{{ cookiecutter.update({
    "azure_devops_organization": "chrisaga",
    "azure_devops_feed": "private-python-feed"
}) }}
{% else %}
{{ cookiecutter.update({
    "azure_devops_organization": "",
    "azure_devops_feed": ""
}) }}
{% endif %}
"""

from __future__ import annotations

import re
import sys

PROJECT_NAME_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
project_name = "{{cookiecutter.project_name}}"
if not re.match(PROJECT_NAME_REGEX, project_name):
    print(
        f"ERROR: The project name {project_name} is not a valid Python module name. Please do not use a _ and use - instead"
    )
    # Exit to cancel project
    sys.exit(1)

PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
project_slug = "{{cookiecutter.project_slug}}"
if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"ERROR: The project slug {project_slug} is not a valid Python module name. Please do not use a - and use _ instead"
    )
    # Exit to cancel project
    sys.exit(1)

# Conditional prompting for Azure DevOps when publish_python_package is "azure_artifacts"
publish_option = "{{cookiecutter.publish_python_package}}"
if publish_option == "azure_artifacts":
    # Get current values from cookiecutter context
    current_org = "{{cookiecutter.azure_devops_organization}}"
    current_feed = "{{cookiecutter.azure_devops_feed}}"

    # Only prompt if running interactively and values are not already provided
    azure_org = current_org
    azure_feed = current_feed

    # Check if we're in an interactive environment and if values need to be provided
    import sys
    if sys.stdin.isatty() and (not current_org or not current_feed):
        print("\nAzure DevOps configuration required:")
        if not current_org:
            azure_org = input(f"azure_devops_organization [{current_org}]: ").strip()
            if not azure_org:
                azure_org = current_org

        if not current_feed:
            azure_feed = input(f"azure_devops_feed [{current_feed}]: ").strip()
            if not azure_feed:
                azure_feed = current_feed

    # Write the values to a temporary file that can be read by post_gen_project
    # (only if they differ from defaults or if we're updating them)
    if azure_org != current_org or azure_feed != current_feed:
        with open('.cookiecutter_azure_config', 'w') as f:
            f.write(f"azure_devops_organization={azure_org}\n")
            f.write(f"azure_devops_feed={azure_feed}\n")
