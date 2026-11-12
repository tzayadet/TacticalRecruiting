# Tactical Recruiting

Prototipo de gestión de procesos de selección orientado a perfiles IT y telecomunicaciones. El repositorio público contiene la aplicación Python/SQLite, el código de desarrollo y una demo web estática independiente.

## Demo web pública

**URL prevista:** https://tzayadet.github.io/TacticalRecruiting/

La publicación está preparada mediante GitHub Actions. El repositorio es público, pero el sitio de GitHub Pages aún no está habilitado. Activa **Settings → Pages → Build and deployment → Source: GitHub Actions** para publicar la demo.

El workflow publica exclusivamente el contenido de `rrhh-demo/`. No publica `main.py`, `FULLAPP.py`, `database.py`, modelos, documentación interna ni datos locales en el sitio web. Esos archivos sí son visibles en el repositorio público.

## Componentes

| Ruta | Función |
|---|---|
| `main.py` + `database.py` | Aplicación de consola modular con persistencia SQLite. |
| `FULLAPP.py` | Versión monolítica alternativa. |
| `models.py` | Modelos y enumeraciones. |
| `questions.py` | Banco de preguntas de entrevista. |
| `rrhh-demo/index.html` | Demo web estática e independiente. |
| `docs/legacy-specification-2026-01.md` | Especificación histórica del proyecto. |

## Ejecutar la aplicación local

Requisitos: Python 3.10 o superior.

```bash
python main.py
```

También existe una versión autocontenida:

```bash
python FULLAPP.py
```

La aplicación guarda datos localmente en SQLite. No subas CV reales, datos personales de candidatos ni bases de selección al repositorio público.

## Arquitectura de la demo

- Es una aplicación estática ejecutada en el navegador.
- Utiliza registros ficticios con direcciones reservadas de ejemplo.
- Guarda el estado en `localStorage` del navegador.
- No se conecta a la base SQLite ni al backend Python.
- No tiene autenticación, API ni persistencia compartida.
- No envía datos a un servidor.

## Alcance y limitaciones

- Es un prototipo, no un ATS listo para producción.
- La demo web es una simulación local con datos ficticios.
- La aplicación de consola y la demo no comparten backend ni base de datos.
- No todos los módulos descritos en la especificación histórica están implementados.
- No utilices el scoring como criterio automático de selección ni como sustituto de una evaluación humana.
- Antes de usar el sistema con personas reales hacen falta controles de acceso, cifrado, retención, trazabilidad, protección de datos y revisión jurídica.

## Despliegue

El workflow `.github/workflows/pages.yml` publica solo `rrhh-demo/` cuando se activa GitHub Pages para el repositorio. La configuración de Pages debe estar habilitada en Settings → Pages.

## Licencia

Consulta [LICENSE](LICENSE).
