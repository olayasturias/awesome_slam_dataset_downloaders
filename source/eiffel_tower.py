from utils.download_utils import extract_zip_files, download_zip_dict


def download_eiffel_tower(output_folder: str = r"D:\Datasets\EiffelTower") -> list[str]:
    urls = {
        2015: "https://www.seanoe.org/data/00810/92226/data/98240.zip",
        2016: "https://www.seanoe.org/data/00810/92226/data/98289.zip",
        2018: "https://www.seanoe.org/data/00810/92226/data/98314.zip",
        2020: "https://www.seanoe.org/data/00810/92226/data/98356.zip",
    }

    return download_zip_dict(urls, output_folder)


if __name__ == "__main__":
    output_dir = r"D:\Datasets\EiffelTower"
    downloaded_files = download_eiffel_tower(output_folder=output_dir)
    extract_zip_files(downloaded_files, output_dir)
