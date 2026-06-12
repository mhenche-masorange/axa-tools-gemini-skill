# AxA Tools Gemini Skill

Este repositorio contiene una **Skill para Gemini CLI** diseñada para gestionar y consultar proxies de Apigee X.

## Pasos para dejar la skill operativa

Si quieres utilizar estas herramientas en tu entorno de Gemini CLI, sigue estos pasos:

### 1. Clonar el repositorio
Asegúrate de tener configurada tu clave SSH en GitHub y clona el proyecto:
```bash
git clone git@github.com:mhenche-masorange/axa-tools-gemini-skill.git
```

### 2. Configurar el contexto de Gemini (GEMINI.md)
Para que Gemini reconozca automáticamente las herramientas, crea un archivo `GEMINI.md` en la raíz de tu espacio de trabajo (fuera de la carpeta del repo si quieres un contexto global, o dentro para este proyecto) con las instrucciones de uso. 

**Ejemplo de contenido para `GEMINI.md`:**
```markdown
# Apigee X Tools Instructions
Este workspace contiene scripts para Apigee X en `./axa-tools-gemini-skill/scripts/`.

## Workflows Principales
1. **Sincronizar Repo**: `python3 ./axa-tools-gemini-skill/scripts/sync_repo.py`
2. **Consultar Config**: `python3 ./axa-tools-gemini-skill/scripts/get_config.py --api "NOMBRE_API"`
3. **Analíticas**: `python3 ./axa-tools-gemini-skill/scripts/get_analytics.py --api "NOMBRE_API"`
4. **Infraestructura**: 
   - `python3 ./axa-tools-gemini-skill/scripts/get_apigee_instances.py --org "ORGANIZACION"`
   - `python3 ./axa-tools-gemini-skill/scripts/get_apigee_org.py --org "ORGANIZACION"`
```

### 3. Requisitos Previos
- **Python 3**: Todos los scripts requieren Python 3.
- **Google Cloud SDK (gcloud)**: Debes estar autenticado con una cuenta que tenga permisos sobre los proyectos de Apigee:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```
- **Dependencias**: Los scripts utilizan librerías estándar de Python (`subprocess`, `json`, `urllib`, etc.), por lo que no requieren un `pip install` externo inicialmente.

### 4. Uso
Una vez configurado el `GEMINI.md`, puedes pedirle a Gemini cosas como:
- "Dime la ventana de mantenimiento para el entorno osp-openapi-int"
- "¿Cuál es el timeout de la API ocsg_micTerminalRepair?"
- "Sincroniza el repositorio de proxies"

---
*Nota: Los scripts han sido adaptados para ser compatibles con entornos Linux/WSL utilizando rutas relativas.*
