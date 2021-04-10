"""Set up the stretch labs"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources

# get compliance configuration
project_compliance_config = pulumi.Config("project-compliance")
rg_purpose = project_compliance_config.require("rg-purpose")
rg_useremailtag = project_compliance_config.require("rg-useremailtag")
rg_environment = project_compliance_config.require("rg_environment")

# get azure configuration
azure_config = pulumi.Config("azure")
azure_location = azure_config.require("location")


# get stretch labs configuration
labs_config = pulumi.Config("labs")
labs_platform = labs_config.require("platform")

# create resources
resource_group = resources.ResourceGroup(
    "EmTech_Stretch_Labs",
    tags={
        "UserEmailTag": rg_useremailtag,
        "purpose": rg_purpose,
        "environment": rg_environment,
    },
)

if labs_platform == "rocos":
    raise NotImplemented

if labs_platform == "iot-hub":
    raise NotImplemented