
import re
from dataclasses import dataclass


@dataclass
class DatalogMetadata:
    accessport_model: str | None = None
    firmware_version: str | None = None
    vehicle: str | None = None
    reflash_tune: str | None = None
    realtime_tune: str | None = None

def parse_metadata(ap_info: str) -> "DatalogMetadata":
    segments = _extract_segments(ap_info)

    

    if not segments:
        return DatalogMetadata()

    metadata = DatalogMetadata()
    # Accessport Information
    if len(segments) >= 1:
        accessport_parts = segments[0].split(" ", 1)

        if len(accessport_parts) == 2:
            metadata.accessport_model = accessport_parts[0]
            metadata.firmware_version = accessport_parts[1]
        else:
            metadata.accessport_model = segments[0]

    #Vehicle
    if len(segments) >= 2:
        metadata.vehicle = segments[1]

    # Tune Information
    if len(segments) >= 3:
        tune_info = segments[2]

        if "Reflash:" in tune_info:
            reflash_part = tune_info.split("Reflash:", 1)[1]

            if "- Realtime:" in reflash_part:
                reflash, realtime = reflash_part.split("- Realtime:", 1)
                metadata.reflash_tune = reflash.strip()
                metadata.realtime_tune = realtime.strip()
            else:
                metadata.reflash_tune = reflash_part.strip()

    return metadata

def _extract_segments(ap_info: str):
    """Extract bracketed metadata segments from an AP Info header."""
    segments = re.findall(r"\[(.*?)\]", ap_info)

    if len(segments) >= 4:
        combine_tunes = f"{segments[2]} - {segments[3]}"
        return segments[:2] + [combine_tunes]
    
    return segments