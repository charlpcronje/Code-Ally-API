# Module: Project Code and Documentation API

> This module provides a Flask-based API that serves code and documentation from configured projects. It uses environment variables for configuration, supports bearer authentication, and can return data in JSON or Markdown format.

## .env
```env
API_KEY=6b49e83f-c2a7-4d1d-9e5d-7f12c3e8567a
LOG_LEVEL=DEBUG
LOG_PATH=./logs/app.log
PORT=5000
```

## requirements.txt
```txt
Flask==2.3.2
python-dotenv==1.0.0
json5==0.9.11
```

## config.py
```python
# config.py
"""
@file config.py
@brief Loads environment variables and provides configuration to the app.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_PATH = os.getenv("LOG_PATH", "./logs/app.log")
    PORT = int(os.getenv("PORT", 5000))
```

## logger.py
```python
# logger.py
"""
@file logger.py
@brief Configures logging for the application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

# Ensure logs directory exists
os.makedirs(os.path.dirname(Config.LOG_PATH), exist_ok=True)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL.upper())

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(Config.LOG_LEVEL.upper())

    # File handler
    fh = RotatingFileHandler(Config.LOG_PATH, maxBytes=1048576, backupCount=5)
    fh.setLevel(Config.LOG_LEVEL.upper())

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
```

## utils/file_handler.py
```python
# utils/file_handler.py
"""
@file utils/file_handler.py
@brief Provides utilities for scanning directories, applying include/exclude patterns, 
      and reading file contents.
"""
import os
import fnmatch
from logger import get_logger

logger = get_logger(__name__)

class FileHandler:
    @staticmethod
    def scan_files(base_path, includes=None, excludes=None):
        """
        Scan files in base_path applying include and exclude patterns.
        includes and excludes are lists of glob-like patterns.
        """
        logger.debug(f"Scanning files in {base_path} with includes={includes}, excludes={excludes}")
        if not os.path.isabs(base_path):
            # If the base_path is relative, we assume it's relative to the project_path.
            # The caller should ensure correctness.
            pass

        all_files = []
        for root, dirs, files in os.walk(base_path):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if not FileHandler._matches_any(os.path.join(root, d), excludes, is_dir=True)]
            for f in files:
                full_path = os.path.join(root, f)
                # Check excludes
                if FileHandler._matches_any(full_path, excludes):
                    continue
                # Check includes if specified
                if includes:
                    if FileHandler._matches_any(full_path, includes):
                        all_files.append(full_path)
                else:
                    # If no includes specified, include all files unless excluded.
                    all_files.append(full_path)

        return all_files

    @staticmethod
    def _matches_any(path, patterns, is_dir=False):
        """Check if a path matches any given pattern. Patterns can use wildcards and **."""
        if not patterns:
            return False

        # Convert path separators to forward slash for consistency in matching
        normalized_path = path.replace(os.sep, "/")
        for p in patterns:
            # Patterns might also be something like "**/*.py,*.html"
            # We'll split by "," and check each.
            sub_patterns = [pt.strip() for pt in p.split(",")]
            for sp in sub_patterns:
                if fnmatch.fnmatch(normalized_path, sp):
                    return True
        return False

    @staticmethod
    def read_file(path):
        """Read the contents of a file and return as string."""
        logger.debug(f"Reading file {path}")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def ensure_json5_file(path, default_content):
        """
        Ensure a JSON5 file exists at 'path'. If not, create it with default_content.
        """
        logger.debug(f"Ensuring json5 file at {path}")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(default_content)
        return path
```

