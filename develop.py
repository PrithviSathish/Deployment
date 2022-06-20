import os
import filecmp
import shutil

dir1 = "./Dev"
dir2 = "./Test"
dir3 = "./Output"

def compare(dir1, dir2, dir3):

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    dirs_cmp2 = filecmp.dircmp(dir1, dir3)
    if len(dirs_cmp.left_only) != 0:
        # move the files or folder directly into output
        for x in dirs_cmp.left_only:
            source = os.path.join(dir1, x)
            # print(source)
            try:
                if os.path.isdir(source):
                    dest = os.path.join(dir3, x)
                    shutil.copytree(source, dest, dirs_exist_ok=True)

                if os.path.isfile(source):
                    dest = os.path.join(dir3)
                    # print(dest)
                    shutil.copy(source, dest)
            except FileExistsError:
                pass


    # Check for common files - compare and paste into output
    match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files)
    for y in mismatch:
        source = os.path.join(dir1, y)
        dest = os.path.join(dir3)
        shutil.copy(source, dest)

    # EDIT: This is to remove excess files in output
    for x in dirs_cmp2.right_only:
        os.remove(os.path.join(dir3, x))

    # Check for common directories - if so, go in and run compare once again
    for z in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, z)
        new_dir2 = os.path.join(dir2, z)
        new_dir3 = os.path.join(dir3, z)
        if not os.path.isdir(new_dir3):
            os.mkdir(new_dir3)
        compare(new_dir1, new_dir2, new_dir3)


def del_excess(dev, out):

    dirs_cmp2 = filecmp.dircmp(dev, out)
    print(dirs_cmp2.right_only)

    for x in dirs_cmp2.right_only:
        os.remove(os.path.join(out, x))

    for z in dirs_cmp2.common_dirs:
        new_dev = os.path.join(dev, z)
        new_out = os.path.join(out, z)
        del_excess(new_dev, new_out)


if not os.path.isdir(dir3):
    os.mkdir(dir3)

compare(dir1, dir2, dir3)
# del_excess(dir1, dir3)
