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
    clean_lines = comment_cleaner(f_lines)
    s_path = f_path.replace('.tex', '-clean.tex')
    save_file_lines(clean_lines, s_path)

