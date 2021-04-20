"""Set up the stretch labs"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
import pulumi_azure_native.web as web

# get compliance configuration
project_compliance_config = pulumi.Config("project-compliance")
rg_purpose = project_compliance_config.require("rg-purpose")
rg_useremailtag = project_compliance_config.require("rg-useremailtag")
rg_environment = project_compliance_config.require("rg_environment")

# get azure configuration
azure_config = pulumi.Config("azure-native")
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
    location=azure_location,
)

if labs_platform == "rocos":
    raise NotImplemented

if labs_platform == "iot-hub":
    raise NotImplemented

app_service_plan = web.AppServicePlan(
    "appservice-asp",
    resource_group_name=resource_group.name,
    kind="App",
    sku=web.SkuDescriptionArgs(
        tier="Basic",
        name="B1",
    ),
)

app = web.WebApp(
    "stretchlabs-",
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[],
    ),
)

pulumi.export(
    "endpoint", app.default_host_name.apply(lambda endpoint: "https://" + endpoint)
)
