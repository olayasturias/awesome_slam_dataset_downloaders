from utils.download_utils import extract_zip_files, download_zip_dict


def download_subpipe(output_folder: str = r"D:\Datasets\SubPipe") -> list[str]:
    urls = {
        "SubPipe": "https://zenodo.org/records/12666132/files/SubPipe.zip?download=1",
    }

    return download_zip_dict(urls, output_folder)


if __name__ == "__main__":
    output_dir = r"D:\Datasets\SubPipe"
    downloaded_files = download_subpipe(output_folder=output_dir)
    extract_zip_files(downloaded_files, output_dir)
