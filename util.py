import os.path


def make_directory(directory):
    """Make directory

    Args:
        directory: name of directory to be made

    Returns:
        True, if created successfully or already exists
        False, if failure
    """
    if not os.path.exists(directory):
        try:
            print("Making directory %s" % directory)
            os.makedirs(directory)
        except OSError as msg:
            print("Failed to create directory %s, because %s" % (directory, str(msg)))
            return False
    return True


def path_split(filename_with_path):
    fullfilename = os.path.abspath(filename_with_path)
    path, name = os.path.split(fullfilename)
    return path, name