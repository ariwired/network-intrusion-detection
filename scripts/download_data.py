"""Baixa a versão 2 do dataset e salva Dataset_resumido.csv em data/raw/."""

import hashlib
import io
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

URL = ("https://www.kaggle.com/api/v1/datasets/download/rebsonramalho/network-threat-detection-dataset?datasetVersionNumber=2")
NAME = "Dataset_resumido.csv"
SHA256 = "bd775a4e982055794c8feda3d4cfcb7ddcea1c4d4e4c4048f0cfcaf8bcd23445"
OUT = Path(__file__).resolve().parents[1] / "data/raw"

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        request = Request(URL, headers={"User-Agent": "NetworkIntrusionLab/1.0"})
        with urlopen(request, timeout=120) as response:
            data = ZipFile(io.BytesIO(response.read())).read(NAME)
    except Exception as exc:
        raise SystemExit("Download indisponível. Verifique sua conexão com a internet e se o Kaggle está acessível.") from exc

    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit("Hash inesperado; nenhum arquivo foi salvo.")
    
    (OUT / NAME).write_bytes(data)
    print(f"Salvo {NAME}: {len(data):,} bytes; SHA-256 validado.")


if __name__ == "__main__":
    main()