## services/project_service.py
```python
# services/project_service.py
"""
@file services/project_service.py
@brief Provides logic to load project configuration, read directories and files, 
       and return requested data for code, docs, components, modules, etc.
"""

import os
import json
import json5
import slugify
from logger import get_logger
from utils.file_handler import FileHandler

logger = get_logger(__name__)

class ProjectService:
    def __init__(self, project_name):
        """
        Load project config from ./projects/{project_name}.json and project.config.json5
        """
        self.project_name = project_name
        self.project_meta_path = os.path.join(".", "projects", f"{project_name}.json")
        
        if not os.path.isfile(self.project_meta_path):
            raise FileNotFoundError(f"Project meta file {self.project_meta_path} not found.")

        with open(self.project_meta_path, "r", encoding="utf-8") as f:
            self.project_meta = json.load(f)

        self.project_path = self.project_meta.get("project_path")
        if not self.project_path or not os.path.isdir(self.project_path):
            raise FileNotFoundError(f"Project path {self.project_path} not found.")

        # Load or create project.config.json5
        self.project_config_path = os.path.join(self.project_path, "project.config.json5")
        default_config = """{
    // Default project config
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
        "LitHtml",
        "Bootstrap 5"
    ],
    "spec": "path/to/project/spec.md",
    "tasks": "path/to/project/tasks.md",
    "modules": {},
    "components": {},
    "config": {},
    "docs": {}
}
"""
        FileHandler.ensure_json5_file(self.project_config_path, default_config)
        with open(self.project_config_path, "r", encoding="utf-8") as f:
            self.project_config = json5.load(f)

        self.exclude_patterns = self.project_meta.get("exclude", [])
        self.docs_path = self.project_meta.get("docs_path", "./docs")
        # docs_path might be relative to project_path
        if not os.path.isabs(self.docs_path):
            self.docs_path = os.path.join(self.project_path, self.docs_path)

    def authenticate(self, token: str):
        # Check token against API_KEY from env
        from config import Config
        logger.debug("Authenticating request")
        return token == f"Bearer {Config.API_KEY}"

    def get_project_info(self):
        logger.debug("Fetching project info")
        info = self.project_config.get("info", {})
        description = info.get("description", "No description")
        url = f"http://{self.project_name}.local"
        return {"description": description, "url": url}

    def get_project_stack(self):
        logger.debug("Fetching project stack")
        stack = self.project_config.get("stack", [])
        return stack

    def get_project_spec(self):
        logger.debug("Fetching project spec")
        spec_path = self.project_config.get("spec")
        if spec_path:
            if not os.path.isabs(spec_path):
                spec_path = os.path.join(self.project_path, spec_path)
            content = FileHandler.read_file(spec_path)
            return {"specification": content if content else ""}
        return {"specification": ""}

    def get_project_tasks(self):
        logger.debug("Fetching project tasks")
        tasks_path = self.project_config.get("tasks")
        if tasks_path:
            if not os.path.isabs(tasks_path):
                tasks_path = os.path.join(self.project_path, tasks_path)
            content = FileHandler.read_file(tasks_path)
            if content:
                # Return as list of tasks (each line as a task for demonstration)
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                return lines
        return []

    def get_project_config_files(self):
        logger.debug("Fetching project config files")
        config_info = self.project_config.get("config", {})
        includes = config_info.get("include", [])
        excludes = config_info.get("exclude", [])
        if isinstance(includes, dict):
            # If structured similarly to modules, handle that
            includes = includes.get("include", [])
        # If needed, we can consider base for config. For now assume project_path root.
        files = FileHandler.scan_files(self.project_path, includes, excludes)
        return files

    def get_project_files_by_category(self):
        """
        Return files in categories: core, config, components, admin, auth, schemas.
        This is user-defined logic. We'll assume:
        - core: *.py files in project_path (except excluded)
        - config: config files found from project config
        - components: from components config
        - admin: *admin* in filename
        - auth: *auth* in filename
        - schemas: *schema* in filename
        """
        logger.debug("Fetching project files by category")
        core = FileHandler.scan_files(self.project_path, excludes=self.exclude_patterns)
        # Filter categories by pattern
        def filter_by_pattern(files, pattern):
            return [f for f in files if pattern in os.path.basename(f).lower()]

        config_files = self.get_project_config_files()
        components = self.get_all_components_files()
        admin = filter_by_pattern(core, "admin")
        auth = filter_by_pattern(core, "auth")
        schemas = filter_by_pattern(core, "schema")

        # core: remove the admin/auth/schema files to avoid duplication
        used = set(admin+auth+schemas+config_files+components)
        core = [f for f in core if f not in used]

        return {
            "core": core,
            "config": config_files,
            "components": components,
            "admin": admin,
            "auth": auth,
            "schemas": schemas
        }

    def get_all_modules(self):
        logger.debug("Fetching modules")
        modules = self.project_config.get("modules", {})
        return list(modules.keys())

    def get_module_files(self, identifier):
        logger.debug(f"Fetching files for module {identifier}")
        modules = self.project_config.get("modules", {})
        if identifier not in modules:
            return []
        mod = modules[identifier]
        base = mod.get("base", self.project_path)
        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base)
        includes = mod.get("include", [])
        excludes = mod.get("exclude", [])
        files = FileHandler.scan_files(base, includes, excludes)
        return files

    def get_all_components(self):
        logger.debug("Fetching all components")
        comp = self.project_config.get("components", {})
        base = comp.get("base", "")
        index_by = comp.get("index_by", "file")
        file_groups = comp.get("file_groups", False)
        file_extension = comp.get("file_extension", "").split(",")
        identifier_mode = comp.get("identifier", "slugify")

        if not base:
            return []

        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base.lstrip("/."))

        includes = comp.get("include", {})
        if isinstance(includes, dict):
            includes = includes.get("include", [])
        excludes = comp.get("exclude", {} )
        if isinstance(excludes, dict):
            excludes = excludes.get("exclude", [])

        files = FileHandler.scan_files(base, includes, excludes)

        # Filter by extension
        filtered = []
        for f in files:
            ext = os.path.splitext(f)[1].lstrip(".")
            if ext in file_extension:
                filtered.append(f)

        if index_by == "folder":
            # Group by folder
            folders = {}
            for f in filtered:
                rel = os.path.relpath(f, base)
                folder = rel.split(os.sep)[0]
                folders.setdefault(folder, []).append(f)
            if identifier_mode == "slugify":
                return [slugify.slugify(k) for k in folders.keys()]
            else:
                return list(folders.keys())
        else:
            # index by file
            if file_groups:
                # Group files by base name
                groups = {}
                for f in filtered:
                    fname = os.path.splitext(os.path.basename(f))[0]
                    groups.setdefault(fname, []).append(f)
                if identifier_mode == "slugify":
                    return [slugify.slugify(k) for k in groups.keys()]
                else:
                    return list(groups.keys())
            else:
                # return every file as a component
                comps = []
                for f in filtered:
                    name = os.path.splitext(os.path.basename(f))[0]
                    if identifier_mode == "slugify":
                        name = slugify.slugify(name)
                    comps.append(name)
                return comps

    def get_component_files(self, identifier):
        logger.debug(f"Fetching files for component {identifier}")
        # Re-run logic of get_all_components but keep the grouping for actual files
        comp = self.project_config.get("components", {})
        base = comp.get("base", "")
        index_by = comp.get("index_by", "file")
        file_groups = comp.get("file_groups", False)
        file_extension = comp.get("file_extension", "").split(",")
        identifier_mode = comp.get("identifier", "slugify")

        if not base:
            return []

        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base.lstrip("/."))

        includes = comp.get("include", {})
        if isinstance(includes, dict):
            includes = includes.get("include", [])
        excludes = comp.get("exclude", {})
        if isinstance(excludes, dict):
            excludes = excludes.get("exclude", [])

        files = FileHandler.scan_files(base, includes, excludes)
        # Filter by extension
        filtered = [f for f in files if os.path.splitext(f)[1].lstrip(".") in file_extension]

        if index_by == "folder":
            # Find the folder that matches the identifier
            folders = {}
            for fpath in filtered:
                rel = os.path.relpath(fpath, base)
                folder = rel.split(os.sep)[0]
                folders.setdefault(folder, []).append(fpath)

            # Slugify check
            mapped = {}
            for k,v in folders.items():
                key = slugify.slugify(k) if identifier_mode == "slugify" else k
                mapped[key] = v

            return mapped.get(identifier, [])

        else:
            # index by file
            groups = {}
            for fpath in filtered:
                fname = os.path.splitext(os.path.basename(fpath))[0]
                key = slugify.slugify(fname) if identifier_mode == "slugify" else fname
                groups.setdefault(key, []).append(fpath)

            # If file_groups = true, then one identifier per group
            if file_groups:
                # identifier corresponds to a group
                return groups.get(identifier, [])
            else:
                # if file_groups=false each file is an identifier?
                # That would mean one file per component.
                # In that case, find the file that matches identifier
                # If file_groups=false, identifier is per-file's base name.
                return groups.get(identifier, [])

    def get_all_components_files(self):
        # Utility for listing all component files (for code categories)
        logger.debug("Fetching all components files")
        comp = self.project_config.get("components", {})
        base = comp.get("base", "")
        if not base:
            return []
        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base.lstrip("/."))

        includes = comp.get("include", {})
        if isinstance(includes, dict):
            includes = includes.get("include", [])
        excludes = comp.get("exclude", {})
        if isinstance(excludes, dict):
            excludes = excludes.get("exclude", [])

        files = FileHandler.scan_files(base, includes, excludes)
        return files

    def get_documentation_list(self):
        logger.debug("Fetching documentation list")
        docs = self.project_config.get("docs", {})
        base = docs.get("base", "")
        identifier_mode = docs.get("identifier", "slugify")

        if not base:
            return []

        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base.lstrip("/."))

        includes = docs.get("include", [])
        excludes = docs.get("exclude", [])

        files = FileHandler.scan_files(base, includes, excludes)
        # Filter for markdown files only
        docs_files = [f for f in files if f.endswith(".md")]

        # Identifier logic
        doc_ids = []
        for fpath in docs_files:
            fname = os.path.splitext(os.path.basename(fpath))[0]
            doc_id = slugify.slugify(fname) if identifier_mode == "slugify" else fname
            doc_ids.append(doc_id)

        return doc_ids

    def get_documentation_file(self, identifier):
        logger.debug(f"Fetching documentation file {identifier}")
        docs = self.project_config.get("docs", {})
        base = docs.get("base", "")
        identifier_mode = docs.get("identifier", "slugify")

        if not base:
            return None

        if not os.path.isabs(base):
            base = os.path.join(self.project_path, base.lstrip("/."))

        includes = docs.get("include", [])
        excludes = docs.get("exclude", [])
        files = FileHandler.scan_files(base, includes, excludes)
        md_files = [f for f in files if f.endswith(".md")]

        mapped = {}
        for fpath in md_files:
            fname = os.path.splitext(os.path.basename(fpath))[0]
            doc_id = slugify.slugify(fname) if identifier_mode == "slugify" else fname
            mapped[doc_id] = fpath

        selected = mapped.get(identifier)
        if selected:
            content = FileHandler.read_file(selected)
            title = os.path.basename(selected)
            return {"title": title, "content": content}
        return None

    def get_project_styles(self):
        # Similar logic as above. If styles are global, we can define in config.
        logger.debug("Fetching project styles")
        # For this example, assume styles are something like *.css files in project_path/styles
        styles_path = os.path.join(self.project_path, "styles")
        if not os.path.isdir(styles_path):
            return []
        files = FileHandler.scan_files(styles_path, excludes=self.exclude_patterns)
        css_files = [f for f in files if f.endswith(".css")]
        return css_files
```

