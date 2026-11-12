# Tactical Recruiting

Prototipo de gestión de procesos de selección orientado a perfiles IT y telecomunicaciones. Incluye una aplicación de consola en Python/SQLite y una demo web estática independiente.

## Componentes

| Archivo | Función |
|---|---|
| `main.py` + `database.py` | Aplicación de consola modular con persistencia SQLite |
| `FULLAPP.py` | Versión monolítica alternativa |
| `models.py` | Modelos de datos y enumeraciones |
| `questions.py` | Banco de preguntas de entrevista |
| `rrhh-demo/index.html` | Demo interactiva estática con datos ficticios |
| `index.html` | Página de entrada a la demo |

## Demo web

La demo estática se puede abrir directamente desde `rrhh-demo/index.html` o publicar con GitHub Pages cuando el repositorio tenga habilitado Pages. Utiliza datos de ejemplo en el navegador y no se conecta a la base de datos Python.

## Aplicación de consola

Requisitos: Python 3.10 o superior. La aplicación utiliza la biblioteca estándar.

```bash
python main.py
```

Los datos locales se guardan en SQLite y los CV se almacenan en el directorio local de la aplicación. No subas datos personales, CV reales ni bases de candidatos a GitHub.

También existe una versión autocontenida:

```bash
python FULLAPP.py
```

Mantén separadas las carpetas de datos y las copias de seguridad. Antes de utilizar el prototipo con personas reales, implementa controles de acceso, cifrado de datos sensibles, retención, trazabilidad y gestión verificable del consentimiento.

## Alcance y limitaciones

- Es un prototipo, no un ATS listo para producción.
- La demo web es una simulación local con datos ficticios.
- La aplicación de consola y la demo no comparten backend ni base de datos.
- La documentación funcional describe ideas y módulos previstos; no todos están implementados en la aplicación.
- No utilices el scoring como criterio automático de selección ni como sustituto de una evaluación humana.
- No almacenes datos reales de candidatos en una versión pública o sin controles adecuados.

## Licencia

Consulta [LICENSE](LICENSE).
