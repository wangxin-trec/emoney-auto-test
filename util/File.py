import os,datetime,shutil,zipfile
from tqdm import tqdm

class FileUtil:
    def _isExists(filePath):
        """
        方法意味：ファイルかどうかを判断する
        params:
            filePath: ソースパス
        return: なし
        """
        return os.path.exists(filePath)
 
    def _isFolderExists(folderPath):
        """
        方法意味：フォルダーかどうかを判断する
        params:
            folderPath: ソースパス
        return: なし
        """
        return os.path.isdir

    def _isFile(filePath):
        """
        方法意味：ファイルかどうかを判断する
        params:
            filePath: ソースパス
        return: なし
        """
        return os.path.isfile(filePath)

    def _isFolderNotNul(folderPath):
        """
        方法意味：フォルダが空でないかどうかを判断する
        params:
            folderPath: ソースパス
        return: なし
        """
        return os.listdir(folderPath)

    def _isFileNotNul(filePath):
        """
        方法意味：ファイルが空でないかどうかを判断する
        params:
            filePath: ソースパス
        return: なし
        """
        return os.path.getsize(filePath)

    def _isExistsFomatFile(folderPath,format):
        """
        方法意味：フォルダが空でないかどうかを判断する
        params:
            filePath: ソースパス
        return: なし
        """
        return any(name.endswith(format) for name in os.listdir(folderPath))

    def _createFolder(folderPath):
        """
        方法意味：新しい空フォルダーを生成
        params:
            folderPath: ソースパス
        return: なし
        """
        if not FileUtil._isExists(folderPath):
            if(os.path.isabs(folderPath)):
                os.makedirs(folderPath)
            else:
                os.makedirs(os.path.abspath(folderPath))

    def _createNewFile(filePath):
        """
        方法意味：新しい空のファイルを生成
        params:
            filePath: ソースパス
        return: なし
        """
        if not os.path.isabs(filePath):
            open(os.path.abspath(filePath), 'w', encoding='utf-8')
 
    def _bkFile(path, bkPath):
        """
        方法意味：ファイルをバックアップ
        params:
            path: ソースパス
            bkPath: 目的パス
        return: なし
        """
        for i in os.listdir(path):
            path_file = os.path.join(path,i)
            FileUtil._createFolder(bkPath)
            strCurrentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            bkFolderPath = bkPath + '/' + strCurrentTime
            FileUtil._createFolder(bkFolderPath)
            shutil.move(path_file, bkFolderPath)

    def _rmFile(path):
        """
        方法意味：ファイルを削除
        params:
            path: ソースパス
        return: なし
        """
        for i in os.listdir(path):
            path_file = os.path.join(path,i)
            if FileUtil._isFile(path_file):
                os.remove(path_file)
            else:
                for f in os.listdir(path_file):
                    path_file2 =os.path.join(path_file,f)
                    if FileUtil._isFile(path_file2):
                        os.remove(path_file2)

    def _zipDir(dirpath, outFullName):
        """
        方法意味：ファイルを削除
        params:
            dirpath: ソースパス,
            outFullName: 圧縮パス
        return: なし
        """
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_LZMA)
        for path, _, filenames in tqdm(os.walk(dirpath)):
            fpath = path.replace(dirpath, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()

    def _copyFile(oldFilePath, newFolderPath):
        """
        方法意味：copy file to folder
        params:
            oldFilePath: file
            newFolderPath: folder
        return: なし
        """
        shutil.copy(os.path.abspath(oldFilePath), os.path.abspath(newFolderPath))

    def _copyTree(oldFolderPath, newFolderPath):
        """
        方法意味：copy oldFolderPath  to newFolderPath
        params:
            oldFilePath: file
            newFolderPath: folder
        return: なし
        """
        shutil.copytree(oldFolderPath, newFolderPath, dirs_exist_ok=True)