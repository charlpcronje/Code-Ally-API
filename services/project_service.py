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
