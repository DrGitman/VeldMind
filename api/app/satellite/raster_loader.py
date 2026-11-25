
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def read_reflectance_metadata(xml_path: Path) -> tuple[float, dict[str, float]]:
    """Read Sentinel-2 BOA quantification value and band offsets."""

    root = ET.parse(xml_path).getroot()

    quantification = None
    band_ids = {}

    for element in root.iter():
        tag = element.tag.split("}")[-1]

        if tag == "BOA_QUANTIFICATION_VALUE":
            quantification = float(element.text)

        elif tag == "Spectral_Information":
            band_ids[element.attrib["physicalBand"]] = (
                element.attrib["bandId"]
            )

    offsets = {}

    for element in root.iter():
        tag = element.tag.split("}")[-1]

        if tag == "BOA_ADD_OFFSET":
            band_id = element.attrib["band_id"]
            offsets[band_id] = float(element.text)

    if quantification is None or quantification <= 0:
        raise ValueError("Invalid BOA quantification value.")

    required_bands = {"B4", "B8"}

    if not required_bands.issubset(band_ids):
        raise ValueError("B04 or B08 mapping missing from metadata.")

    for band in required_bands:
        if band_ids[band] not in offsets:
            raise ValueError(f"Offset missing for {band}.")

    return quantification, {
        "B04": offsets[band_ids["B4"]],
        "B08": offsets[band_ids["B8"]],
    }


def _resample_band_to_scl(
    band_path: Path,
    destination_transform,
    destination_crs,
    destination_shape,
) -> np.ndarray:
    """Resample a Sentinel-2 band to the SCL grid."""

    with rasterio.open(band_path) as src:
        source = src.read(1).astype(np.float32)

        destination = np.full(
            destination_shape,
            np.nan,
            dtype=np.float32,
        )

        reproject(
            source=source,
            destination=destination,
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=0,
            dst_transform=destination_transform,
            dst_crs=destination_crs,
            dst_nodata=np.nan,
            resampling=Resampling.average,
        )

    return destination


def load_sentinel2_bands(
    data_dir: Path,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load Sentinel-2 B04, B08 and SCL.

    B04 and B08 are converted to surface reflectance
    and resampled to the 20 m SCL grid.

    Returns:
        nir: B08 surface reflectance
        red: B04 surface reflectance
        scl: Scene Classification Layer
    """

    data_dir = Path(data_dir)
    
    red_path = next(data_dir.glob("*_B04_10m.jp2"))
    nir_path = next(data_dir.glob("*_B08_10m.jp2"))
    scl_path = next(data_dir.glob("*_SCL_20m.jp2"))
    xml_path = next(data_dir.glob("MTD_MSIL2A*.xml"))



    for path in (red_path, nir_path, scl_path, xml_path):
        if not path.exists():
            raise FileNotFoundError(f"Required Sentinel-2 file not found: {path}")

    quantification, offsets = read_reflectance_metadata(xml_path)

    with rasterio.open(scl_path) as scl_src:
        scl = scl_src.read(1)

        destination_transform = scl_src.transform
        destination_crs = scl_src.crs
        destination_shape = (scl_src.height, scl_src.width)

    red_dn = _resample_band_to_scl(
        red_path,
        destination_transform,
        destination_crs,
        destination_shape,
    )

    nir_dn = _resample_band_to_scl(
        nir_path,
        destination_transform,
        destination_crs,
        destination_shape,
    )

    red = (red_dn + offsets["B04"]) / quantification
    nir = (nir_dn + offsets["B08"]) / quantification

    return nir.astype(np.float32), red.astype(np.float32), scl
