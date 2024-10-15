from typing import List, Dict
from cloudvision.cvlib import ActionFailed

maintenanceUnit = ctx.action.args.get("maintenanceUnit")

ctx.info("Exiting Maintenance Mode for Unit " + maintenanceUnit)
cmds = [
    "enable",
    "configure",
    "maintenance",
    "unit " + maintenanceUnit,
    "default quiesce",
    "copy running-config startup-config",
]

cmdResponses: List[Dict] = ctx.runDeviceCmds(cmds)
errs = [resp.get('error') for resp in cmdResponses if resp.get('error')]
if errs:
    raise ActionFailed(f"Exiting maintenance mode failed with: {errs[0]}")