## controllers/api.py
```python
# controllers/api.py
"""
@file controllers/api.py
@brief Defines the Flask routes and integrates with ProjectService.
"""
from flask import Blueprint, request, jsonify, Response
from services.project_service import ProjectService
from logger import get_logger
import os

logger = get_logger(__name__)
api_bp = Blueprint('api', __name__)

def authenticate_request(service: ProjectService):
    auth = request.headers.get('Authorization', '')
    if not service.authenticate(auth):
        return False
    return True

def respond_json(data):
    return jsonify({"status": "success", "data": data})

def respond_error(msg, code=400):
    return jsonify({"status": "error", "message": msg}), code

def respond_markdown(md_content):
    return Response(md_content, mimetype='text/markdown')

@api_bp.route("/<project>/info", methods=["GET"])
def get_project_info(project):
    logger.debug("GET /<project>/info called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        fmt = request.args.get("in", "md")
        data = svc.get_project_info()
        if fmt == "json":
            return respond_json(data)
        else:
            md = f"# Project Info\n**Description:** {data['description']}\n**URL:** {data['url']}"
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/stack", methods=["GET"])
def get_project_stack(project):
    logger.debug("GET /<project>/stack called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        data = svc.get_project_stack()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(data)
        else:
            md = "# Project Stack\n" + "\n".join([f"- {item}" for item in data])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/spec", methods=["GET"])
def get_project_spec(project):
    logger.debug("GET /<project>/spec called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        data = svc.get_project_spec()
        fmt = request.args.get("in", "md")
        content = data.get("specification","")
        if fmt == "json":
            return respond_json(data)
        else:
            md = f"# Project Specification\n```markdown\n{content}\n```"
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/tasks", methods=["GET"])
def get_project_tasks(project):
    logger.debug("GET /<project>/tasks called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        tasks = svc.get_project_tasks()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(tasks)
        else:
            md = "# Project Tasks\n" + "\n".join([f"- {t}" for t in tasks])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/config", methods=["GET"])
def get_project_config(project):
    logger.debug("GET /<project>/config called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        files = svc.get_project_config_files()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(files)
        else:
            md = "# Project Config Files\n" + "\n".join([f"- {f}" for f in files])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code", methods=["GET"])
def list_all_project_files(project):
    logger.debug("GET /<project>/code called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        data = svc.get_project_files_by_category()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(data)
        else:
            # Convert to markdown
            md = "# Project Files\n"
            for cat, files in data.items():
                md += f"## {cat.capitalize()}\n"
                for f in files:
                    md += f"- {f}\n"
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code/modules", methods=["GET"])
def list_all_modules(project):
    logger.debug("GET /<project>/code/modules called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        modules = svc.get_all_modules()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(modules)
        else:
            md = "# Modules\n" + "\n".join([f"- {m}" for m in modules])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code/module/<identifier>", methods=["GET"])
def get_specific_module_files(project, identifier):
    logger.debug("GET /<project>/code/module/<identifier> called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        files = svc.get_module_files(identifier)
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(files)
        else:
            md = f"# Module: {identifier}\n" + "\n".join([f"- {f}" for f in files])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code/components", methods=["GET"])
def list_all_components(project):
    logger.debug("GET /<project>/code/components called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)
        comps = svc.get_all_components()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(comps)
        else:
            md = "# Components\n" + "\n".join([f"- {c}" for c in comps])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code/component/<identifier>", methods=["GET"])
def get_specific_component_code(project, identifier):
    logger.debug("GET /<project>/code/component/<identifier> called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        files = svc.get_component_files(identifier)
        fmt = request.args.get("in", "md")

        if fmt == "json":
            # Return JSON with files and their contents
            data = {}
            for f in files:
                data[os.path.basename(f)] = FileHandler.read_file(f)
            return respond_json({"component_name": identifier, "files": data})
        else:
            # Return a markdown combined
            md = f"# Component: {identifier}\n"
            for f in files:
                ext = os.path.splitext(f)[1].lstrip(".")
                content = FileHandler.read_file(f)
                md += f"\n## {os.path.basename(f)}\n```{ext}\n{content}\n```\n"
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/docs", methods=["GET"])
def list_documentation(project):
    logger.debug("GET /<project>/docs called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        docs = svc.get_documentation_list()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(docs)
        else:
            md = "# Documentation\n" + "\n".join([f"- {d}" for d in docs])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/docs/<identifier>", methods=["GET"])
def get_specific_documentation(project, identifier):
    logger.debug("GET /<project>/docs/<identifier> called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        doc = svc.get_documentation_file(identifier)
        if not doc:
            return respond_error("Not found", 404)

        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(doc)
        else:
            md = f"# {doc['title']}\n```markdown\n{doc['content']}\n```"
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)

@api_bp.route("/<project>/code/styles", methods=["GET"])
def get_project_styles(project):
    logger.debug("GET /<project>/code/styles called")
    try:
        svc = ProjectService(project)
        if not authenticate_request(svc):
            return respond_error("Unauthorized", 401)

        styles = svc.get_project_styles()
        fmt = request.args.get("in", "md")
        if fmt == "json":
            return respond_json(styles)
        else:
            md = "# Styles\n" + "\n".join([f"- {s}" for s in styles])
            return respond_markdown(md)
    except Exception as e:
        logger.error(str(e))
        return respond_error(str(e), 500)
```

## main.py
```python
# main.py
"""
@file main.py
@brief Entry point for the Flask application.
"""
from flask import Flask
from controllers.api import api_bp
from config import Config
from logger import get_logger

logger = get_logger(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    @app.route("/health", methods=["GET"])
    def health():
        logger.debug("Health check endpoint called")
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT, debug=False)
```

\n
\n
