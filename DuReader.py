import os
import hashlib
import urllib.request
import zipfile
import sys

def file_exists(path):
    return os.path.exists(path)

def download_file(url, filename):
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded {filename}")

def verify_md5(file_path, expected_md5):
    print(f"Verifying MD5 for {file_path}...")
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    file_md5 = hash_md5.hexdigest()
    print(f"Expected: {expected_md5}, Found: {file_md5}")
    return file_md5 == expected_md5

def unzip_file(zip_path, extract_to='.'):
    print(f"Unzipping {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {zip_path} to {extract_to}")

def main():
    # Check if directories exist
    if file_exists("preprocessed") and file_exists("raw"):
        print("Data exists")
        sys.exit(0)

    # Download the files
    raw_url = "https://dataset-bj.cdn.bcebos.com/dureader/dureader_raw.zip"
    preprocessed_url = "https://dataset-bj.cdn.bcebos.com/dureader/dureader_preprocessed.zip"
    raw_zip = "dureader_raw.zip"
    preprocessed_zip = "dureader_preprocessed.zip"

    if not file_exists(raw_zip):
        download_file(raw_url, raw_zip)

    if not file_exists(preprocessed_zip):
        download_file(preprocessed_url, preprocessed_zip)

    # Replace these with the actual expected MD5 hash values
    expected_md5_raw = "expected_md5_hash_for_raw"
    expected_md5_preprocessed = "expected_md5_hash_for_preprocessed"

    # Verify MD5 checksums
    if not verify_md5(raw_zip, expected_md5_raw):
        print("Download data error for raw.zip!", file=sys.stderr)
        sys.exit(1)

    if not verify_md5(preprocessed_zip, expected_md5_preprocessed):
        print("Download data error for preprocessed.zip!", file=sys.stderr)
        sys.exit(1)

    # Unzip files
    unzip_file(raw_zip)
    unzip_file(preprocessed_zip)

if __name__ == "__main__":
    main()
