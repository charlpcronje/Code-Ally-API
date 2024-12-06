# Prompts for the API
Below are the prompts that were used to create the API.
## Original Prompt
The following was prompted or o1.

I have the following OpenAI Schema for an API, I wan you to help me to create the API with Python / Flask:
```yml
openapi: 3.1.0
info:
  title: Project Code and Documentation API
  version: 1.0.0
  description: >
    This API allows fetching code and documentation organized by project. It supports authentication and can respond in
    JSON or Markdown format. By default, if the "in" parameter is not specified, the response will be in Markdown.
servers:
  - url: https://example.com/api
paths:
  /{project}/code:
    get:
      operationId: listAllProjectFiles
      summary: Get list of all files categorized by type
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: List of files
          content:
            application/json:
              schema:
                type: object
                properties:
                  core:
                    type: array
                    items:
                      type: string
                  config:
                    type: array
                    items:
                      type: string
                  components:
                    type: array
                    items:
                      type: string
                  admin:
                    type: array
                    items:
                      type: string
                  auth:
                    type: array
                    items:
                      type: string
                  schemas:
                    type: array
                    items:
                      type: string
        "401":
          description: Unauthorized
  /{project}/code/modules:
    get:
      operationId: listAllModules
      summary: Get list of all modules
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: List of modules
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized
  /{project}/code/components:
    get:
      operationId: listAllComponents
      summary: Get list of all components
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: List of components
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized
  /{project}/code/component/{identifier}:
    get:
      operationId: getSpecificComponentCode
      summary: Get the code for a specific component
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: identifier
          in: path
          required: true
          description: Component identifier (ID or slug)
          schema:
            oneOf:
              - type: string
              - type: integer
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Specific component code
          content:
            application/json:
              schema:
                type: object
                properties:
                  component_name:
                    type: string
                  code:
                    type: string
        "401":
          description: Unauthorized
  /{project}/code/module/{identifier}:
    get:
      operationId: getSpecificModuleFiles
      summary: Get files in a specific module
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: identifier
          in: path
          required: true
          description: Module identifier (ID or slug)
          schema:
            oneOf:
              - type: string
              - type: integer
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Specific module files
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized
  /{project}/docs:
    get:
      operationId: listDocumentation
      summary: Get a list of all documentation files
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Documentation list
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized
  /{project}/docs/{identifier}:
    get:
      operationId: getSpecificDocumentation
      summary: Get a specific documentation file
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: identifier
          in: path
          required: true
          description: Documentation identifier (ID or slug)
          schema:
            oneOf:
              - type: string
              - type: integer
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Specific documentation
          content:
            application/json:
              schema:
                type: object
                properties:
                  title:
                    type: string
                  content:
                    type: string
        "401":
          description: Unauthorized

  /{project}/info:
    get:
      operationId: getProjectInfo
      summary: Get all the project's info
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Project info
          content:
            application/json:
              schema:
                type: object
                properties:
                  description:
                    type: string
                  url:
                    type: string
        "401":
          description: Unauthorized

  /{project}/code/styles:
    get:
      operationId: getProjectStyles
      summary: Get global project styles
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: List of styles
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized

  /{project}/stack:
    get:
      operationId: getProjectStack
      summary: Get the tech stack of the project
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Tech stack
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized

  /{project}/spec:
    get:
      operationId: getProjectSpecification
      summary: Get the project specification
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Project specification
          content:
            application/json:
              schema:
                type: object
                properties:
                  specification:
                    type: string
        "401":
          description: Unauthorized

  /{project}/tasks:
    get:
      operationId: getProjectTasks
      summary: Get the list of project tasks
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: List of tasks
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized

  /{project}/config:
    get:
      operationId: getProjectConfig
      summary: Get the project's config files
      parameters:
        - name: project
          in: path
          required: true
          schema:
            type: string
        - name: in
          in: query
          required: false
          schema:
            type: string
            enum:
              - json
              - md
            default: md
      responses:
        "200":
          description: Project config files
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
        "401":
          description: Unauthorized
components:
  schemas: {}
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
security:
  - BearerAuth: []

```

What the schema does not tell us is the following
- Each endpoint begins with /{project}
/{project} refers to a JSON file at ./projects/{project}.json

```json
{
    "project_path": "/absolute/project/path",         // Absolute path to project 
    "docs_path": "./docs",                            // Relative path from project_path
    "exclude": [
        "node_modules"                                // paths to exclude from everything relative to project_path
    ]
}
```

