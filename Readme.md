===============================================================================
TACTICAL RECRUITING NETUSHIM

[MODULO_01] BASE_DATOS_CANDIDATOS
|
|-- [SUBMODULO] FICHA_CANDIDATO
| |-- ID_Candidato (UUID autogenerado)
| |-- Datos_Personales
| | |-- Nombre_Completo
| | |-- Email
| | |-- Teléfono
| | |-- LinkedIn_URL
| | |-- GitHub_URL
| | |-- Localización (País, Provincia, Ciudad)
| | |-- Disponibilidad_Remoto (Total/Parcial/Presencial)
| | |-- Disponibilidad_Incorporación (Inmediata/15d/30d/60d+)
| | |-- Carnet_Conducir (Sí/No)
| | |-- Vehículo_Propio (Sí/No)
| |-- Formación
| | |-- Nivel_Estudios (Grado/Máster/Doctorado/FP)
| | |-- Titulación
| | |-- Certificaciones_Relevantes (lista)
| | |-- Idiomas (nivel CERF)
| |-- Experiencia_Profesional
| | |-- Total_Años_IT
| | |-- Total_Años_Telecom/OSS/BSS
| | |-- Último_Puesto
| | |-- Última_Empresa
| | |-- Proyectos_Relevantes (lista con stack y duración)
| | |-- Experiencia_TMForum_ODA (Sí/No/Nivel)
| |-- Stack_Técnico (matriz ponderada)
| | |-- Lenguajes_Programación
| | | |-- Java (Nivel: Junior/Mid/Senior/Expert)
| | | |-- Python (Nivel: ...)
| | | |-- Node.js (Nivel: ...)
| | | |-- Go (Nivel: ...)
| | | |-- TypeScript (Nivel: ...)
| | |-- Frameworks_Backend
| | | |-- Spring_Boot
| | | |-- Django
| | | |-- Express
| | |-- Frameworks_Frontend
| | | |-- Angular
| | | |-- React
| | |-- Bases_Datos
| | | |-- SQL (Oracle/PostgreSQL/MySQL)
| | | |-- NoSQL
| | |-- Cloud_Platforms
| | | |-- AWS
| | | |-- Azure
| | | |-- GCP
| | |-- DevOps_Tools
| | | |-- Docker
| | | |-- Kubernetes/OpenShift
| | | |-- Terraform
| | | |-- Ansible
| | | |-- GitLab_CI/Jenkins
| | |-- APIs_Integración
| | | |-- REST
| | | |-- TMForum_OpenAPIs
| | | |-- SOAP
| | | |-- GraphQL
| | |-- Mensajería
| | | |-- Kafka
| | | |-- RabbitMQ
| |-- Competencias_Blandas
| | |-- Comunicación_Técnica
| | |-- Trabajo_en_Equipo
| | |-- Resolución_Problemas
| | |-- Adaptabilidad
| | |-- Ownership
| |-- Adjuntos
| | |-- CV_PDF (enlace/encriptado)
| | |-- Portfolio_URL
| | |-- Certificados (lista enlaces)
| |-- Metadata_Privacidad
| | |-- Fecha_Registro
| | |-- Consentimiento_GDPR (Sí/No + fecha)
| | |-- Origen_Captación (LinkedIn/Referido/JobBoard)
| | |-- Última_Actualización
| | |-- Estado_Activo (Activo/Inactivo/Archivado)
|
|-- [SUBMODULO] HISTORIAL_INTERACCIONES
| |-- Fecha_Interacción
| |-- Tipo (Email/Entrevista/Call/LinkedIn)
| |-- Responsable_RRHH
| |-- Notas (texto libre + etiquetas)
| |-- Próximo_Paso (fecha + acción)
|
|-- [SUBMODULO] BUSQUEDA_AVANZADA
|-- Filtros_Múltiples (AND/OR)
|-- Búsqueda_Semántica (stack + perfil)
|-- Exportar_Listado (CSV/Excel)
|-- Etiquetas_Custom (ej: "urgente", "recomendado", "en_standby")
[MODULO_02] GESTION_VACANTES
|
|-- [SUBMODULO] FICHA_VACANTE
| |-- ID_Vacante (ALV-YYYY-NNN)
| |-- Datos_Básicos
| | |-- Título_Puesto (ej: "Backend Developer - Java/Spring")
| | |-- Perfil_Tipo (Backend/DevOps/QA/Cloud/Integrations/SA/PO/Support/Frontend)
| | |-- Seniority_Requerido (Junior/Mid/Senior/Lead)
| | |-- Departamento (Desarrollo/DevOps/Producto/Arquitectura/Operaciones)
| | |-- Tipo_Necesidad (Nueva/Reemplazo)
| | |-- Motivo_Reemplazo (opcional)
| |-- Requisitos_Técnicos
| | |-- Stack_Obligatorio (lista con niveles mínimos)
| | |-- Stack_Deseable (lista con niveles)
| | |-- Experiencia_TMForum_ODA (Obligatorio/Deseable/No_relevante)
| | |-- Experiencia_Telecom (Obligatorio/Deseable/No_relevante)
| | |-- Certificaciones_Requeridas (ej: AWS/Azure/ISO27001)
| |-- Condiciones_Contratación
| | |-- Modalidad (Remoto_Total/Remoto_Parcial/Presencial)
| | |-- Ubicación_Oficina (Madrid/Avilés/Indistinto)
| | |-- Rango_Salarial_Min (EUR)
| | |-- Rango_Salarial_Max (EUR)
| | |-- Tipo_Contrato (Indefinido/Temporal)
| | |-- Jornada (Completa/Parcial)
| |-- Stakeholders
| | |-- Responsable_Selección (RRHH)
| | |-- Responsable_Técnico (Tech Lead/Arquitecto)
| | |-- Hiring_Manager (Jefe de Área)
| | |-- Aprobador_Final (Director)
| |-- Cronograma
| | |-- Fecha_Apertura
| | |-- Fecha_Cierre_Estimada
| | |-- Fecha_Cierre_Real
| | |-- Deadline_Urgente (Sí/No + fecha)
| |-- Estado_Vacante
| | |-- Abierta/En_proceso/Cerrada_Cancelada/Cerrada_Cubierta
| | |-- Razón_Cierre (Cubierta/Cancelada_Cambio_Prioridad/...)
| |-- KPI_Vacante
| | |-- Time_to_Hire (días)
| | |-- Cost_per_Hire (EUR)
| | |-- Nº_Candidatos_Totales
| | |-- Nº_Entrevistas_Realizadas
|
|-- [SUBMODULO] PIPELINE_CANDIDATOS
| |-- Etapa_01_Sourcing (candidatos identificados)
| |-- Etapa_02_Screening_Telefónico (entrevista RRHH)
| |-- Etapa_03_Entrevista_Técnica (Tech Lead/Arquitecto)
| |-- Etapa_04_Entrevista_Cultural (Hiring Manager)
| |-- Etapa_05_Finalistas (top 3)
| |-- Etapa_06_Offer (enviada/aceptada/rechazada)
| |-- Etapa_07_Onboarding (incorporado)
| |-- Visualización_Kanban (drag&drop entre etapas)
| |-- Alertas_Automáticas (ej: etapa estancada >7d)
|
|-- [SUBMODULO] FINALISTAS_SELECCIONADOS
|-- Candidato_Finalista_01 (ID + nombre + score_final)
|-- Candidato_Finalista_02 (ID + nombre + score_final)
|-- Candidato_Finalista_03 (ID + nombre + score_final)
|-- Candidato_Seleccionado (ID + nombre + fecha_aceptación)
|-- Feedback_Rechazados (notas por candidato)
[MODULO_03] EVALUACION_AUTOMATICA
|
|-- [SUBMODULO] RUBRICA_RST
| |-- Dimensión_R (Entrevista/Comunicación)
| | |-- Puntuación (1-10)
| | |-- Criterios_Guía_Alignados
| | | |-- 1-3: respuestas vagas, sin ejemplos, confusión conceptos base
| | | |-- 4-6: base correcta, algunos ejemplos, huecos puntuales
| | | |-- 7-8: sólido, ejemplos claros, buena toma decisiones
| | | |-- 9-10: excelente, liderazgo/ownership, profundidad, anticipa riesgos
| | |-- Notas_Evaluador
| |-- Dimensión_S (Técnica/Stack)
| | |-- Puntuación (1-10)
| | |-- Criterios_Guía_Alignados (por perfil específico)
| | |-- Notas_Evaluador
| | |-- Ejercicio_Práctico (Sí/No + resultado)
| |-- Dimensión_T (Cultural/Soft_Skills)
| | |-- Puntuación (1-10)
| | |-- Criterios_Guía_Alignados
| | | |-- Alineación con DevSecOps/cloud-native
| | | |-- Colaboración equipos multidisciplinares
| | | |-- Estabilidad/proyectos larga duración
| | | |-- Explicación decisiones técnicas con claridad
| | |-- Notas_Evaluador
|
|-- [SUBMODULO] CALCULO_SCORE_AUTOMATICO
| |-- Ponderación_por_Rol (tabla RoleWeights)
| | |-- Ej_Backend: R(20%) + S(60%) + T(20%)
| | |-- Ej_SolutionArchitect: R(25%) + S(50%) + T(25%)
| | |-- Ej_ProductOwner: R(30%) + S(40%) + T(30%)
| |-- Fórmula: Score_Final = (R * P_R) + (S * P_S) + (T * P_T)
| |-- Umbral_Minimo_Aprobación (configurable por rol)
| |-- Bandas_Automáticas
| | |-- Rojo (<5.0): descartar
| | |-- Amarillo (5.0-6.9): evaluar con precaución
| | |-- Verde (7.0-8.4): buen candidato
| | |-- Azul (8.5-10.0): top talent
|
|-- [SUBMODULO] SEÑALES_BUEN_ENCAJE
|-- Checklist_por_Perfil (autocompletado al evaluar)
|-- Backend: [ ] Explica decisiones técnicas con datos
|-- Backend: [ ] Piensa en resiliencia (timeouts/retries)
|-- Backend: [ ] Conoce prácticas calidad (tests/code review)
|-- DevOps: [ ] Automatiza por defecto
|-- DevOps: [ ] Enfoca seguridad sin bloquear entregas
|-- QA: [ ] Pensamiento crítico y precisión
|-- QA: [ ] Colabora como habilitador (no policía)
|-- SA: [ ] Visión sistémica y criterio técnico
|-- SA: [ ] Documentación útil y comunicación impecable
|-- PO: [ ] Claridad, estructura, foco en valor
|-- PO: [ ] Respeta límites técnicos
|-- Integrations: [ ] Precisión en contratos y logs
|-- Integrations: [ ] Piensa interoperabilidad desde diseño
|-- Support: [ ] Calma bajo presión y método
|-- Support: [ ] Documenta para evitar recurrencias
[MODULO_04] COMPARADOR_MULTICANDIDATO
|
|-- [SUBMODULO] SELECCION_CANDIDATOS
| |-- Mínimo: 2 candidatos
| |-- Máximo: ilimitado (recomendado ≤5 para visualización)
| |-- Origen: misma vacante / candidatos guardados / búsqueda libre
|
|-- [SUBMODULO] MATRIZ_COMPARATIVA
| |-- Columnas: Candidato_A | Candidato_B | Candidato_C | ...
| |-- Filas_Comparativas
| | |-- Score_Final_RST
| | |-- Stack_Java (nivel + años)
| | |-- Stack_Python (nivel + años)
| | |-- Kubernetes (nivel + años)
| | |-- TMForum_ODA (Sí/No + experiencia)
| | |-- Telecom_OSS/BSS (años)
| | |-- Inglés (nivel)
| | |-- Disponibilidad_Incorporación
| | |-- Expectativas_Salariales
| | |-- Riesgo_Fuga (Bajo/Medio/Alto)
|
|-- [SUBMODULO] DESTACADO_DIFERENCIAS
| |-- Resaltado_Automático (colores)
| | |-- Verde: ventaja significativa (+2 niveles o +3 años)
| | |-- Rojo: carencia crítica (no cumple stack obligatorio)
| | |-- Amarillo: diferencia moderada
| |-- Filtro_Prioridad (mostrar solo diferencias críticas)
|
|-- [SUBMODULO] RANKING_AUTOMATICO
|-- Ordenar_por_Score_Final (descendente)
|-- Ordenar_por_Afinidad_Stack (personalizable pesos)
|-- Exportar_Ranking (PDF/Excel)
[MODULO_05] BANCO_PREGUNTAS_ENTREVISTA
|
|-- [SUBMODULO] PREGUNTAS_GENERALES
| |-- Identificación_Datos_Básicos (9 preguntas predefinidas)
| |-- Experiencia_General (6 preguntas)
| |-- Encaje_Cultural (6 preguntas)
| |-- Situacionales_Behavioral (4 preguntas)
|
|-- [SUBMODULO] PREGUNTAS_POR_PERFIL
| |-- Backend_FullStack
| | |-- Técnicas_Core (7 preguntas)
| | |-- Ejercicio_Práctico (latencia alta endpoint)
| |-- Frontend
| | |-- Técnicas_Core (5 preguntas)
| | |-- Ejercicio_Práctico (rendimiento componente)
| |-- DevOps_Cloud_Security
| | |-- Técnicas_Core (5 preguntas)
| | |-- Ejercicio_Práctico (incidente producción)
| |-- QA_Automation
| | |-- Técnicas_Core (5 preguntas)
| | |-- Ejercicio_Práctico (bug crítico pre-despliegue)
| |-- Solution_Architect
| | |-- Arquitectura_Core (6 preguntas)
| | |-- Ejercicio_Práctico (diseño alta transaccionalidad)
| |-- Product_Owner_Manager
| | |-- Producto_Core (5 preguntas)
| | |-- Ejercicio_Práctico (priorización recursos limitados)
| |-- Integrations_API_Specialist
| | |-- Integración_Core (5 preguntas)
| | |-- Ejercicio_Práctico (APIs incompatibles)
| |-- Operations_Support_Engineer
| | |-- Operaciones_Core (4 preguntas)
| | |-- Ejercicio_Práctico (incidente crítico horario cliente)
|
|-- [SUBMODULO] GESTION_PREGUNTAS
|-- Crear_Nueva_Pregunta (texto + etiquetas perfil)
|-- Etiquetar_Por_Tecnología (ej: "Kubernetes", "TMForum")
|-- Marcar_Favoritas (por entrevistador)
|-- Exportar_Guía_Entrevista (PDF personalizado por vacante)
[MODULO_06] METODOLOGIAS_AGILES
|
|-- [SUBMODULO] RESUMEN_METODOLOGIAS
| |-- Scrum (roles, artefactos, eventos, duración sprints)
| |-- Kanban (principios WIP, lead time, tablero)
| |-- Lean (7 principios, eliminación waste)
| |-- XP (prácticas TDD, pair programming, CI)
| |-- Crystal (ajuste por tamaño/criticidad)
| |-- FDD (phases por feature)
| |-- DSDM (principios negocio + tiempo)
| |-- AUP (fases RUP ágil)
| |-- Scrumban (híbrido)
| |-- SAFe (escalado niveles)
|
|-- [SUBMODULO] USO_RRHH
|-- Preguntas_Entrevista_Agile (para evaluar experiencia)
|-- Checklist_Evaluación_Agile (ej: "participó en retros", "gestionó backlog")
|-- Ejemplos_Reales_para_Pedir (que cuente sprint planning real)
[MODULO_07] MARCO_LEGAL_ESPANA
|
|-- [SUBMODULO] CONVENIO_OFICINAS_MADRID
| |-- Tabla_Salarial_Actualizada (grupos + complementos)
| |-- Jornada_y_Horarios
| |-- Vacaciones_y_Perms
| |-- Plus_Transporte/Alimentación
| |-- Actualizaciones_Automáticas (notificación cambios normativos)
|
|-- [SUBMODULO] ESTATUTO_TRABAJADORES
| |-- Artículos_Relevantes_RRHH (selección práctica)
| |-- Contratación (tipos, duración, renovación)
| |-- Extinción_Contrato (causas, indemnizaciones)
| |-- Derechos_y_Deberes
| |-- Vacaciones_y_Ausencias
|
|-- [SUBMODULO] CUMPLIMIENTO_GDPR_LOPD
|-- Registro_Actividades_Tratamiento
|-- Consentimientos_Candidatos (registro fechas + scope)
|-- Derecho_Olvido (procedimiento archivado)
|-- Retención_Datos (plazos legales)
|-- Plantilla_Aviso_Privacidad (para emails RRHH)
[MODULO_08] EMPRESA_ALVATROSS
|
|-- [SUBMODULO] PRESENTACION_CORPORATIVA
| |-- Quienes_Somos (misión, historia, Grupo SATEC)
| |-- Plataforma_OSS (características cloud-native, TMForum, ODA)
| |-- Stack_Tecnológico (microservicios, APIs, BBDD compatibles)
| |-- Clientes_y_Alcance (geografía, casos uso)
| |-- Oficinas (Madrid Aravaca, Avilés)
| |-- Cultura (colaborativa, DevSecOps, Great Place to Work)
| |-- Qué_Buscamos (perfil ideal candidato)
| |-- Qué_Offeremos (estabilidad, proyectos internacionales)
|
|-- [SUBMODULO] SCRIPT_TELEFONICO_ENTREVISTA
|-- Guion_Inicial (presentación + objetivo llamada)
|-- Guion_Cierre (próximos pasos + FAQ candidato)
|-- Plantilla_Email_Seguimiento
[MODULO_09] PERFILES_HABITUALES_IT_TELECOM
|
|-- [SUBMODULO] FICHAS_DETALLADAS_ROLES
| |-- Backend_FullStack_Developer
| | |-- Área: Desarrollo Producto / Ingeniería Software
| | |-- Resumen_Objetivo
| | |-- Responsabilidades_Principales (6 items)
| | |-- Requisitos_Técnicos (6 items)
| | |-- Soft_Skills (5 items)
| | |-- Seniority (Junior/Mid/Senior criterios)
| | |-- Cultura_Forma_Trabajar
| | |-- KPI_Criterios_Éxito
| |-- Frontend_Developer (estructura idéntica)
| |-- DevOps_Cloud_Security_Engineer (estructura idéntica)
| |-- QA_Automation_Engineer (estructura idéntica)
| |-- Integrations_API_Specialist (estructura idéntica)
| |-- Solution_Architect (estructura idéntica)
| |-- Product_Owner_Manager (estructura idéntica)
| |-- Operations_Support_Engineer (estructura idéntica)
|
|-- [SUBMODULO] CHULETA_RAPIDA_STACK
|-- Tabla_Resumen_Perfiles (Rol | Área | Tecnologías_Principales | Objetivo)
|-- Mapa_Calor_Tecnologías (frecuencia demanda por rol)
[MODULO_10] GLOSARIO_TERMINOS
|
|-- [SUBMODULO] TERMINOS_TECNICOS_IT
| |-- OSS/BSS (definición + contexto Alvatross)
| |-- TMForum_OpenAPIs
| |-- ODA (Open Digital Architecture)
| |-- Cloud_Native
| |-- Microservicios
| |-- DevSecOps
| |-- CI/CD
| |-- IaC (Infrastructure as Code)
| |-- ... (todos términos relevantes stack Alvatross)
|
|-- [SUBMODULO] TERMINOS_RRHH
|-- Sourcing
|-- Screening
|-- Time_to_Hire
|-- Cost_per_Hire
|-- Offer_Stage
|-- Onboarding
|-- ... (términos recruiting)
[MODULO_11] TAREAS_Y_WORKFLOW_RRHH
|
|-- [SUBMODULO] LISTA_TAREAS_PERSONAL
| |-- Tareas_Pendientes (con fecha límite)
| |-- Tareas_En_Progreso
| |-- Tareas_Completadas (histórico)
| |-- Recordatorios_Automáticos (email/app push)
|
|-- [SUBMODULO] CALENDARIO_ENTREVISTAS
| |-- Vista_Día/Semana/Mes
| |-- Bloques_Disponibilidad_Entrevistadores
| |-- Reserva_Automática (evita conflictos)
| |-- Notificaciones_Participantes (24h y 1h antes)
| |-- Enlace_Videollamada (Zoom/Teams autogenerado)
[MODULO_12] ONBOARDING_POSTSELECCION
|
|-- [SUBMODULO] CHECKLIST_INCORPORACION
| |-- Pre_Incorporación (contrato firmado, equipo IT, cuentas)
| |-- Día_1 (bienvenida, presentación equipo, documentación)
| |-- Semana_1 (formación producto, acceso repositorios, primer ticket)
| |-- Mes_1 (revisión 30 días, feedback inicial)
| |-- Mes_3 (evaluación 90 días, objetivos primer año)
|
|-- [SUBMODULO] FEEDBACK_HIRING_MANAGER
|-- Formulario_Estructurado (30/60/90 días)
|-- Puntuación_Alineación_Esperada_vs_Realidad
|-- Comentarios_Libres
|-- Alertas_Riesgo_Retention (si puntuación <6)
[MODULO_13] REPORTING_ANALYTICS
|
|-- [SUBMODULO] DASHBOARDS_EJECUTIVOS
| |-- Pipeline_Vacantes (abiertas vs cerradas)
| |-- Time_to_Hire_Promedio (últimos 6 meses)
| |-- Source_of_Hire (LinkedIn/Referido/JobBoard %)
| |-- Retention_90d (tasa éxito incorporaciones)
| |-- Cost_per_Hire_vs_Budget
|
|-- [SUBMODULO] EXPORTACION_DATOS
|-- Reporte_Mensual_RRHH (PDF/Excel)
|-- Exporte_Candidatos (CSV con GDPR compliance)
|-- Audit_Trail (todas acciones en sistema)
[MODULO_14] CONFIGURACION_SISTEMA
|
|-- [SUBMODULO] USUARIOS_Y_PERMISOS
| |-- Roles (RRHH_Admin / RRHH_Básico / Tech_Lead / Hiring_Manager)
| |-- Permisos_por_Rol (lectura/escritura/eliminación)
| |-- Auditoría_Accesos
|
|-- [SUBMODULO] PONDERACIONES_PERSONALIZADAS
| |-- RoleWeights (tabla editable por perfil)
| |-- Umbral_Minimo_Score (configurable)
| |-- Etiquetas_Custom (creación/modificación)
|
|-- [SUBMODULO] INTEGRACIONES_EXTERNAS
|-- API_LinkedIn_Recruiter (búsqueda candidatos)
|-- Webhook_GitHub (verificación perfil técnico)
|-- Calendly/Outlook (sincronización entrevistas)
|-- Slack/Teams (notificaciones equipo RRHH)
===============================================================================
