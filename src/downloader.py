import os
import requests


DOWNLOAD_FOLDER = "downloads"



def create_download_folder():

    if not os.path.exists(DOWNLOAD_FOLDER):

        os.makedirs(
            DOWNLOAD_FOLDER
        )



def download_file(url):

    try:

        create_download_folder()


        filename = url.split("/")[-1]


        file_path = os.path.join(
            DOWNLOAD_FOLDER,
            filename
        )


        print("Downloading:")
        print(url)


        response = requests.get(
            url,
            stream=True,
            timeout=30,
            verify=False
        )


        response.raise_for_status()


        total_size = int(
            response.headers.get(
                "content-length",
                0
            )
        )


        downloaded = 0


        with open(
            file_path,
            "wb"
        ) as file:


            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:

                    file.write(
                        chunk
                    )

                    downloaded += len(chunk)


                    if total_size:

                        percent = (
                            downloaded * 100
                        ) / total_size


                        print(
                            f"\rProgress: {percent:.1f}%",
                            end=""
                        )


        print("\nDownload completed.")

        return file_path



    except Exception as e:


        print(
            "Download Error:",
            e
        )

        return None