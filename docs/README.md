# Project Code and Documentation API

Welcome to the **Project Code and Documentation API**! This API provides endpoints to fetch code files, documentation, component code, modules, and various other project-specific data. It supports both JSON and Markdown responses and is secured with Bearer token authentication.

- **Author:** Charl Cronje  
- **Contact:** [charl@webally.co.za](mailto:charl@webally.co.za)  
- **More Info / CV:** [https://cv.webally.co.za](https://cv.webally.co.za)  

## Overview

This API is built to help developers easily access project-related resources, such as:
- Lists of project files categorized by type (core, config, components, etc.)
- Detailed module and component listings
- Global project styles
- Project stack, specification, and tasks
- Documentation files

It supports returning responses in JSON or Markdown format. Use the `?in=json` or `?in=md` query parameter to specify the format. By default, the response is Markdown if the `in` parameter is not set.

## Authentication

All endpoints require a valid Bearer token. Include the following header in your requests:
```
Authorization: Bearer <YOUR_API_KEY>
```

The API key is stored in an `.env` file. If you need a key, please contact the API owner.

## Schema

For a detailed look at the OpenAPI specification of the API, see the [OpenAISchema.yml](./OpenAISchema.yml) file.

## Full Documentation

For more in-depth details, guides, and examples, please refer to the [Full Documentation](./docs/README.md).

## Base URL

```
https://ally.code.webally.co.za
```

## Endpoints and Responses

Below is a comprehensive list of endpoints. For each endpoint:
- `{project}` is a placeholder for your actual project name.
- The `in` query parameter can be `json` or `md`. If not provided, `md` is used by default.

### 1. Get Project Info

**Endpoint:** `GET /{project}/info`  
**Description:** Returns the project's info, including a description and URL.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": {
    "description": "Project Description",
    "url": "http://project.local"
  }
}
```

### 2. Get Project Stack

**Endpoint:** `GET /{project}/stack`  
**Description:** Returns the tech stack used by the project.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "Astro 5",
    "LitElement",
    "LitHtml",
    "Bootstrap 5"
  ]
}
```

### 3. Get Project Specification

**Endpoint:** `GET /{project}/spec`  
**Description:** Returns the project's specification in markdown or JSON.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": {
    "specification": "# Project Spec\nThis is the specification..."
  }
}
```

### 4. Get Project Tasks

**Endpoint:** `GET /{project}/tasks`  
**Description:** Returns the project's tasks, usually from a tasks markdown file.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "Task 1",
    "Task 2",
    "Task 3"
  ]
}
```

### 5. Get Project Config Files

**Endpoint:** `GET /{project}/config`  
**Description:** Returns a list of configuration files for the project.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "/absolute/project/path/config.json",
    "/absolute/project/path/settings.py"
  ]
}
```

### 6. Get Project Files by Category

**Endpoint:** `GET /{project}/code`  
**Description:** Returns categorized files: core, config, components, admin, auth, schemas.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": {
    "core": ["file1.py", "file2.py"],
    "config": ["config.yaml"],
    "components": ["component1.svelte"],
    "admin": ["admin_panel.py"],
    "auth": ["auth_service.py"],
    "schemas": ["schema.json"]
  }
}
```

### 7. List All Modules

**Endpoint:** `GET /{project}/code/modules`  
**Description:** Returns a list of all modules defined in `project.config.json5`.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "config",
    "user",
    "database"
  ]
}
```

### 8. Get Specific Module Files

**Endpoint:** `GET /{project}/code/module/{identifier}`  
**Description:** Returns files from a specific module.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "path/to/module/file1.py",
    "path/to/module/file2.json"
  ]
}
```

Replace `{identifier}` with the module's ID or slug.

### 9. List All Components

**Endpoint:** `GET /{project}/code/components`  
**Description:** Returns a list of all components. If `index_by` is folder, each folder is a component. If `index_by` is file and `file_groups` is true, it lists grouped components by their base file names.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "panelcomponent",
    "headercomponent"
  ]
}
```

### 10. Get Specific Component Code

**Endpoint:** `GET /{project}/code/component/{identifier}`  
**Description:** Returns the code for a specific component. If multiple related files exist (e.g., `.svelte`, `.css`, `.js`), they are grouped and returned together.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": {
    "component_name": "panelcomponent",
    "files": {
      "panelComponent.svelte": "<script>...</script>",
      "panelComponent.css": "body { ... }",
      "panelComponent.js": "console.log('...');"
    }
  }
}
```

Replace `{identifier}` with the component identifier (slugified file or folder name).

### 11. List Documentation

**Endpoint:** `GET /{project}/docs`  
**Description:** Returns a list of documentation files (identified by slugified filenames).

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "getting-started",
    "api-overview"
  ]
}
```

### 12. Get Specific Documentation

**Endpoint:** `GET /{project}/docs/{identifier}`  
**Description:** Returns the content of a specific documentation file.

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": {
    "title": "getting-started.md",
    "content": "# Getting Started\nThis is how you get started..."
  }
}
```

Replace `{identifier}` with the documentation identifier.

### 13. Get Project Styles

**Endpoint:** `GET /{project}/code/styles`  
**Description:** Returns a list of global project style files (e.g., `.css`).

**Response (JSON Example):**
```json
{
  "status": "success",
  "data": [
    "/absolute/project/path/styles/global.css",
    "/absolute/project/path/styles/theme.css"
  ]
}
```

## Error Responses

**401 Unauthorized:**
```json
{
  "status": "error",
  "message": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "status": "error",
  "message": "Not found"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "Internal server error"
}
```