Then inside the project path the API must either find or add a file named: project.config.json, if the file is not found the API will create it with the following structure:
```json
{   
    "info": {
        "title": "Project Title",
        "description": "Project Description",
        "version": "1.0.0",
        "author": "Author Name",
        "license": "MIT"
    },
    "stack": [
        "Astro 5",
        "LitElement",
        "LitHtml"
        "Bootstrap 5"
    ],
    "spec": "path/to/project/spec.md",                    // relative path to project spec in markdown format
    "tasks": "path/to/project/tasks.md"                   // relative path to project tasks in markdown format
    "modules":  {
        "config: {
            "name": "Config Module",
            "base": "module/base/path/*",                 // This is optional, if `base` is specified then all the paths below will be relative to this module's base path, if it is not specified, then all paths are relative to the `project_path`
            "include": [                                  // If no includes are specified then all the files must be included in the module's `base` and all the sub-folders if base is defined with module/base/path/**/*. The base can also be specified with "/module/base/path/*.py,*.json,*.html"
                "specific/file/to/include.py",            // Specific file to include    
                "folder/to/include/*",                    // Include all files in this folder
                "folder/to/include/*.py",                 // Include all .py files in this folder, this can override the base 
                "folder/to/include/*.py,*.html",          // Can also have multiple file extensions separated by ","
                "folder/to/include/**/*",                 // Include all files in folder and sub folders
                "folder/to/include/**/*.py",              // Include all .py files in this folder and sub-folders
                "folder/to/include/**/*.py,*.html"        // Can also have multiple file extensions separated by ","
             ]
            "exclude: [
                 "path/to/file.txt",                   // Exclude specific file,
                 "folder/to/exclude",                  // This could be one of the sub-folder of base or any folder specified above
                 "**/*.txt",                           // File Extension to exclude from all includes
                 "folder/*.txt",                       // File Extension to exclude from specific folder
                 "folder/**/*.txt",                    // File Extension to exclude from specific folder and sub-folders
                 "folder/**/filename.log               // File to be excluded from ll folders and sub-folders for  ./folder
             ]
        },
        "user": {
            "name": "Users Module",
            "base": "path/to/module/*" 
        }
    },
    "components": {
        "base": "/components/**/*.svelte,*.vue,*.astro",   // Path where the components are located
        "index_by": "folder",   file / folder              // When listing components, is every file a component or is every folder a component one
        "file_groups": true,                               // If true then just one component will be listed
        "file_extension": "svelte,vue,astro"               // File extensions to be considered as components
        "identifier": "slugify"                            // list all the files without the extension and slugify the name for the identifier, if false then the file name will be used as the identifier
        "include": {
            // Same rules as for modules
        },
        "exclude": {
            // Same rules as for modules
        }
    },
    "config": [
        "include": [
            // same as modules include
        ],
        exclude: [
            // same as modules exclude
        ]
    ],
    "docs": {
       "base": "/docs/**/*.md",
       "include": [
            // same rules as for modules
       ],
       "exclude": [
           "folder/to/exact/from/docs",
           "file/to/exclude/from/docs/file.md"
           ... // All the same rules as for the modules
       ],
       identifier: "slugify"                              // list all the files without the extension and slugify the name for the identifier, if false then the file name will be used as the identifier
    },
    
}
```

## Coding Rules that must be followed
- make the API modular
- use .env file for any settings beyond what I mentioned
- start each file with the relative path and file name
- Always provide production ready code
- Do not use placeholders in the code, only full files with no omissions
- when giving updates to files, do not remove  the comments
- When you are not giving entire files, then at the least give full method / functions at a time and be sure to say which file they must open and give a search string for the user so that he can find the exact place easily
- Use classes above functional where possible.
- Rather ask if anything is unclear before you begin.
- Create a response template so that all responses will have the same shape
- Add error checking and error handling to all the code
- Add a logger to the app that can be switched of or on or whatever in the .env
- add the port number the app will run on in .env
- When multiple files have to be returned then add all of them to a markdown doc that looks like

````
# Module: {module name} 

> Module description

## {filename}
```{file_extension}
{File contents}
```
\n
\n

## {filename}
```{file_extension}
{File contents}
```
\n
\n
````

Even if you are just giving a single file, then still wrap the file in the style above.

The JSON response should be obvious or come up with a consistent style for the JSON response.

## The AI Response

I have the following OpenAI Schema for an API, I want you to help me create the API with Python/Flask." 

Below is my response with any spelling or grammar fixes made by changing the least amount of characters:

