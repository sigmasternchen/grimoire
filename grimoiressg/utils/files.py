import glob
import os


def to_relative(path):
    trimmed = path.removeprefix(os.getcwd())
    if trimmed != path:
        trimmed = "." + trimmed
    return trimmed


def for_each_glob(glob_path, callback):
    results = []

    for filename in glob.glob(os.path.realpath(glob_path)):
        results.extend(callback(filename))

    return results
