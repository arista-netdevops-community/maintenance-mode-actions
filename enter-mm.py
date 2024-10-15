from time import sleep
from cloudvision.cvlib import ActionFailed


MAX_TRY = 15
INTERVAL = 15 # in seconds

maintenanceUnit = ctx.action.args.get("maintenanceUnit")

ctx.info("Entering Maintenance Mode for Unit " + maintenanceUnit)
cmds = [
    "enable",
    "configure",
    "maintenance",
    "unit " + maintenanceUnit,
    "quiesce",
    "copy running-config startup-config",
]
cmdResponses: list[dict] = ctx.runDeviceCmds(cmds)
errs = [resp.get('error') for resp in cmdResponses if resp.get('error')]
if errs:
    raise ActionFailed(f"Entering maintenance mode failed with: {errs[0]}")

count = 0
has_unit_entered_mm = False
cmds = [
        "enable",
        "show maintenance"
    ]
cmdResponses = []
while count < MAX_TRY and has_unit_entered_mm == False:
    cmdResponses: list[dict] = ctx.runDeviceCmds(cmds)
    if cmdResponses[1]["response"]["units"][maintenanceUnit]["state"] == "underMaintenance":
        has_unit_entered_mm = True
        break
    count += 1
    ctx.info(f"Switch did not enter maintenance mode. Check: {count} / {MAX_TRY}")
    sleep(INTERVAL)

if has_unit_entered_mm == False:
    raise ActionFailed(f"Entering maintenance mode failed with: {cmdResponses[1]}")
else:
    ctx.info(f"Switch entered maintenance mode successfully.")