I have the following OpenAI Schema for an API. I want you to help me to create the API with Python/Flask. Please let me know if there is anything specific that is unclear or that you would like me to clarify before you begin implementing the code.

I noticed that the instructions mention asking if anything is unclear before starting. I have a few questions and points I would like to clarify:

1. For authentication (BearerAuth), is there a specific token validation method, or should I stub this out with a dummy check?
2. The `exclude` rules and `include` rules can get quite complex. Should I implement a full file scanning and filtering system that respects all of these `include` and `exclude` patterns (like using glob patterns), or should I just demonstrate the logic and use simplified file scanning?
3. For the `project.config.json` file creation, if it does not exist, do you want it automatically populated with default values, or do you want an error response if it is missing?
4. The schema references multiple endpoints that return code, docs, and other content. Are these endpoints just reading files from the specified `project_path`, `docs_path`, etc., and returning them as responses? Similarly, when a `spec` or `tasks` file is referenced, should I just read that file’s content from the file system and return it?
5. For logging, can I use Python’s built-in `logging` module, and should the log level be configurable via `.env`?
6. For the response templates and JSON responses, is it correct to assume that all successful responses will be JSON (unless the user sets `in=md`, in which case I format the response as Markdown)? If `in=md` is provided, do you want me to convert the file contents into Markdown code blocks, or just return the raw file content as Markdown?
7. For `index_by` and `file_groups` in components, would you like a specific interpretation, such as if `file_groups` is true, grouping all component files under a single component name, or should I just return them as-is based on `index_by` logic?

Please let me know on these points, and once I have your clarification, I will proceed with a fully fleshed-out, production-ready code solution following all the rules provided.

## My Response to AI
1. There should be an API key saved in the .env file, here is the one to start with: 6b49e83f-c2a7-4d1d-9e5d-7f12c3e8567a 
2. If glob patterns can do the same, then please use that, just make sure to explain it when you are done and give a json file like I gave you with the same examples with that pattern then is will be fine
3. If project.config.json does not exist, then please create it with any defaults or just with comments, if you can use json5 so that comments are allowed then that would be a bonus
4. It should just read that file contents and return it and if there are multiple files then combine them like I demonstrated above 
5.  Yes configure the log level in the .env, and there must be at least one log in each function and method that writes to both a file and to the terminal depending on the log level, and the logs folder path must also be in .env
6. These responses will go direct to a custom GPT, so whatever form the GPT will easiest understand should be default if not specified.
7. When it is index_by folder then each folder will be a component, but in the case of index_by files then the could be components that look like

files
```sh
panelComponent.svelte
panelComponent.css
panelComponent.js
```

So when it is grouped then the component should just be listed as panelComponent. But when you respond with a  single component the you must respond with all the file combined like I showed in markdown or all the files in json objects the same as the headings in markdown

## AI Response with Code

"Can you give me a simple script that will parse the code block you just gave me and create all the files and put the content in each, I'll save the code blocks contents in all.md?"

Below is my response with minimal grammar and spelling changes:

Can you give me a simple script that will parse the code blocks I just gave you and create all the files, putting the content of each block into its respective file? I will save the code blocks content in `all.md` before running the script.

Below is a Python script that does the following:

1. Reads the file `all.md`.
2. Searches for code blocks in the markdown file. Each code block is preceded by a line starting with `## {filename}`.
3. Extracts the filename from that line.
4. Reads the code fence (the line with triple backticks and possibly a language specifier) and then captures all subsequent lines until another triple backticks line.
5. Creates the file and writes the code block content into it.

**Notes:** 
- The script assumes that for each `## {filename}` line, the next code fence block ``` will contain the code for that file.
- The script also assumes that each file only has one code block following its title line.
- Make sure you have write permissions in the directory where the files will be created.
- If a file already exists, it will be overwritten.

````markdown
# Module: File Extraction Script

> This script parses `all.md` and creates files from code blocks.

## create_files.py
```python
import os
import re

def parse_markdown_for_files(input_file):
    """
    Parse the given markdown file and extract code blocks along with their target filenames.
    This function assumes a pattern like:
    ## filename.ext
    ```language
    ... code ...
    ```
    """
    files_content = {}
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filename_pattern = re.compile(r"^##\s+(.*)$")
    code_block_start_pattern = re.compile(r"^```")
    
    current_filename = None
    capturing = False
    code_lines = []

    for line in lines:
        line_stripped = line.rstrip("\n")

        if not capturing:
            # Look for filename line
            match = filename_pattern.match(line_stripped)
            if match:
                current_filename = match.group(1).strip()
                code_lines = []  # Reset code lines for this file
                continue

            # If we have a current_filename and we find a code block start:
            if current_filename and code_block_start_pattern.match(line_stripped):
                # Start capturing code lines
                capturing = True
                continue
        else:
            # We are capturing code until we hit a code_block end
            if code_block_start_pattern.match(line_stripped):
                # End of code block
                capturing = False
                # Store the captured lines into the dictionary
                files_content[current_filename] = "\n".join(code_lines) + "\n"
                current_filename = None
                code_lines = []
            else:
                code_lines.append(line_stripped)

    return files_content

