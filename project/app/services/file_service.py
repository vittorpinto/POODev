import os

class FileService:
    UPLOAD_FOLDER = 'uploads/'

    @staticmethod
    def save_file(file, filename):
        filepath = os.path.join(FileService.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
