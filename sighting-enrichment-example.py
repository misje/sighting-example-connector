import stix2
import sys
import time
from datetime import datetime
from pycti import Identity, OpenCTIConnectorHelper, StixSightingRelationship

DUMMY_INDICATOR_ID = "indicator--167565fe-69da-5e2f-a1c1-0542736f9f9a"


class ExampleConnector:
    def __init__(self) -> None:
        self.helper = OpenCTIConnectorHelper({}, True)
        self.helper.listen(self.process)

    def process(self, data: dict) -> str:
        system = stix2.Identity(
            id=Identity.generate_id("fjas", "system"),
            name="fjas",
            identity_class="system",
        )
        seen_at = datetime.now()
        sighting = stix2.Sighting(
            id=StixSightingRelationship.generate_id(
                data["entity_id"], system.id, seen_at, seen_at
            ),
            first_seen=seen_at,
            last_seen=seen_at,
            count=1,
            where_sighted_refs=[system.id],
            # confidence=100,
            sighting_of_ref=DUMMY_INDICATOR_ID,
            allow_custom=True,
            x_opencti_sighting_of_ref=data["entity_id"],
        )
        self.helper.log_info(sighting)
        bundle = [system, sighting]

        self.helper.send_stix2_bundle(
            self.helper.stix2_create_bundle(bundle),  # type: ignore
            update=True,
        )
        return "Done"


if __name__ == "__main__":
    try:
        ExampleConnector()

    except Exception as e:
        print(e)
        time.sleep(2)
        sys.exit(0)