def create_files_from_markdown(input_file):
    files_content = parse_markdown_for_files(input_file)
    for fname, content in files_content.items():
        # Ensure directory structure if any
        dir_name = os.path.dirname(fname)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Created {len(files_content)} files.")

if __name__ == "__main__":
    create_files_from_markdown("all.md")
```
\n
\n
````

**How this works:**  
- Save the large combined code block you got previously into a file named `all.md`.
- Run the `create_files.py` script.
- The script will parse `all.md` for lines starting with `## filename` and then look for the code fenced section that follows, and write all that code into `filename`.

For example, if `all.md` contains:
````markdown
## some/path/to/file.py
```python
print("Hello world")
```
````

The script will create `some/path/to/file.py` and write `print("Hello world")` into it.

## My Final Final Code Request

Can you give me a simple script that will parse the code block you just gave me and create all the files and put the content in each, ill save the code blocks contents in all.md

## AI's final code response

"Can you give me a simple script that will parse the code block you just gave me and create all the files and put the content in each, I'll save the code blocks contents in all.md?"

Below is my response with minimal grammar and spelling changes:

Can you give me a simple script that will parse the code blocks I just gave you and create all the files, putting the content of each block into its respective file? I will save the code blocks content in `all.md` before running the script.

Below is a Python script that does the following:

1. Reads the file `all.md`.
2. Searches for code blocks in the markdown file. Each code block is preceded by a line starting with `## {filename}`.
3. Extracts the filename from that line.
4. Reads the code fence (the line with triple backticks and possibly a language specifier) and then captures all subsequent lines until another triple backticks line.
5. Creates the file and writes the code block content into it.

**Notes:** 
- The script assumes that for each `## {filename}` line, the next code fence block ``` will contain the code for that file.
- The script also assumes that each file only has one code block following its title line.
- Make sure you have write permissions in the directory where the files will be created.
- If a file already exists, it will be overwritten.

````markdown
# Module: File Extraction Script

> This script parses `all.md` and creates files from code blocks.

## create_files.py
```python
import os
import re

def parse_markdown_for_files(input_file):
    """
    Parse the given markdown file and extract code blocks along with their target filenames.
    This function assumes a pattern like:
    ## filename.ext
    ```language
    ... code ...
    ```
    """
    files_content = {}
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filename_pattern = re.compile(r"^##\s+(.*)$")
    code_block_start_pattern = re.compile(r"^```")
    
    current_filename = None
    capturing = False
    code_lines = []

    for line in lines:
        line_stripped = line.rstrip("\n")

        if not capturing:
            # Look for filename line
            match = filename_pattern.match(line_stripped)
            if match:
                current_filename = match.group(1).strip()
                code_lines = []  # Reset code lines for this file
                continue

            # If we have a current_filename and we find a code block start:
            if current_filename and code_block_start_pattern.match(line_stripped):
                # Start capturing code lines
                capturing = True
                continue
        else:
            # We are capturing code until we hit a code_block end
            if code_block_start_pattern.match(line_stripped):
                # End of code block
                capturing = False
                # Store the captured lines into the dictionary
                files_content[current_filename] = "\n".join(code_lines) + "\n"
                current_filename = None
                code_lines = []
            else:
                code_lines.append(line_stripped)

    return files_content

def create_files_from_markdown(input_file):
    files_content = parse_markdown_for_files(input_file)
    for fname, content in files_content.items():
        # Ensure directory structure if any
        dir_name = os.path.dirname(fname)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Created {len(files_content)} files.")

if __name__ == "__main__":
    create_files_from_markdown("all.md")
```
\n
\n
````

**How this works:**  
- Save the large combined code block you got previously into a file named `all.md`.
- Run the `create_files.py` script.
- The script will parse `all.md` for lines starting with `## filename` and then look for the code fenced section that follows, and write all that code into `filename`.

For example, if `all.md` contains:
````markdown
## some/path/to/file.py
```python
print("Hello world")
```
````

The script will create `some/path/to/file.py` and write `print("Hello world")` into it.