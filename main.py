import os, shutil, json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_source_path(data):
    if 'source_path' in data and data['source_path'] is None:
        data['source_path'] = os.getcwd()
    return data['source_path']

class FileGroup:
    def __init__(self, type, sub_type, extensions, substrings, alt_subtype=None):
        self.type = type
        self.sub_type = sub_type
        self.extensions = extensions
        self.substrings = substrings
        self.alt_subtype = alt_subtype

video_group = FileGroup(type='media', sub_type='video', extensions=['.mpeg', '.mp4', '.mov', '.wmv', '.flv', '.mkv', '.avi', '.f4v'],substrings=None, alt_subtype=None)
audio_group = FileGroup(type='media', sub_type='audio', extensions=['.mp3', '.wav', '.flac', '.ogg'],substrings=None, alt_subtype=None)
image_group = FileGroup(type='media', sub_type='image', extensions=['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.apng', '.avif', '.svg'],substrings=None, alt_subtype=None)
invoice_group = FileGroup(type='docs', sub_type='invoice', extensions=['.pdf'], substrings=['invoice', 'rechnung'], alt_subtype='readonly')
readonly_group = FileGroup(type='docs', sub_type='readonly', extensions=['.pdf'],substrings=None, alt_subtype=None)
changeable_group = FileGroup(type='docs', sub_type='changeable', extensions=['.txt', '.nfo,', '.xls', '.xlsx', '.doc', '.docx', '.ppt', '.pptx'],substrings=None, alt_subtype=None)
dev_group = FileGroup(type='data', sub_type='devdocs', extensions=['.md', '.csv', '.xml', '.drawio'],substrings=None, alt_subtype=None)
dimg_group = FileGroup(type='data', sub_type='disk_images', extensions=['.iso', '.dmg', '.img', '.disk'],substrings=None, alt_subtype=None)
installer_group = FileGroup(type='exec', sub_type='installer', extensions=['.exe', '.msi'], substrings=['install', 'setup'], alt_subtype='execute')
exec_group = FileGroup(type='exec', sub_type='execute', extensions=['.exe', '.msi'],substrings=None, alt_subtype=None)
script_group = FileGroup(type='exec', sub_type='script', extensions=['.bat', '.sh', '.cmd'],substrings=None, alt_subtype=None)
archive_group = FileGroup(type='data', sub_type='archive', extensions=['.rar', '.zip', '.7z'],substrings=None, alt_subtype=None)

# Liste mit beiden Objekten
def get_media_groups():
    return [video_group, audio_group, image_group, invoice_group, readonly_group, changeable_group, installer_group, exec_group, script_group, archive_group, dimg_group, dev_group]


def check_file_type(filename):
    file_groups = get_media_groups()
    for filegroup in file_groups:
        for extension in filegroup.extensions:
            if filename.lower().endswith(extension):
                if filegroup.substrings is not None:
                    for substring in filegroup.substrings:
                        if substring in filename.lower():
                            return [filegroup.type, filegroup.sub_type]
                elif filegroup.alt_subtype is not None:
                    return [filegroup.type, filegroup.alt_subtype]
                else:
                    return [filegroup.type, filegroup.sub_type]
    return [None, None]         
def main():
    if os.path.exists('config-personal.json'):
        file_path = 'config-personal.json'
    else:
        file_path = 'config.json'
    data = read_json(file_path)
    source_path = read_source_path(data)
    destination_path = data['destination_path'] if data['destination_path'] is not None else source_path
    for folders, subfolders, filenames in os.walk(source_path):
        for filename in filenames:
            if folders == source_path:
                complete_path_source = folders + '/' + filename
                [ file_type, sub_type ] = check_file_type(filename)
                if file_type is not None:
                    if os.path.exists(destination_path):
                        os.chdir(destination_path)
                        if not os.path.exists(file_type):
                            os.mkdir(file_type)
                        os.chdir(file_type)
                        if sub_type is not None:
                            if not os.path.exists(sub_type):
                                os.mkdir(sub_type)
                            os.chdir(sub_type)
                        complete_path_dest = os.getcwd() + '/' + filename
                        shutil.move(complete_path_source, complete_path_dest)
                        
                    else: 
                        raise Exception("Defined destination path does not exist, check your typing")



if __name__ == "__main__":
    main()








