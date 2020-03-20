def get_file_from_input(line):
    """
    Returns the file path from line containing the \input latex command

    @param line: a line from a file as a string
    @return: the path to the file
    """
    start_idx = -1
    for i, char in enumerate(line):
        if char == '{':
            start_idx = i
            break
    
    line = line[start_idx+1:]
    new_end = -1
    for i, char in enumerate(line):
        if char == '}':
            new_end = i
            break

    line = line[:new_end]
    return line

    # First remove the tail of the line if any
    # new_end = -1
    # for i, char in enumerate(line):
    #     if char == '}':
    #         new_end = i
    #         break
    # line = line[:new_end]

    # line.replace('\\input{', '')
    # line.replace('}', '')
    # return line

def get_file_from_includegraphics(line):
    """
    Returns the file path from line containing the \includegraphics latex command

    @param line: a line from a file as a string
    @return: the path to the file
    """
    start_idx = -1
    for i, char in enumerate(line):
        if char == '{':
            start_idx = i
            break
    
    line = line[start_idx+1:]
    new_end = -1
    for i, char in enumerate(line):
        if char == '}':
            new_end = i
            break

    line = line[:new_end]
    return line

def get_referenced_files(file_lines):
    """
    Gets a list of filenames or relative paths of images and files which are used in the doc
    This allows one to delete figures which are not used

    At present this function only checks for files based on \input and \includegraphics

    ideally this function should utilize the functions of a latex compiler

    @param file_lines: a list of strings for lines in the file
    @return a list of filenames / paths
    """
    referenced_files = []
    for line in file_lines:
        if '\input' in line:
            referenced_files.append(get_file_from_input(line))
        elif '\includegraphics' in line:
            referenced_files.append(get_file_from_includegraphics(line))
    
    return referenced_files

def line_cleaner(line):
    """
    Removes anything after a '%' unless it is escaped '\%'.

    @param line: a string representing a line of a file
    @return the cleaned line
    """
    new_end = -1
    for i, char in enumerate(line):
        if char == '%' and line[i-1] != '\\':
            new_end = i
            break

    if new_end > 0:
        line =  line[:new_end+1] + '\n'
    elif new_end == 0:
        line = '%\n'

    return line

def comment_cleaner(file_lines):
    """
    Iterates through the file lines
    For each line if a '%' (latex comment symbol) is encountered the remainder of the line is removed

    @param file_lines a list of strings for lines in the file
    @return a list of strings representing the lines of the file after cleaning
    """
    cleaned_lines = list(map(line_cleaner, file_lines))
    return cleaned_lines

def load_file_lines(file_path):
    """
    Loads a text file and returns a list of the file lines

    @param file_path: the path to the file
    """
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
    return lines

def save_file_lines(file_lines, file_path):
    """
    Saves the file lines to the provided path

    @param file_path: the path to save file
    @param file_lines: The lines to write to the file
    """
    with open(file_path, 'w') as fp:
        for line in file_lines:
            fp.write(line)

if __name__ == '__main__':
    """
    Testing code
    """
    
    f_path = 'ycviu-template-with-authorship-referees.tex'
    f_lines = load_file_lines(f_path)
    print(get_referenced_files(f_lines))
    clean_lines = comment_cleaner(f_lines)
    s_path = f_path.replace('.tex', '-clean.tex')
    save_file_lines(clean_lines, s_path)

