import io, gzip, requests, time
from typing import Iterator, Iterable, Literal, Optional
from warcio.archiveiterator import ArchiveIterator  # pip install warcio

BASE = "https://data.commoncrawl.org"

def fetch_paths(crawl: str, kind: Literal["warc","wat","wet"]) -> Iterator[str]:
    """
    Yield full HTTPS URLs for all files of a given kind in a crawl.
    Uses the per-crawl gzip listings (warc.paths.gz, wat.paths.gz, wet.paths.gz).
    Example crawl: CC-MAIN-2025-21
    """
    assert kind in {"warc","wat","wet"}
    url = f"{BASE}/crawl-data/{crawl}/{kind}.paths.gz"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with gzip.GzipFile(fileobj=io.BytesIO(r.content)) as gz:
        for line in gz.read().decode("utf-8", "replace").splitlines():
            line = line.strip()
            if line:
                yield f"{BASE}/{line}"

def fetch_urls(crawl: str) -> Iterator[str]:
    """
    Yield full HTTPS URLs for all files of a given kind in a crawl.
    Uses the per-crawl gzip listings (warc.paths.gz, wat.paths.gz, wet.paths.gz).
    Example crawl: CC-MAIN-2025-21
    """
    url = f"{BASE}/crawl-data/{crawl}/cc-index.paths.gz"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with gzip.GzipFile(fileobj=io.BytesIO(r.content)) as gz:
        for line in gz.read().decode("utf-8", "replace").splitlines():
            line = line.strip()
            if line:
                yield f"{BASE}/{line}"

def iter_warc_records(file_url: str, record_types: Optional[Iterable[str]] = None) -> Iterator:
    """
    Stream and parse records from a WARC/WAT/WET file URL using warcio.
    record_types example: {"response","request","warcinfo","metadata","conversion"}
    """
    with requests.get(file_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        for rec in ArchiveIterator(r.raw, arc2warc=True):
            if record_types and rec.rec_type not in record_types:
                continue
            yield rec

def download_range(url: str, offset: int, length: int, retries: int = 3) -> bytes:
    """
    Byte-range fetch for a single WARC record (useful with CDX/Athena offsets).
    """
    start, end = offset, offset + length - 1
    headers = {"Range": f"bytes={start}-{end}"}
    for attempt in range(retries):
        resp = requests.get(url, headers=headers, timeout=60)
        if resp.status_code in (200, 206):
            return resp.content
        time.sleep(1.5 * (attempt + 1))
    resp.raise_for_status()

