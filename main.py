#!/usr/bin/env python3

import os
import json
import base64
import requests
import datetime

maxModified = datetime.datetime.now(datetime.timezone.utc)
apiEndpoint = "https://synthetics.newrelic.com/synthetics/api"
apiVersion = "v3"


def getMonitors(proxies, accountId, adminApiKey, startTime, downloadDir="accounts/"):
    global maxModified
    offset = 0
    limit = 100
    accountDir = downloadDir + "/" + str(accountId) + "/monitors/"
    while True:
        try:
            response = requests.get(
                "{}/{}/monitors?limit={}&offset={}".format(
                    str(apiEndpoint), str(apiVersion), str(limit), str(offset)
                ),
                headers={"X-Api-Key": adminApiKey},
                proxies=proxies,
            )
        except Exception as e:
            print("Connection Error")
            return 2
        if "count" in response.json().keys():
            if response.json()["count"] == 0:
                break
            else:
                offset = offset + limit
                if not os.path.exists(accountDir):
                    os.makedirs(accountDir)
                for monitor in response.json()["monitors"]:
                    modifiedTime = datetime.datetime.strptime(
                        monitor["modifiedAt"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                    if modifiedTime >= startTime:
                        getMonitorDetails(
                            proxies, accountId, adminApiKey, monitor, accountDir
                        )
                        if modifiedTime > maxModified:
                            maxModified = modifiedTime
        else:
            print("Below invalid response received for account-id: " + str(accountId))
            print(response.json())
            break
    return 1


def getMonitorDetails(proxies, accountId, adminApiKey, monitor, downloadDir):
    if monitor["type"] == "SCRIPT_API" or monitor["type"] == "SCRIPT_BROWSER":
        scriptFileName = downloadDir + "/" + monitor["id"] + ".script"
        scriptFile = open(scriptFileName, "w")
        scriptFile.write(json.dumps(monitor, indent=2))
        try:
            response = requests.get(
                "{}/{}/monitors/{}/script".format(
                    str(apiEndpoint), str(apiVersion), str(monitor["id"])
                ),
                headers={"X-Api-Key": adminApiKey},
                proxies=proxies,
            )
        except Exception as e:
            print("Connection Error")
            return 2
        scriptFile.write("\n\n")
        scriptFile.write("#--------------------------------------#\n")
        scriptFile.write("#------------- SCRIPT BODY ------------#\n")
        scriptFile.write("#--------------------------------------#\n")
        scriptFile.write(
            base64.b64decode(response.json()["scriptText"]).decode("utf-8")
        )
        scriptFile.write("\n")
        scriptFile.write("#--------------------------------------#\n")
        scriptFile.write("#------------ /SCRIPT BODY ------------#\n")
        scriptFile.write("#--------------------------------------#\n")
        scriptFile.close()
    else:
        monitorFileName = downloadDir + "/" + monitor["id"] + ".json"
        monitorFile = open(monitorFileName, "w")
        monitorFile.write(json.dumps(monitor, indent=2))
        monitorFile.close()
    return 1


def main():
    global apiEndpoint
    global apiVersion
    global maxModified
    timeNow = datetime.datetime.now(datetime.timezone.utc)
    if not os.path.exists("config.json"):
        print("config.json NOT FOUND")
        return False
    with open("config.json", "r") as config_file:
        cfg = json.load(config_file)
    startFrom = 0
    downloadDir = None
    proxies = {}
    if "proxy" in cfg.keys():
        if "http_proxy" in cfg["proxy"].keys() and cfg["proxy"]["http_proxy"] != "":
            proxies["http"] = cfg["proxy"]["http_proxy"]
        if "https_proxy" in cfg["proxy"].keys() and cfg["proxy"]["https_proxy"] != "":
            proxies["https"] = cfg["proxy"]["https_proxy"]
    if "common" in cfg.keys():
        if (
            "api-endpoint" in cfg["common"].keys()
            and cfg["common"]["api-endpoint"] != ""
        ):
            apiEndpoint = cfg["common"]["api-endpoint"]
        if "api-version" in cfg["common"].keys() and cfg["common"]["api-version"] != "":
            apiVersion = cfg["common"]["api-version"]
        if "download-dir" in cfg["common"].keys():
            downloadDir = cfg["common"]["download-dir"]
        if "start-from" in cfg["common"].keys() and cfg["common"]["start-from"] != "":
            startFrom = datetime.datetime.strptime(
                cfg["common"]["start-from"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
        else:
            startFrom = timeNow
    maxModified = startFrom
    if downloadDir is None or downloadDir == "":
        downloadDir = "accounts"
    if not os.path.exists(downloadDir):
        os.makedirs(downloadDir)
    print("--------------------------------------------------")
    print("using config.json:")
    # print("--------------------------------------------------")
    # print(json.dumps(cfg, indent=2))
    print("--------------------------------------------------")
    print("apiEndpoint: " + apiEndpoint)
    print("apiVersion: " + apiVersion)
    print("downloadDir: " + downloadDir)
    print(
        "startFrom: " + datetime.datetime.strftime(startFrom, "%Y-%m-%dT%H:%M:%S.%f%z")
    )
    print(
        "maxModified: "
        + datetime.datetime.strftime(maxModified, "%Y-%m-%dT%H:%M:%S.%f%z")
    )
    print("--------------------------------------------------")
    for account in cfg["accounts"]:
        getMonitors(
            proxies,
            account["account-id"],
            account["admin-api-key"],
            startFrom,
            downloadDir,
        )
        # pass
    print("-------------------JOB COMPLETED------------------")
    if maxModified > startFrom:
        cfg["common"]["start-from"] = datetime.datetime.strftime(
            maxModified, "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        print("--------------------------------------------------")
        print(
            "startFrom: "
            + datetime.datetime.strftime(startFrom, "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        print(
            "maxModified: "
            + datetime.datetime.strftime(maxModified, "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        print("updating config.json")
        # print("--------------------------------------------------")
        # print(json.dumps(cfg, indent=2))
        with open("config.json", "w") as config_file:
            json.dump(cfg, config_file, indent=4)
        print("--------------------------------------------------")
    else:
        print("--------------------------------------------------")
        print(
            "startFrom: "
            + datetime.datetime.strftime(startFrom, "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        print(
            "maxModified: "
            + datetime.datetime.strftime(maxModified, "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        print("NOT updating config.json")
        print("--------------------------------------------------")
    return 1


if __name__ == "__main__":
    main()
