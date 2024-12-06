# OpenAI Schema

```yml
openapi: 3.1.0
info:
  title: Project Code and Documentation API
  version: 1.0.0
  description: >
    This API allows fetching code and documentation organized by project. It supports authentication and can respond in
    JSON or Markdown format.
servers:
  - url: https://ally.code.webally.co.za
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
components:
  schemas: {}
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
security:
  - BearerAuth: []
```
