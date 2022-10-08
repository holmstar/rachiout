import json
from time import sleep

import yaml
import requests


class RachioClient:

    def __init__(self):
        # Read YAML file
        with open("rachiout.yml", 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            print(data_loaded)
            self.apikey = data_loaded.get("api-token")
            self.apiBaseUri = data_loaded.get("api-base-uri")
            self.deviceName = data_loaded.get("rachio-device-name")
            self.zoneDuration = int(data_loaded.get("purge-sec"))
            self.rechargeDuration = int(data_loaded.get("compressor-recharge-delay-sec"))
            self.repetitions = int(data_loaded.get("repetitions"))

    def blow_out_system(self):
        print("Getting person id...")
        person_id = self.get_person_id()
        print("Getting devices...")
        person_info = self.get_person_info(person_id)
        devices = person_info.get("devices")
        print("Found % s devices" % len(devices))
        device = list(filter(lambda a_device: a_device.get("name") == self.deviceName, devices))[0]
        print("Found % s" % self.deviceName)
        # print(json.dumps(device, indent=2))

        i = 0
        while i < self.repetitions:
            for zone in device.get("zones"):
                if bool(zone.get("enabled")):
                    print("Purging zone % s for % s seconds" % (zone.get("zoneNumber"), self.zoneDuration))
                    self.zone_start(zone.get("id"), self.zoneDuration)
                    sleep(self.zoneDuration)
                    print("Recharging compressor for % s seconds" % self.rechargeDuration)
                    sleep(self.rechargeDuration)
                else:
                    print("Skipping disabled zone: % s" % zone.get("zoneNumber"))
            i = i + 1

    def get_person_id(self):
        response = requests.get("% s/person/info" % self.apiBaseUri,
                                headers={"Authorization": "Bearer % s" % self.apikey})
        return response.json().get("id")

    def get_person_info(self, person_id):
        response = requests.get("% s/person/% s" % (self.apiBaseUri, person_id),
                                headers={"Authorization": "Bearer % s" % self.apikey})
        # print(json.dumps(response.json(), indent=2))
        return response.json()

    def zone_start(self, zone_id, duration):
        response = requests.put("% s/zone/start" % self.apiBaseUri,
                                data="""{"id": "% s", "duration": % s}""" % (zone_id, self.zoneDuration),
                                headers={"Authorization": "Bearer % s" % self.apikey})


def main():
    client = RachioClient()
    client.blow_out_system()


if __name__ == '__main__':
    main()
