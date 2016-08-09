import os
from PIL import Image
from PythonMagick import Image as PyImage
import pdfkit
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import datetime


class ImageOpr:

    def __init__(self):
        pass

    @staticmethod
    def tiff_to_pdf(list_of_file_paths, destination_directory):
        """
        This method converts individual TIFF image files to PDF.
        :param list_of_file_paths: This argument is the list of absolute file paths for example
        ['C:/User/Documents/Images/Image1.tiff', 'C:/User/Documents/Images/Image2.tiff' ]
        :param destination_directory: Pass in the absolute path to the directory you want the
        converted files to be saved to.
        :return: This method returns a dictionary giving information about the success or failure
        of the operation and also gives the list of files that failed the conversion..
        """
        operation_result = {}
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                continue
            else:
                invalid_file_paths.append(files)
                list_of_file_paths.remove(files)

        if not os.path.exists(os.path.join(os.getcwd(), "temp_dir")):
            os.mkdir(os.path.join(os.getcwd(), "temp_dir"))

        path_to_temp = os.path.join(os.getcwd(), "temp_dir")

        for image in list_of_file_paths:
            temp_file_list = []
            img = Image.open(image)
            tif_file_full_name = os.path.basename(image)
            tif_file_name, tif_file_ext = os.path.splitext(tif_file_full_name)
            for i in range(100):
                try:
                    img.seek(i)
                    temp_file_list.append(os.path.join(path_to_temp, 'page' + str(i + 1) + ".tif"))
                    img.save(os.path.join(path_to_temp, 'page' + str(i + 1) + ".tif"))
                except EOFError:
                    break

            png_temp_array = []
            for tif_img in temp_file_list:
                img_png = Image.open(tif_img)
                file_name = os.path.basename(tif_img)
                name, ext = os.path.splitext(file_name)
                file_name_at_destination = os.path.join(path_to_temp, name + ".png")
                png_temp_array.append(file_name_at_destination)
                img_png.save(file_name_at_destination)
                os.remove(tif_img)

            pdf_temp_array = []
            for png_img in png_temp_array:
                image = PyImage()
                image.density("600")
                image.read(png_img)
                png_file_name = os.path.basename(png_img)
                png_name, png_ext = os.path.splitext(png_file_name)
                file_name_at_destination = os.path.join(path_to_temp, png_name + ".pdf")
                pdf_temp_array.append(file_name_at_destination)
                image.write(file_name_at_destination)
                os.remove(png_img)

            if pdf_temp_array.__len__() > 1:
                ImageOpr.merge_pdf(pdf_temp_array, destination_directory, tif_file_name, delete_source=False)
                for pdfs in pdf_temp_array:
                    os.remove(pdfs)
            else:
                os.rename(pdf_temp_array[0], os.path.join(path_to_temp, tif_file_name + ".pdf"))
                destination_directory_file_name = os.path.join(destination_directory, tif_file_name + ".pdf")
                shutil.move(os.path.join(path_to_temp, tif_file_name + ".pdf"), destination_directory_file_name)

        shutil.rmtree(path_to_temp, ignore_errors=True)

        if not invalid_file_paths:
            operation_result.update({"code": 0, "invalid_file_paths": "None"})
        else:
            invalid_files = ",".join(list_of_file_paths)
            operation_result.update({"code": 1, "invalid_file_paths": invalid_files})
        return operation_result

    @staticmethod
    def bmp_to_png(list_of_file_paths, destination_directory, delete_source=False):
        operation_result = {}
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                continue
            else:
                invalid_file_paths.append(files)
                list_of_file_paths.remove(files)
        for files in list_of_file_paths:
            image = Image.open(files)
            file_name = os.path.basename(files)
            name, ext = os.path.splitext(file_name)
            file_name_at_destination = os.path.join(destination_directory, name + ".png")
            image.save(file_name_at_destination, "PNG")
        if delete_source is True:
            for files in list_of_file_paths:
                os.remove(files)
        if not invalid_file_paths:
            operation_result.update({"code": 0, "invalid_file_paths": "None"})
        else:
            invalid_files = ",".join(list_of_file_paths)
            operation_result.update({"code": 1, "invalid_file_paths": invalid_files})
        return operation_result

    @staticmethod
    def bmp_to_jpeg(list_of_file_paths, destination_directory, delete_source=False):
        operation_result = {}
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                continue
            else:
                invalid_file_paths.append(files)
                list_of_file_paths.remove(files)
        for files in list_of_file_paths:
            image = Image.open(files)
            file_name = os.path.basename(files)
            name, ext = os.path.splitext(file_name)
            file_name_at_destination = os.path.join(destination_directory, name + ".jpg")
            image.save(file_name_at_destination, "JPEG")
        if delete_source is True:
            for files in list_of_file_paths:
                os.remove(files)
        if not invalid_file_paths:
            operation_result.update({"code": 0, "invalid_file_paths": "None"})
        else:
            invalid_files = ",".join(list_of_file_paths)
            operation_result.update({"code": 1, "invalid_file_paths": invalid_files})
        return operation_result

    @staticmethod
    def bmp_or_jpg_to_pdf(list_of_file_paths, destination_directory, delete_source=False):
        operation_result = {}
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                continue
            else:
                invalid_file_paths.append(files)
                list_of_file_paths.remove(files)
        for files in list_of_file_paths:
            image = PyImage()
            image.density("600")
            image.read(files)
            file_name = os.path.basename(files)
            name, ext = os.path.splitext(file_name)
            file_name_at_destination = os.path.join(destination_directory, name + ".pdf")
            image.write(file_name_at_destination)
        if delete_source is True:
            for files in list_of_file_paths:
                os.remove(files)
        if not invalid_file_paths:
            operation_result.update({"code": 0, "invalid_file_paths": "None"})
        else:
            invalid_files = ",".join(list_of_file_paths)
            operation_result.update({"code": 1, "invalid_file_paths": invalid_files})
        return operation_result

    @staticmethod
    def html_text_to_pdf(html_text, destination_directory, output_file_name):
        file_path = os.path.join(destination_directory, output_file_name)
        if os.path.exists(file_path):
            new_file_path = os.path.join(destination_directory, "Alt" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        options = {
            'page-size': 'Letter',
            'dpi': '600'
        }
        pdfkit.from_string(html_text, file_path, options=options)
        return new_file_path

    @staticmethod
    def merge_pdf(list_of_file_paths, destination_directory, file_name, delete_source=False):
        merge = PdfFileMerger()
        operation_result = {}
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                continue
            else:
                invalid_file_paths.append(files)
                list_of_file_paths.remove(files)

        for files in list_of_file_paths:
            merge.append(PdfFileReader(files, True))

        merged_pdf_filename = file_name + ".pdf"
        merge.write(os.path.join(destination_directory, merged_pdf_filename))

        if delete_source is True:
            for files in list_of_file_paths:
                os.remove(files)

        if not invalid_file_paths:
            operation_result.update({"code": 0, "invalid_file_paths": "None"})
        else:
            invalid_files = ",".join(list_of_file_paths)
            operation_result.update({"code": 1, "invalid_file_paths": invalid_files})
        return operation_result












