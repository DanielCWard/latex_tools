# latex_tools
A few scripts to automatically process latex projects for easier online publishing.

## Functions
* Reducing the size of a project. By downsampling and resizing images one can significantly reduce the size of their compiled PDFs.
* Removing comments from all .tex files. This is can be important before uploading your project to somewhere like ArXiv where people can potentially access the raw tex files

# Setting Optimisation Parameters
Use the provided config.json as a guide. You can provide parameters for specific files if you want. The top level parameters are applied to all files unless a filename is specified in the special cases config field.

# Usage
1. Set options in the config.json file.
2. Run with ```python3 optimize_latex.py --tex_dir <path_to_latex_project_directory> --config <path_to_config_json>```

# Dependencies
* PIL >= v5.1.0

# TODO