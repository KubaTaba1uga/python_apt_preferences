def process_files_map(files_map, tmpdir):
    for file_path, file_content in files_map.items():
        local_dir = tmpdir

        if len(splitted_by_slash := file_path.split("/")) > 1:
            file_path = splitted_by_slash.pop()

            for dir_name in splitted_by_slash:
                new_dir = local_dir.ensure_dir(dir_name)
                local_dir = new_dir

        file_ = local_dir.join(file_path)
        file_.write_text(file_content, encoding="utf-8")
