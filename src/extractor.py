import os
import zipfile
import shutil



TEMP_FOLDER = "temp"



def create_temp_folder():

    if os.path.exists(TEMP_FOLDER):

        shutil.rmtree(
            TEMP_FOLDER
        )


    os.makedirs(
        TEMP_FOLDER
    )



def extract_zip(zip_path):

    try:

        create_temp_folder()


        print("Extracting:")
        print(zip_path)


        with zipfile.ZipFile(
            zip_path,
            "r"
        ) as zip_file:


            zip_file.extractall(
                TEMP_FOLDER
            )


        print(
            "Extraction completed."
        )


        return TEMP_FOLDER



    except Exception as e:


        print(
            "Extraction Error:",
            e
        )


        return None