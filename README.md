# Tactical Recruiting | IT Talent Operations

[![Python CI](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/ci.yml/badge.svg)](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/ci.yml) [![Pages deployment](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/pages.yml)

Prototipo de operaciones de talento IT y telecomunicaciones, con gestión local de candidatos, evaluación técnica orientativa y demo web independiente. Incluye una aplicación Python/SQLite, un banco de preguntas técnicas y una demo web estática independiente. Los datos y perfiles precargados son ilustrativos.

## Demo web pública

**URL:** https://tzayadet.github.io/TacticalRecruiting/

La demo estática está en `rrhh-demo/`. El workflow publica exclusivamente esa carpeta, nunca el backend Python, los modelos, la documentación interna ni los datos locales.

Para habilitar la primera publicación:

1. En **Settings → Pages**, selecciona **GitHub Actions** como origen.
2. En **Settings → Secrets and variables → Actions → Variables**, crea `ENABLE_PAGES` con valor `true`.
3. Ejecuta **Deploy sanitized Tactical Recruiting demo to GitHub Pages** desde Actions.

La demo usa datos ficticios y almacenamiento local del navegador. No se conecta a la aplicación Python ni a SQLite.

## Componentes

| Ruta | Función |
|---|---|
| `main.py` + `database.py` | Aplicación de consola modular con persistencia SQLite. |
| `archive/FULLAPP.legacy.py` | Snapshot monolítico histórico; no es la aplicación mantenida ni se recomienda ejecutarlo. |
| `models.py` | Modelos y enumeraciones. |
| `questions.py` | Banco de preguntas de entrevista. |
| `rrhh-demo/index.html` | Demo web estática e independiente. |
| `scripts/validate_demo.py` | Validaciones de privacidad y comportamiento de la demo. |
| `tests/` | Pruebas automáticas de inicialización y operaciones básicas. |
| `docs/legacy-specification-2026-01.md` | Diseño funcional histórico, anonimizado y no normativo. |

## Ejecutar la aplicación local

Requisitos: Python 3.10 o superior.

```bash
python main.py
```

La aplicación guarda datos localmente en SQLite. El registro modular exige una respuesta afirmativa antes de recoger datos personales o leer un CV. El prototipo solo implementa este flujo de consentimiento y no modela otras bases jurídicas. El consentimiento registrado no constituye por sí solo una garantía de cumplimiento del RGPD ni sustituye la información, finalidad, conservación, derechos y controles que correspondan. Los CV se limitan a PDF/DOC/DOCX de hasta 10 MB y se guardan sin cifrado en el almacenamiento local. No subas CV reales, datos personales de candidatos, exportaciones ni bases de selección al repositorio público. La base SQLite y los CV locales no están cifrados. Las carpetas locales de datos y CV están excluidas mediante `.gitignore`.

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
- La especificación histórica contiene ideas y módulos que pueden no estar implementados en el código actual.
- Los rangos salariales y perfiles precargados son ejemplos orientativos, no datos de mercado ni ofertas reales.
- No utilices el scoring como criterio automático de selección ni como sustituto de una evaluación humana.
- Antes de usar el sistema con personas reales hacen falta controles de acceso, cifrado, retención, trazabilidad, protección de datos y revisión jurídica.

## Despliegue

El workflow `.github/workflows/pages.yml` publica solo `rrhh-demo/` cuando Pages está habilitado y la variable `ENABLE_PAGES=true` está configurada. Consulta los pasos de **Demo web pública**.

## Licencia

No se ha publicado una licencia de reutilización. El repositorio es público para revisión técnica y portfolio, pero no concede por sí mismo permiso de redistribución, modificación o uso comercial.
