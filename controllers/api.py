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
