


from app.services.metadata import _extract_segments, parse_metadata


def test_extract_segments():
    ap_info = (
        "AP Info: [AP3-SUB-004 v1.7.6.0]"
        "[2021 USDM WRX MT CCF Gen2]"
        "[Reflash: Stage1+BigSF 03 v400.ptm]"
        "[Realtime: Stage1+BigSF 03 v400.ptm]"
    )
        
    segments = _extract_segments(ap_info)

    assert segments == [
        "AP3-SUB-004 v1.7.6.0",
        "2021 USDM WRX MT CCF Gen2",
        "Reflash: Stage1+BigSF 03 v400.ptm - Realtime: Stage1+BigSF 03 v400.ptm",
    ]

def test_extract_segments_with_no_segments():
    ap_info = "AP Info:"
    segments = _extract_segments(ap_info)

    assert segments == []

def test_extract_segments_with_empty_string():
    segments = _extract_segments("")

    assert segments == []

def test_parse_metadata():
    ap_info = (
        "AP Info: [AP3-SUB-004 v1.7.6.0]"
        "[2021 USDM WRX MT CCF Gen2]"
        "[Reflash: Stage1+BigSF 03 v400.ptm]"
        "[Realtime: Stage1+BigSF 03 v400.ptm]"
    )
    
    metadata = parse_metadata(ap_info)

    assert metadata.accessport_model == "AP3-SUB-004"
    assert metadata.firmware_version == "v1.7.6.0"
    assert metadata.vehicle == "2021 USDM WRX MT CCF Gen2"
    assert metadata.reflash_tune == "Stage1+BigSF 03 v400.ptm"
    assert metadata.realtime_tune == "Stage1+BigSF 03 v400.ptm"