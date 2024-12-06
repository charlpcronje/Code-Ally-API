# Project Code and Documentation API

Welcome to the **Project Code and Documentation API**. This API provides convenient access to project code files, components, modules, documentation, and related metadata. It supports authentication via Bearer tokens, and you can request responses as JSON or Markdown. By default, Markdown is returned if you do not specify `?in=json`.

## Key Features

- **Code Listing & Retrieval:** Fetch categorized lists of files (core, config, components, etc.).
- **Module & Component Management:** Easily browse modules and components, including their code.
- **Documentation Access:** Read project documentation files in either JSON or Markdown format.
- **Project Metadata:** Retrieve project stack, specifications, tasks, and more.

## Getting Started

1. **Authentication:**  
   Include the following header in all requests:
   ```
   Authorization: Bearer <YOUR_API_KEY>
   ```

2. **Format Selection:**  
   Add `?in=json` to the endpoint for JSON responses, or `?in=md` for Markdown. Without this parameter, Markdown is returned by default.

3. **Base URL:**  
   The API is hosted at:
   ```
   https://api.example.com
   ```

## API Schema

For a detailed OpenAPI schema of this API, please refer to the [OpenAISchema.yml](./docs/OpenAISchema.md).

## PostMan Collection
[PostMan Collection](./docs/PostManCollection.md)

## Example `project.config.json` file
- [project.config.json](./docs/project.config.json)

## Full Documentation

Looking for more details, examples, and best practices? Please visit the [Full Documentation](./docs/README.md). The docs cover all endpoints, describe response structures, and provide additional guidance on usage.

## Contact

**Author:** Charl Cronje  
**Email:** [charl@webally.co.za](mailto:charl@webally.co.za)  
**More Info / CV:** [https://cv.webally.co.za](https://cv.webally.co.za)


