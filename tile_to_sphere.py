import os
import  shutil

KRPANO_TOOL_PATH = "/Applications/krpano-1.21.2/krpanotools"

def stitch_tiles(input_dir, level, output_file, is_annotation):
    split_count = 2 ** (level - 1)
    temp_dir = os.path.abspath("temp_tiles")
    total_size =  512 * split_count
    print(f"total size: {total_size}")
    os.makedirs(temp_dir, exist_ok=True)
    for i in range(split_count):
        for j in range(split_count):
            # copy and rename file from input_dir/i/j.jpg to temp_dir/tile_i_j.jpg using shutil
            shutil.copyfile(os.path.join(input_dir, str(i), f"{j}{"_annotation" if is_annotation else ""}.jpg"), os.path.join(temp_dir, f"tile_{i+1}_{j+1}.jpg"))


    temp_dir = temp_dir.replace(" ", "\ ")
    output_file = output_file.replace(" ", "\ ")
    os.system(f"{KRPANO_TOOL_PATH} maketiles {temp_dir}/tile_%v_%h.jpg {output_file} -insize={total_size}x{total_size} -intilesize=512")
    # remove temp files
    os.system(f"rm -rf {temp_dir}")

    return output_file

def cube_to_sphere(input_dir, level=1, is_annotation=False):
    output_file = os.path.join(input_dir, f"merged_sphere_level_{level}.jpg") if not is_annotation else os.path.join(input_dir, f"merged_sphere_level_{level}_annotation.jpg")
    temp_dir = os.path.abspath("temp_faces")
    os.makedirs(temp_dir, exist_ok=True)
    for face in ["l", "r", "u", "d", "f", "b"]:
        output_face_file = os.path.join(temp_dir, f"face_{face}.jpg")
        stitch_tiles(os.path.join(input_dir, str(level), face), level, output_face_file, is_annotation)
    temp_dir = temp_dir.replace(" ", "\ ")
    os.system(f"{KRPANO_TOOL_PATH} cubetosphere  -l={temp_dir}/face_l.jpg -r={temp_dir}/face_r.jpg -u={temp_dir}/face_u.jpg -d={temp_dir}/face_d.jpg -f={temp_dir}/face_f.jpg -b={temp_dir}/face_b.jpg -o={output_file}")
    # remove temp files
    os.system(f"rm -rf {temp_dir}")

    return output_file

if __name__ == "__main__":
    input_dir = "/Users/davidyang/Downloads/Northeastern_Forest_Obliques/8928de8c9dbffff/8d62ebee-1ae9-4797-a597-40b8468c2f2d"
    cube_to_sphere(input_dir, 5)