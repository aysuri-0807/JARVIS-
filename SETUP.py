#Run this first in order to set up the paths for different apps
import os
import json

STORED_PATHS = "savedPaths.json"
if os.path.exists(STORED_PATHS):
    with open(STORED_PATHS, "r") as f:
        paths = json.load(f)
else:
    if __name__ != "__main__":
        print ("No existing paths! Functionality will be limited. (run SETUP to add paths)")
        paths = None
    else:
        paths = {}

STORED_APPS = "savedApps.json"
if os.path.exists(STORED_APPS):
    with open(STORED_APPS, "r") as r:
        apps = json.load(r)
else:
    if __name__ != "__main__":
        print ("No existing apps! Functionality will be limited. (run SETUP to add apps)")
        apps = None
    else:
        apps = []
if __name__ == "__main__":

    while True:
        app_name = input("Enter an app name, or enter q to quit: ").strip()
        app_name = app_name.lower()
        if app_name == "q":
            break
        app_path = input("Enter app path: ").strip()

        paths[app_name] = app_path
        apps.append(app_name)
        print (f"Added: {app_name} Successfully!")
    with open(STORED_PATHS, "w") as f:
        json.dump(paths, f, indent=4)
    with open(STORED_APPS, "w") as r:
        json.dump(apps, r, indent=4)


